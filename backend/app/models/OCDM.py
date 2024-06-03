from sqlalchemy import Sequence
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

event_changelog_relation = db.Table('event_changelog_relation',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id', ondelete="CASCADE"), primary_key=True),
    db.Column('change_log_id', db.Integer, db.ForeignKey('change_log.id', ondelete="CASCADE")),
)
event_object_relation = db.Table('event_object_relation',
    db.Column('event_id', db.Integer, db.ForeignKey('event.id', ondelete="CASCADE"), primary_key=True),
    db.Column('object_id', db.Integer, db.ForeignKey('object.id', ondelete="CASCADE"), primary_key=True)
)
object_object_relation = db.Table('object_object_relation',
    db.Column('source_id', db.Integer, db.ForeignKey('object.id', ondelete="CASCADE"), primary_key=True),
    db.Column('target_id', db.Integer, db.ForeignKey('object.id', ondelete="CASCADE"), primary_key=True)
)
process_object_relation = db.Table('process_object_relation',
    db.Column('process_id', db.Integer, db.ForeignKey('process.id', ondelete="CASCADE"), primary_key=True),
    db.Column('object_id', db.Integer, db.ForeignKey('object.id', ondelete="CASCADE"), primary_key=True)
)
object_table_relation = db.Table('object_table_relation',
    db.Column('tablet_id', db.Integer, db.ForeignKey('table.id', ondelete="CASCADE"), primary_key=True),
    db.Column('object_id', db.Integer, db.ForeignKey('object.id', ondelete="CASCADE"), primary_key=True)
)
table_meta_relation = db.Table('table_meta_relation',
    db.Column('table_id', db.Integer, db.ForeignKey('table.id', ondelete="CASCADE"), primary_key=True),
    db.Column('meta_id', db.Integer, db.ForeignKey('meta.id', ondelete="CASCADE"), primary_key=True)
)

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, Sequence('event_id_seq'), primary_key=True)
    name = db.Column(db.String, unique=True)
    event_id = db.Column(db.String)
    attributes = db.Column(db.String)
    condition = db.Column(db.String)

    log = db.relationship('ChangeLog', secondary=event_changelog_relation, backref='events')
    objects = db.relationship('Object', secondary=event_object_relation, backref='events')
    
    def __init__(self, name, event_id, attributes, condition):
        self.name = name
        self.event_id = event_id
        self.attributes = attributes
        self.condition = condition

    def update(self, data):
        self.name = data.get('name')
        self.event_id = data.get('event_id')
        self.attributes = data.get('attributes')
        self.condition = data.get('condition')

    @classmethod
    def from_dict(cls, data):
        name = data.get('name')
        event_id = data.get('event_id')
        attributes = data.get('attributes')
        condition = data.get('condition')
            
        return cls(name, event_id, attributes, condition)
    
    def to_dict(self):
        objs = [{'id': obj.id, 'name': obj.name} for obj in self.objects]
        logs = [{'id': log.id, 'name': log.name} for log in self.log]
        return {
            'id': self.id,
            'meta': {
                'name': self.name,
                'event_id': self.event_id,
                'attributes': self.attributes,
                'condition': self.condition,
                'objects': objs,
                'logs': logs
            }
        }
    
    def format_name(self):
        return "".join(word.capitalize() for word in self.name.split())
    
    def get_attributes(self):
        return self.attributes.split(',') if self.attributes else []
    
    def generate_create_table_sql(self):
        attributes = self.get_attributes()
        columns_definitions = [f"{attribute} TEXT" for attribute in attributes]
        
        # Only add a trailing comma if there are attributes to list.
        columns_definitions_str = ''
        if attributes:
            columns_definitions_str = ',\n    '.join(columns_definitions) + ',\n    '
    
        
        table_name = f"event_{self.format_name()}"
        create_table_query = (
            f"CREATE TABLE {table_name} (\n"
            f"    ocel_id TEXT PRIMARY KEY,\n"
            f"    ocel_time INTEGER NOT NULL,\n"
            f"    {columns_definitions_str}\n"
            f"    FOREIGN KEY (ocel_id) REFERENCES event(ocel_id)\n"
            f");"
        )
        
        return create_table_query

    def __repr__(self) -> str:
        return super().__repr__() + f" {self.name} {self.event_id} {self.object_id} {self.attributes} {self.condition}"
    

