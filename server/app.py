from flask import Flask, send_from_directory, render_template, request, jsonify, session, g
import atexit, os, jinja2, json, sqlite3

app = Flask(__name__, static_url_path='/static')
app.secret_key = "supersecretkey"
DATABASE = "database.db"

TEMPLATES_DIR = 'templates'
STATIC_DIR = 'static'

with open("config.json", "r") as file:
    json_data = json.load(file)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db

@app.before_request
def setup():
    with app.app_context():
        atexit.register(close_db)

@app.teardown_appcontext
def close_db(exception=None):
    """Closes the database connection if it's open"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def read_file(file_path):
    try:
        with open(f"static/txt/{file_path}", 'r') as file:
            file_content = file.read()
        return file_content
    except FileNotFoundError:
        return f"Error: The file '{file_path}' was not found."
    except IOError:
        return f"Error: There was an issue reading the file '{file_path}'."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

@app.route('/login', methods=['POST'])
def handle_login():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    sql_data = cursor.fetchone()

    print("SQL Data:", sql_data)

    if sql_data and sql_data[1] == password:
        session["username"] = username
        return jsonify({"response": True})
    else:
        return jsonify({"response": False})
        

@app.route("/status", methods=["GET"])
def status():
    current_user = get_user()
    if current_user != False:
        return jsonify({"response": current_user})
    else:
        return jsonify({"response": False}), 401
    
def get_user():
    if "username" in session:
        return session['username']
    else:
        return False

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("username", None)
    return jsonify({"response": "Logged out successfully"})

@app.route('/heartRate')
def serve_heartrate():
    try:
        with open('static/txt/heartrate.txt', 'r') as file:
            bpm = file.read().strip()
        return jsonify({"bpm": bpm})
    except Exception as e:
        return jsonify({"bpm": 100})


@app.route('/<filename>.html')
def serve_html(filename):
    try:
        return render_template(f'{filename}.html')
    except jinja2.exceptions.TemplateNotFound:
        return jsonify({"error": f"Template {filename}.html not found."}), 40

@app.route('/static/css/<filename>')
def serve_css(filename):
    try:
        return send_from_directory(os.path.join(STATIC_DIR, 'css'), filename)
    except FileNotFoundError:
        return f"The CSS file {filename} isn't available", 404

@app.route('/static/js/<filename>')
def serve_js(filename):
    try:
        return send_from_directory(os.path.join(STATIC_DIR, 'js'), filename)
    except FileNotFoundError:
        return f"The JS file {filename} isn't available", 404

@app.route('/')
def index():
    text_contents = read_file("about.txt")
    return render_template('index.html', about_text=text_contents)

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Page not found", "message": "The requested URL was not found on the server."}), 404

atexit.register(close_db)

if __name__ == '__main__':
    app.run(debug=False)
