from flask import Flask, render_template, url_for, request, redirect, jsonify, flash

app= Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Club, User

# create engine
engine = create_engine('sqlite:///mitclubswithusers.db')     
Base.metadata.bind = engine

from flask import session as login_session
import random, string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json','r').read())['web']['client_id']

DBSession = sessionmaker(bind = engine)
session = DBSession()

# creating a new user
def createUser(login_session):
    newUser = User(name=login_session['username'], googid=login_session[
              'googid'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(googid = login_session['googid']).one()
    return user.id

# fetch user given user id
def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

# fetch user id given google id
def getUserID(googid):
    try:
        user = session.query(User).filter_by(googid = googid).one()
        return user.id
    except:
        return None

# create homepage
@app.route('/clubs')
@app.route('/')
def homepage():
    categories = session.query(Category).all()
    if 'username' not in login_session:
        return render_template('publichome.html', categories = categories)
    print(getUserID(login_session['googid']))
    return render_template('home.html', categories = categories)

# login page
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE = state)

# to connect
@app.route('/gconnect', methods=['POST'])
def gconnect():    
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads((h.request(url, 'GET')[1]).decode("utf-8"))
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['googid'] = data['id']

    # Verify if user is already registered
    # if user is not registered, then create account
    user_id = getUserID(data["id"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
        
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output

# log out
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print ('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print ('result is ')
    print (result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        # return response
        return redirect('/')
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# view each category
@app.route('/clubs/<int:category_id>')
def clubCategory(category_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    clubs = session.query(Club).filter_by(category_id = category.id)
    # public template
    if 'username' not in login_session:
        return render_template('publiccategory.html', category = category, clubs = clubs, categories = categories)
    # private template
    return render_template('category.html', category = category, clubs=clubs, categories=categories)

# view individual club info
@app.route('/clubs/<int:category_id>/<int:club_id>')
def clubInfo(category_id, club_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    clubs = session.query(Club).filter_by(id= club_id).one()
    try:
        creator = getUserInfo(clubs.user_id)
    except:
        pass
    # public template
    print('username' not in login_session)
    if 'username' not in login_session or creator.id != getUserID(login_session['googid']):
        return render_template('publicclubinfo.html', categories = categories, category = category, clubs = clubs)
    # private template
    return render_template('clubinfo.html', categories = categories, category = category, clubs = clubs)

# page to add club, linked from category page
@app.route('/clubs/<int:category_id>/new', methods=['GET','POST'])
def addClub(category_id):
    # redirect user to login if not already
    if 'username' not in login_session:
        return redirect('\login')
    category = session.query(Category).filter_by(id=category_id).one()
    if request.method == 'POST':
        newClub = Club(user_id = getUserID(login_session['googid']), name = request.form['name'], description = request.form['description'], link = request.form['link'], category = category)
        session.add(newClub)
        session.commit()
        # redirect back to category page, after adding
        return redirect(url_for('clubCategory', category_id = category.id))
    else:
        return render_template('clubcreate.html', category = category)

# edit club from individual club info
@app.route('/clubs/<int:category_id>/<int:club_id>/edit', methods=['GET','POST'])
def editClub(category_id,club_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    clubs = session.query(Club).filter_by(id= club_id).one()
    if request.method == 'POST':
        # populate club fields
        if request.form['name']:
            clubs.name = request.form['name']
            session.add(clubs)
            session.commit()
        if request.form['description']:
            clubs.description = request.form['description']
            session.add(clubs)
            session.commit()
        if request.form['link']:
            clubs.link = request.form['link']
            session.add(clubs)
            session.commit()
        if (request.form['name']) or (request.form['description']) or request.form['link']:
            return redirect(url_for('clubInfo', category_id = category.id, club_id = clubs.id))
    else:           
        return render_template('clubedit.html', categories = categories, category = category, clubs = clubs)

# delete club from individual club info and from database
@app.route('/clubs/<int:category_id>/<int:club_id>/delete', methods=['GET','POST'])
def deleteClub(category_id,club_id):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(id=category_id).one()
    clubs = session.query(Club).filter_by(id= club_id).one()
    if request.method == 'POST':
        session.delete(clubs)
        session.commit()
        return redirect(url_for('clubCategory', category_id = category.id))
    else:
        return render_template('clubdelete.html', categories = categories, category = category, clubs = clubs)


# JSON

# all clubs
@app.route('/clubs/JSON')
def clubsJSON():
    clubs = session.query(Club).all()
    return jsonify(clubs = [club.serialize for club in clubs])

# all categories
@app.route('/clubs/categories/JSON')
def categoriesJSON():
    categories = session.query(Category).all()
    return jsonify(categories = [cat.serialize for cat in categories])

# all clubs in a particular category
@app.route('/clubs/<path:categoryName>/clublist/JSON')
def categoryClubsJSON(categoryName):
    category = session.query(Category).filter_by(name = categoryName).one()
    clubs = session.query(Club).filter_by(category = category).all()
    return jsonify(clubs = [club.serialize for club in clubs])
    
# a particular club given the club name and category name
@app.route('/clubs/<path:categoryName>/<path:clubName>/JSON')
def clubJSON(categoryName, clubName):
    club = session.query(Club).filter_by(name = clubName).one()
    return jsonify(club = [club.serialize])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run('0.0.0.0',port=5000)
