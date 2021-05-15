

from flask import Flask, redirect, render_template, request, session, flash
from os import getenv
from flask_sqlalchemy import SQLAlchemy
import users
from app import app
from db import db
import courses
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")


@app.route("/")
def index():
    if 'user_id' in session:
        print("user id: " + str(session["user_id"]))
        course_list = courses.get_courses_for_user(session['user_id'])
        
        teachers = users.get_teachers()
        return render_template("teacher_view.html", teachers=teachers)
    
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        print("login successful.")
    
    return redirect("/")

@app.route("/logout")
def logout():

    for item in list(session.keys()):
        print(item)
        del session[item]
    return redirect("/")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        role = request.form["role"]
        f_name = request.form["f_name"]
        l_name = request.form["l_name"]
        username = request.form["username"]
        password = request.form["password"]
        passwordconf = request.form["passwordconf"]
        
        users.register(role, f_name, l_name, username, password, passwordconf)
        

    return render_template("register.html")


@app.route("/addcourse", methods=['POST'])
def add_course():
    course_name = request.form['course_name']
    teacher_id = request.form['opettaja']
    print("course_name: " + str(type(course_name)))
    print("teacher_id: " + str(teacher_id))
    if courses.add_course(course_name, teacher_id):
        flash("Course " + course_name + " has been successfully added!")
    else:
        flash("You need to specify a course name and teacher!")
    return redirect("/")

@app.route("/courses", methods=['GET', 'POST'])
def view_courses():
    if session['role'] == 'opettaja':
        course_list = courses.teacher_courses()
        return render_template("teacher_courses.html", courses=course_list)

@app.route("/course", methods=['POST','GET'])
def view_course():
    if request.method=='POST':
        course = request.form['course']
        session["current_course_id"] = course
        session["current_course_name"] = courses.get_course_name_from_id(course)
    else:
        course = session["current_course_id"]
    if session['role'] == 'opettaja':
            participant_list = courses.participants(course)
            return render_template("teacher_course_view.html", participants=participant_list)

@app.route("/removestudent", methods=['POST'])
def remove_student():
    value = request.form['remove'].split(':')
    
    print("user id and course_id:")
    print(value)
    
    if courses.remove_from_course(value[0],value[1]):
        student_name = users.get_name_from_id(value[0])
        flash("Opiskelija " + student_name[0] + " " + student_name[1] + " on poistettu kurssilta.")
    else:
        flash("Opiskelijan poistaminen kurssilta ei onnistunut.")
    return render_template("teacher_course_view.html", participants=courses.participants(value[1]))

@app.route("/removecourse", methods=['POST'])
def remove_course():
    course = request.form['removecourse']
    if courses.remove_course(course):
        flash("Kurssi on poistettu.")
        session["current_course_id"] = None
        session["current_course_name"] = None
    else:
        flash("Kurssin poistaminen ei onnistunut.")
    return redirect("/courses")

@app.route("/changecoursename", methods=['POST'])
def change_course_name():
    new_course_name = request.form['newcoursename']
    old_course_id = session["current_course_id"]
    if courses.change_course_name(old_course_id, new_course_name):
        flash("Changed course " + session["current_course_name"] + " name to " + new_course_name)
    else:
        flash("Something went wrong - course name was not changed.")
    return redirect("/course")

@app.route("/addstudent", methods=['POST'])
def add_student():
    if session['role'] == 'opettaja':
        student = request.form['addstudent']
        course = session["current_course_id"]
        if courses.add_student(student, course):
            flash("Added student to course successfully.")
        else:
            flash("Something went wrong. Student was not added to course. Perhaps they are already a participant?")
        return redirect("/course")

@app.context_processor
def utility_processor():
    def teachers():
        return users.get_teachers()
    return dict(teachers=teachers)