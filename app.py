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

from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user
)

# constants
anderson_static_path = "/home/anderson/Des_Bas_Plat/Project_SACPU/SACPU/templates/static"
chang_static_path = "/home/chang/Escritorio/SACPU/templates/static"

anderson_uri = 'postgresql://postgres:231102DA@localhost:5432/sacpu'
chang_uri ='postgresql://postgres:admin@localhost:5432/sacpu'

# configurations
app = Flask(__name__, static_folder=chang_static_path)
app.config['SQLALCHEMY_DATABASE_URI'] = chang_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'papasfritas15'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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
    create_by = db.Column(db.Integer, ForeignKey('userinfo.id'), nullable=False, default="1")
    date_modified = db.Column(db.DateTime, nullable=False, default=func.now())
    modify_by = db.Column(db.Integer, ForeignKey('userinfo.id'), nullable=False, default="1")

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
    create_by = db.Column(db.Integer, ForeignKey('userinfo.id'), nullable=False, default="1")
    date_modified = db.Column(db.DateTime, nullable=False, default=func.now())
    modify_by = db.Column(db.Integer, ForeignKey('userinfo.id'), nullable=False, default="1")

    def __repr__(self):
        return f'component: {self.name}'

class Compatible(db.Model):
    __tablename__ = 'compatible'
    id_motherboard = db.Column(db.Integer, ForeignKey('motherboard.id'), primary_key=True)
    id_component = db.Column(db.Integer, ForeignKey('component.id'), primary_key=True)
    date_created = db.Column(db.DateTime, nullable=False, default=func.now())
    create_by = db.Column(db.Integer, ForeignKey('userinfo.id'), nullable=False, default="1")
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
    password_length = True if len(password_to_check) >= 6 and len(password_to_check) <= 20 else False
    if mayusc_amount and minusc_amount and digit_amount and special_amount and password_length:
        return True
    else:
        return False

# controllers

# login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


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
            # user does not exists
            response['invalid_login'] = True
        elif user.password == password:
            # correct login     
            login_user(user)
            response['invalid_login'] = False
        else:
            # incorrect login
            response['invalid_login'] = True
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
        elif len(username) > 20 or len(username) < 4:
            response['invalid_register'] = "Username must be 4 to 20 characters"
        elif password != password_check:
            response['invalid_register'] = "Passwords do not match"
        elif not check_password_difficulty(password):
            response['invalid_register'] = "This is an unsafe password. Password must contain 1 upper, 1 lower, 1 digit, 1 especial character and 6 to 20 characters."
        else:
            # valid register
            response['invalid_register'] = False
            new_user = User(username=username, password=password)
            db.session.add(new_user)
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
@login_required
def simulator():
    return render_template('simulator.html', motherboards=MotherBoard.query.all())


# simulator motherboard
@app.route('/simulator/<motherboard>', methods=['POST', 'GET'])
@login_required
def simulator_motherboard(motherboard):
    error = False
    try:
        query = db.session.query(Component, Compatible).filter(Component.id == Compatible.id_component).filter(Compatible.id_motherboard==int(motherboard))
        # componentes compatibles con el id de la motherboard (RAM, SSD, GPU, PC Cooling)
        list_RAM = [component[0] for component in query.filter_by(component_type = 'RAM')]
        list_SSD = [component[0] for component in query.filter_by(component_type = 'SSD')]
        list_GPU = [component[0] for component in query.filter_by(component_type = 'GPU')]
        list_PC_Cooling = [component[0] for component in query.filter_by(component_type = 'PC Cooling')]

        query2 = db.session.query(Component)
        # componentes que no requieren compatibilidad
        list_HDD = query2.filter_by(component_type = 'HDD').all()
        list_CPU = query2.filter_by(component_type = 'CPU').all()
        list_PSU = query2.filter_by(component_type = 'PSU').all()
        list_Peripheral = query2.filter_by(component_type = 'Peripheral').all()

    except Exception as e:
        error = True
        print(e)
    finally:
        pass
    
    if error:
        abort(400)
    else:
        return render_template('simulator_motherboard.html',
            motherboard=MotherBoard.query.filter_by(id=int(motherboard)).first(),
            list_RAM=list_RAM,
            list_SSD=list_SSD,
            list_HDD=list_HDD,
            list_CPU=list_CPU,
            list_GPU=list_GPU,
            list_PSU=list_PSU,
            list_PC_Cooling=list_PC_Cooling,
            list_Peripheral=list_Peripheral)

