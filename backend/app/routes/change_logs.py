from flask import Blueprint, request
from app.services.logs_service import create_change_log, delete_change_log, fetch_change_logs, update_change_log


change_logs = Blueprint('change_logs', __name__, url_prefix='/api/change-logs')

@change_logs.route('/all', methods=['GET'])
def get_all_change_logs():
    response = fetch_change_logs()
    return response

@change_logs.route('/new', methods=['POST'])
def add_change_log():
    data = request.get_json()
    response = create_change_log(data)
    return response

@change_logs.route('/update', methods=['POST'])
def modify_change_log():
    
    data = request.get_json()
    response = update_change_log(data)
    return response

@change_logs.route('/remove', methods=['POST'])
def remove_change_log():
    id = request.json.get('id')
    response = delete_change_log(id)
    return response
