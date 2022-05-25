# imports
from typing import final
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

from flask_login import (
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user
)

import bcrypt

# constants
anderson_static_path = "/home/anderson/Des_Bas_Plat/Project_SACPU/SACPU/templates/static"
chang_static_path = "D:/2 UTEC/Desarrollo Basado en Plataformas (CS2031)/SACPU/templates/static"

anderson_uri = 'postgresql://postgres:231102DA@localhost:5432/sacpu'
chang_uri ='postgresql://postgres:admin@localhost:5432/sacpu'

# configurations
app = Flask(__name__, static_folder=chang_static_path)
app.config['SQLALCHEMY_DATABASE_URI'] = chang_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 20
app.config['SECRET_KEY'] = 'papasfritas15'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# models
with app.app_context():
    from models import (
        db,
        User,
        MotherBoard,
        Component,
        Compatible,
        Simulation,
        SimulationComponent
    )
migrate = Migrate(app, db)

# functions
from functions import (
    check_password_difficulty,
    verificar_todo
)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = chang_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'papasfritas15'
    db.init_app(app)
    return app

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
        elif bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):      
      #  elif user.password == password:
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
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            new_user = User(username=username, password=hashed.decode('utf-8'))
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
    try:
        lista_motherboards = MotherBoard.query.all()
        if current_user.role == "admin":
            admin = True
        else:
            admin = False
    except Exception as e:
        print(e)
        db.session.rollback()
        abort(500)
    finally:
        db.session.close()

    return render_template('simulator.html', motherboards=lista_motherboards, admin=admin)


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

        # motherboard
        list_motherboard = MotherBoard.query.filter_by(id=int(motherboard)).first()

    except Exception as e:
        error = True
        print(e)
        db.session.rollback()
    finally:
        db.session.close()
    
    if error:
        abort(400)
    return render_template('simulator_motherboard.html',
            motherboard=list_motherboard,
            list_RAM=list_RAM,
            list_SSD=list_SSD,
            list_HDD=list_HDD,
            list_CPU=list_CPU,
            list_GPU=list_GPU,
            list_PSU=list_PSU,
            list_PC_Cooling=list_PC_Cooling,
            list_Peripheral=list_Peripheral,)

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
    if current_user.role != 'admin':
        abort(401)
    else:
        return render_template('admin.html')

@app.route("/admin/<action>", methods=['POST', 'GET'])
@login_required
def admin_action(action):
    try:
        # motherboard
        list_motherboard = MotherBoard.query.all()
        # components
        component_list = Component.query.all()
        # create
        ram_list = Component.query.filter(Component.component_type == 'RAM').all()
        ssd_list = Component.query.filter(Component.component_type == 'SSD').all()
        gpu_list = Component.query.filter(Component.component_type == 'GPU').all()
        pc_cooling_list = Component.query.filter(Component.component_type == 'PC Cooling').all()
        component_list_need_compatibility = ram_list + ssd_list + gpu_list + pc_cooling_list
        # delete
        componentTuples= db.session.query(Compatible, MotherBoard, Component).filter(Compatible.id_motherboard==MotherBoard.id).filter(Compatible.id_component==Component.id).all()

    except Exception as e:
        print(e)
        abort(500)
        db.session.rollback()
    finally:
        db.session.close()

    if current_user.role != 'admin':
        abort(401)
    elif action == "create":
        return render_template("admin_create.html", motherboards=list_motherboard, components=component_list_need_compatibility)
    elif action == "update":
        return render_template("admin_update.html", motherboards=list_motherboard, components=component_list)
    elif action == "delete":
        return render_template("admin_delete.html", motherboards=list_motherboard, components=component_list, compatibles=componentTuples)
    else:
        abort(404)

