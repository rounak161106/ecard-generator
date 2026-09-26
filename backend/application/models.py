from .database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, unique = True, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    role = db.Column(db.String, nullable = False, default = 'user')
    card_details = db.relationship('UserCardDetail', backref='bearer', lazy=True)

class UserCardDetail(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    attr_name = db.Column(db.String, nullable = False)
    attr_value = db.Column(db.String, nullable = False)
    card_name = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    