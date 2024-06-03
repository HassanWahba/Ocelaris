from flask import jsonify
from app.models.ERPSystem import ERPSystem
from app.models.OCDM import ChangeLog, Event, Object


def fetch_events():
    """Fetches all events from the database and returns them as a JSON object."""
    events = Event.query.all()
    
    events_with_previews = [ERPSystem.instance.get_event_preview(event) for event in events]

    return jsonify(events_with_previews), 200

def create_event(data):
    """Creates a new event in the database and returns it as a JSON object."""
    change_log = ChangeLog.query.get(data['change_log'])
    if change_log is None:
        return jsonify({'error': 'Change log not found'}), 404
    
    objs = Object.query.filter(Object.id.in_(data.get('objects'))).all()
    if len(objs) != len(data.get('objects')):
        return jsonify({'error': 'Object not found'}), 404
    
    new_event = Event.from_dict(data)
    new_event.log = [change_log]
    new_event.objects = objs

    ERPSystem.instance.add_entity(new_event)

    return jsonify(ERPSystem.instance.get_event_preview(new_event)), 201

def update_event(data):   
    """Updates an existing event in the database and returns it as a JSON object."""
    change_log = ChangeLog.query.get(data['change_log'])
    if change_log is None:
        return jsonify({'error': 'Change log not found'}), 404
    
    objs = Object.query.filter(Object.id.in_(data.get('objects'))).all()
    if len(objs) != len(data.get('objects')):
        return jsonify({'error': 'Object not found'}), 404
    
    event = Event.query.get(data.get('id'))
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    
    event.update(data)
    event.log = [change_log]
    event.objects = objs
    
    ERPSystem.instance.internal_db.session.commit()

    return jsonify(ERPSystem.instance.get_event_preview(event)), 201

def delete_event(id):
    """Deletes an event from the database and returns its ID."""
    event = Event.query.get(id)
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    
    ERPSystem.instance.remove_entity(event)

    return jsonify({'message': 'Event deleted'}), 200
