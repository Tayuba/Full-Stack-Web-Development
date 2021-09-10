from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Wrong password, try again", category="error")
        else:
            flash("Email does not exists, create an account.", category="error")
    # data = request.form
    # print(data)
    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email in use, choose another email", category="error")
        elif len(email) < 5:
            flash("Email must be greater than 4 characters.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character.", category="error")
        elif len(last_name) < 2:
            flash("Last name must be greater than 1 character.", category="error")
        elif password1 != password2:
            flash("Password not matching.", category="error")
        elif len(password1) < 7:
            flash("Password must be greater than 6 characters.", category="error")
        else:
           # Add user to database
           new_user = User(email=email, first_name=first_name, last_name=last_name, password=generate_password_hash(password1, method="sha256"))
           db.session.add(new_user)
           db.session.commit()
           login_user(user, remember=True)
           flash("Account Created.", category="Successful")
           return redirect(url_for("views.home"))

    return render_template("sign_up.html", user=current_user)
