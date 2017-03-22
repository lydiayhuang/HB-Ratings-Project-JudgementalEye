"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    # a = jsonify([1,3])
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/register", methods=['GET'])
def register_form():
    """New user registration."""

    return render_template('registration_form.html')

@app.route("/log_out", methods=['GET'])
def log_out():
    """logs user out."""
    del session["logged_in"]
    flash("Logged out")
    return render_template('homepage.html')

@app.route("/register", methods=['POST'])
def register_process():
    """Process the form."""
    email = request.form.get('uemail')
    password = request.form.get('psw')

    user = User.query.filter(User.email == email).first()

    if user is None:
        
        flash("You've created your account!")
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        session['logged_in'] = new_user.user_id

        return redirect("/")
    else:
        flash("Email has been registered. Please use another one.")
        return render_template("registration_form.html")


@app.route("/login_form")
def show_form():
    """Login Form."""

    return render_template("login_form.html")


@app.route("/login_form", methods=['POST'])
def process_form():
    """Checks if email and password match."""

    email = request.form.get('uemail')
    password = request.form.get('psw')

    user = User.query.filter(User.email == email).first()

    if user is None:
        flash("Email doesn't exist. Please log in again.")
        return render_template("login_form.html")
    elif user.password != password:
        flash("Wrong password. Please type in your password again.")
        return render_template("login_form.html")
    else:
        session['logged_in'] = user.user_id
        return redirect("/")





if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
