from flask import Flask, url_for, redirect, session
from main.main_routes import blueprint_main
from complex.complex_routes import blueprint_complex
from client.client_routes import blueprint_client
from manager.manager_routes import blueprint_manager
from auth.auth_routes import blueprint_auth
from apart.apart_routes import blueprint_apart
#from access import login_required
import json
import os
import sys

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, '../company')
app = Flask(__name__, template_folder=template_path)

static_path = os.path.join(project_root, '../company/static')

app = Flask(__name__, template_folder=template_path, static_folder=static_path)
app.secret_key = 'kisssick'


app.register_blueprint(blueprint_main, url_prefix='/main')
app.register_blueprint(blueprint_complex, url_prefix='/complexes')
app.register_blueprint(blueprint_auth, url_prefix='/auth')
app.register_blueprint(blueprint_client, url_prefix='/client')
app.register_blueprint(blueprint_manager, url_prefix='/manager')
app.register_blueprint(blueprint_apart, url_prefix='/apartments')


app.config['dbconfig'] = {'host': '127.0.0.1', 'user': 'root', 'password': 'qwerty123', 'database': 'company'}
app.config['access_config'] = json.load(open('configs/access.json'))


@app.route('/')
def complex_choice():
    return redirect(url_for('blueprint_main.main'))


@app.route('/exit')
def goodbye():
    return 'До новых встреч!'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