class Object(db.Model):
    __tablename__ = 'object'

    id = db.Column(db.Integer, Sequence('object_id_seq'), primary_key=True)
    name = db.Column(db.String, unique=True)
    object_id = db.Column(db.String)
    object_date = db.Column(db.String)
    attributes = db.Column(db.String)
    from_tables = db.Column(db.String)
    condition = db.Column(db.String)
    
    tables = db.relationship('Table', secondary=object_table_relation, backref='objects')
    related_objects = db.relationship(
        'Object',
        secondary=object_object_relation,
        primaryjoin=id==object_object_relation.c.source_id,
        secondaryjoin=id==object_object_relation.c.target_id,
        backref='related_to_objects'
    )
    
    def __init__(self, name, attributes, object_id, object_date, from_tables, condition):
        self.name = name
        self.object_id = object_id
        self.attributes = attributes
        self.object_date = object_date
        self.from_tables = from_tables
        self.condition = condition

    def update(self, data):
        self.name = data.get('name')
        self.object_id = data.get('object_id')
        attributes_timestamps = data.get('attributes')
        self.attributes = ",".join([att_ts['attribute_column'] for att_ts in attributes_timestamps])
        self.object_date = ",".join([att_ts['timestamp_column'] for att_ts in attributes_timestamps])
        self.from_tables = data.get('from_tables')
        self.condition = data.get('condition')

    @classmethod
    def from_dict(cls, data):
        name = data.get('name')
        attributes_timestamps = data.get('attributes')
        attributes = ",".join([att_ts['attribute_column'] for att_ts in attributes_timestamps])
        object_date = ",".join([att_ts['timestamp_column'] for att_ts in attributes_timestamps])
        object_id = data.get('object_id')
        from_tables = data.get('from_tables')
        condition = data.get('condition')
        return cls(name, attributes, object_id, object_date, from_tables, condition)

    def to_dict(self):
        objs = [{'id': obj.id, 'name': obj.name} for obj in self.related_objects]
        tables = [{'id': table.id, 'name': table.name} for table in self.tables]
        attributes_timestamps = [{"attribute_column": att, "timestamp_column": ts} for att, ts in zip(self.attributes.split(','), self.object_date.split(','))]
        return {
            'id': self.id,
            'meta': {
                'name': self.name,
                'attributes': attributes_timestamps,
                'object_id': self.object_id,
                'from_tables': self.from_tables,
                'condition': self.condition,
                'tables': tables,
                'objects': objs
            }
        }
    
    def format_name(self):
        return "".join(word.capitalize() for word in self.name.split())
    
    def get_attributes(self):
        atts = [self.object_id]
        atts += self.attributes.split(',') if self.attributes else []
        atts_without_tables = [att.split('.')[1] if '.' in att else att for att in atts]

        # check if 2 attributes have the same name, if they do, rename them from table.attribute to table_attribute
        atts_without_tables = [att if atts_without_tables.count(att) == 1 else f"{atts[atts_without_tables.index(att)].replace('.', '_')}" for att in atts_without_tables]
        atts_dict = dict(zip(atts, atts_without_tables))
        return atts_dict
    
    def get_attributes_without_timestamps(self):
        atts = self.get_attributes()
        atts_ts = ['']
        atts_ts += self.object_date.split(',') if self.object_date else []
        atts_dict = dict(zip(atts, atts_ts))
        atts_without_ts = [att.lower() for att, ts in atts_dict.items() if not ts or ts in ['NULL', 'None', '']]
        return atts_without_ts
    
    def generate_create_table_sql(self):
        attributes = self.get_attributes().values()
        columns_definitions = [f"{attribute} TEXT" for attribute in attributes]
        
        # Only add a trailing comma if there are attributes to list.
        columns_definitions_str = ''
        if attributes:
            columns_definitions_str = ',\n    '.join(columns_definitions) + ',\n    '
        
        table_name = f"object_{self.format_name()}"
        create_table_query = (
            f"CREATE TABLE {table_name} (\n"
            f"    ocel_id TEXT PRIMARY KEY,\n"
            f"    ocel_time INTEGER NOT NULL,\n"
            f"    ocel_changed_field TEXT,\n"
            f"    {columns_definitions_str}"
            f"\n    FOREIGN KEY (ocel_id) REFERENCES object(ocel_id)\n"
            f");"
        )
        
        return create_table_query
    
    def __repr__(self) -> str:
        return super().__repr__() + f" {self.name} {self.object_id} {self.object_date} {self.attributes} {self.from_tables} {self.condition}"
    
