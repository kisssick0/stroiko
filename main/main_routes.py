import ast
import datetime

from flask import Flask, Blueprint, current_app, render_template, request, session, redirect, url_for
from sql_provider import SQLProvider
from db_work import work_with_db
import os
from access import group_required

blueprint_main = Blueprint('blueprint_main', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

@blueprint_main.route('/', methods=['GET', 'POST'])
def main():
    return render_template('main_page.html')


@blueprint_main.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact_page.html')