# create routes
@app.route("/admin/create/motherboard", methods=['POST', 'GET'])
@login_required
def create_motherboard():
    response = {}
    if current_user.role != 'admin':
        abort(401)
    else:
        try:
            motherboard_name = request.get_json()["motherboard_name"]
            motherboard_description = request.get_json()["motherboard_description"]
            motherboard_price = request.get_json()["motherboard_price"]
            response['error'] = False
            if motherboard_name == '':
                response['invalid_register'] = "Motherboard name cannot be empty"
            elif motherboard_name in [motherboard.name for motherboard in MotherBoard.query.all()]:
                response['invalid_register'] = "Motherboard with same name found in database. Try another name"
            elif motherboard_price == '':
                response['invalid_register'] = "Motherboard price cannot be empty"
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
                    create_by = current_user.id,
                    modify_by = current_user.id)
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
            if component_name == '':
                response['invalid_register'] = "Component name cannot be empty"
            elif component_name in [component.name for component in Component.query.all()]:
                response['invalid_register'] = "Component with same name found in database. Try another name"
            elif component_price == '':
                response['invalid_register'] = "Component price cannot be empty"
            elif float(component_price) <= 0:
                response['invalid_register'] = "Component price cannot be negative or zero"
            elif component_description == '':
                response['invalid_register'] = "Description cannot be empty"
            elif component_type == '':
                response['invalid_register'] = "Component type cannot be empty"
            elif component_type not in ['RAM', 'SSD', 'HDD', 'CPU', 'GPU', 'PSU', 'PC Cooling', 'Peripheral']:
                response['invalid_register'] = "Component type is not valid"
            else:
                response['invalid_register'] = False
                component = Component(
                    name=component_name,
                    description=component_description,
                    price=component_price,
                    component_type=component_type,
                    create_by = current_user.id,
                    modify_by = current_user.id)
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
        response['invalid_register'] = False
        id_motherboard = request.get_json()["id_motherboard"]
        id_component = request.get_json()["id_component"]

        if id_motherboard == '':
            response['invalid_register'] = "Motherboard cannot be empty"
        elif id_component == '':
            response['invalid_register'] = "Component cannot be empty"
        else:
            query = Compatible.query.filter(Compatible.id_component==id_component).filter(Compatible.id_motherboard==id_motherboard).all()

            if query != []:
                response['invalid_register'] = "The compatible choosen already exists"
            else:
                compatible = Compatible(
                    id_component=id_component,
                    id_motherboard=id_motherboard,
                    create_by = current_user.id)
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
        if id_motherboard == '':
            response['invalid_register'] = "You must choose a MotherBoard"
        else:
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
        response['error'] = False
        id_component = request.get_json()["id_component"]
        if id_component == '':
            response['invalid_register'] = "You must choose a Component"
        else:
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
        response['error'] = False
        id_compatible = request.get_json()["id_compatible"]
        if id_compatible == '':
            response['invalid_register'] = "You must choose a Compatible"
        else:
            # separate ids
            id_motherboard, id_component = id_compatible.split()

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
        response['error'] = False
        motherboard_id = request.get_json()["motherboard_id"]

        motherboard_name = request.get_json()["motherboard_name"]
        motherboard_price = request.get_json()["motherboard_price"]
        motherboard_description = request.get_json()["motherboard_description"]

        if motherboard_id == '':
            response['invalid_register'] = "You must choose a MotherBoard"
        else:
            query = MotherBoard.query.filter(MotherBoard.id==motherboard_id)

            if query == []:
                response['invalid_register'] = "There is no motherboard in database"
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

                if motherboard_name == '' and motherboard_description == '' and motherboard_price == '':
                    response['invalid_register'] = "Cannot update if no data is provided"

                if response['invalid_register']:
                    # actualizacion no se hace
                    db.session.rollback()
                else:
                    # actualizacion se hace
                    query.dateModified = func.now()
                    query.modify_by = current_user.id
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
        response['error'] = False
        component_id = request.get_json()["component_id"]

        component_name = request.get_json()["component_name"]
        component_price = request.get_json()["component_price"]
        component_description = request.get_json()["component_description"]
        component_type = request.get_json()["component_type"]

        if component_id == '':
            response['invalid_register'] = "You must choose a component"
        else:
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
                
                if component_name == '' and component_price == '' and component_description == '' and component_type == '':
                    response['invalid_register'] = "Cannot update if no data is provided"

                if response['invalid_register']:
                    # actualizacion no se hace
                    db.session.rollback()
                else:
                    # actualizacion se hace
                    query.dateModified = func.now()
                    query.modify_by = current_user.id
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

        """
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
        """
        simulation = Simulation(id_motherboard=motherboard, create_by=current_user.id)
        db.session.add(simulation)

        components_list_verified = []
        total_price = MotherBoard.query.get(motherboard).price

        def check_component(component_id, components_list_verified):
            if component_id == 0:
                pass
            if Component.query.get(component_id) is None:
                pass
            else:
                components_list_verified.append(component_id)
        
        components_list = peripherals + [psu] + [cpu] + [hdd] + [ram] + [ssd] + [gpu] + [pc_cooling]
        for component in components_list:
            check_component(component, components_list_verified)
        
        for component in components_list_verified:
            total_price += Component.query.get(component).price
            db.session.add(SimulationComponent(id_simulation=simulation.id, id_component=component))

        simulation.total_price = total_price

        db.session.commit()

        response['id_simulation'] = simulation.id
#        response['precio_total'] = round(precio_total, 2)
#        response['matriz'] = matriz

    except Exception as e:
        response['error'] = True
        db.session.rollback()
        print(e)
    finally:
        db.session.close()

    return jsonify(response)

@app.route('/simulation/<id_simulation>')
@login_required
def simulation(id_simulation):
    try:
        # getting the simulation
        simulation = Simulation.query.get(id_simulation)
        # la simulacion no le pertence
        if simulation.create_by != current_user.id:
            abort(401)
        # getting the motherboard from the simulation
        motherboard = MotherBoard.query.get(simulation.id_motherboard)
        # getting the id from components
        simulation_components = SimulationComponent.query.filter_by(id_simulation = id_simulation)
        # getting the components from id simulation_components
        components = []
        for component in simulation_components:
            components.append(Component.query.get(component.id_component))

    except Exception as e:
        db.session.rollback()
        print(e)
        abort(500)
    finally:
        db.session.close()
    
    return render_template('simulation.html',
        simulation=simulation,
        motherboard=motherboard,
        components=components
    )

@app.route('/buy/<precio_total>/<lista>')
@login_required
def compra_resultado(precio_total, lista):
    try:
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
    except Exception as e:
        print(e)
        abort(400)
    finally:
        pass

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
    if int(error) == 400:
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

@app.errorhandler(401)
def error_401(error):
    return render_template('401.html'), 401

@app.errorhandler(400)
def error_400(error):
    return render_template('400.html'), 400

#run
if __name__ == '__main__':
    app.run(debug=True, port=5002)