import ast
import datetime

from flask import Flask, Blueprint, current_app, render_template, request, session, redirect, url_for
from sql_provider import SQLProvider
from db_work import work_with_db
import os
from access import group_required


blueprint_complex = Blueprint('blueprint_complex', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_complex.route('/', methods=['GET', 'POST'])
#@group_required
def main():
    _sql = provider.get('get_complexes.sql')
    complexes, _ = work_with_db(current_app.config['dbconfig'], _sql)
    print(complexes)
    return render_template('complexes_page.html', complexes=complexes)
