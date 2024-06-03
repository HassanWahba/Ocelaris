from flask import Blueprint, request, jsonify
from app.services.db_service import establish_connection, get_table_names, get_table_from_id, get_supported_dbs
from app.models.ERPSystem import ERPSystem
import configparser

bp = Blueprint('db_connect', __name__, url_prefix='/api/db')

config = configparser.ConfigParser()

@bp.route('/connect', methods=['POST'])
def connect():
    data = request.get_json()
    config.read('config/connection.cfg')

    config['REMOTE']['hostname'] = data.get('hostname')
    config['REMOTE']['port'] = data.get('port')
    config['REMOTE']['sid'] = data.get('sid')
    config['REMOTE']['username'] = data.get('username')
    config['REMOTE']['password'] = data.get('password')
    config['REMOTE']['db_type'] = data.get('db_type')
    config['REMOTE']['erp_type'] = data.get('erp_type')
    
    with open('config/connection.cfg', 'w') as configfile:
        config.write(configfile)
    
    response = establish_connection()
    return jsonify(response)

@bp.route('/table-names', methods=['GET'])
def table_names():
    table_names = get_table_names()
    return jsonify(table_names)

@bp.route('/tables-with', methods=['POST'])
def table_with():
    filter = request.get_json().get('filter')
    # table_names = get_table_with(filter)
    return jsonify(filter)

@bp.route('/table-view', methods=['POST'])
def table_view():
    id = request.get_json().get('id')
    table_names = get_table_from_id(id)
    return jsonify(table_names)

@bp.route('/supported_databases', methods=['GET'])
def supported_databases():
    dbs = get_supported_dbs()

    return jsonify(dbs)

@bp.route('/validate', methods=['GET'])
def validate_connection():
    is_connected, info = ERPSystem.instance.validate_connection()
    if is_connected:
        return jsonify(info), 200
    else:
        return jsonify({"status": "error", "message": "Connection to database failed"})