class Process(db.Model):
    __tablename__ = 'process'

    id = db.Column(db.Integer, Sequence('process_id_seq'), primary_key=True)
    name = db.Column(db.String, unique=True)

    objects = db.relationship('Object', secondary=process_object_relation, backref='processes')

    def __init__(self, name):
        self.name = name
        
    def update(self, data):
        self.name = data.get('name')

    @classmethod
    def from_dict(cls, data):
        name = data.get('name')
        return cls(name)
    
    def to_dict(self):
        objs = [{'id': obj.id, 'name': obj.name} for obj in self.objects]
        return {
            'id': self.id,
            'meta': {
                'name': self.name,
                'objects': objs
            }
        }
    
    @staticmethod
    def get_meta_entities_ddls():
        event_map_type = """CREATE TABLE event_map_type (
    ocel_type TEXT PRIMARY KEY,
    ocel_type_map TEXT
);"""

        event = """CREATE TABLE event (
    ocel_id TEXT PRIMARY KEY,
    ocel_type TEXT NOT NULL,
    FOREIGN KEY (ocel_type) REFERENCES event_map_type(ocel_type)
);"""

        object_map_type = """CREATE TABLE object_map_type (
    ocel_type TEXT PRIMARY KEY,
    ocel_type_map TEXT
);"""

        object = """CREATE TABLE object (
    ocel_id TEXT PRIMARY KEY,
    ocel_type TEXT NOT NULL,
    FOREIGN KEY (ocel_type) REFERENCES object_map_type(ocel_type)
);"""

        e2o = """CREATE TABLE event_object (
    ocel_event_id TEXT NOT NULL,
    ocel_object_id TEXT NOT NULL,
    ocel_qualifier TEXT,
    PRIMARY KEY (ocel_event_id, ocel_object_id, ocel_qualifier),
    FOREIGN KEY (ocel_event_id) REFERENCES event(ocel_id),
    FOREIGN KEY (ocel_object_id) REFERENCES object(ocel_id)
);"""

        o2o = """CREATE TABLE object_object (
    ocel_source_id TEXT NOT NULL,
    ocel_target_id TEXT NOT NULL,
    ocel_qualifier TEXT,
    PRIMARY KEY (ocel_source_id, ocel_target_id, ocel_qualifier),
    FOREIGN KEY (ocel_source_id) REFERENCES object(ocel_id),
    FOREIGN KEY (ocel_target_id) REFERENCES object(ocel_id)
);"""

        return [event, event_map_type, object, object_map_type, e2o, o2o]
    
    def __repr__(self) -> str:
        return super().__repr__() + f" {self.name}"

class Table(db.Model):
    __tablename__ = 'table'

    id = db.Column(db.Integer, Sequence('table_id_seq'), primary_key=True)
    owner = db.Column(db.String)
    table = db.Column(db.String, unique=True)
    meta_table = db.relationship('Meta', secondary=table_meta_relation, backref='tables')

    def __init__(self, table, owner):
        self.owner = owner
        self.table = table

    def update(self, data):
        self.owner = data.get('owner')
        self.table = data.get('table')

    def to_dict(self):
        metas = [{'id': meta.id, 'name': meta.name} for meta in self.meta_table]
        return {
            'id': self.id,
            'meta': {
                'owner': self.owner,
                'name': self.table,
                'metas': metas
            }
        }
    
    def to_simple_dict(self):
        return {
            'id': self.id,
            'meta': {
                'owner': self.owner,
                'name': self.table
            }
        }
    
    @classmethod
    def from_dict(cls, data):
        table = data.get('table')
        owner = data.get('owner')
        return cls(table, owner)

    def __repr__(self) -> str:
        return super().__repr__() + f" {self.table} {self.owner} {self.meta_table}"

