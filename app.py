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
from sqlalchemy import func

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
    role = db.Column(db.String(), nullable=False)
    dateCreated = db.Column(db.DateTime, nullable=False)

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

# global variables
actual_user = ''

# controllers
@app.route('/', methods=['POST', 'GET'])
def index():
    global actual_user
    actual_user = ''
    print("user", actual_user)
    return render_template('index.html')

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
            actual_user = user.username
    except Exception as e:
        response['error'] = True
        print(e)
        db.session.rollback()
    finally:
        db.session.close()

    return jsonify(response)

@app.route('/register', methods=['POST', 'GET'])
def register():
    return render_template('register.html')

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


@app.route('/register/create', methods=['POST', 'GET'])
def register_create():
    error = False
    try:
        username = request.form.get("username", '')
        password = request.form.get("password", '')
        password_check = request.form.get("password_check", '')
        if password == password_check and check_password_difficulty(password) and len(username) > 0:
            user = User(username=username, password=password, role="user", dateCreated=func.now())
            db.session.add(user)
            db.session.commit()
        else:
            error = True
            db.session.rollback()
    except Exception as e:
        error = True
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
    
    if error:
        abort(500)
    else:
        return redirect(url_for('login'))

@app.route('/simulator', methods=['POST', 'GET'])
def simulator():
    global actual_user
    if actual_user != '':
        return render_template('simulator.html')
    else:
        abort(401)

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500

@app.route('/errors/<error>', methods=['POST', 'GET'])
def redirect_errors(error):
    if int(error) == 500:
        abort(500)
    else:
        abort(404)

#run
if __name__ == '__main__':
    app.run(debug=True, port=5002)