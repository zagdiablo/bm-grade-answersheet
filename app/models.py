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


class Soal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_soal = db.Column(db.String(300), nullable=False, default='Untitled soal')
    link_id = db.Column(db.String(300), nullable=False)
    