@app.route('/simulator/motherboard', methods=['POST', 'GET'])
@login_required
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
@login_required
def admin():
    # TODO: hacer que /simulator tenga un botòn que rediriga aquì (html)
    if current_user.role != 'admin':
        abort(401)
    else:
        return render_template('admin.html')

@app.route("/admin/<action>", methods=['POST', 'GET'])
@login_required
def admin_action(action):
    if current_user.role != 'admin':
        abort(401)
    elif action == "create":
        ram_list = Component.query.filter(Component.component_type == 'RAM').all()
        ssd_list = Component.query.filter(Component.component_type == 'SSD').all()
        gpu_list = Component.query.filter(Component.component_type == 'GPU').all()
        pc_cooling_list = Component.query.filter(Component.component_type == 'PC Cooling').all()
        component_lists = ram_list + ssd_list + gpu_list + pc_cooling_list
        return render_template("admin_create.html", motherboards=MotherBoard.query.all(), components=component_lists)
    elif action == "update":
        return render_template("admin_update.html", motherboards=MotherBoard.query.all(), components=Component.query.all())
    elif action == "delete":
        componentTuples= db.session.query(Compatible, MotherBoard, Component).filter(Compatible.id_motherboard==MotherBoard.id).filter(Compatible.id_component==Component.id).all()
        return render_template("admin_delete.html", motherboards=MotherBoard.query.all(), components=Component.query.all(), compatibles=componentTuples)
    else:
        abort(404)

# create routes
@app.route("/admin/create/motherboard", methods=['POST', 'GET'])
@login_required
def create_motherboard():
    response = {}
    if current_user.role != 'admin':
        abort(400)
    else:
        try:
            motherboard_name = request.get_json()["motherboard_name"]
            motherboard_description = request.get_json()["motherboard_description"]
            motherboard_price = request.get_json()["motherboard_price"]
            response['error'] = False
            if motherboard_name in [motherboard.name for motherboard in MotherBoard.query.all()]:
                response['invalid_register'] = "Motherboard with same name found in database. Try another name"
            elif float(motherboard_price) <= 0:
                response['invalid_register'] = "Motherboard price cannot be negative or zero"
            elif motherboard_description == '':
                response['invalid_register'] = "Description cannot be empty"
            else:
                response['invalid_register'] = False
                motherboard = MotherBoard(
                    name=motherboard_name,
                    description=motherboard_description,
                    price=motherboard_price,
                    create_by = actual_user.username,
                    modify_by = actual_user.username)
                db.session.add(motherboard)
                db.session.commit()

                response['child_name'] = motherboard_name
                response['child_id'] = motherboard.id

        except Exception as e:
            response['error'] = True
            print(e)
            db.session.rollback()
        finally:
            db.session.close()
    
    return jsonify(response)

@app.route("/admin/create/component", methods=['POST', 'GET'])
@login_required
def create_component():
    response = {}
    if current_user.role != 'admin':
        abort(400)
    else:
        try:
            component_name = request.get_json()["component_name"]
            component_description = request.get_json()["component_description"]
            component_type = request.get_json()["component_type"]
            component_price = request.get_json()["component_price"]
            response['error'] = False
            if component_name in [component.name for component in Component.query.all()]:
                response['invalid_register'] = "Component with same name found in database. Try another name"
            elif float(component_price) <= 0:
                response['invalid_register'] = "Component price cannot be negative or zero"
            elif component_description == '':
                response['invalid_register'] = "Description cannot be empty"
            elif component_type not in ['RAM', 'SSD', 'HDD', 'CPU', 'GPU', 'PSU', 'PC Cooling', 'Peripheral']:
                response['invalid_register'] = "Component type is not valid"
            else:
                response['invalid_register'] = False
                component = Component(
                    name=component_name,
                    description=component_description,
                    price=component_price,
                    component_type=component_type,
                    create_by = actual_user.username,
                    modify_by = actual_user.username)
                db.session.add(component)
                db.session.commit()

                response['child_name'] = component_name
                response['child_id'] = component.id
        except Exception as e:
            response['error'] = True
            print(e)
            db.session.rollback()
        finally:
            db.session.close()
    
    return jsonify(response)

@app.route("/admin/create/compatible", methods=['POST', 'GET'])
@login_required
def create_compatible():
    response = {}
    try:
        id_motherboard = request.get_json()["id_motherboard"]
        id_component = request.get_json()["id_component"]

        response['error'] = False
        query = Compatible.query.filter(Compatible.id_component==id_component).filter(Compatible.id_motherboard==id_motherboard).all()

        if query != []:
            response['invalid_register'] = "The compatible choosen already exists"
        else:
            response['invalid_register'] = False
            compatible = Compatible(
                id_component=id_component,
                id_motherboard=id_motherboard,
                create_by = actual_user.username)
            db.session.add(compatible)
            db.session.commit()
    except Exception as e:
        response['error'] = True
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
    
    return jsonify(response)

