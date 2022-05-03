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
from flask_migrate import Migrate

# configurations
app = Flask(__name__, static_folder="/home/chang/Escritorio/SACPU/templates/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/sacpu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# models
class User(db.Model):
    __tablename__ = 'userinfo'
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
    dateCreated = db.Column(db.DateTime, nullable=False)
    dateModified = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'motherboard: {self.name}'

class Component(db.Model):
    __tablename__ = 'component'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(), nullable=False)
    componentType = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    dateCreated = db.Column(db.DateTime, nullable=False)
    dateModified = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f'component: {self.name}'

# controllers
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register.html')

@app.route('/simulator', methods=['POST', 'GET'])
def simulator():
    return render_template('simulator.html')

#run
if __name__ == '__main__':
    app.run(debug=True, port=5002)