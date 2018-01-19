import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

# create User table
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    name = Column(String(250), nullable = False)
    googid = Column(String(300), nullable = False)
    picture = Column(String(250))

# create Category table
class Category(Base):
    __tablename__ = 'category'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return{
            'name': self.name,
            'id': self.id
        }

# create Club table
class Club(Base):
    __tablename__ = 'club'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(1000))
    link = Column(String(200))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    # add decorator property to serialize data from database
    @property
    def serialize(self):
        return{
            'name': self.name,
            'id': self.id,
            'description': self.description,
            'link': self.link,
            'category': self.category.name
        }
    

# create database
engine = create_engine("sqlite:///mitclubswithusers.db")

# adds tables to database
Base.metadata.create_all(engine)
