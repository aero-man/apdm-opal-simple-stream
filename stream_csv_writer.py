'''
This class handles the writing of APDM Opal sensor data to files.
'''

import csv
import settings
from app_logger import AppLogger
from datetime import datetime


logger = AppLogger(__name__)

class StreamCsvWriter:
    def __init__(self):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S") 
        csv_name = 'trial_{0}.csv'.format(timestamp) 
        file = open(csv_name, 'w')
        self.sensor_data_csv = csv.writer(file)
        self._write_header()

    def _write_header(self):
        column_names = [['computer_unix_time_ms','sensor_unix_time_ms', 'device_id', 
                        'accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z',
                        'mag_x', 'mag_y', 'mag_z']]
        self.write(column_names)

    def write(self, sensor_data):
        logger.logger.debug("Writing sensor data to CSV file: {0}".format(sensor_data))
        for device_data in sensor_data:
            self.sensor_data_csv.writerow(device_data)

