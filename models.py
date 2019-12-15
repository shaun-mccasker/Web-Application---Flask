from . import db
from datetime import datetime
from flask_login import UserMixin


# varchar 400 - message/text
# varchar 255 - names like text // may include foreign chracters
# varchar 100 - few word text
# varchar 50 - single word text

# shaun updated-30/9/2019 OPEN
class User(db.Model, UserMixin):
    __tablename__ = 'users'  # tablename
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), index=True, nullable=False)
    emailid = db.Column(db.String(255), index=True,
                        unique=True, nullable=False)
    phone_no = db.Column(db.Integer, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    # relationships
    enquiries = db.relationship('Enquiry', backref='user')
    bids = db.relationship('Bid', backref='user')
    items = db.relationship('Item', backref='user')
    purchased = db.relationship('Purchased_item', backref='user')

    def __repr__(self):  # string print method
        return "<Name: {}, ID: {}>".format(self.name, self.id)


class Bid(db.Model):
    __tablename__ = 'bids'  # tablename
    id = db.Column(db.Integer, primary_key=True)
    bidder_name = db.Column(db.String(255), index=True, nullable=False)
    bidder_email = db.Column(db.String(255), index=True, nullable=False)
    bidder_phone = db.Column(db.Integer, index=True, nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())
    # foreign
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    # relationships
    purchased = db.relationship('Purchased_item', backref='bid')


class Enquiry(db.Model):
    __tablename__ = 'enquiries'  # tablename
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(255), index=True, nullable=False)
    recipient = db.Column(db.String(255), index=True, nullable=False)
    message = db.Column(db.String(400), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())
    # foreign
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))    #
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    # relationships NULL


class Item(db.Model):
    __tablename__ = 'items'  # tablename
    id = db.Column(db.Integer, primary_key=True)
    seller = db.Column(db.String(255), index=True, nullable=False)
    name = db.Column(db.String(255), index=True, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    quality = db.Column(db.String(50), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now())
    image = db.Column(db.String, nullable=False)
    # foreign
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # relationships

    bids = db.relationship('Bid', backref='item')
    purchased = db.relationship('Purchased_item', backref='item')
    status = db.relationship('Item_status', backref='item')


class Item_status(db.Model):
    __tablename__ = 'item_status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)
    # foreign
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    # relationships NULL


class Purchased_item(db.Model):
    __tablename__ = 'purchased_items'
    id = db.Column(db.Integer, primary_key=True)
    buyer = db.Column(db.String(255), index=True, nullable=False)
    seller = db.Column(db.String(255), index=True, nullable=False)
    created_date = db.Column(db.DateTime, nullable=False)
    purchased_date = db.Column(db.DateTime, default=datetime.now())
    # foreign
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    bid_id = db.Column(db.Integer, db.ForeignKey('bids.id'))
    # relationships NULL

# shaun updated-30/9/2019 CLOSE
