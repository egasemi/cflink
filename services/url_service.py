import hashlib

from flask import request
from flask_jwt_extended import get_jwt_identity
import validators
from database import get_db

def slug_exists(slug):
    db = get_db()
    url = db.execute('SELECT 1 FROM urls WHERE short_url = ?', (slug,)).fetchone()
    return url is not None

def generate_short_url(custom_slug, original_url):
    if custom_slug:
        if slug_exists(custom_slug):
            return None
        return custom_slug
    else:
        # Generar el código corto a partir de un hash
        short_url = hashlib.md5(original_url.encode()).hexdigest()[:6]

        while slug_exists(short_url):
            short_url = hashlib.md5(short_url.encode()).hexdigest()[:6]
        return short_url


def create_short_url(data):
    original_url = data.get('url')
    custom_slug = data.get('slug')
    user_id = get_jwt_identity()
    short_url = generate_short_url(custom_slug, original_url)
    
    # Validar URL
    if not validators.url(original_url):
        return {'error': 'Invalid URL'}, 400

    if not short_url:
        return {'error': 'Slug alredy in use'}, 409

    db = get_db()
    db.execute('INSERT INTO urls (original_url, short_url, user_id) VALUES (?, ?, ?)', (original_url, short_url, user_id))
    db.commit()

    return {'short_url': request.host_url + short_url}, 201

def edit_url(url_id, data):
    new_url = data.get('new_url')
    db = get_db()
    db.execute('UPDATE urls SET original_url = ? WHERE id = ?', (new_url, url_id))
    db.commit()

    return {'message': 'URL updated sucessfully'}, 200

def delete_url(url_id):
    db = get_db()
    db.execute('DELETE FROM urls WHERE id = ?', (url_id,))
    db.commit()

    return {'message': 'URL deleted successfully'}, 200