from flask_cors import CORS
from app import db, create_app
from app.services.db_service import establish_connection
import logging
import os

log_dir = 'log'
log_file = 'app.log'
log_path = os.path.join(log_dir, log_file)

# Ensure the log directory exists
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(filename=log_path, filemode='w', level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = create_app()
CORS(app)

with app.app_context():
    db.create_all()
    logger.info("Created all tables")
    logger.info("Establishing connection to database")
    establish_connection()

if __name__ == '__main__':
    logger.info("Starting application")
    app.run(debug=True, use_reloader=False)
