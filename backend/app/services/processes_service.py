from flask import jsonify, send_file
from app.models.ERPSystem import ERPSystem
from app.models.OCDM import Process, Object
from app.utils.db_utils import create_tmp_db, remove_db


def fetch_processes():
    """Fetches all processes from the database and returns them as a JSON object."""
    processes = Process.query.all()
    
    processes_with_previews = [ERPSystem.instance.get_process_info(process) for process in processes]

    return jsonify(processes_with_previews), 200

def create_process(data):
    """Creates a new process in the database and returns it as a JSON object."""
    new_process = Process.from_dict(data)

    objs = Object.query.filter(Object.id.in_(data.get('objects'))).all()
    if len(objs) != len(data.get('objects')):
        return jsonify({'error': 'Object not found'}), 404
    
    new_process.objects = objs
    ERPSystem.instance.add_entity(new_process)

    return jsonify(ERPSystem.instance.get_process_info(new_process)), 201

def update_process(data):
    """Updates an existing process in the database and returns it as a JSON object."""
    process = Process.query.get(data['id'])
    if process is None:
        return jsonify({'error': 'Process not found'}), 404

    objs = Object.query.filter(Object.id.in_(data.get('objects'))).all()
    if len(objs) != len(data.get('objects')):
        return jsonify({'error': 'Object not found'}), 404

    process.update(data)
    ERPSystem.instance.internal_db.session.commit()

    process.objects = objs
    return jsonify(ERPSystem.instance.get_process_info(process)), 201

def delete_process(id):
    """Deletes a process from the database and returns its ID."""
    process = Process.query.get(id)
    if process is None:
        return jsonify({'error': 'Process not found'}), 404
    
    ERPSystem.instance.remove_entity(process)

    return jsonify({'id': id}), 200

def create_ocel(process_id, format):
    """Creates an OCEL representation of a process and returns it as a JSON object."""
    try:
        process_id = int(process_id)
    except ValueError:
        return jsonify({'error': 'Invalid process ID'}), 400
    
    try:
        process_ocel_sql, dfs, o2o_relations = ERPSystem.instance.extract_ocel_sql_query(process_id)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    if format == 'sqlite':
        tmp_db_path = create_tmp_db(process_ocel_sql)
        o2o_relations.to_sql('object_object', 'sqlite:///' + tmp_db_path, if_exists='append', index=False)
        for df in dfs:
            info = df.name.split('+')
            # write to tmp db which is an sqlite db
            if info[0].startswith('event'):
                df_relation = df[['ocel_id', 'ocel_object_id']].drop_duplicates()
                df_relation.rename(columns={'ocel_id': 'ocel_event_id'}, inplace=True)
                df_relation['ocel_qualifier'] = info[0]
                df_relation.to_sql('event_object', 'sqlite:///' + tmp_db_path, if_exists='append', index=False)

                df_res = df[['ocel_id']].drop_duplicates()
                df_res['ocel_type'] = info[1]
                df_res.to_sql('event', 'sqlite:///' + tmp_db_path, if_exists='append', index=False)

                df.drop(columns=['ocel_object_id'], inplace=True)
            elif info[0].startswith('object'):
                df_res = df[['ocel_id']].drop_duplicates()
                df_res['ocel_type'] = info[1]
                df_res.to_sql('object', 'sqlite:///' + tmp_db_path, if_exists='append', index=False)
            df.to_sql(info[0], 'sqlite:///' + tmp_db_path, if_exists='replace', index=False)

        return send_file(tmp_db_path, as_attachment=True, download_name='database.sqlite3'), 200

    else:
        return jsonify({'error': 'Invalid format'}), 400
    
def remove_tmp_db(file_path):
    """Removes the temporary SQLite database if exists."""
    return remove_db(file_path)
