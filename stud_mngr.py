import json
from flask import Flask, render_template, request, redirect, session
import utility.json_utils as json_utils
import utility.utils as utils

app=Flask(__name__)

USER_FILE="data/user_data.json"
app.secret_key="sakthicomputersstudentregistrationform"

def checkloggedin():
    try:
        if session["loggedin"]:
           return True
        else:
            return False
    except:
        return False

@app.route("/")
def index():
    return render_template("home.html")

### This function is still not completed
@app.route("/search")
def student_data():
    if not checkloggedin():
        return render_template("home.html",error="User not logged in")
    data=json_utils.read_json(USER_FILE)
    return render_template("search.html",student_list=data["user_type"]["student"])

@app.route("/add_course", methods=["POST","GET"])
def add_course():
    data=json_utils.read_json(USER_FILE)
    for stud in data["user_type"]["student"]:
        if stud["user_id"]==session["username"]:
            if request.form['course']:
                stud["course"][request.form['course']]="Inprogress"
                json_utils.write_json(USER_FILE,data)
            return render_template("student_profile.html", stud=stud)
    return render_template("home.html" ,error="Somthing went wrong !! Please login again")

@app.route("/register_student", methods=["POST","GET"])
def register_student():
    if not checkloggedin():
        return render_template("home.html",error="User not logged in")
    msg=""
    error=""
    user_details=""
    if request.method=="POST":
        data=json_utils.read_json(USER_FILE)
        if request.form["course"]=="1":
            error="Course not chosen"
            return render_template("student_registration.html", error=error)
        for student in data["user_type"]["student"]:
            if student["user_id"]==str(request.form["firstname"])+"."+str(request.form["lastname"])+"@sakthicomputers.com":
                error=f"user {student['user_id']} already exist"
                render_template("student_registration.html", error=error)
        course_list=[]
        course_data={
            request.form["course"]:"Inprogress"
            }
        course_list.append(course_data)
        stud_json={
            "first_name": request.form["firstname"],
            "last_name": request.form["lastname"],
            "qualification": request.form["qualification"],
            "phone" : request.form["phone"],
            "address": request.form["address"],
            "gender" : request.form["inlineRadioOptions"],
            "doj": request.form["date"],
            "course": course_data,
            "email": request.form["email"],
            "user_id":str(request.form["firstname"])+"."+str(request.form["lastname"])+"@sakthicomputers.com",
            "password": str(request.form["phone"])
        }
        data["user_type"]["student"].append(stud_json)
        json_utils.write_json(USER_FILE,data)
        msg="User registered successfully!!"
        user_details=("please take note of \nuser_id : " + 
        str(request.form["firstname"])+"."+str(request.form["lastname"])+
        "@sakthicomputers.com\n" + "password : " + str(request.form["phone"]))
    return render_template("student_registration.html", msg=msg,user_details=user_details)

@app.route("/login", methods=["POST","GET"])
def login():
    error=""
    if request.method=="POST":
        data=json_utils.read_json(USER_FILE)
        if utils.checkadmin(request.form["user"]):
            for admin in data["user_type"]["admin"]:
                if admin["user_email"]==request.form["user"]:
                    if admin["user_password"]==request.form["password"]:
                        session['loggedin'] = True
                        session['username'] = request.form["user"]
                        return render_template("student_registration.html")
                    else:
                        error="Invalid password"
                        break
                else:
                    error="User not registered"
        else:
            for stud in data["user_type"]["student"]:
                if stud["user_id"]==request.form["user"]:
                    if stud["password"]==request.form["password"]:
                        session['loggedin'] = True
                        session['username'] = request.form["user"]
                        return render_template("student_profile.html", stud=stud)
                    else:
                        error="Invalid password"
                        break
                else:
                    error="User not registered"
    return render_template("home.html",error=error)

@app.route("/register", methods=["POST","GET"])
def register():
    data=json_utils.read_json(USER_FILE)
    if request.method=="POST":
        
        for admin in data["user_type"]["admin"]:
            if admin["user_email"]==request.form["email"]:
                msg=f"user {request.form['email']} already exist"
                render_template("register.html",msg=msg)
            elif request.form["password"]!= request.form["repeat_password"]:
                msg="Entered password is not same"
                render_template("register.html",msg=msg)
        user_data={
        "user_name" : request.form["username"],
        "user_email": request.form["email"],
        "user_password": request.form["password"]
        }
        data["user_type"]["admin"].append(user_data)
        json_utils.write_json(USER_FILE,data)
        msg="user registered successfully! Please login to continue!!"
        return render_template("home.html",msg=msg)
        
    return render_template("register.html")

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)