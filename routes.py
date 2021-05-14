from flask import Flask
from flask import redirect, render_template, request, session
from os import getenv
from flask_sqlalchemy import SQLAlchemy
import users
from app import app
from db import db
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=['POST'])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        session["username"] = username
    
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
        username = request.form["username"]
        password = request.form["password"]
        passwordconf = request.form["passwordconf"]
        
        if password == passwordconf:
            users.register(username, password, passwordconf, role)
            session["registered"] = True
            session["username"] = username
        else:
            session["error"] = True
            return render_template("register.html")
        
        return render_template("register.html")
    else:
        return render_template("register.html")


