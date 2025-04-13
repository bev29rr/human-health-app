from flask import Flask, send_from_directory, render_template, jsonify, g, abort
import atexit, os, jinja2, json, secrets
from api import api, get_db

app = Flask(__name__, static_url_path='/static')
app.register_blueprint(api)
app.secret_key = secrets.token_hex(24)

TEMPLATES_DIR = 'templates'
STATIC_DIR = 'static'

try:
    with open("config.json", "r") as file:
        json_data = json.load(file)
except Exception as e:
    print("Error loading config.json:", e)
    json_data = {}

@app.teardown_appcontext
def close_db(exception=None):
    """Closes the database connection if it's open"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def read_file(file_path):
    try:
        with open(f"static/txt/{file_path}", 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except IOError:
        return f"Error: There was an issue reading the file '{file_path}'."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@app.route('/<filename>.html')
def serve_html(filename):
    try:
        return render_template(f'{filename}.html')
    except jinja2.exceptions.TemplateNotFound:
        abort(404)

@app.route('/static/css/<filename>')
def serve_css(filename):
    try:
        return send_from_directory(os.path.join(STATIC_DIR, 'css'), filename)
    except FileNotFoundError:
        abort(404)

@app.route('/static/js/<filename>')
def serve_js(filename):
    try:
        return send_from_directory(os.path.join(STATIC_DIR, 'js'), filename)
    except FileNotFoundError:
        abort(404)

@app.route('/')
def index():
    text_contents = read_file("about.txt")
    return render_template('index.html', about_text=text_contents)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=False)
