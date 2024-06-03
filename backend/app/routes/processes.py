import os
from flask import Blueprint, request, send_file
from app.services.processes_service import create_ocel, create_process, fetch_processes, delete_process, update_process

processes = Blueprint('processes', __name__, url_prefix='/api/processes')

@processes.route('/all', methods=['GET'])
def get_processes():
    response = fetch_processes()
    return response

@processes.route('/new', methods=['POST'])
def new_process():
    data = request.get_json()

    response = create_process(data)
    return response

@processes.route('/update', methods=['POST'])
def modify_process():
    data = request.get_json()

    response = update_process(data)
    return response

@processes.route('/remove', methods=['POST'])
def remove_process():
    id = request.json.get('id')

    response = delete_process(id)
    return response

@processes.route('/ocel-sql', methods=['POST'])
def get_ocel():
    id = request.json.get('id')
    format = request.json.get('format')

    response = create_ocel(id, format)
    return response

@processes.route('/export-db-snapshot', methods=['GET'])
def export_db_snapshot():
    filename = os.path.abspath('instance/prod.db')
    return send_file(filename, as_attachment=True)

# @processes.route('/import-db-snapshot', methods=['POST'])
# def import_db_snapshot():
#     file = request.files['file']
#     # check if file is not empty and is a sqlite db
#     if file:
#         # save file as sqlite db
#         file.save('instance/prod.db')
#     return {'message': 'Database snapshot imported successfully'}, 200

# @app.route('/import-db', methods=['POST'])
# def import_db():
#     if 'file' not in request.files:
#         return 'No file part', 400
    
#     file = request.files['file']
#     if file and file.filename == '':
#         return 'No selected file', 400
    
#     if file.filename.endswith('.db'):
#         file.save('instance/prod.db')
#         return 'Database imported successfully', 200
    
#     return 'Invalid file type', 400
