from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name', 'phone_number')
    def validates_author(self, key, value):
        if key == 'name':
            if not value:
                raise ValueError('A valid name is required')
        
            found_name = Author.query.filter(Author.name == value).first()
            
            if found_name:
                raise ValueError('Author by that name already exists')
        
        elif key == 'phone_number':
            #Filtered non-digits using regex
            clean_number = re.sub("[^0-9]", "", value)
            if len(clean_number) != 10:
                raise ValueError('Phone number must be exactly ten digits')
        
        return value
        
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('title', 'content', 'summary', 'category')
    def validates_post(self, key, value):
        if key == 'title':
            if not value:
                raise ValueError("Post must have a title")
            
            if not any(phrase in value for phrase in ["Won't Believe", "Secret", "Top", "Guess"]):
                raise ValueError("Title is not clickbait-y")
            
        elif key == 'content':
            if len(value) < 250:
                raise ValueError("Content must be at least 250 characters long")
            
        elif key == 'summary':
            if(len(value) > 250):
                raise ValueError("Summary has a maximum of 250 characters")
            
        elif key == 'category':
            if value not in ['Fiction','Non-Fiction']:
                raise ValueError("Category must be either fiction or non-fiction")
        
        


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
