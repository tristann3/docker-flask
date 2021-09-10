from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from students_app.models import  User, Student, Professor, Class
from students_app.main.forms import StudentForm, ProfessorForm, ClassForm
from students_app import bcrypt

# Import app and db
from students_app import app, db
main = Blueprint('main', __name__)

# Create your routes here.
@main.route('/')
def homepage():
    ''' Delivers homepage '''
    all_classes = Class.query.all()
    all_students = Student.query.all()
    all_professors = Professor.query.all()
    print(all_classes)
    return render_template('home.html',
        all_students=all_students, all_professors=all_professors, all_classes=all_classes)

@main.route('/create_student', methods=['GET', 'POST'])
@login_required
def create_student():
    ''' Route to create a Student '''
    form = StudentForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_student = Student(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            classes=form.classes.data
        )
        db.session.add(new_student)
        db.session.commit()

        flash('New student was created successfully.')
        return redirect(url_for('main.student_detail', student_id=new_student.id))
    return render_template('create_student.html', form=form)

@main.route('/student/<student_id>', methods=['GET', 'POST'])
@login_required
def student_detail(student_id):
    ''' Route to show Student details '''
    student = Student.query.get(student_id)
    form = StudentForm(obj=student)
    print(student.classes)

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.classes = form.classes.data

        db.session.commit()

        flash('New student was updated successfully.')
        return redirect(url_for('main.student_detail', student_id=student_id))

    return render_template('student_detail.html', student=student, form=form)

@main.route('/create_professor', methods=['GET', 'POST'])
@login_required
def create_professor():
    ''' Route to create a Professor '''
    form = ProfessorForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_professor = Professor(
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        db.session.add(new_professor)
        db.session.commit()

        flash('New professor was created successfully.')
        return redirect(url_for('main.professor_detail', professor_id=new_professor.id))
    return render_template('create_professor.html', form=form)

@main.route('/professor/<professor_id>', methods=['GET', 'POST'])
@login_required
def professor_detail(professor_id):
    ''' Route to show Professor details '''
    professor = Professor.query.get(professor_id)
    form = ProfessorForm(obj=professor)
    print(professor.classes)

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        professor.first_name = form.first_name.data
        professor.last_name = form.last_name.data

        db.session.commit()

        flash('New professor was updated successfully.')
        return redirect(url_for('main.professor_detail', professor_id=professor_id))

    return render_template('professor_detail.html', professor=professor, form=form)

@main.route('/create_class', methods=['GET', 'POST'])
@login_required
def create_class():
    ''' Route to create a Class '''
    form = ClassForm()

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        new_class = Class(
            title=form.title.data,
            professor=form.professor.data
        )
        db.session.add(new_class)
        db.session.commit()

        flash('New class was created successfully.')
        return redirect(url_for('main.class_detail', class_id=new_class.id))
    return render_template('create_class.html', form=form)

@main.route('/class/<class_id>', methods=['GET', 'POST'])
@login_required
def class_detail(class_id):
    ''' Route to show Class details '''
    class_object = Class.query.get(class_id)
    form = ClassForm(obj=class_object)

    # if form was submitted and contained no errors
    if form.validate_on_submit(): 
        class_object.title = form.title.data
        class_object.professor = form.professor.data

        db.session.commit()

        flash('New class was updated successfully.')
        return redirect(url_for('main.class_detail', class_id=class_id))

    return render_template('class_detail.html', class_object=class_object, form=form)