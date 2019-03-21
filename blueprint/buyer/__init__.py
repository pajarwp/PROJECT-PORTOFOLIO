import random, logging
from blueprint import db
from flask_restful import fields

class Buyers(db.Model):
    __tablename__ = "buyer"
    buyer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    fullname = db.Column(db.String(50))
    address = db.Column(db.String(50))
    phone = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    status = db.Column(db.String(50))
    url_image = db.Column(db.String(50))

    response_field = {
        'buyer_id' : fields.Integer,
        'username' : fields.String,
        'fullname' : fields.String,
        'address' : fields.String,
        'phone' : fields.String,
        'email' : fields.String,
        'password' : fields.String,
        'status' : fields.String,
        'url_image' : fields.String,
    }

    def __init__(self, buyer_id, username, fullname, address, phone, email, password, status, url_image):
        self.buyer_id = buyer_id
        self.username = username
        self.fullname = fullname
        self.address = address
        self.phone = phone
        self.email = email
        self.password = password
        self.status = status
        self.url_image = url_image

    def __repr__(self):
        return '<%d>' % self.username
