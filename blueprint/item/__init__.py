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
    description = db.Column(db.String(50))
    imgurl1 = db.Column(db.String(50))
    imgurl2 = db.Column(db.String(50))
    imgurl3 = db.Column(db.String(50))
    imgurl4 = db.Column(db.String(50))

    response_field = {
        'item_id' : fields.Integer,
        'item_name' : fields.String,
        'category' : fields.String,
        'price' : fields.Integer,
        'size' : fields.String,
        'color' : fields.String,
        'qty' : fields.Integer,
        'posted_by' : fields.String,
        'description' : fields.String,
        'imgurl1' : fields.String,
        'imgurl2' : fields.String,
        'imgurl3' : fields.String,
        'imgurl4' : fields.String,
    }

    def __init__(self, item_id, item_name, category, price, size, color, qty, posted_by, description, imgurl1, imgurl2, imgurl3, imgurl4):
        self.item_id = item_id
        self.item_name = item_name
        self.category = category
        self.price = price
        self.size = size
        self.color = color
        self.qty = qty
        self.posted_by = posted_by
        self.description = description
        self.imgurl1 = imgurl1
        self.imgurl2 = imgurl2
        self.imgurl3 = imgurl3
        self.imgurl4 = imgurl4

    def __repr__(self):
        return '<%d>' % self.item_name
