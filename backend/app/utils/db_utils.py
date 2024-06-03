import sqlite3
import os

def create_tmp_db(sql_query):
    # Create a temporary SQLite database
    tmp_db_path = 'temp_database.sqlite'
    if os.path.exists(tmp_db_path):
        os.remove(tmp_db_path)

    full_path = os.path.abspath(tmp_db_path)

    conn = sqlite3.connect(full_path)
    cursor = conn.cursor()
    # split commands by ;
    sql_commands = sql_query.split(';')
    for command in sql_commands:
        cursor.execute(command)
        
    conn.commit()
    conn.close()
    
    return full_path

def remove_db(file_path):
    """Removes the temporary SQLite database if exists."""
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    else:
        return False