# delete routes
@app.route("/admin/delete/motherboard", methods=['DELETE', 'GET'])
@login_required
def delete_motherboard():
    response = {}
    try:
        id_motherboard = request.get_json()["id_motherboard"]

        response['error'] = False
        # necesario primero eliminar dependecias SI existen
        query1 = Compatible.query.filter_by(id_motherboard=id_motherboard)
        query1.delete()
        db.session.commit()
        
        query2 = MotherBoard.query.filter_by(id=id_motherboard)

        if query2.all() == []:
            response['invalid_register'] = "There is no motherboard in database"
        else:
            response['invalid_register'] = False
            response['child_id'] = f"m-{id_motherboard}"
            query2.delete()
            db.session.commit()


    except Exception as e:
        response['error'] = True
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
    
    return jsonify(response)

@app.route("/admin/delete/component", methods=['DELETE', 'GET'])
@login_required
def delete_component():
    response = {}
    try:
        id_component = request.get_json()["id_component"]

        response['error'] = False
        # necesario primero eliminar dependecias SI existen
        query1 = Compatible.query.filter_by(id_component=id_component)
        query1.delete()
        db.session.commit()

        query2 = Component.query.filter_by(id=id_component)

        if query2.all() == []:
            response['invalid_register'] = "There is no component in database"
        else:
            response['invalid_register'] = False
            response['child_id'] = f"c-{id_component}"
            query2.delete()
            db.session.commit()

    except Exception as e:
        response['error'] = True
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
    
    return jsonify(response)

@app.route("/admin/delete/compatible", methods=['DELETE', 'GET'])
@login_required
def delete_compatible():
    response = {}
    try:
        id_compatible = request.get_json()["id_compatible"]
        id_motherboard, id_component = id_compatible.split()

        response['error'] = False
        query = Compatible.query.filter(Compatible.id_motherboard==id_motherboard).filter(Compatible.id_component==id_component)

        if query.all() == []:
            response['invalid_register'] = "There is no compatible in database"
        else:
            response['invalid_register'] = False
            response['child_id'] = f"mc-{id_motherboard}-{id_component}"
            query.delete()
            db.session.commit()

    except Exception as e:
        response['error'] = True
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
    
    return jsonify(response)

# update routes
@app.route("/admin/update/motherboard", methods=['PUT', 'GET'])
@login_required
def update_motherboard():
    response = {}
    try:
        motherboard_id = request.get_json()["motherboard_id"]

        motherboard_name = request.get_json()["motherboard_name"]
        motherboard_price = request.get_json()["motherboard_price"]
        motherboard_description = request.get_json()["motherboard_description"]

        response['error'] = False
        query = MotherBoard.query.filter(MotherBoard.id==motherboard_id)

        if query == []:
            response['invalid_register'] = "There is motherboard in database"
        else:
            query = query.first()
            response['invalid_register'] = False

            if motherboard_name != '':
                if motherboard_name in [motherboard.name for motherboard in MotherBoard.query.all()]:
                    response['invalid_register'] = "Motherboard with same name found in database. Try another name"
                else:
                    query.name = motherboard_name
                    response['child_id'] = f"m-{motherboard_id}"
                    response['child_name'] = motherboard_name
                    
            if motherboard_price != '':
                if float(motherboard_price) <= 0:
                    response['invalid_register'] = "Motherboard price cannot be negative or zero"
                else:
                    query.price = motherboard_price
            if motherboard_description != '':
                query.description = motherboard_description

            if response['invalid_register']:
                # actualizacion no se hace
                db.session.rollback()
            else:
                # actualizacion se hace
                query.dateModified = func.now()
                query.modify_by = actual_user.username
                db.session.commit()

    except Exception as e:
        response['error'] = True
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
    
    return jsonify(response)

