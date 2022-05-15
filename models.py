# imports
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import func, ForeignKey

# configuration
db = SQLAlchemy()

# models
class User(db.Model, UserMixin):
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(), nullable=False, default="user")
    date_created = db.Column(db.DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f'user: {self.username}'

class MotherBoard(db.Model):
    __tablename__ = 'motherboard'
    id = db.Column(db.Integer, primary_key=True, unique=True)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=func.now())
    create_by = db.Column(db.Integer, ForeignKey('userinfo.id'), nullable=False, default=0)
    date_modified = db.Column(db.DateTime, nullable=False, default=func.now())
    modify_by = db.Column(db.Integer, ForeignKey('userinfo.id'), nullable=False, default=0)

    def __repr__(self):
        return f'motherboard: {self.name}'

class Component(db.Model):
    __tablename__ = 'component'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(), nullable=False, unique=True)
    component_type = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=func.now())
    create_by = db.Column(db.Integer, ForeignKey('userinfo.id'), nullable=False, default=0)
    date_modified = db.Column(db.DateTime, nullable=False, default=func.now())
    modify_by = db.Column(db.Integer, ForeignKey('userinfo.id'), nullable=False, default=0)

    def __repr__(self):
        return f'component: {self.name}'

class Compatible(db.Model):
    __tablename__ = 'compatible'
    id_motherboard = db.Column(db.Integer, ForeignKey('motherboard.id'), primary_key=True)
    id_component = db.Column(db.Integer, ForeignKey('component.id'), primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=func.now())
    create_by = db.Column(db.Integer, ForeignKey('userinfo.id'), nullable=False, default=0)
    def __repr__(self):
        return f'compatible: {self.id_motherboard}-{self.id_component}'