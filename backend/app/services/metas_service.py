from flask import jsonify
from app.models.OCDM import Meta
from app.models.ERPSystem import ERPSystem
from app.utils.erp_utils import get_meta_tables


def fetch_metas():
    """Fetches all meta tables from the database and returns them as a JSON object."""
    meta_tables = get_meta_tables()

    return jsonify([ERPSystem.instance.get_meta_table_preview(meta_table) for meta_table in meta_tables]), 200

def create_meta(data):
    """Creates a new meta table in the database and returns it as a JSON object."""
    meta_table = Meta.from_dict(data)

    ERPSystem.instance.add_entity(meta_table)
    
    return jsonify(ERPSystem.instance.get_meta_table_preview(meta_table)), 201

def update_meta(data):
    """Updates an existing meta table in the database and returns it as a JSON object."""
    meta_table = Meta.query.get(data.get('id'))
    if meta_table is None:
        return jsonify({'error': 'MetaTable not found'}), 404

    meta_table.update(data)
    ERPSystem.instance.internal_db.session.commit()

    return jsonify(ERPSystem.instance.get_meta_table_preview(meta_table)), 200

def delete_meta(id):
    """Deletes a meta table from the database and returns its ID."""
    meta_table = Meta.query.get(id)
    if meta_table is None:
        return jsonify({'error': 'MetaTable not found'}), 404
    
    for table in meta_table.tables:
        ERPSystem.instance.remove_entity(table)

    ERPSystem.instance.remove_entity(meta_table)
    
    return jsonify({'id': id}), 200