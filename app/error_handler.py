from flask import Blueprint, render_template


error_handler = Blueprint("error_handler", __name__)


@error_handler.errorhandler(401)
def unauthorized_401(e):
    return render_template("home.html"), 401
