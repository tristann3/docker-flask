from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SelectField, SubmitField, TextAreaField
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from students_app.models import Student, Professor, Class

class StudentForm(FlaskForm):
    """Form to create a student."""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=80)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=80)])
    classes = QuerySelectMultipleField('Class', query_factory=lambda: Class.query, allow_blank=False)
    submit = SubmitField('Submit')

class ProfessorForm(FlaskForm):
    """Form to create a professor."""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=3, max=80)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Submit')

class ClassForm(FlaskForm):
    """Form to create a professor."""
    title = StringField('Class Title', validators=[DataRequired(), Length(min=3, max=80)])
    professor = QuerySelectField('Professor', query_factory=lambda: Professor.query, allow_blank=False)
    submit = SubmitField('Submit')