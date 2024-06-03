from flask import Blueprint, request
from app.services.events_service import create_event, fetch_events, delete_event, update_event

events = Blueprint('events', __name__, url_prefix='/api/events')

@events.route('/all', methods=['GET'])
def get_events():
    response = fetch_events()
    return response

@events.route('/new', methods=['POST'])
def new_event():
    data = request.get_json()
    
    response = create_event(data)
    return response

@events.route('/update', methods=['POST'])
def modify_event():
    data = request.get_json()
    
    response = update_event(data)
    return response

# Not Tested
@events.route('/remove', methods=['POST'])
def remove_event():
    id = request.json.get('id')

    response = delete_event(id)
    return response
