from flask import jsonify
from app.models.OCDM import ChangeLog
from app.models.ERPSystem import ERPSystem
from app.utils.erp_utils import get_change_logs


def fetch_change_logs():
    """Fetches all change logs from the database and returns them as a JSON object."""
    change_logs = get_change_logs()
    
    return jsonify([ERPSystem.instance.get_change_log_preview(change_log) for change_log in change_logs]), 200

def create_change_log(data):
    """Creates a new change log in the database and returns it as a JSON object."""
    change_log = ChangeLog.from_dict(data)

    ERPSystem.instance.add_entity(change_log)

    return jsonify(ERPSystem.instance.get_change_log_preview(change_log)), 201

def update_change_log(data):
    """Updates an existing change log in the database and returns it as a JSON object."""
    change_log = ChangeLog.query.get(data.get('id'))
    if change_log is None:
        return jsonify({'error': 'ChangeLog not found'}), 404

    change_log.update(data)
    ERPSystem.instance.internal_db.session.commit()

    return jsonify(ERPSystem.instance.get_change_log_preview(change_log)), 200

def delete_change_log(id):
    """Deletes a change log from the database and returns its ID."""
    change_log = ChangeLog.query.get(id)
    if change_log is None:
        return jsonify({'error': 'ChangeLog not found'}), 404
    
    ERPSystem.instance.remove_entity(change_log)

    return jsonify({'id': id}), 200
