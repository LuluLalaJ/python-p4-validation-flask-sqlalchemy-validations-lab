from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

    @validates('name')
    def check_name(self, key, name):
        all_names = db.session.query(Author.name).all()
        if name and (name not in all_names):
            return name
        raise ValueError ('error')

    @validates('phone_number')
    def check_number(self, key, number):
        if len(number) == 10:
            return number
        raise ValueError ('error')

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title')
    def check_title(self, key, title):
        keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if any(word in title for word in keywords):
            return title
        raise ValueError('error')

    @validates('content', 'summary')
    def check_length(self, key, text):
        if key == "content":
            if len(text) >= 250:
                return text
        if key == "summary":
            if len(text) < 250:
                return text
        raise ValueError ('error')

    @validates('category')
    def check_category(self, key, cat):
        if cat == "Fiction" or cat == "Non-Fiction":
            return cat
        raise ValueError('error')


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
