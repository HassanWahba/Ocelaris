from flask import Blueprint, request, send_file
from app.services.objects_service import create_sql_object, delete_object, fetch_objects, update_sql_object

objects = Blueprint('objects', __name__, url_prefix='/api/objects')

@objects.route('/all', methods=['GET'])
def get_all_objects():
    response = fetch_objects()
    return response

@objects.route('/sql/new', methods=['POST'])
def new_object():
    data = request.get_json()

    response = create_sql_object(data)
    return response

@objects.route('/sql/update', methods=['POST'])
def modify_sql_object():
    data = request.get_json()

    response = update_sql_object(data)
    return response

@objects.route('/remove', methods=['POST'])
def remove_object():
    id = request.json('id')

    response = delete_object(id)
    return response
