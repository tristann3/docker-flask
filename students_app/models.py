"""Create database models to represent tables."""
from students_app import db
from sqlalchemy.orm import backref
from flask_login import UserMixin
import enum

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f'<User: {self.username}>'

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    classes = db.relationship('Class', secondary='student_class', back_populates='students')
  
    def __repr__(self):
        return f'<Student: {self.first_name} {self.last_name}>'

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    classes = db.relationship('Class', back_populates='professor')
  
    def __repr__(self):
        return f'{self.first_name} {self.last_name}'

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    professor_id = db.Column(db.Integer, db.ForeignKey('professor.id'), nullable=False)
    professor = db.relationship('Professor', back_populates='classes')
    students = db.relationship('Student', secondary='student_class', back_populates='classes')
  
    def __repr__(self):
        return f'{self.title}'



course_table = db.Table('student_class',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'))
)

