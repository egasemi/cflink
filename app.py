from flask import Flask, redirect, request, send_from_directory
from user_agents import parse
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes import auth, links, urls
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
app.register_blueprint(links.bp)

@app.route('/')
def serve_forntend():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory('static', path)

@app.route('/<short_url>')
def redirect_to_url(short_url):
    user_agent_string = request.user_agent.string
    ip_address = request.headers.get('X-Real-IP', request.remote_addr)
    user_agent = parse(user_agent_string)
    browser = (user_agent.browser.family or "Unknown") + ", " + (user_agent.browser.version_string or "Unknown")
    os = (user_agent.os.family or "Unknown") + ", " + (user_agent.os.version_string or "Unknown")
    device = (user_agent.device.family or "Unknown") + ", " + (user_agent.device.brand or "Unknown")
    referrer = (request.headers.get('Referrer') or 'Unknown')
    db = get_db()
    url = db.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,)).fetchone()
    if url:
        db.execute("""
        INSERT INTO link_visits (short_url, original_url, user_agent, ip_address, browser, os, device, referrer)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (short_url, url[0], user_agent_string, ip_address, browser, os, device, referrer))

        db.commit()
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