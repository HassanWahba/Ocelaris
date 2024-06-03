from app.models.OCDM import Process, Event, Object


def get_processes():
    """
    Returns the processes from the local database.
    """
    return Process.query.all()

def get_events():
    """
    Returns the events from the local database.
    """
    return Event.query.all()

def get_objects():
    """
    Returns the objects from the local database.
    """
    return Object.query.all()

def get_process_by_id(process_id):
    """
    Returns the process with the given id from the local database.
    """
    return Process.query.get(process_id)

def get_event_by_id(event_id):
    """
    Returns the event with the given id from the local database.
    """
    return Event.query.get(event_id)

def get_object_by_id(object_id):
    """
    Returns the object with the given id from the local database.
    """
    return Object.query.get(object_id)
