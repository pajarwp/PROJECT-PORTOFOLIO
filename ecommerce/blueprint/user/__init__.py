import random, logging
from blueprint import db
from flask_restful import fields

class Users(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    status = db.Column(db.String(50))

    response_field = {
        'user_id' : fields.Integer,
        'username' : fields.String,
        'email' : fields.String,
        'password' : fields.String,
        'status' : fields.String,
    }

    def __init__(self, user_id, username, email, password, status):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.status = status

    def __repr__(self):
        return '<%d>' % self.username
