# imports
import sys
from crypt import methods
from flask import (
    jsonify,
    Flask,
    abort,
    render_template,
    request,
    redirect,
    url_for
)

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null

# configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:231102DA@localhost:5432/sacpu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# models
class User(db.Model):
    __tablename__ = 'user'
    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)


    def __repr__(self):
        return f'user: {self.username}'

class MotherBoard(db.Model):
    __tablename__ = 'motherboard'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'motherboard: {self.name}'

class Component(db.Model):
    __tablename__ = 'component'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return f'component: {self.name}'

db.create_all()

# controllers
@app.route('/', methods=['GET'])
def index():
    

#run
if __name__ == '__main__':
    app.run(debug=True, port=5000)