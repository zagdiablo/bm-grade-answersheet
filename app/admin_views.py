"""
a view that is only available to the admins, and can only be accessed by
a user that has admin privileges

ex: database edit, add new product to the store listing
"""

from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user

from .models import User


admin_views = Blueprint("admin_views", __name__)


@admin_views.route("/admin_dashboard", methods=["GET"])
@login_required
def admin_dashboard():
    """
    when admin login is success

    return render admin_dashboard.html
    """

    # check if user is admin
    user = User.query.get(current_user.get_id())
    if not user.role == "admin":
        return redirect(url_for("user_views.user_profile"))

    return render_template("admin_templates/admin_dashboard.html")
