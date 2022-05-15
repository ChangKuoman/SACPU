# <img src="https://user-images.githubusercontent.com/92172040/168483567-d59c8404-fe28-4a1d-80e1-c1e7eaafd230.png" alt="logoSACPU" width="35"/>  SACPU - PC Build Simulator

### Integrantes

* Anderson Cárcamo (100%)
* Susana Chang (100%)

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

Host de postgres: localhost (127.0.0.1)

Puerto de postgres: 5432

Host para la aplicación web: localhost (127.0.0.1)

Puerto para la aplicación web: 5002

### Forma de autenticación

Para la autenticación dentro de la aplicación web se creó un endpoint /register para el registro de usuarios. Se pide al usuario ingresar un username e ingresar dos veces una clave. El username es único y no puede repetirse en la base de datos, si lo hace, se mostrará al usuario un mensaje de que el username ya está en uso. Asimismo debe tener una longitud entre 4 y 20 caracteres. La clave coincidir las 2 veces que el usuario la ingresa, además pasa por un chequeo de seguridad en el que se pide que contenga 1 letra mayúscula, 1 letra minúscula, 1 dígito, 1 caracter especial y una longitud entre 6 y 20 caracteres. Las claves ingresadas a la base de datos son encriptadas mediante el uso de la librería bcrypt, para mantener la seguridad de los usuarios.

El rol automático que se les dará a los usuarios que se registren es 'user', solo pudiendo acceder a ciertos endpoints relacionados a la simulación de la compra de componentes. El rol de 'admin' solo puede ser otorgado mediante un update en la base de datos. Este rol permite acceder al endpoint /admin y todas las funcionalidades dentro de ella como son la creación de productos, eliminación de los mismos y la actualización de las propiedades de los productos.

Después de la creación del usuario en la base de datos la página redirige al endpoint /login para que el usuario ingrese poniendo su username y el pasword.

### Manejo de errores HTTP
**500: Errores en el servidor**

* Error 500: Internal Server Error
    Al momento de que haya un error en el servidor, la aplicación web redirige a una página que muestra que se ha producido un error 500 y un botón para regresar a la página principal.

**400: Errores en el cliente**

* Error 404: Page not Found
    
    Si una página no se encuentra, la aplicación web redirige a una página que muestra que se ha producido un error 404 y un botón para regresar a la página principal.
    
* Error 401: Unauthorized
    
    Si el usuario trata de ingresar a un endpoint al que no tiene acceso, la aplicación web redirige a una página que muestra que se ha producido un error 401 y un botón para regresar a la página principal.
    
* Error 400: Bad Request
   
    Si ocurre una petición incorrecta por parte del usuario, la aplicación web redirige a una página que muestra que se ha producido un error 400 y un botón para regresar a la página principal.

**300: Redirección**

    En el desarrollo de la aplicación web, no se visto necesario implementar visualmente al usuario las respuestas de redirección.

**200: Exitoso**

    En el desarrollo de la aplicación web, no se visto necesario implementar visualmente al usuario las respuestas exitosas.

**100: Informacional**

    En el desarrollo de la aplicación web, no se visto necesario implementar visualmente al usuario las respuestas informacionales.

### Deployment scripts

Para ejecutar la aplicación web primero se deben seguir los pasos para iniciar la base de datos como se mostró más arriba. Luego debe cambiar el path del static folder. Ejemplo:

``` python
app = Flask(__name__, static_folder='home/chang/Escritorio/SACPU/templates/static')
```

Por último ya estaía listo toda la configuración necesaria y se puede ejecutar la aplicación web.

``` bash
python3 app.py
```
