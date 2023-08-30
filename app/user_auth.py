"""
for user authentication process
"""

from flask import Blueprint, render_template, redirect, flash, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

from .models import User
from . import db


user_auth = Blueprint("user_auth", __name__)


# add route API below as needed
# ex: login authentication


#
#
#
#
# user login API section
#
@user_auth.route("/login", methods=["GET"])
def login():
    """
    display login page when /login url is requested using GET method

    return render user_login.html
    """

    return render_template("user_templates/user_login.html")


#
# user login handler API
@user_auth.route("/user_login_handler", methods=["POST"])
def user_login_handler():
    """
    handle login form post request

    accept username and password from user_login.html
    check if username is available in the database
    compare password hash in the database to the recieved plaintext password

    if username and password is correct and validated:
    redirect to user_profile in user_views

    if not correct and not validated:
    redirect back to login page
    """

    # if user is loged in, redirect to user profile
    if current_user.get_id():
        flash(
            f"Please log out before login in again with other account.",
            category="error",
        )
        return redirect(url_for("user_views.user_profile"))

    username = request.form.get("username")
    password = request.form.get("password")

    to_login_user = User.query.filter_by(username=username).first()

    if to_login_user and to_login_user.role != "admin":
        if check_password_hash(to_login_user.password, password):
            login_user(to_login_user)
            return redirect(url_for("user_views.user_profile"))

    flash(f"Username or password is wrong.", category="error")
    return redirect("/login")


@user_auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()

    flash(f"Logout successful", category="success")
    return redirect("/login")


#
#
#
#
# user registration API section
#
@user_auth.route("/register", methods=["GET"])
def register():
    """
    display register page when /register url is requested using GET method

    return render user_register.html
    """

    return render_template("user_templates/user_register.html")


#
# user registration handler API
@user_auth.route("/user_register_handler", methods=["POST"])
def user_register_handler():
    """
    handle register form post request

    accept username password, repassword from user_register.html
    check if username is available in the database
    - if yes, registration failed

    compare password with the re-entered password:
    - if not match, registration failed

    if username not taken and password is match:
    process registration

    if all failed:
    redirect back to register page
    """

    # if user is loged in, redirect to user profile
    if current_user.get_id():
        flash(f"Please log out before registering another account.", category="error")
        return redirect(url_for("user_views.user_profile"))

    username = request.form.get("username")
    password = request.form.get("password")
    repassword = request.form.get("repassword")

    # check if username is already used
    to_check_username = User.query.filter_by(username=username).first()
    if to_check_username:
        flash(f"Username is aready taken.", category="warning")
        return redirect("/register")

    # check if password match
    if password == repassword:
        # add new user
        new_user = User(
            username=username,
            password=generate_password_hash(password, "pbkdf2:sha256"),
        )
        db.session.add(new_user)
        db.session.commit()

        flash(f"Account successfully created. Please login", category="success")
        return redirect("/login")
    elif password != repassword:
        flash("Password did not match.", category="error")
        return redirect("/login")

    # if all failed, redirect back
    flash(f"Account creation failed", category="error")
    return redirect("/register")
