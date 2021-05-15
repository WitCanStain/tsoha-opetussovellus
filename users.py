from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db
def login(username, password):
    sql = "SELECT password, user_id, role, visible FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    
    if user == None or user[3]==0:
        print("user not found in database")
        return False
    else:
        if check_password_hash(user[0],password):
            if user[2]=='oppilas':
                print("User " + username + " is a student.")
                session['role']='oppilas'
            elif user[2]=='opettaja':
                print("User " + username + " is a teacher.")
                session['role']='opettaja'
            else:
                print("An error occurred - user is neither teacher not student.")
            session["user_id"] = user[1]
            session["username"] = username

            return True
        else:
            print("Login failed: password incorrect.")
            return False

def register(role, f_name, l_name, username, password, passwordconf):
    hash_value = generate_password_hash(password)
    print("entered register function")
    if password == passwordconf:
        print("passwords match")
        try:
            sql = "INSERT INTO users (f_name, l_name, username, password, role, visible) VALUES (:f_name, :l_name, :username, :password, :role, :visible)"
            db.session.execute(sql, {"f_name":f_name, "l_name":l_name, "username":username, "password":hash_value, "role": role, "visible": 1})
            db.session.commit()
            print("user registered successfully")
        except:
            return False
    else:
        session["error"] = True
        return False

    return login(username,password)

def delete_user(user_id):
    try:
        sql = "UPDATE users SET visible=0 WHERE user_id=:user_id"
        db.session.execute(sql, {"user_id":user_id})
        db.session.commit()
        print("User deleted successfully.")
        return True
    except:
        return False

def get_teachers():
    try:
        sql = "SELECT f_name, l_name, user_id FROM users WHERE role='opettaja'"
        results = db.session.execute(sql).fetchall()
        print("getteach results:")
        for item in results:
            print(item)
        return results
    except:
        print("Something went wrong getting a list of teachers")

def get_name_from_id(user_id):
    try:
        sql = "SELECT f_name, l_name FROM users WHERE user_id=:user_id"
        result = db.session.execute(sql, {"user_id":user_id}).fetchone()
        return result
    except Exception as e:
        print(e)
        return False