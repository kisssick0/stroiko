import ast
import datetime

from flask import Flask, Blueprint, current_app, render_template, request, session, redirect, url_for
from sql_provider import SQLProvider
from db_work import work_with_db
import os
from access import group_required


blueprint_client = Blueprint('blueprint_client', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_client.route('/', methods=['GET', 'POST'])
def main():
    name = session['name'] if 'name' in session else ''
    surname = session['surname'] if 'surname' in session else ''
    return render_template('client_profile.html', full_name=f'{name} {surname}')


@blueprint_client.route('/entries', methods=['GET', 'POST'])
def entries():
    print('session id: ', session['id'])
    sql_get_entries = provider.get('client_entries.sql', client_id=session['id'])
    entries, _ = work_with_db(current_app.config['dbconfig'], sql_get_entries)
    print(entries)
    entries = [list(entrie) for entrie in entries]
    print(entries)
    return render_template('client_entries.html', entries=entries)


@blueprint_client.route('/profile', methods=['GET', 'POST'])
def profile():
    print('session id: ', session['id'])
    sql_get_client = provider.get('client_information.sql', client_id=session['id'])
    client, _ = work_with_db(current_app.config['dbconfig'], sql_get_client)
    return render_template('client_profile.html', client=client[0])


@blueprint_client.route('/make_entry', methods=['GET', 'POST'])
def make_entry():
    selected_apart = request.args.get('id')
    if request.method == 'POST':
        entry_date = request.form.get('entry_date')
        sql_make_entry = provider.get('make_entry.sql',
                                      client_id=session['id'],
                                      apart_id=selected_apart,
                                      entry_date=entry_date)

        work_with_db(current_app.config['dbconfig'], sql_make_entry)
        return render_template('client_entries.html')
    return render_template('client_make_entry.html', id=selected_apart)


@blueprint_client.route('/exit', methods=['GET', 'POST'])
def exit():
    session.clear()
    return redirect(url_for('blueprint_main.main'))