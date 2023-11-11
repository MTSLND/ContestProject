from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Votos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grupo = db.Column(db.Integer)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', back_populates='voto', uselist=False)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    voto = db.relationship('Votos', back_populates='user', uselist=False)