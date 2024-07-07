from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import text
import os
import logging

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from routes import *

if __name__ == '__main__':
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Check database connection
    try:
        with app.app_context():
            # Perform a simple query to test the database connection
            result = db.session.execute(text('SELECT 1'))
            # Log the result
            logger.info('Database connected: %s', result.fetchone())
    except Exception as e:
        logger.error('Database connection failed: %s', e)
    
    app.run(debug=True)
