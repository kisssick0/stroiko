import ast
import datetime

from flask import Flask, Blueprint, current_app, render_template, request, session, redirect, url_for
from sql_provider import SQLProvider
from db_work import work_with_db
import os
from access import group_required


blueprint_manager = Blueprint('blueprint_manager', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_manager.route('/', methods=['GET', 'POST'])
@group_required
def main():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('blueprint_main.main'))
    name = session['name'] if 'name' in session else ''
    surname = session['surname'] if 'surname' in session else ''
    return render_template('manager_page.html', full_name=f'{surname} {name}')


@blueprint_manager.route('/entries', methods=['GET', 'POST'])
@group_required
def entries():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('blueprint_main.main'))
    sql_get_entries = provider.get('manager_entries.sql', manager_id=session['id'])
    entries, _ = work_with_db(current_app.config['dbconfig'], sql_get_entries)
    entries = [list(entrie) for entrie in entries]
    return render_template('manager_entries.html', entries=entries)


@blueprint_manager.route('/requests', methods=['GET', 'POST'])
@group_required
def requests():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('blueprint_main.main'))
    _sql = provider.get('get_manager_requests.sql')
    print(_sql)
    requests, _ = work_with_db(current_app.config['dbconfig'], _sql)
    print(requests)
    return render_template('manager_requests.html', requests=requests)

@blueprint_manager.route('/aparts', methods=['GET', 'POST'])
@group_required
def aparts():
    if request.method == 'POST':
        pass
    _sql = provider.get('get_manager_aparts.sql')
    aparts, _ = work_with_db(current_app.config['dbconfig'], _sql)
    aparts = list(aparts)
    for i, apart in enumerate(aparts):
        aparts[i] = list(aparts[i])
        print(url_for('static', filename=aparts[i][5]))
        aparts[i][5] = url_for('static', filename=aparts[i][5])
    print(aparts)
    return render_template('manager_aparts.html', aparts=aparts)


@blueprint_manager.route('/confirm', methods=['GET', 'POST'])
@group_required
def confirm():
    selected_entry = request.args.get('id')
    print(selected_entry)
    _sql = provider.get('add_manager_entry.sql', entry_id=selected_entry, manager_id=session['id'])
    entries, _ = work_with_db(current_app.config['dbconfig'], _sql)
    entries = [list(entrie) for entrie in entries]
    return render_template('manager_entries.html', entries=entries)
