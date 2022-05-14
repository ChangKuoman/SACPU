# SACPU - PC Build Simulator

### Integrantes
* Anderson Cárcamo (100%)
* Susana Chang (100%)
* Mishelle Villareal (0%)
* Leandro Machaca (0%)

### Descripción del proyecto
Nuestro proyecto es una aplicación web realizada con el _micro_ Framework Flask que permite el simulado de compra de una computadora teniendo en cuenta como pieza base la tarjeta madre y la compatibilidad de esta con los diferentes componentes. La información de la base de datos está basada en direntes páginas web de compra de tecnología especializada en computadoras como LoginStore, y marcas propias como MSI, AMD, Intel, entre otros.

### Objetivos principales
* **Misión**

    Simular el armado de una PC para ayudar a nuestros usuarios que no tengan un conociemiento base de como comprar una computadora por piezas.

* **Visión**

    Cumplir con la demanda de nuestros usuarios, siendo útil y de fácil manejo. Subir la aplicación web a la nube para tener más alcance y expandir nuestra base de datos.

### Información de librerías/frameworks/plugins

| Librería | Versión |
| ----------- | ----------- |
| alembic | 1.7.7 |
| bcrypt | 3.2.2 |
| cffi | 1.15.0 |
| click | 8.1.3 |
| dnspython | 2.2.1 |
| Flask | 2.1.2 |
| Flask-Login | 0.6.1 |
| Flask-Migrate | 3.1.0 |
| Flask-SQLAlchemy | 2.5.1 |
| greenlet | 1.1.2 |
| importlib-metadata | 4.11.3 |
| importlib-resources | 5.7.1 |
| is-disposable-email | 1.0.0 |
| itsdangerous | 2.1.2 |
| Jinja2 | 3.1.2 |
| Mako | 1.2.0 |
| MarkupSafe | 2.1.1 |
| psycopg2-binary | 2.9.3 |
| pycparser | 2.21 |
| SQLAlchemy | 1.4.36 |
| Werkzeug | 2.1.2 |
| zipp | 3.8.0 |

### Script a ejecutar la base de datos

Para ejecutar la base de datos con datos, lo primero que se tiene que realizar es crear en **postgresql** la base de datos con nombre **sacpu**

``` sql
CREATE DATABASE sacpu;
```

Teniendo la base de datos creada, en el archivo main.py se debe cambiar el URI. Ejemplo:

``` python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://usuario:clave@host:puerto/sacpu'
```

Tener en cuenta que se deben importar las librerías usadas en el pyotecto (requirements.txt) en tu ambiente virtualizado.

``` bash
pip install -r requirements.txt
```

Y también actualizar el esquema en la base de datos:

``` bash
flask db upgrade
```

Por último para que la base de datos tenga datos se deben ejecutar en el siguiente orden los archivos:

``` bash
python3 data_users.py
```

``` bash
python3 data_motherboards.py
```

``` bash
python3 data_components.py
```

``` bash
python3 data_compatible.py
```

### Hosts
localhost:5432
puerto para la aplicación web: 5002

### Forma de autenticación

### Manejo de errores HTTP
**500: Errores en el servidor**

**400: Errores en el cliente**

**300: Redirección**

**200: Exitoso**

**100: Informacional**

### Deployment scripts

Para ejecutar la aplicación web primero se deben seguir los pasos para iniciar la base de datos como se mostró más arriba. Luego debe cambiar el path del static folder. Ejemplo:

``` python
app = Flask(__name__, static_folder='home/chang/Escritorio/SACPU/templates/static')
```

Por último ya estaía listo toda la configuración necesaria y se puede ejecutar la aplicación web.

``` bash
python3 app.py
```
