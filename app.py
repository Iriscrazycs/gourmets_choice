from flask import Flask
from flask import redirect, render_template, request,session

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

#for password


app = Flask(__name__)
app.secret_key = '5a367c29b8da2dc543a1f3d264f78abe' #how to set up enviromental variable
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///postgres"
db = SQLAlchemy(app)


@app.route("/")
def main():
    return render_template("main.html")

@app.route("/loggin")
def loggin():
    return render_template("loggin.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register",methods=["POST"])
def registerCheck():
    email1=request.form["email"]
    password=request.form["password"]
    pswd=generate_password_hash(password)
    db.session.execute("INSERT into users (email, password) Values (:email1, :pswd)",
    {"email1": email1, "pswd":pswd})
    db.session.commit()
    return redirect("/loggin")

@app.route("/loggin", methods=["POST"])
def loggincheck():
    email1=request.form["email"]
    password=request.form["password"]
    sql=db.session.execute("Select * from users where email=:email1",{"email1":email1})
    print("1")
    email=sql.fetchall()
    if len(email)==0:
        
        return redirect("/register")    
    else :

        check=check_password_hash(email[0][2],password)
        if (check):
            session["user"]=email1
            return redirect("/restaurants")
        else:
            return redirect("/loggin")
        

    
    
#redirect to all restaurants page

@app.route("/restaurants")
def restaurants():
    result= db.session.execute("Select * from restaurants")
    data=result.fetchall()
    print(data)
    return render_template("restaurants.html",restaurants=data)

@app.route("/restaurants/<int:id1>")
def restaurant(id1):
    result= db.session.execute("Select * from restaurants where id=:id1",{"id1":id1})
    data=result.fetchall()
    print(data)
    return render_template("restaurant.html",restaurants=data)



