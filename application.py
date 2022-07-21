import os
from flask import Flask, redirect, render_template, request, session, url_for
from flask.scaffold import _matching_loader_thinks_module_is_package
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from datetime import datetime
import math
import simplejson as json

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fproject.db"
app.config["SESSION_TYPE"] = "filesystem"

# Initialize database
db = SQLAlchemy(app)

# Create db model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    hash = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "<User %r>" % self.username

class Sessions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return "<Session %r>" % self.name

class Todolist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return "<Todolist %r>" % self.name

# Login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if session["user_id"] is None:
            return redirect("/")
        data = json.loads(request.data)
        if data["name"] == " " or data["name"] == "":
            name = "-"
        else:
            name = data.get("name")
        date = datetime.now()
        duration = data.get("duration")

        new_session = Sessions(name=name, duration=duration, date=date, user_id=session["user_id"])
        db.session.add(new_session)
        db.session.commit()
        return redirect("/")
    else:
        # display todo tasks
        # check if user is logged in
        if session.get("user_id") is None:
            userLoggedIn = False
            message = "Login to start creating your todo lists!"
            return render_template("index.html", message=message, user=userLoggedIn)
        else:
            userLoggedIn = True
            todoTasks = db.session.query(Todolist).filter(Todolist.user_id == session["user_id"]).all()
            return render_template("index.html", todoTasks=todoTasks, user=userLoggedIn)

@app.route("/register", methods=["GET", "POST"])
def redister():
    """Register user"""

    if request.method == "POST":

        # Forget any user_id
        session.clear()

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure everything is filled out
        if not username or not password or not confirmation:
            return render_template("register.html", message="Please fill in all fields")

        # Ensure passwords match
        if password != confirmation:
            return render_template("register.html", message="Passwords do not match")

        # Ensure username is unique
        if db.session.query(Users).filter(Users.username == username).count() > 0:
            return render_template("register.html", message="Username already exists")

        # Add new user to database
        new_user = Users(username=username, hash=generate_password_hash(password))
        try:
            db.session.add(new_user)
            db.session.commit()
            return render_template("register.html", message="Registration successful")
        except:
            return render_template("register.html", message="Something went wrong")

    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

            # Forget any user_id
            session.clear()
    
            # Ensure username was submitted
            username = request.form.get("username")
            password = request.form.get("password")
    
            # Ensure username exists and password is correct
            user = db.session.query(Users).filter(Users.username == username).first()
            if not user or not check_password_hash(user.hash, password):
                return render_template("login.html", message="Invalid username and/or password")

            # Remember which user has logged in
            session["user_id"] = user.id
    
            # Redirect user to home page
            return redirect("/") 
    else:
        return render_template("login.html")

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    if request.method == "POST":
        # Forget any user_id
        session.clear()
        return redirect("/")
    else:
        # display username of the user
        user = db.session.query(Users).filter(Users.id == session["user_id"]).first()
        sessionsHistory = db.session.query(Sessions).filter(Sessions.user_id == session["user_id"]).order_by(Sessions.id.desc())
        for sessionRow in sessionsHistory:
            hours = math.floor(sessionRow.duration / 3600)
            minutes = math.floor((sessionRow.duration % 3600) / 60)
            seconds = (sessionRow.duration % 3600) % 60
            if hours == 0 and minutes == 0:
                sessionRow.duration = str(seconds) + "s"
            elif hours == 0:
                sessionRow.duration = str(minutes) + "m " + str(seconds) + "s"
            else:
                sessionRow.duration = str(hours) + "h " + str(minutes) + "m"
        
        if sessionsHistory.count() == 0:
            return render_template("account.html", username=user.username, message = "No finished sessions yet")
        else:
            return render_template("account.html", username=user.username, sessions=sessionsHistory)

@app.route("/todolist", methods=["POST"])
def todolist():
    if request.method == "POST":
        addTask = request.form.get("todoItem")
        newTask = Todolist(name=addTask, complete = False, user_id=session["user_id"])
        db.session.add(newTask)
        db.session.commit()
        return redirect("/")

@app.route("/update/<int:task_id>")
def update(task_id):
    # delete todo task
    todo = Todolist.query.filter_by(id=task_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete(task_id):
    # delete todo task
    todo = Todolist.query.filter_by(id=task_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
