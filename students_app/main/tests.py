import os
import unittest

from datetime import date
 
from students_app import app, db, bcrypt
from students_app.models import Student, Professor, User, Class

"""
Run these tests with the command:
python -m unittest books_app.main.tests
"""

#################################################
# Setup
#################################################

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def create_classes():
    p1 = Professor(first_name='Joi', last_name='Anderson')
    c1 = Class(
        title='CS 1.2',
        professor=p1
    )
    db.session.add(c1)
    db.session.add(p1)

    s1 = Student(first_name='Tristan', last_name='Thompson')
    db.session.add(s1)
    db.session.commit()

def create_user():
    password_hash = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='me1', password=password_hash)
    db.session.add(user)
    db.session.commit()

#################################################
# Tests
#################################################

class MainTests(unittest.TestCase):
 
    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    def test_homepage_logged_out(self):
        """Test that the class, student and professor show up on the homepage."""
        # Set up
        create_classes()
        create_user()

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('CS 1.2', response_text)
        self.assertIn('Joi Anderson', response_text)
        self.assertIn('Log In', response_text)
        self.assertIn('Sign Up', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged in users)
        self.assertNotIn('Create Student', response_text)
        self.assertNotIn('Create Class', response_text)
        self.assertNotIn('Create Professor', response_text)

    
    def test_homepage_logged_in(self):
        """Test that the details show up on the homepage."""
        # Set up
        create_classes()
        create_user()
        login(self.app, 'me1', 'password')

        # Make a GET request
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Check that page contains all of the things we expect
        response_text = response.get_data(as_text=True)
        self.assertIn('Joi Anderson', response_text)
        self.assertIn('CS 1.2', response_text)
        self.assertIn('me1', response_text)
        self.assertIn('+ New Student', response_text)
        self.assertIn('+ New Class', response_text)
        self.assertIn('+ New Professor', response_text)

        # Check that the page doesn't contain things we don't expect
        # (these should be shown only to logged out users)
        self.assertNotIn('Log In', response_text)
        self.assertNotIn('Sign Up', response_text)

    def test_student_detail_logged_in(self):
        """Test that the class appears on student detail page."""
        create_classes()
        create_user()
        login(self.app, 'me1', 'password')

        response = self.app.get('/student/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('Tristan Thompson', response_text)
        self.assertIn('CS 1.2', response_text)
        self.assertIn('You are logged in as me1', response_text)

        self.assertNotIn('Sign Up', response_text)


    def test_class_detail_logged_in(self):
        """Test that the class details appears on its detail page."""
        create_classes()
        create_user()
        login(self.app, "me1", "password")

        response = self.app.get('/class/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('CS 1.2', response_text)
        self.assertIn('Joi Anderson', response_text)

    def test_professor_detail_logged_in(self):
        """Test that the professor details appears on its detail page."""
        create_classes()
        create_user()
        login(self.app, "me1", "password")

        response = self.app.get('/professor/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        response_text = response.get_data(as_text=True)
        self.assertIn('CS 1.2', response_text)
        self.assertIn('Joi Anderson', response_text)
