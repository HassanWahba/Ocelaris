from flask import Blueprint, request
from app.services.metas_service import create_meta, delete_meta, fetch_metas, update_meta


meta_tables = Blueprint('meta_tables', __name__, url_prefix='/api/meta-tables')

@meta_tables.route('/all', methods=['GET'])
def get_all_meta_tables():
    response = fetch_metas()
    return response

@meta_tables.route('/new', methods=['POST'])
def add_meta_table():
    data = request.json
    response = create_meta(data)
    return response

@meta_tables.route('/update', methods=['POST'])
def modify_meta_table():
    data = request.json
    response = update_meta(data)
    return response

@meta_tables.route('/remove', methods=['POST'])
def remove_meta_table():
    id = request.json.get('id')
    response = delete_meta(id)
    return response
