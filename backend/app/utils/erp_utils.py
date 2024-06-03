import json
import uuid

import pandas as pd
from app.models.OCDM import Meta, ChangeLog, Table


def get_meta_tables():
    """
    Returns the meta table for the Oracle EBS ERP system.
    The meta table could be different for each ERP system.
    """
    return Meta.query.all()

def get_change_logs():
    """
    Returns the change log from the PO_HEADERS_ALL table in the Oracle EBS ERP system.
    """
    return ChangeLog.query.all()

def query_preview_from_df(table, num_rows=30, num_cols=15):
    """
    Formats the given table into the desired structure for the frontend.

    Args:
        table (pd.DataFrame): The table to format.
        num_rows (int): The number of rows to return.
        num_cols (int): The number of columns to return.

    Returns:
        dict: The formatted table.
    """
    
    # Get the column names from the table class
    headers = [{'text': column, 'value': column} for column in table.columns[:num_cols]]

    # Iterate over the rows to format them into the desired structure
    items = [{column: row[column] for column in table.columns[:num_cols]} for _, row in table.head(num_rows).iterrows()] 

    return {'headers': headers, 'items': items}

def get_entity_from_config(config, entity_name):
    """
    Returns the entities from the given configuration.
    """
    return [json.loads(meta[1]) for meta in config.items(entity_name)]

def check_changelog_exists(name):
    """
    Checks if a changelog with the given name exists in the local database.

    Args:
        name (str): The name of the changelog to check.

    Returns:
        bool: True if the changelog exists, False otherwise.
    """
    changelog = ChangeLog.query.filter_by(name=name).first()
    return changelog is not None

def check_meta_exists(name):
    """
    Checks if a meta table with the given name exists in the local database.

    Args:
        name (str): The name of the meta table to check.

    Returns:
        bool: True if the meta table exists, False otherwise.
    """
    meta = Meta.query.filter_by(name=name).first()
    return meta is not None    

def check_table_exists(table_name):
    """
    Checks if a table with the given name exists in the local database.

    Args:
        table_name (str): The name of the table to check.

    Returns:
        bool: True if the table exists, False otherwise.
    """
    table = Table.query.filter_by(table=table_name).first()
    return table is not None

def get_meta_by_name(name):
    """
    Returns the meta table with the given name from the local database.

    Args:
        name (str): The name of the meta table to return.

    Returns:
        Meta: The meta table with the given name.
    """
    return Meta.query.filter_by(name=name).first()

def group_events_by_date(events):
    """
    Groups and clusters events based on their timestamps and the object types they affect.
    Each event within 1 second of another is considered in the same group.

    Args:
        events (DataFrame): The events to group, each event is expected to have 'ocel_time' and 'object_type'.

    Returns:
        DataFrame: Categorized events with an additional 'ocel_id' column.
    """
    # Ensure ocel_time column is in datetime format and sort events
    events['ocel_time'] = pd.to_datetime(events['ocel_time'])
    events.sort_values(by='ocel_time', inplace=True)

    # Generate group identifiers based on time difference
    events['group_id'] = (events['ocel_time'].diff().dt.total_seconds() > 1).cumsum()

    # Assign a unique identifier for each group
    unique_ids = {idx: str(uuid.uuid4()) for idx in events['group_id'].unique()}
    events['ocel_id'] = events['group_id'].map(unique_ids)
    events.drop(columns='group_id', inplace=True)

    return events
