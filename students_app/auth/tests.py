from unittest import TestCase

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

class AuthTests(TestCase):
    """Tests for authentication (login & signup)."""

    def setUp(self):
        """Executed prior to each test."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_signup(self):
        ''' Test that the user can signup '''
        form_data = {
          'username': 'signuptest',
          'password': 'signuppassword'
        }
        result = app.test_client().post('/signup', data=form_data)
        user = User.query.filter_by(username='signuptest').first()

        self.assertIsNotNone(user)
        self.assertEqual(result.status_code, 302)

    def test_signup_existing_user(self):
        ''' Test that a user cannot sign in with a duplicate username '''
        form_data = {
          'username': 'signuptest',
          'password': 'signuppassword'
        }
        response = app.test_client().post('/signup', data=form_data)
        response_text = response.get_data(as_text=True)

        self.assertNotIn('That username is taken. Please choose a different one.', response_text)
        self.assertEqual(response.status_code, 302)

    def test_login_correct_password(self):
        ''' Test that the user successfully logs in '''
        form_data = {
          'username': 'testlogin',
          'password': 'testlogin'
        }
        response = app.test_client().post('/signup', data=form_data)
        user = User.query.filter_by(username='testlogin').first()
        self.assertEqual(response.status_code, 302)

        response = app.test_client().post('/login', data=form_data)
        response_text = response.get_data(as_text=True)

        self.assertNotIn('Log In', response_text)
        self.assertEqual(response.status_code, 302)

    def test_login_nonexistent_user(self):
        ''' Test that a user cannot login if they havent made an account '''
        form_data = {
          'username': 'nopewrong',
          'password': 'totallyincorrect'
        }
        response = app.test_client().post('/login', data=form_data)
        response_text = response.get_data(as_text=True)

        self.assertIn('Log In', response_text)
        self.assertIn('No user with that username. Please try again.', response_text)

    def test_login_incorrect_password(self):
        ''' Test that a User gets an error message when they enter an incorrect password '''
        create_user()

        form_data = {
          'username': 'me1',
          'password': 'totallyincorrect'
        }
        response = app.test_client().post('/login', data=form_data)
        response_text = response.get_data(as_text=True)

        self.assertIn('Password doesn&#39;t match. Please try again.', response_text)

    def test_logout(self):
        ''' Test a User can loggout '''
        create_user()

        form_data = {
          'username': 'me1',
          'password': 'password'
        }
        app.test_client().post('/login', data=form_data)
        response = app.test_client().get('/logout', follow_redirects=True)
        response_text = response.get_data(as_text=True)

        self.assertIn('Log In', response_text)
