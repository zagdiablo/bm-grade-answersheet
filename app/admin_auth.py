"""
for admin authentication process
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import (
    current_user,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash

from .models import User


admin_auth = Blueprint("admin_auth", __name__)


#
#
#
#
# TODO test admin login
#
@admin_auth.route("/admin_login", methods=["GET"])
def admin_login():
    """
    display admin login page
    when /admin_login url is requested using GET method
    and not loged in into any other user or admin account

    return render admin_login.html
    """

    # check if user is loged in
    if current_user.get_id():
        return redirect(url_for("user_views.user_profile"))

    return render_template("admin_templates/admin_login.html")


#
# admin login handler
@admin_auth.route("/admin_login_handler", methods=["POST"])
def admin_login_hander():
    """
    handle admin login form post request
    accept username and password from admin_login.html
    check if username is available in the database
    compare password hash in the database to the recieved plaintext password
    check if user role is admin

    if username, password is correct and user is admin:
    redirect to admin_dashboard in admin_views

    if not correct and not validated:
    redirect back to login page
    """

    username = request.form.get("username")
    password = request.form.get("password")

    to_check_username = User.query.filter_by(username=username).first()

    if to_check_username:
        if not to_check_username.role == "admin":
            flash("Username or password is wrong.", category="error")
            return redirect("/admin_login")

        if check_password_hash(to_check_username.password, password):
            login_user(to_check_username)
            return redirect(url_for("admin_views.admin_dashboard"))

    flash(
        f"Something is wrong, if this continues, contact your site administrator.",
        category="error",
    )
    return redirect("/admin_login")


#
# admin logout handler
@admin_auth.route("/admin_logout", methods=["GET"])
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for("user_views.home"))
