'''
This class handles all database interactions.
'''

import settings
import sqlite3
from app_logger import AppLogger


logger = AppLogger(__name__)

class ApdmDatabase:
    def __init__(self):
        '''
        Connect to sensor database. Sqlite3 automatically creates a 
        DB on connection if one doesn't exist, so checking existence of
        tables themselves is necessary for proper functioning.
        '''
        logger.logger.info("Connecting to database `{0}`...".format(settings.DATABASE_NAME))
        self.connection = sqlite3.connect(settings.DATABASE_NAME)
        self.cursor = self.connection.cursor()
        logger.logger.info("Connected to database.")
        if not self._trial_tables_exist():
            logger.logger.info("Necessary tables do not exist. Creating tables...")
            self._create_trial_tables()
            logger.logger.info("Created tables for sensor data.")
            tables = self._get_table_names()
            logger.logger.info("Currently existing tables: {0}".format(tables))

    def add_new_trial(self, data):
        # Add new trial to the database
        logger.logger.debug("Adding new trial to database: {0}".format(data))
        self.cursor.execute("INSERT INTO trials VALUES (?,?,?)", data)
        self.connection.commit()

    def add_sensor_event_data(self, data):
        # Add a record of sensor data from a single sensor to the DB
        logger.logger.debug("Adding row to database: {0}".format(data))
        self.cursor.execute("INSERT INTO trial_data VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", data)
        self.connection.commit()

    def _trial_tables_exist(self):
        '''
        Check if the required tables for data collection exist.
        If `SELECT` from a table fails, then the table does not exist.
        '''
        try:
            self.cursor.execute("SELECT * FROM trials")
            self.cursor.execute("SELECT * FROM trial_data")
        except sqlite3.OperationalError as e:
            logger.logger.error(e)
            return False

    def _create_trial_tables(self):
        # Create tables for storing APDM sensor data
        try:
            self.cursor.execute('''CREATE TABLE trials 
                                   (trial_id int primary key, start_time int, 
                                   device_ids text)
                                   ''')
        except sqlite3.OperationalError as e:
            logger.logger.error(e)
        try:
            self.cursor.execute('''CREATE TABLE trial_data
                                   (trial_id int primary key, computer_timestamp int,
                                   sensor_timestamp int, sensor_id int, accel_x real, 
                                   accel_y real, accel_z real, gyro_x real, gyro_y real,
                                   gyro_z real, magnet_x real, magnet_y real, magnet_z real)
                                   ''')
        except sqlite3.OperationalError as e:
            logger.logger.error(e)

    def _get_table_names(self):
        # Get names of all tables in database
        result = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = result.fetchall()
        return tables


