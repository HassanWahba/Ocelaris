from flask import Flask
import configparser

from app.models.OCDM import db
from app.routes import db_connect, meta_tables, change_logs, processes, events, objects

config = configparser.ConfigParser()
config.read('config/connection.cfg')

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = config['LOCAL']['database_url']

    app.register_blueprint(db_connect.bp),
    app.register_blueprint(meta_tables.meta_tables)
    app.register_blueprint(change_logs.change_logs)
    app.register_blueprint(processes.processes)
    app.register_blueprint(events.events)
    app.register_blueprint(objects.objects)

    db.init_app(app)

    return app
