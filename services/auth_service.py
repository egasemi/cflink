from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_db

def register_user(data):
    username = data.get('username')
    password = generate_password_hash(data.get('password'))

    db = get_db()
    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    db.commit()

    return {'message': 'User registered successfully'}, 201

def login_user(data):
    username = data.get('username')
    password = data.get('password')

    db = get_db()
    user = db.execute('SELECT * FROM users  WHERE username = ?', (username,)).fetchone()

    if user:
        if check_password_hash(user[2], password):
            access_token = create_access_token(identity=user[0])
            return {"access_token" : access_token}, 200
    
    return {'error': 'Invalid credentials'}, 401