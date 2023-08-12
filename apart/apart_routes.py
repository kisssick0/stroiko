import ast
import datetime

import requests
import json
import phonenumbers

from flask import Flask, Blueprint, current_app, render_template, request, session, redirect, url_for
from sql_provider import SQLProvider
from db_work import work_with_db
import os
from access import group_required


blueprint_apart = Blueprint('blueprint_apart', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_apart.route('/', methods=['GET', 'POST'])
def main():
    _sql = provider.get('get_aparts.sql')
    aparts, _ = work_with_db(current_app.config['dbconfig'], _sql)
    if request.method == 'POST':
        apart_rooms = request.form.get('apart_rooms')
        price_from = request.form.get('price_from')
        price_to = request.form.get('price_to')
        squares_from = request.form.get('squares_from')
        squares_to = request.form.get('squares_to')

        sorting = request.form.get('sorting')
        if sorting == 'По возрастанию цены':
            order_by = 'order by apart_price asc'
        elif sorting == 'По убыванию цены':
            order_by = 'order by apart_price desc'
        elif sorting == 'По возрастанию площади':
            order_by = 'order by apart_square asc'
        elif sorting == 'По убыванию площади':
            order_by = 'order by apart_square desc'

        else:
            order_by = ''
        if apart_rooms == '':
            _sql = provider.get('get_aparts.sql')
        else:
            _sql = provider.get('filter_apartments.sql',
                                apart_rooms=apart_rooms,
                                price_from=price_from,
                                price_to=price_to,
                                squares_from=squares_from,
                                squares_to=squares_to,
                                order_by=order_by)
    else:
        _sql = provider.get('get_aparts.sql')
    aparts, _ = work_with_db(current_app.config['dbconfig'], _sql)
    aparts = list(aparts)
    for i, apart in enumerate(aparts):
        aparts[i] = list(aparts[i])
        aparts[i][5] = url_for('static', filename=aparts[i][5])

    return render_template('aparts_page.html', aparts=aparts)


@blueprint_apart.route('/apart', methods=['GET', 'POST'])
def apart():
    selected_apart = request.args.get('id')
    _sql = provider.get('get_apart.sql', id=selected_apart)
    apart, _ = work_with_db(current_app.config['dbconfig'], _sql)
    apart = list(apart)
    print(apart)
    for i, el in enumerate(apart):
        apart[i] = list(apart[i])
        apart[i][6] = url_for('static', filename=apart[i][6])
    #input_dict = {
     #   'build_tech': apart[0][9],
      #  'floor': apart[0][3],
       # 'area': apart[0][2],
        #'rooms': apart[0][1],
        #'balcon': apart[0][10],
        #'metro_dist': apart[0][11]
    #}
    #resp = requests.post('http://127.0.0.1:8000/predict/', data=json.dumps(input_dict))
   # market_price = int(resp.json())
    #print(market_price)
    if request.method == 'POST':
        if 'role' in session:
            return redirect(url_for('blueprint_client.make_entry', id=selected_apart))
        else:
            return redirect(url_for('blueprint_auth.auth'))
    return render_template('apart_page.html', apart=apart[0], market_price=100)


@blueprint_apart.route('/apart3d', methods=['GET', 'POST'])
def apart3d():
    selected_apart = request.args.get('id')
    _sql = provider.get('get_apart.sql', id=selected_apart)
    apart, _ = work_with_db(current_app.config['dbconfig'], _sql)
    apart = list(apart)
    for i, el in enumerate(apart):
        apart[i] = list(apart[i])
        apart[i][7] = url_for('static', filename=apart[i][7])

    return render_template('3d_page.html', apart=apart[0])