class Meta(db.Model):
    __tablename__ = 'meta'

    id = db.Column(db.Integer, Sequence('meta_id_seq'), primary_key=True)
    name = db.Column(db.String, unique=True)
    source_table = db.Column(db.String)
    condition = db.Column(db.String)
    owner_column = db.Column(db.String)
    tables_column = db.Column(db.String)
    attributes = db.Column(db.String)

    def __init__(self, name, source_table, condition, owner_column, tables_column, attributes):
        self.name = name
        self.source_table = source_table
        self.condition = condition
        self.owner_column = owner_column
        self.tables_column = tables_column
        self.attributes = attributes

    def update(self, data):
        self.name = data.get('name')
        self.source_table = data.get('source_table')
        self.condition = data.get('condition')
        self.owner_column = data.get('owner_column')
        self.tables_column = data.get('tables_column')
        self.attributes = data.get('attributes')
    
    @classmethod
    def from_dict(cls, data):
        name = data.get('name')
        source_table = data.get('source_table')
        condition = data.get('condition')
        owner_column = data.get('owner_column')
        tables_column = data.get('tables_column')
        attributes = data.get('attributes')
        return cls(name, source_table, condition, owner_column, tables_column, attributes)
    
    def to_dict(self):
        return {
            'id': self.id,
            'meta': {
                'name': self.name,
                'source_table': self.source_table,
                'condition': self.condition,
                'owner_column': self.owner_column,
                'tables_column': self.tables_column,
                'attributes': self.attributes
            }
        }
    
    def __repr__(self) -> str:
        return super().__repr__() + f" {self.name} {self.source_table} {self.condition} {self.owner_column} {self.tables_column} {self.attributes}"

class ChangeLog(db.Model):
    __tablename__ = 'change_log'

    id = db.Column(db.Integer, Sequence('changelog_id_seq'), primary_key=True)
    name = db.Column(db.String, unique=True)
    owner = db.Column(db.String)
    table = db.Column(db.String)
    condition = db.Column(db.String)
    event_timestamp = db.Column(db.String)
    event_target = db.Column(db.String)
    attributes = db.Column(db.String)

    def __init__(self, name, owner ,table, condition, event_timestamp, event_target, attributes):
        self.name = name
        self.owner = owner
        self.table = table
        self.condition = condition
        self.event_timestamp = event_timestamp
        self.event_target = event_target
        self.attributes = attributes

    def to_dict(self):
        return {
            'id': self.id,
            'meta': {
                'name': self.name,
                'owner': self.owner,
                'table': self.table,
                'condition': self.condition,
                'event_timestamp': self.event_timestamp,
                'event_target': self.event_target,
                'attributes': self.attributes
            }
        }
    
    def update(self, data):
        self.name = data.get('name')
        self.owner = data.get('owner')
        self.table = data.get('table')
        self.condition = data.get('condition')
        self.event_timestamp = data.get('event_timestamp')
        self.event_target = data.get('event_target')
        self.attributes = data.get('attributes')
    
    @classmethod
    def from_dict(cls, data):
        name = data.get('name')
        owner = data.get('owner')
        table = data.get('table')
        condition = data.get('condition')
        event_timestamp = data.get('event_timestamp')
        event_target = data.get('event_target')
        attributes = data.get('attributes')
        return cls(name, owner, table, condition, event_timestamp, event_target, attributes)
    
    def __repr__(self) -> str:
        return super().__repr__() + f" {self.name} {self.owner} {self.table} {self.condition} {self.event_timestamp} {self.event_target} {self.attributes}"
