from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db
def login(username, password):
    sql = "SELECT password, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    
    if user == None:
        return False
    else:
        if check_password_hash(user[0],password):
            session["user_id"] = user[1]
            return True
        else:
            return False

def register(username, password, passwordconf, role):
    hash_value = generate_password_hash(password)

    try:
        sql = "INSERT INTO users (username, password, role) VALUES (:username, :password, :role)"
        db.session.execute(sql, {"username":username, "password":hash_value, "role": role})
        db.session.commit()
    except:
        return False
    return login(username,password)

    
