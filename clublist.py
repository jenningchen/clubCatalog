from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Club, User

engine = create_engine('sqlite:///mitclubswithusers.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create dummy user
User1 = User(name="Robo Barista", googid=" ",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Category Academic Societies and clubs
category1 = Category(user_id = 1, name="Academic Societies")

session.add(category1)
session.commit()

club1 = Club(user_id = 1, name = "American Indian Science and Engineering Society",
             description = "We are the MIT Native American chapter and we "\
             "reach out to the Native American community in the greater "\
             "Boston area for collaboration. We hold events to build community "\
             "with in the MIT Native population.",
             link = "http://web.mit.edu/aises/www/",
             category = category1)
session.add(club1)
session.commit()

club3 = Club(user_id = 1, name = "American Institute of Architecture Students",
             description = "The American Institute of Architecture Students, or "\
             "AIAS, is a national organization with local chapters at universities "\
             "throughout the US. The AIAS works to address issues affecting students, "\
             "including studio culture, internships, the accredidation process, and the "\
             "advancement of architecture itself.",
             link="http://web.mit.edu/aias/",
             category = category1)
session.add(club3)
session.commit()

club4 = Club(user_id = 1, name = "Biology Undergraduate Student Association",
             description = "The Biology Undergraduate Students Association (BUSA) serves all "\
             "MIT students with an interest in biology. BUSA helps to broaden the biology "\
             "undergraduate experience through both social and academic activities. BUSA also "\
             "provides resources and support for biology students.",
             link="http://web.mit.edu/busa/",
             category = category1)
session.add(club4)
session.commit()

club5 = Club(user_id = 1, name = "Society for Biomaterials",
             description = "The MIT student chapter of the Society for Biomaterials encourages the "\
             "development, dissemination, integration, and utilization of knowledge in biomaterials. "\
             "All students interested in biomaterials (biologically compatible materials) are welcome.",
             link="http://web.mit.edu/sbm/www/index.html",
             category = category1)
session.add(club5)
session.commit()

club6 = Club(user_id = 1, name = "Biomedical Engineering Society",
             description = "The Biomedical Engineering Society serves to bring knowledge to its members "\
             "concerning the advancement of biomedical research and technology in the medical field. It "\
             "also exists as a forum for discussion among the MIT community who would like share ideas or "\
             "opinions. Meetings shall promote interests through activities such as lectures, presentations, "\
             "tours, and social activities.",
             link="http://bmes.scripts.mit.edu/",
             category = category1)
session.add(club6)
session.commit()

club7 = Club(user_id = 1, name = "Undergraduate Economics Association",
             description = "The UEA is a group of undergraduates interested in economics who meet for the purpose "\
             "of supporting academic endeavors, improving employment opportunities, and extending networks with each "\
             "other and the outside world.",
             link="http://web.mit.edu/uea/www/",
             category = category1)
session.add(club7)
session.commit()

club8 = Club(user_id = 1, name = "Eta Kappa Nu, National Electrical Engineering and Computer Science Honor Society",
             description = "At MIT, HKN is primarily interested in improving course VI by providing students with many "\
             "helpful resources. These resources include the Underground guide to course VI and VI-A, the HKN tutoring "\
             "program, and many social events.",
             link="https://hkn.mit.edu/",
             category = category1)
session.add(club8)
session.commit()

club9 = Club(user_id = 1, name = "IEEE/ACM Club",
             description = "The MIT IEEE/ACM Club represents the student branch for two professional international "\
             "organizations, the Institute of Electrical and Electronics Engineers (IEEE) and the Association for Computing "\
             "Machinery (ACM). Our mission is to create and support a tight-knit community among the students, mainly undergraduates, "\
             "and faculty in the Department of Electrical Engineering and Computer Science (EECS) at MIT.",
             link="http://ieee.scripts.mit.edu/",
             category = category1)
session.add(club9)
session.commit()

club10 = Club(user_id = 1, name = "MEGAWomen",
              description = "MEGAWomen is the association of graduate women in the MIT Department of Mechanical Engineering. Our goal "\
              "is to foster life-long friendships, mentor new women students, help them lead an enriching graduate school life and assist "\
              "with their personal and professional goals.",
              link="http://web.mit.edu/megawomen/",
              category = category1)
session.add(club10)
session.commit()

club11 = Club(user_id = 1, name = "Society of Physics Students",
              description = "Whether you spend your spare time reading about quantum field theory, or you just think that electromagnetism is cool, "\
              "you would fit in at the Society of Physics Students. We are open to anyone with an appreciation for physics. Whether you have a mild "\
              "curiosity for the science, or an intellectual passion, our goal is to make you enjoy physics more.",
              link="https://sps.scripts.mit.edu/",
              category = category1)
session.add(club11)
session.commit()

club12 = Club(user_id = 1, name = "Pi Tau Sigma, Mechanical Engineering Honory Society",
              description = "The object of this organization shall be to encourage and recognize superior scholarship, "\
              "to foster the high ideals of the engineering profession, to stimulate interest in coordinating departmental "\
              "activities, to promote the mutual professional welfare of its members, and to develop in students of mechanical "\
              "engineering the attributes necessary for effective leadership and the taking up the responsibilities of a "\
              "citizen living in a democracy.",
              link="http://pts.mit.edu/",
              category = category1)
session.add(club12)
session.commit()

club13 = Club(user_id = 1, name = "Premedical Society",
              description = "A group for students interested in the medical field as a future career.",
              category = category1)
session.add(club13)
session.commit()

club14 = Club(user_id = 1, name = "Society of Women Engineers",
              description = "MIT SWE strives to: -educate members about career choices in engineering and promote community between "\
              "professionals and students, including through alumni -inspire younger generations about engineering, encourage the notion "\
              "of diversity in engineering, and determine and advocate for the needs of women engineers at MIT -build community at MIT SWE, "\
              "bridge a relationship with local and national sections, and record and disseminate the culture, history, and events of MIT SWE.",
              link="http://swe.mit.edu/",
              category = category1)
session.add(club14)
session.commit()

# add the rest of the categories

category2 = Category(user_id = 1, name="Arts")

session.add(category2)
session.commit()

club2 = Club(user_id = 1, name = "Arts at MIT",
             description = "The purpose of the MIT Art Club is to promote the appreciation "\
             "and practice of visual arts at MIT. We hope to provide an outlet for any student "\
             "or member of the MIT community to express their creativity and explore the arts "\
             "with other people who share this interest. We will run activities such as but not "\
             "limited to: Hosting 2 hour meetings every two weeks where members can meet to draw, "\
             "paint, and work on art together, Inviting artists, lecturers, architects, and designers, "\
             "whether permanent members of the MIT faculty or visiting presenters, to give lectures and "\
             "presentations to the club, Studying art history and the works of other artists together. We "\
             "will visit the Boston Museum of Fine Arts together and other exhibitions throughout Boston, "\
             "Selling our artworks or crafts to raise money for charitable groups on campus, Partnering with "\
             "MIT educational organizations to offer art lessons to kids who might not otherwise have such "\
             "exposure to art.",
             link = "http://artclub.mit.edu/about-0",
             category = category2)
session.add(club2)
session.commit()


category3 = Category(user_id = 1, name="Campus Media")
session.add(category3)
session.commit()

category4 = Category(user_id = 1, name="Computing")
session.add(category4)
session.commit()

category5 = Category(user_id = 1, name="Living Groups and Greeks")
session.add(category5)
session.commit()

category6 = Category(user_id = 1, name="Political Groups")
session.add(category6)
session.commit()

category7 = Category(user_id = 1, name="Religious Groups")
session.add(category7)
session.commit()

category8 = Category(user_id = 1, name="Services")
session.add(category8)
session.commit()

category9 = Category(user_id = 1, name="Social and Ethnic Groups")
session.add(category9)
session.commit()

category10 = Category(user_id = 1, name="Social Life Groups")
session.add(category10)
session.commit()

category11 = Category(user_id = 1, name="Special Interest Groups")
session.add(category11)
session.commit()

category12 = Category(user_id = 1, name="Sports")
session.add(category12)
session.commit()

category13 = Category(user_id = 1, name="Student Government")
session.add(category13)
session.commit()

print("added clubs!")
