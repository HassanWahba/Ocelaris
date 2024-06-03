from flask import jsonify
from app.models.ERPSystem import ERPSystem
from app.models.OCDM import Object


def fetch_objects():
    objects = Object.query.all()

    objects_with_previews = [ERPSystem.instance.get_object_preview(object) for object in objects]
    
    return jsonify(objects_with_previews), 200

def create_sql_object(data):
    new_object = Object.from_dict(data)
    
    objs = Object.query.filter(Object.id.in_(data.get('objects'))).all()
    if len(objs) != len(data.get('objects')):
        return jsonify({'error': 'Object not found'}), 404
    new_object.related_objects = objs

    ERPSystem.instance.add_entity(new_object)
    
    return jsonify(ERPSystem.instance.get_object_preview(new_object)), 201

def update_sql_object(data):   
    """Updates an existing SQL object in the database and returns it as a JSON object."""
    object = Object.query.get(data.get('id'))
    if object is None:
        return jsonify({'error': 'Event not found'}), 404

    objs = Object.query.filter(Object.id.in_(data.get('objects'))).all()
    if len(objs) != len(data.get('objects')):
        return jsonify({'error': 'Object not found'}), 404
    
    object.update(data)
    object.related_objects = objs

    ERPSystem.instance.internal_db.session.commit()

    return jsonify(ERPSystem.instance.get_object_preview(object)), 201

def delete_object(id):
    obj = Object.query.get(id)
    if obj is None:
        return jsonify({'error': 'Object not found'}), 404
    
    ERPSystem.instance.remove_entity(obj)

    return jsonify({'message': 'Object deleted'}), 200
