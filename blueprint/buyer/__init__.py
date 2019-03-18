import random, logging
from blueprint import db
from flask_restful import fields

class Buyers(db.Model):
    __tablename__ = "buyer"
    buyer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    contact = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    status = db.Column(db.String(50))

    response_field = {
        'buyer_id' : fields.Integer,
        'username' : fields.String,
        'contact' : fields.String,
        'email' : fields.String,
        'password' : fields.String,
        'status' : fields.String,
    }

    def __init__(self, buyer_id, username, contact, email, password, status):
        self.buyer_id = buyer_id
        self.username = username
        self.contact = contact
        self.email = email
        self.password = password
        self.status = status

    def __repr__(self):
        return '<%d>' % self.username
