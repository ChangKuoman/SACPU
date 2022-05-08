# imports
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
from sqlalchemy import func, ForeignKey

anderson_static_path = "/home/anderson/Des_Bas_Plat/Project_SACPU/SACPU/templates/static"
chang_static_path = "/home/chang/Escritorio/SACPU/templates/static"

anderson_uri = 'postgresql://postgres:231102DA@localhost:5432/sacpu'
chang_uri ='postgresql://postgres:admin@localhost:5432/sacpu'

# configurations
app = Flask(__name__, static_folder=chang_static_path)
app.config['SQLALCHEMY_DATABASE_URI'] = chang_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# models
class User(db.Model):
    __tablename__ = 'userinfo'
    username = db.Column(db.String(), primary_key=True)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False, default="user")
    dateCreated = db.Column(db.DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f'user: {self.username}'

class MotherBoard(db.Model):
    __tablename__ = 'motherboard'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.Text(), nullable=False)
    dateCreated = db.Column(db.DateTime, nullable=False, default=func.now())
    dateModified = db.Column(db.DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f'motherboard: {self.name}'

class Component(db.Model):
    __tablename__ = 'component'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(), nullable=False, unique=True)
    componentType = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    dateCreated = db.Column(db.DateTime, nullable=False, default=func.now())
    dateModified = db.Column(db.DateTime, nullable=False, default=func.now())

    def __repr__(self):
        return f'component: {self.name}'

class Compatible(db.Model):
    __tablename__ = 'compatible'
    id_motherboard = db.Column(db.Integer, ForeignKey('motherboard.id'), primary_key=True)
    id_component = db.Column(db.Integer, ForeignKey('component.id'), primary_key=True)
    dateCreated = db.Column(db.DateTime, nullable=False, default=func.now())
    dateModified = db.Column(db.DateTime, nullable=False, default=func.now())
    def __repr__(self):
        return f'compatible: {self.id_motherboard}-{self.id_component}'

# global variables
actual_user = ''

# functions
def check_password_difficulty(password_to_check):
    with open("password_lists.txt", "r") as file:
        for password in file:
            if password.rstrip() == password_to_check:
                return False
    mayusc_amount = len([i for i in password_to_check if i.isupper()])
    minusc_amount = len([i for i in password_to_check if i.islower()])
    digit_amount = len([i for i in password_to_check if i.isdigit()])
    special_amount = len([i for i in password_to_check if i in "!#$%&()=+-."])
    password_length = True if len(password_to_check) >= 6 else False
    if mayusc_amount and minusc_amount and digit_amount and special_amount and password_length:
        return True
    else:
        return False

# controllers

# home
@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

# login
@app.route('/login', methods=['POST', 'GET'])
def login():
    return render_template('login.html')

@app.route('/login/enter', methods=['POST', 'GET'])
def login_enter():
    response = {}
    try:
        username = request.get_json()['username']
        password = request.get_json()['password']
        user = User.query.filter_by(username=username).first()
        response['error'] = False
        if user == None:
            response['invalid_login'] = True
        elif user.password != password:
            response['invalid_login'] = True
        else:
            response['invalid_login'] = False
            global actual_user
            actual_user = user
    except Exception as e:
        response['error'] = True
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify(response)

# register
@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register.html')

@app.route('/register/create', methods=['POST', 'GET'])
def register_create():
    response = {}
    try:
        username = request.get_json()["username"]
        password = request.get_json()["password"]
        password_check = request.get_json()["password_check"]
        response['error'] = False
        if username in [user.username for user in User.query.all()]:
            response['invalid_register'] = "Username already exists. Try another one"
        elif not len(username) >= 4:
            response['invalid_register'] = "Username must be 4 or more characters"
        elif password != password_check:
            response['invalid_register'] = "Passwords do not match"
        elif not check_password_difficulty(password):
            response['invalid_register'] = "This is an unsafe password. Password must contain 1 upper, 1 lower, 1 digit, 1 especial character and a minimun length of 6."
        else:
            response['invalid_register'] = False
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
    except Exception as e:
        response['error'] = True
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
    
    return jsonify(response)

# simulator home
@app.route('/simulator', methods=['POST', 'GET'])
def simulator():
    global actual_user
    if actual_user != '':
        return render_template('simulator.html', motherboards=MotherBoard.query.all())
    else:
        abort(401)

# simulator motherboard
@app.route('/simulator/<motherboard>', methods=['POST', 'GET'])
def simulator_motherboard(motherboard):
    global actual_user
    error = False
    try:
        componentTuples= db.session.query(Component, Compatible).filter(Component.id == Compatible.id_component).filter(Compatible.id_motherboard == int(motherboard)).all()
        componentList = [componentTuple[0] for componentTuple in componentTuples]
    except Exception as e:
        error = True
        print(e)
    finally:
        pass
    
    if actual_user == '':
        abort(401)
    if error:
        abort(400)
    else:
        return render_template('simulator_motherboard.html', motherboard=MotherBoard.query.filter_by(id=int(motherboard)).first(), components=componentList)

@app.route('/simulator/motherboard', methods=['POST', 'GET'])
def simulator_choose_motherboard():
    response = {}
    try:
        motherboard = request.get_json()["motherboard"]
        motherboard = int(motherboard.strip('/'))
        response['error'] = False
        response['motherboard'] = motherboard
    except Exception as e:
        response['error'] = True
        print(e)
    finally:
        pass
    
    return jsonify(response)

# vista admin
@app.route('/admin', methods=['POST', 'GET'])
def admin():
    # TODO: hacer que /simulator tenga un botòn que rediriga aquì (html)
    global actual_user
    if actual_user == '':
        abort(401)
    elif actual_user.role != 'admin':
        abort(401)
    else:
        return render_template('admin.html')

# error redirect
@app.route('/errors/<error>', methods=['POST', 'GET'])
def redirect_errors(error):
    if int(error) == 500:
        abort(500)
    else:
        abort(404)

# error handlers
@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500

#run
if __name__ == '__main__':
    app.run(debug=True, port=5002)