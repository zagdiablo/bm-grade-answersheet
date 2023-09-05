"""
create a database models
"""
from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    """
    basic user model with username, password, and role to define its role: admin, staff, or user
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_name = db.Column(db.String(300), nullable=False, default="Untitled soal")
    number_of_questions = db.Column(db.Integer, nullable=False, default=1)
    number_of_answers = db.Column(db.Integer, nullable=False, default=4)
    work_timer = db.Column(db.Integer, nullable=False, default=10)
    link_id = db.Column(db.String(300), nullable=False)
    qr_code_img = db.Column(db.String(300), nullable=False)
    answer = db.relationship("Question", backref="quiz")
    played_by_history = db.relationship("StudentWorkHistory", backref="Quiz")


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), nullable=False)
    answer = db.Column(db.String(5), nullable=False)
    answer_weight = db.Column(db.Integer, nullable=False, default=1)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"))


class StudentWorkHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(300), nullable=False, default="No Name")
    played_date = db.Column(db.String(300), nullable=False)
    student_answer = db.Column(db.String(300), nullable=False)
    correct_answer = db.Column(db.Integer, nullable=False, default=0)
    wrong_answer = db.Column(db.Integer, nullable=False, default=0)
    work_time = db.Column(db.String(100), nullable=False, default="NaN")
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"))
