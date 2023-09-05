"""
a view that is only available to the admins, and can only be accessed by
a user that has admin privileges

ex: database edit, add new product to the store listing
"""

from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from .models import User
from . import db


admin_views = Blueprint("admin_views", __name__)


#
#
#
#
# admin dashboard
#
@admin_views.route("/admin_dashboard", methods=["GET"])
@login_required
def admin_dashboard():
    """
    when admin login is success

    return render admin_dashboard.html
    """
    user = User.query.get(current_user.get_id())
    username = user.username
    role = user.role

    print(username, role)

    return render_template(
        "admin_templates/admin_dashboard.html", username=username, role=role
    )


#
#
#
#
# admin account setting
@admin_views.route("/admin_setting", methods=["GET"])
@login_required
def admin_setting():
    """
    render admin setting manager page
    """
    user = User.query.get(current_user.get_id())
    username = user.username
    role = user.role

    return render_template(
        "admin_templates/admin_setting.html", username=username, role=role
    )


#
# handle admin account settings
@admin_views.route("/handle_admin_setting", methods=["POST"])
@login_required
def handle_admin_setting():
    password = request.form.get("password")
    repassword = request.form.get("repassword")

    to_edit_user = User.query.get(current_user.get_id())

    if password == repassword:
        to_edit_user.password = generate_password_hash(password, "pbkdf2:sha256")
        db.session.commit()
        flash(f"Password telah berhasil di ganti.")
        return redirect("/admin_setting")

    flash(f"Password tidak sama.")
    return redirect("/admin_setting")


#
#
#
#
# admin quiz creator TODO
@admin_views.route("/admin_quiz_creator", methods=["GET"])
@login_required
def admin_quiz_creator():
    user = User.query.get(current_user.get_id())
    username = user.username
    role = user.role

    return render_template(
        "admin_templates/admin_quiz_creator.html", username=username, role=role
    )
