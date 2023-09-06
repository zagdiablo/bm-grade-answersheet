"""
a view that is only available to the admins, and can only be accessed by
a user that has admin privileges

ex: database edit, add new product to the store listing
"""

from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from .models import User, Quiz
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
# admin quiz creator
@admin_views.route("/admin_quiz_creator", methods=["GET"])
@login_required
def admin_quiz_creator():
    user = User.query.get(current_user.get_id())
    username = user.username
    role = user.role

    return render_template(
        "admin_templates/admin_quiz_creator.html", username=username, role=role
    )


#
# admin quiz creator request handler
@admin_views.route('/admin_quiz_creator_handler', methods=['POST'])
@login_required
def admin_quiz_creator_handler():
    judul_quiz = request.form.get('judul_quiz')
    jumlah_jawaban = request.form.get('jumlah_jawaban')
    jumlah_nomor_soal = request.form.get('jumlah_nomor_soal')
    waktu_pengerjaan = request.form.get('waktu_pengerjaan')

    print(judul_quiz, jumlah_jawaban, jumlah_nomor_soal, waktu_pengerjaan)
    # TODO handle quiz creation

    return redirect('/admin_quiz_creator')


#
# answer sheet creation
@admin_views.route('/admin_quiz_answersheet_create/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def admin_quiz_answersheet_create(quiz_id):
    quiz = Quiz.query.get(quiz_id)

    quiz_name = quiz.quiz_name
    quiz_total_number = quiz.number_of_questions
    quiz_total_answer = quiz.number_of_answers
    quiz_timer = quiz.work_timer

    # TODO render answersheet edit template

    return render_template('admin_templates/quiz_answersheet.html', quiz_id=quiz_id, quiz_name=quiz_name, quiz_total_number=quiz_total_number, 
        quiz_total_answer=quiz_total_answer, quiz_timer=quiz_timer)
