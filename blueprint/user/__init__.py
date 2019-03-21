import random, logging
from blueprint import db
from flask_restful import fields

class Users(db.Model):
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    store_name = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(50))
    password = db.Column(db.String(50))
    website = db.Column(db.String(50))
    status = db.Column(db.String(50))
    url_image = db.Column(db.String(50))
    description = db.Column(db.String(50))

    response_field = {
        'user_id' : fields.Integer,
        'store_name' : fields.String,
        'email' : fields.String,
        'phone' : fields.String,
        'password' : fields.String,
        'website' : fields.String,
        'status' : fields.String,
        'url_image' : fields.String,
        'description': fields.String,
    }

    def __init__(self, user_id, store_name, email, phone, password, website, status, url_image, description):
        self.user_id = user_id
        self.store_name = store_name
        self.email = email
        self.phone = phone
        self.password = password
        self.website = website
        self.status = status
        self.url_image = url_image
        self.description = description

    def __repr__(self):
        return '<%d>' % self.username
