'''
This class handles all database interactions.
'''

import settings
import sqlite3
from app_logger import AppLogger


logger = AppLogger(__name__)

class Database:
    def __init__(self):
        logger.logger.info("Creating database...")
        self.connection = sqlite3.connect(settings.DATABASE_NAME)
        self.cursor = self.connection.cursor()
        self.cursor.execute('''CREATE TABLE apdm_records
                               (computer_unix_time_ms int, sensor_unix_time_ms int, 
                               device_id int, accel_x real, accel_y real, accel_z real,
                               gyro_x real, gyro_y real, gyro_z real,
                               mag_x real, mag_y real, mag_z real)
                               ''')
        logger.logger.info("Database created")

    def add_row(self, data):
        '''
        Add a record of gait data to the DB

        Data gets padded with `0` values to match the number of columns in the DB
        '''
        logger.logger.debug("Adding row to database: {0}".format(data))
        padded_data = self._pad_data_with_zeros(data)
        self.cursor.execute('''INSERT INTO apdm_records
                               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                               ''', padded_data)
        self.connection.commit()

    def _pad_data_with_zeros(self, data):
        '''
        Helper function to pad row of gait data with `0` values to match # of DB columns.

        Function can accept any number of valid columns less than 11 and still return 11 columns total.
        '''
        return data + ([0] * (12-len(data)))

