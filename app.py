""" from flask import Flask, request, jsonify, redirect
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import validators
import sqlite3
import hashlib

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

# Conexión a la base de datos SQLite

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla de enlaces acortados

def init_db():
    conn = get_db_connection()

    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user' -- 'user' or 'admin'
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_url TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()
# Verificar si es admin

def is_admin(user_id):
    with sqlite3.connect('database.db') as conn:
        cursor = conn.execute('SELECT role FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        if user and user[0] == 'admin':
            return True
        return False
# Verificar si el slug existe

def slug_exists(slug):
    conn = get_db_connection()
    url = conn.execute('SELECT 1 FROM urls WHERE short_url = ?', (slug,)).fetchone()
    conn.close()
    return url is not None
# Ruta principal para acortar URL

@app.route('/shorten', methods=['POST'])
@jwt_required()
def shorten_url():
    data = request.get_json()
    original_url = data.get('url')
    custom_slug = data.get('slug')
    user_id = get_jwt_identity()

    # Validar URL
    if not validators.url(original_url):
        return jsonify({'error': 'Invalid URL'}), 400
    
    # Verificar si el slug existe

    if custom_slug:
        if slug_exists(custom_slug):
            return jsonify({'error': 'Slug alredy in use'}), 409
        short_url = custom_slug
    else:
        # Generar el código corto a partir de un hash
        short_url = hashlib.md5(original_url.encode()).hexdigest()[:6]

        while slug_exists(short_url):
            short_url = hashlib.md5(short_url.encode()).hexdigest()[:6]



    # Guardar en la base de datos
    conn = get_db_connection()
    conn.execute('INSERT INTO urls (original_url, short_url, user_id) VALUES (?, ?, ?)', (original_url, short_url, user_id))
    conn.commit()
    conn.close()

    return jsonify({'short_url': request.host_url + short_url}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and pbkdf2_sha256.verify(password, user['password']):
        # Crear token de acceso JWT
        acces_token = create_access_token(identity=user['id'])
        return jsonify(acces_token=acces_token), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# Redireccionar a la URL original

@app.route('/<short_url>')
def redirect_to_url(short_url):
    conn = get_db_connection()
    url = conn.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,)).fetchone()
    conn.close()

    if url:
        return redirect(url['original_url'])
    else:
        return jsonify({'error': 'URL not found'}), 404
    
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Validar que los campos no estén vacíos
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Hash de la contaseña
    hashed_pasword = pbkdf2_sha256.hash(password)

    # Guardar el usuario

    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pasword))
        conn.commit()
        conn.close()
    except:
        return jsonify({'error': 'Username alredy exists'})
    
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/my-urls', methods=['GET'])
@jwt_required()
def get_user_urls():
    user_id = get_jwt_identity()

    conn = get_db_connection()
    urls = conn.execute('SELECT original_url, short_url FROM urls WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()

    urls_list = [{'original_url': url['original_url'], 'short_url': request.host_url + url['short_url']} for url in urls]

    return jsonify(urls_list), 200
    
if __name__ == '__main__':
    init_db()
    app.run(debug=True) """

from flask import Flask, redirect
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes import auth, urls
from database import init_db, get_db

app = Flask(__name__)
CORS(app)

app.config.from_object('config.Config')
jwt = JWTManager(app)

with app.app_context():
    # Inicializar db
    init_db()

# Registrar blueprints de las rutas
app.register_blueprint(auth.bp)
app.register_blueprint(urls.bp)

@app.route('/<short_url>')
def redirect_to_url(short_url):
    db = get_db()
    url = db.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,)).fetchone()

    if url:
        return redirect(url[0])
    else:
        return {'error': 'URL not found'}, 404


""" from flask import jsonify

# Captura todos los errores 404 (Not Found)
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404

# Captura todos los errores 500 (Internal Server Error)
@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

# Captura cualquier otro error y lo devuelve en formato JSON
@app.errorhandler(Exception)
def handle_exception(e):
    # Si el error ya tiene un código de estado, lo usamos
    status_code = getattr(e, 'code', 500)
    return jsonify({'error': str(e)}), status_code
 """

if __name__ == '__main__':
    app.run(debug=True)