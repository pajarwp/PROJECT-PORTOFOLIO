import random, logging
from blueprint import db
from flask_restful import fields

class Items(db.Model):
    __tablename__ = "item"
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(50))
    category = db.Column(db.String(50))
    price = db.Column(db.Integer)
    size = db.Column(db.String(50))
    color = db.Column(db.String(50))
    qty = db.Column(db.Integer)
    posted_by = db.Column(db.String(50))

    response_field = {
        'item_id' : fields.Integer,
        'item_name' : fields.String,
        'category' : fields.String,
        'price' : fields.Integer,
        'size' : fields.String,
        'color' : fields.String,
        'qty' : fields.Integer,
        'posted_by' : fields.String,
    }

    def __init__(self, item_id, item_name, category, price, size, color, qty, posted_by):
        self.item_id = item_id
        self.item_name = item_name
        self.category = category
        self.price = price
        self.size = size
        self.color = color
        self.qty = qty
        self.posted_by = posted_by

    def __repr__(self):
        return '<%d>' % self.item_name
