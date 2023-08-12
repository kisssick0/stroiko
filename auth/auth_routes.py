import phonenumbers
from flask import request, render_template, session, Blueprint, current_app, url_for, redirect
from sql_provider import SQLProvider
from db_work import work_with_db
import os

blueprint_auth = Blueprint('blueprint_auth', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def auth():
    if 'role' in session:
        if session['role'] == 'client':
            return redirect(url_for('blueprint_client.profile'))
        if session['role'] == 'manager':
            return redirect(url_for('blueprint_manager.main'))
    login = request.form.get('email')
    password = request.form.get('password')
    is_find, id, user_type, internal_type = auth_user(login, password)
    if is_find:
        session['user_login'] = login
        session['id'] = id
        session.permanent = True
        if user_type == 'client':
            print('i in client')
            name, surname = get_name_surname(login, password)
            session['name'] = name
            session['surname'] = surname
            session['role'] = 'client'
            return redirect(url_for('blueprint_client.profile'))

        elif user_type == 'manager':
            print('i in manager')
            name, surname = get_manager_name_surname(manager_id=id)
            session['name'] = name
            session['surname'] = surname
            session['role'] = 'manager'
            return redirect(url_for('blueprint_manager.main'))
    return render_template('authorization.html')


@blueprint_auth.route('/registration', methods=['GET', 'POST'])
def registration():

    name = request.form.get('name')
    surname = request.form.get('surname')
    second_name = request.form.get('second_name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    if name and surname and second_name and phone and email and password:
        if not auth_user(email, password)[0]:
            sql_new_user = provider.get('new_client.sql',
                                        client_name=name,
                                        surname=surname,
                                        second_name=second_name,
                                        phone=phone,
                                        email=email,
                                        password=password)
            result_internal, _ = work_with_db(current_app.config['dbconfig'], sql_new_user)
            session['id'] = auth_user(email, password)[1]
            session['user_login'] = email
            session['name'] = name
            session['surname'] = surname
            session['role'] = 'client'
            return redirect(url_for('blueprint_client.profile'))
        else:
            return "Пользователь уже зарегистрирован"

    return render_template('registration.html')


def auth_user(user_email, user_password):
    sql_client = provider.get('check_client.sql', email=user_email, password=user_password)
    sql_manager = provider.get('check_manager.sql', email=user_email, password=user_password)
    result_client, _ = work_with_db(current_app.config['dbconfig'], sql_client)
    print(result_client)
    if len(result_client) == 1:
        return True, result_client[0][0], 'client', result_client[0][3]

    result_manager, _ = work_with_db(current_app.config['dbconfig'], sql_manager)
    if len(result_manager) == 1:
        return True, result_manager[0][0], 'manager', None
    return False, None, None, None


def get_name_surname(user_email, user_password):
    sql_external = provider.get('get_client_name.sql', email=user_email, password=user_password)
    result_external, _ = work_with_db(current_app.config['dbconfig'], sql_external)
    return result_external[0][0], result_external[0][1]


def get_manager_name_surname(manager_id):
    sql_external = provider.get('get_manager_name.sql', manager_id=manager_id)
    result_external, _ = work_with_db(current_app.config['dbconfig'], sql_external)
    print(result_external)
    return result_external[0][0], result_external[0][1]


