import uuid
import pandas as pd
import logging
import configparser
from app.models.OCDM import ChangeLog, Meta, Process, Table, Object

from app.utils.erp_utils import check_changelog_exists, check_meta_exists, check_table_exists, get_entity_from_config, get_meta_by_name, get_meta_tables, group_events_by_date, query_preview_from_df
from app.utils.transform_utils import get_process_by_id


class ERPSystem:

    supported_systems = {
        "oracle-ebs": configparser.ConfigParser(),
        "sap-erp": None,
        "custom-erp": None
    }
    
    supported_systems["oracle-ebs"].read('config/erp_systems/oracle_ebs.cfg')

    instance = None

    @classmethod
    def create_erp_system(cls, system, database, internal_db):
        if system in cls.supported_systems:
            cls.instance = cls(database, internal_db, cls.supported_systems[system])
            return cls.instance
        else:
            return None
        
    def __init__(self, database, internal_db, config):
        self.logger = logging.getLogger(__name__)
        self.database = database
        self.internal_db = internal_db
        if config:
            self.config = config
            self.load_all()

    def add_entity(self, entity):
        self.internal_db.session.add(entity)
        self.internal_db.session.commit()

    def remove_entity(self, entity):
        self.internal_db.session.delete(entity)
        self.internal_db.session.commit()

    def load_metas(self):
        """
        Load all meta tables known from Oracle EBS ERP system.
        """
        for dic in get_entity_from_config(self.config, 'META'):
            if check_meta_exists(dic['name']):
                continue
            self.add_entity(Meta.from_dict(dic))

    def load_tables(self):
        """
        Load all tables known from Oracle EBS ERP system.
        """
        for _, row in self.get_tables().iterrows():
            table = row['table_name']
            if check_table_exists(table):
                continue
            new_table = Table(table=table, owner=row['owner'])
            meta_table = get_meta_by_name(row['meta_table_name'])
            if meta_table is not None:
                new_table.meta_table.append(meta_table)
                
            self.add_entity(new_table)

    def load_change_logs(self):
        """
        Load all change logs known from Oracle EBS ERP system.
        """
        for dic in get_entity_from_config(self.config, 'CHANGELOG'):
            if check_changelog_exists(dic['name']):
                continue
            new_change_log = ChangeLog.from_dict(dic)
            self.add_entity(new_change_log)

    def load_saved_objects(self):
        """
        Load all saved objects from the internal database.
        """
        pass

    def load_saved_events(self):
        pass

    def load_saved_processes(self):
        pass

    def load_all(self):
        """
        Load all metadata from the Oracle EBS ERP system.
        """
        self.load_metas()
        self.load_tables()
        self.load_change_logs()
        self.load_saved_objects()
        self.load_saved_events()
        self.load_saved_processes()

    def validate_connection(self):
        try:
            is_conn, msg = self.database.validate_connection()
            if not is_conn:
                self.logger.error(msg)
                return False, msg
            self.logger.info("Connection to database validated")
            return True, self.database.get_connection_info()
        except Exception as e:
            self.logger.error("Could not connect to database with provided info")
            self.logger.error(f"Exception: {str(e)}")
            return False, None

    def get_tables(self):
        """
        Returns all tables in the Oracle EBS ERP system by executing a query on the meta table.
        """
        all_tables = pd.DataFrame()

        for meta_table in get_meta_tables():
            atts = ", " + meta_table.attributes if meta_table.attributes != '' else ''
            select_clause = meta_table.tables_column + ", " + meta_table.owner_column + atts

            query_result, is_success = self.database.execute_query(select_=select_clause, from_=meta_table.source_table, where_=meta_table.condition)
            if not is_success:
                self.logger.error(f'Failed to execute query: {query_result}')
                return query_result
            
            # Add a column with constant value equal to meta_table_name
            query_result['meta_table_name'] = meta_table.name
            all_tables = pd.concat([all_tables, query_result], ignore_index=True)

        self.logger.info(f'Table query executed successfully')
        return all_tables

    def get_table_preview(self, table):
        """
        Returns a preview of the table with the given name.

        Args:
            table (Table): The table to return a preview of.

        Returns:
            dict: A dictionary containing the id, meta and preview of the table.
        """
        from_clause = table.owner + "." + table.table if table.owner is not None and table.owner != '' else table.table
        self.logger.info(f'Executing query on table: {from_clause}')

        content, is_success = self.database.execute_query(select_='*', from_=from_clause, limit_=20)
        
        preview = query_preview_from_df(content.astype(str)) if is_success else {"status": "error", "message": content}
        
        res = table.to_dict()
        res['preview'] = preview
        return res
    
    def get_meta_table_preview(self, table):
        """
        Returns a preview of the table with the given name.
        """
        select_clause = table.owner_column + ", " + table.tables_column
        content, is_success = self.database.execute_query(select_=select_clause, from_=table.source_table, where_=table.condition, limit_=20)
        
        preview = query_preview_from_df(content) if is_success else {"status": "error", "message": content}
        
        res = table.to_dict()
        res['preview'] = preview
        return res
    
    def get_change_log_preview(self, change_log):
        """
        Returns a preview of the given change log.

        Args:
            change_log (ChangeLog): The change log to return a preview of.

        Returns:
            dict: A dictionary containing the id, meta and preview of the change log.
        """
        atts = ", " + change_log.attributes if change_log.attributes and change_log.attributes != '' else ''
        select_clause = change_log.event_target + ", " + change_log.event_timestamp + atts

        from_clause = change_log.owner + "." + change_log.table if change_log.owner is not None and change_log.owner != '' else change_log.table
        content, is_success = self.database.execute_query(select_=select_clause, from_=from_clause, where_=change_log.condition, limit_=20)
        
        preview = query_preview_from_df(content) if is_success else {"status": "error", "message": content}
        res = change_log.to_dict()
        res['preview'] = preview
        return res
    
    def get_event_preview(self, event):
        """
        Returns a preview of the given event.

        Args:
            event (Event): The event to return a preview of.

        Returns:
            dict: A dictionary containing the id, meta and preview of the event.
        """
        content, is_success = self.get_event_df(event, limit=20)
        
        preview = query_preview_from_df(content) if is_success else {"status": "error", "message": content}
        res = event.to_dict()
        res['preview'] = preview
        return res
    
    def get_event_df(self, event, limit=None):
        """
        Returns a preview of the given event.

        Args:
            event (Event): The event to return a preview of.

        Returns:
            dict: A dictionary containing the id, meta and preview of the event.
        """
        if len(event.log) == 0:
            content = {"status": "error", "message": "Change log not found"}, 404
        
        change_log = event.log[0]
        if change_log is None:
            content = {"status": "error", "message": "Change log not found"}, 404
            is_success = False
            return content, is_success
        else:
            from_clause = change_log.owner + "." + change_log.table if change_log.owner is not None and change_log.owner != '' else change_log.table
            select_clause = f"{change_log.event_target} as object_id, {change_log.event_timestamp} as ocel_time"
            if event.event_id:
                select_clause += ", " + event.event_id
            if change_log.attributes and change_log.attributes != '':
                select_clause += ", " + change_log.attributes

            if event.condition and event.condition != '':
                where_clause = event.condition
            else:
                where_clause = "1=1"

            content, is_success = self.database.execute_query(select_=select_clause, from_=from_clause, where_=where_clause, limit_=limit)
            return content, is_success
        
    def get_event_populate_sql_query(self, event, obj_dfs):
        """
        Returns the SQL query to populate the given event.
        """
        content, is_success = self.get_event_df(event)
        if not is_success:
            return content
        df = self.assign_objects_to_object_ids(content, event.objects, obj_dfs)
        df = df.dropna(subset=['obj_name'])
        df = df.drop(columns=['obj_name'])
        if not event.event_id or event.event_id == '':
            df = group_events_by_date(df)

        insert_event_map = f"""INSERT INTO event_map_type (ocel_type, ocel_type_map) VALUES ('{event.name}', '{event.format_name()}');"""

        return insert_event_map, df

    def assign_objects_to_object_ids(self, df, objs, obj_dfs):
        """
        Assigns objects to object ids in the given dataframe.
        """
        for obj in objs:
            obj_table_name = f'object_{obj.format_name()}'
            # find df with the same name as the object. don't use next
            for df_obj in obj_dfs:
                if df_obj.name.startswith(obj_table_name):
                    df_obj_tmp = df_obj[[obj.object_id.split('.')[-1].lower(), 'ocel_id']
                                        ].rename(columns={obj.object_id.split('.')[-1].lower(): 'object_id', 'ocel_id': 'ocel_object_id'})
                    df = df.merge(df_obj_tmp, on='object_id', how='left')
                    break
            
            df['obj_name'] = obj.name
        df = df.dropna(subset=['ocel_object_id'])
        return df
    
    def get_object_preview(self, object):
        """
        Returns a preview of the given object.

        Args:
            object (Object): The object to return a preview of.

        Returns:
            dict: A dictionary containing the id, meta and preview of the object.
        """
        object_date_non_empty = ','.join(list(set(filter(None, object.object_date.split(',')))))
        if object_date_non_empty and object_date_non_empty != '':
            object_date_non_empty += ', '
        content, is_success = self.database.execute_query(select_="DISTINCT " + object.object_id + ", "  + object_date_non_empty + object.attributes, from_=object.from_tables, where_=object.condition, limit_=20)

        preview = query_preview_from_df(content.astype(str)) if is_success else {"status": "error", "message": content}
        res = object.to_dict()
        res['preview'] = preview
        return res
    
    def get_object_populate_sql_query(self, object):
        """
        Returns the SQL query to populate the given object.
        """
        atts = object.get_attributes()
        condition = object.condition if object.condition and object.condition != '' else '1=1'
        atts_ts = ['']
        atts_ts += object.object_date.split(',') if object.object_date else []
        atts_dict = dict(zip(atts, atts_ts))

        insert_object_map = f"""INSERT INTO object_map_type (ocel_type, ocel_type_map) VALUES ('{object.name}', '{object.format_name()}');"""

        atts_without_ts = [att for att, ts in atts_dict.items() if not ts or ts in ['NULL', 'None', '']]
        atts_with_ts = {att : ts for att, ts in atts_dict.items() if ts and ts not in ['NULL', 'None', '']}

        data_query = f"""SELECT DISTINCT {', '.join(atts_without_ts)} FROM {object.from_tables} WHERE {condition}"""
        default_df, is_success = self.database.execute_custom_query(data_query)
        default_df['changed_field'] = ''
        if not is_success:
            return default_df
        dataframes = []
        for att, ts in atts_with_ts.items():

            q = f"""SELECT DISTINCT {object.object_id}, '{att.split('.')[-1].lower()}' AS changed_field, {att.split('.')[-1].lower()}, {ts} AS ocel_time FROM {object.from_tables} WHERE {condition} AND {att} IS NOT NULL ORDER BY {object.object_id}, {ts}"""
            df, is_success = self.database.execute_custom_query(q)
            if not is_success:
                return df
            df["prev_value"] = df.groupby(object.object_id.split('.')[-1].lower())[att.split('.')[-1].lower()].shift(1)
            df.loc[df["prev_value"].isna(), "changed_field"] = ''
            # drop rows where prev_value equals to attribute_value
            df = df[df["prev_value"] != df[att.split('.')[-1].lower()]]
            df = df.drop(columns=["prev_value"])
            df.name = att.split('.')[-1].lower()
            dataframes.append(df)

        # join the dataframes
        df = default_df
        changed_fields = pd.DataFrame()
        for d in dataframes:
            if d.empty:
                continue
            changed_df = d[d["changed_field"] != '']
            changed_fields = pd.concat([changed_fields, changed_df], ignore_index=True)
            d = d[d["changed_field"] == '']
            if d.empty:
                continue
            d.drop(columns=["changed_field", "ocel_time"], inplace=True)
            df = df.merge(d, on=[atts[object.object_id].lower()], how="left", suffixes=('', '_y'))
            for col in df.columns:
                if not col.endswith("_y"):
                    continue
                if col.startswith(atts[object.object_id].lower()):
                    df = df.drop(columns=col)
                else:
                    df = df.rename(columns={col: col[:-2]})
        
        df = pd.concat([df, changed_fields], ignore_index=True)
        
        df['ocel_id'] = df[atts[object.object_id].lower()].apply(lambda x: str(uuid.uuid4()))

        df = df.dropna(subset=[atts[object.object_id].lower()])

        # Get relations between objects
        objs = []
        for obj in object.related_objects:

            obj_atts = [attr.lower().split('.')[-1].split(' as ')[-1] for attr in obj.get_attributes_without_timestamps()]
            object_atts = [attr.lower().split('.')[-1].split(' as ')[-1] for attr in object.get_attributes_without_timestamps()]

            # get the common attributes between the two objects
            common_atts = list(set(obj_atts) & set(object_atts))
            if len(common_atts) == 0:
                continue
            elif len(common_atts) > 1:
                # check if the common attributes are the object id of one of the objects
                obj_id_formatted = obj.object_id.lower().split('.')[-1].split(' as ')[-1]
                object_id_formatted = object.object_id.lower().split('.')[-1].split(' as ')[-1]
                if obj_id_formatted in common_atts:
                    objs += [f'{object.name}#+#{obj.name}#+#{obj_id_formatted}#+#remove_source_column']
                elif object_id_formatted in common_atts:
                    objs += [f'{object.name}#+#{obj.name}#+#{object_id_formatted}#+#remove_target_column']
                
                # check if one of the common attributes contains the string 'id'
                else:
                    for att in common_atts:
                        if 'id' in att.lower():
                            objs += [f'{object.name}#+#{obj.name}#+#{att}#+#remove_both_columns']
                            break
            else:
                common_att = common_atts[0]
                if object.object_id.lower().split('.')[-1].split(' as ')[-1] == common_att:
                    objs += [f'{object.name}#+#{obj.name}#+#{common_att}#+#remove_source_column']
                elif obj.object_id.lower().split('.')[-1].split(' as ')[-1] == common_att:
                    objs += [f'{object.name}#+#{obj.name}#+#{common_att}#+#remove_target_column']
                else:
                    objs += [f'{object.name}#+#{obj.name}#+#{common_att}#+#remove_both_columns']
        return insert_object_map, df, objs

    def get_process_info(self, process):
        """
        Returns the info of the process with the given id.
        
        Args:
            process_id (int): The id of the process to return the info of.

        Returns:
            dict: A dictionary containing the id, meta and preview of the process.
        """
        if process is None:
            return {"status": "error", "message": "Process not found"}, 404
        
        return process.to_dict()
    
    def extract_ocel_sql_query(self, process_id):
        """
        Extracts the OCEL of the process from the ERP system.
        """
        process = get_process_by_id(process_id)
        if process is None:
            raise Exception("Process ID was not found")
        
        objs = process.objects
        if len(objs) == 0:
            raise Exception("No objects were found")
        
        events = []
        for obj in objs:
            events.extend(obj.events)
        
        if len(events) == 0:
            raise Exception("No events were found")
        
        ddl_queries = Process.get_meta_entities_ddls()
        # ddl_queries.extend([obj.generate_create_table_sql() for obj in objs])
        # ddl_queries.extend([event.generate_create_table_sql() for event in events])
        ddl_queries_str = "\n\n".join(ddl_queries)

        self.logger.info("OCEL DDLs created successfully for process id: " + str(process_id))
        self.logger.debug(ddl_queries_str)

        dfs = []
        dml_queries = []
        obj_relations = []
        for obj in objs:
            insert_object_map, df, obj_relation = self.get_object_populate_sql_query(obj)
            if obj_relation:
                obj_relations += obj_relation

            dml_queries += [insert_object_map]
            df.name = f"object_{obj.format_name()}+{obj.name}"
            dfs.append(df)

        o2o_relations = pd.DataFrame()
        for rel in obj_relations:
            source_object_name, target_object_name, common_att, removal_msg = rel.split('#+#')
            
            source_object = [df for df in dfs if df.name.endswith(source_object_name)][0]
            source_object_df = source_object[['ocel_id', common_att]].copy()
            source_object_df.rename(columns={'ocel_id': 'ocel_source_id'}, inplace=True)

            target_object = [df for df in dfs if df.name.endswith(target_object_name)][0]
            target_object_df = target_object[['ocel_id', common_att]].copy()
            target_object_df.rename(columns={'ocel_id': 'ocel_target_id'}, inplace=True)

            if removal_msg == 'remove_source_column' or removal_msg == 'remove_both_columns':
                source_object.drop(columns=[common_att], inplace=True)
                source_object.drop_duplicates(inplace=True)

            if removal_msg == 'remove_target_column' or removal_msg == 'remove_both_columns':
                target_object.drop(columns=[common_att], inplace=True)
                target_object.drop_duplicates(inplace=True)

            # merge the two dataframes on the common attribute keeping the ids
            df = source_object_df.merge(target_object_df, on=common_att, how='inner')
            df = df.dropna(subset=['ocel_source_id', 'ocel_target_id'])
            df = df.drop(columns=[common_att])
            df = df.drop_duplicates()

            df['ocel_qualifier'] = f"{source_object_name} relates to {target_object_name}"
            o2o_relations = pd.concat([o2o_relations, df], ignore_index=True)
    
        for event in events:
            insert_event_map, df = self.get_event_populate_sql_query(event, dfs.copy())
            dml_queries.append(insert_event_map)
            df.name = f"event_{event.format_name()}+{event.name}"
            dfs.append(df)

        dml_queries_str = "\n\n".join(dml_queries)

        self.logger.info("OCEL DMLs created successfully for process id: " + str(process_id))
        self.logger.debug(dml_queries_str)

        return ddl_queries_str + dml_queries_str, dfs, o2o_relations