@app.route("/admin/update/component", methods=['PUT', 'GET'])
@login_required
def update_component():
    response = {}
    try:
        component_id = request.get_json()["component_id"]

        component_name = request.get_json()["component_name"]
        component_price = request.get_json()["component_price"]
        component_description = request.get_json()["component_description"]
        component_type = request.get_json()["component_type"]

        response['error'] = False
        query = Component.query.filter(Component.id==component_id)

        if query == []:
            response['invalid_register'] = "There is component in database"
        else:
            query = query.first()
            response['invalid_register'] = False

            if component_name != '':
                if component_name in [component.name for component in Component.query.all()]:
                    response['invalid_register'] = "Component with same name found in database. Try another name"
                else:
                    query.name = component_name
                    response['child_id'] = f"c-{component_id}"
                    response['child_name'] = component_name
                    
            if component_price != '':
                if float(component_price) <= 0:
                    response['invalid_register'] = "Component price cannot be negative or zero"
                else:
                    query.price = component_price
            if component_description != '':
                query.description = component_description
            if component_type != '':
                if component_type not in ['RAM', 'SSD', 'HDD', 'CPU', 'GPU', 'PSU', 'PC Cooling', 'Peripheral']:
                    response['invalid_register'] = "Component type is not valid"
                else:
                    query.component_type = component_type

            if response['invalid_register']:
                # actualizacion no se hace
                db.session.rollback()
            else:
                # actualizacion se hace
                query.dateModified = func.now()
                query.modify_by = actual_user.username
                db.session.commit()

    except Exception as e:
        response['error'] = True
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
    
    return jsonify(response)

# buy
@app.route('/simulator/buy', methods=['POST', 'GET'])
@login_required
def simulator_buy():
    response = {'error': False}
    try:
        matriz = [] 
        # 0: nombre, 1: precio
        precio_total = 0

        motherboard = request.get_json()['motherboard']
        psu = request.get_json()['psu']
        cpu = request.get_json()['cpu']
        hdd = request.get_json()['hdd']
        ram = request.get_json()['ram']
        ssd = request.get_json()['ssd']
        gpu = request.get_json()['gpu']
        pc_cooling = request.get_json()['pc_cooling']
        peripherals = request.get_json()['peripherals']

        '''
        print('motherboard', motherboard)
        print('psu', psu)
        print('cpu', cpu)
        print('hdd', hdd)
        print('ram', ram)
        print('ssd', ssd)
        print('gpu', gpu)
        print('pc_cooling', pc_cooling)
        print('peripherals', peripherals)

        '''

        def verificar_existencia(id_componente, Tipo):
            if id_componente == 0:
                return False
            if Tipo.query.get(id_componente) is None:
                db.session.close()
                return False
            db.session.close()
            return True
        
        def retornar_tipo(id_componente, Tipo):
            return Tipo.query.get(id_componente)

        def agregar_a_matriz(componente, matriz):
            matriz.append(componente.name)
            matriz.append(componente.price)


        def sumar_a_precio_total(componente, precio_total):
            precio_total += componente.price
            return precio_total
        
        def verificar_todo(id, Tipo, matriz, precio_total):
            if verificar_existencia(id, Tipo):
                componente = retornar_tipo(id, Tipo)
                agregar_a_matriz(componente, matriz)
                precio_total = sumar_a_precio_total(componente, precio_total)
            return precio_total

        precio_total = verificar_todo(motherboard, MotherBoard, matriz, precio_total)
        precio_total = verificar_todo(psu, Component, matriz, precio_total)
        precio_total = verificar_todo(cpu, Component, matriz, precio_total)
        precio_total = verificar_todo(hdd, Component, matriz, precio_total)
        precio_total = verificar_todo(ram, Component, matriz, precio_total)
        precio_total = verificar_todo(ssd, Component, matriz, precio_total)
        precio_total = verificar_todo(gpu, Component, matriz, precio_total)
        precio_total = verificar_todo(pc_cooling, Component, matriz, precio_total)

        for peripheral in peripherals:
            precio_total = verificar_todo(peripheral, Component, matriz, precio_total)


        response['precio_total'] = round(precio_total, 2)
        response['matriz'] = matriz

    except Exception as e:
        response['error'] = True
        db.session.rollback()
        print(e)
    finally:
        db.session.close()

    return jsonify(response)

@app.route('/buy/<precio_total>/<lista>')
@login_required
def compra_resultado(precio_total, lista):
    lista = lista.strip("]")
    lista = lista.strip("[")

    lista_nombres = []
    lista_precios = []

    counter = 0
    for i in lista.split(','):
        if counter % 2 == 0:
            lista_nombres.append(str(i.strip('"')))
        else:
            lista_precios.append(float(i))
        counter += 1
    
    lista = list(zip(lista_nombres, lista_precios))

    return render_template('simulator_buy.html',
                            precio_total=precio_total,
                            components=lista)

# error redirect
@app.route('/errors/<error>', methods=['POST', 'GET'])
@login_required
def redirect_errors(error):
    if int(error) == 500:
        abort(500)
    if int(error) == 401:
        abort(401)
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