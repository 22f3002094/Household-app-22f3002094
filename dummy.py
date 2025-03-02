#using sqlalchemy declarative base
from flask import Flask
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Flask App Setup
app = Flask(__name__)
DATABASE_URL = 'sqlite:///example.db'
engine = create_engine(DATABASE_URL)  # Engine
Base = declarative_base()  # SQLAlchemy Base class
Session = scoped_session(sessionmaker(bind=engine))  # Session factory

# Define a Model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)

# Create tables
with app.app_context():
    Base.metadata.create_all(engine)

# CRUD Example: Insert Data
@app.route('/add_user')
def add_user():
    session = Session()  # Manual session management
    new_user = User(name="John Doe", email="john@example.com")
    session.add(new_user)
    session.commit()
    session.close()  # Must manually close the session
    return "User added!"





#=================using flask sqlalchemy=========


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Flask App Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)  # Flask-SQLAlchemy setup

# Define a Model
class User(db.Model):
    __tablename__ = "usertable"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# CRUD Example: Insert Data
@app.route('/add_user')
def add_user():
    new_user = User(name="John Doe", email="john@example.com")
    db.session.add(new_user)  # Automatic session management
    db.session.commit()  # No need to close session explicitly
    return "User added!"



#=========how sqlalchemy works under the hood ============
user = User.query.filter_by(name="John").first()
#SELECT * FROM users WHERE name='John' LIMIT 1;




#============parentchild=====
# Parent class
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return f"{self.name} makes a sound."

# Child class
class Dog(Animal):
    def __init__(self, name, breed):
        # Calling the parent class constructor
        super().__init__(name)
        self.breed = breed
    
    

# Create instances of the classes
animal = Animal("Generic Animal")
dog = Dog("Buddy", "Golden Retriever")

# Call methods
print(animal.speak())  # Output: Generic Animal makes a sound.
print(dog.speak())     # Output: Buddy barks.





#=========one to many========

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # One-to-Many relationship with Post using backref
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    
    # Foreign Key to User (Many side of the relationship)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
