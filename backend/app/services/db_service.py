from app.models.DBConnection import DatabaseFactory
from app.models.ERPSystem import ERPSystem
from app.models.OCDM import db, Table
import configparser
import logging

config = configparser.ConfigParser()

def establish_connection():
    """
    Establishes a connection to a remote database and ERP system, and stores metadata about the ERP system in the local database.

    Returns:
        dict: A dictionary containing the status of the operation and a message.
        int: HTTP status code.
    """
    config.read('config/connection.cfg')

    # Get the connection details from the configuration file
    erp_type = config.get('REMOTE', 'erp_type')

    database = DatabaseFactory.get_database(config)
    if not database:
        logging.error("Could not connect to database with provided info")
        return {"status": "error", "message": "Could not connect to database with provided info"}, 400
    
    # Initialize the ERP system
    erp_system = ERPSystem.create_erp_system(erp_type, database, db)
    if not erp_system: 
        logging.error("Chosen ERP system is not supported")
        return {"status": "error", "message": "Chosen ERP system is not supported"}, 400
    
    logging.info("Successfully stored metadata in local database")
    is_conn, msg = erp_system.validate_connection(), 200
    if not is_conn:
        logging.error("Could not connect to database with provided info")
        return {"status": "error", "message": "Could not connect to database with provided info"}, 400
    return msg, 200

def get_table_names():
    """
    Gets the names of all tables in the local database.

    Returns:
        list: A list of table names.
    """
    tables = Table.query.all()
    return [table.to_simple_dict() for table in tables]

def get_table_from_id(filter_id):
    """
    Gets the names of all tables in the local database that are related to the given table.

    Args:
        filter_id (int): The ID of the table to filter by.

    Returns:
        list: A list of table names.
    """
    table = Table.query.get(filter_id)
    if table is None:
        return {"status": "error", "message": "Table not found"}, 404
    
    # Query the table and limit the results
    
    return ERPSystem.instance.get_table_preview(table)

def get_supported_dbs():
    """
    Gets the names of all supported databases.

    Returns:
        list: A list of database names.
    """
    return DatabaseFactory.get_supported_dbs()
