"""
a view that is only available to the logged in users
ex: dashboard, shoping history, change password
"""

from flask import Blueprint, render_template
from flask_login import login_required, current_user

from .models import User


user_views = Blueprint("user_views", __name__)


@user_views.route("/home", methods=["GET"])
def home():
    return render_template("home.html")


@user_views.route("/user_profile", methods=["GET"])
@login_required
def user_profile():
    loged_in_user = User.query.get(current_user.get_id())

    username = loged_in_user.username

    return render_template("user_templates/user_profile.html", username=username)
