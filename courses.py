from flask import session
from db import db


def get_courses_for_user(user_id):
    try:
        sql = """SELECT name FROM courses LEFT JOIN course_subscriptions 
                ON courses.course_id=course_subscriptions.course_id 
                AND course_subscriptions.user_id=:user_id"""
        results = [row[0] for row in db.session.execute(sql, {"user_id":user_id}).fetchall()]
        return results
    except Exception as e:
        print(e)
        return False

def get_course_name_from_id(course_id):
    try:
        sql = " SELECT name FROM courses WHERE course_id=:course_id "
        result = db.session.execute(sql, {"course_id":course_id}).fetchone()
        return result[0]
    except Exception as e:
        print(e)
        return False

def change_course_name(old_course_id, new_course_name):
    try:
        sql = " UPDATE courses SET name=:new_name WHERE course_id=:course_id "
        db.session.execute(sql, {"new_name":new_course_name, "course_id":old_course_id})
        db.session.commit()
        print("Changed course name to " + new_course_name)
        return True
    except Exception as e:
        print(e)
        return False


def teacher_courses():
    try:
        
        sql = """ SELECT courses.name, courses.course_id, COUNT(course_subscriptions.course_id)
        FROM courses LEFT JOIN course_subscriptions
        ON courses.teacher_id=:user_id
        AND course_subscriptions.course_id=courses.course_id
        GROUP BY courses.course_id, courses.name
        """
        results = db.session.execute(sql, {"user_id":session['user_id']}).fetchall()
        print("Query results for teacher_courses:")
        print(results)
        
        return results
        
    except Exception as e:
        print(e)
        return False


        """ SELECT courses.name, course_subscriptions.course_id, COUNT(*)
        FROM courses LEFT JOIN course_subscriptions
        ON courses.teacher_id=:user_id
        WHERE course_subscriptions.course_id=courses.course_id
        GROUP BY course_subscriptions.course_id, courses.name
        """

def participants(course):

    sql = """ SELECT users.f_name, users.l_name, users.user_id, :course
    FROM users LEFT JOIN  course_subscriptions
    ON course_subscriptions.course_id=:course
    WHERE users.user_id=course_subscriptions.user_id
    """
    try:
        results = db.session.execute(sql, {"course":course}).fetchall()
        print(results)
        if len(results)==0:
            return False
        return results
    except Exception as e:
        print(e)

def add_course(course_name, teacher_id):
    
    if course_name == "":
        print("error: course_name or teacher_id inexistent.")
        return False
    try:
        sql = "INSERT INTO courses (name, teacher_id) VALUES (:course_name, :teacher_id)"
        db.session.execute(sql, {"course_name":course_name, "teacher_id":teacher_id})
        db.session.commit()
        print("Course " + course_name + " taught by " + str(teacher_id) +  " added.")
        return True
    except:
        print("Something went wrong when adding course.")
        return False

def remove_from_course(student_id, course_id):
    try:
        sql = " DELETE FROM course_subscriptions WHERE user_id=:student_id AND course_id=:course_id "
        db.session.execute(sql, {"student_id":student_id, "course_id":course_id})   
        db.session.commit()
        print("Student successfully removed from course.")
        return True
    except Exception as e:
        print(e)
        return False

def remove_course(course_id):
    try:
        sql = " DELETE FROM courses WHERE course_id=:course_id "
        db.session.execute(sql, {"course_id":course_id})   
        db.session.commit()
        print("Course successfully removed.")
        return True
    except Exception as e:
        print(e)
        return False

def add_student(student, course_id):
    try:
        if student.isnumeric():
            sql = " INSERT INTO course_subscriptions (user_id, course_id) VALUES (:student_id, :course_id) "
            db.session.execute(sql, {"student_id":student,"course_id":course_id})   
            db.session.commit()
            print("Student added to course successfully.")
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
