'''
APDM Opal Sensor Tool.

This tool simplifies configuration and streaming for APDM Opal wearable sensors.
APDM Opal wearable sensors are wireless, wearable sensors that track body movement
using an inertial measurement unit (IMU).

Usage:
  main.py configure
  main.py stream (--sql | --csv)
  
Options:
  -h --help     Show this screen.
  --sql         Write sensor data to a SQL database.
  --csv         Write sensor data to a CSV file.
'''
import csv
from app_logger import AppLogger
from database import Database
from docopt import docopt
from sensor_config import SensorConfig
from sensor_stream import SensorStream
from stream_csv_writer import StreamCsvWriter


logger = AppLogger(__name__)

def get_sensor_data_and_write_to_csv():
    logger.logger.info("Getting sensor data and writing to CSVs...")
    stream = SensorStream()
    stream.start()
    csv_writer = StreamCsvWriter()
    while True:
        try:
            sensor_data = stream.get_next()
            logger.logger.debug("Received sensor data: {0}".format(sensor_data))
            csv_writer.write(sensor_data)
        except Exception as e:
            logger.logger.error("Could not retrieve sensor data. Error: {0}"
                .format(e))

def get_sensor_data_and_write_to_sql():
    logger.logger.info("Getting sensor data and writing to SQL database...")
    stream = SensorStream()
    stream.start()
    db = Database()
    while True:
        try:
            all_sensors = stream.get_next()
            logger.logger.debug("Received sensor data: {0}".format(all_sensors))
        except Exception as e:
            logger.logger.error("Could not retrieve sensor data. Error: {0}"
                .format(e))
        try:
            logger.logger.info("Writing sensor data to SQL database...")
            for sensor in all_sensors:
                logger.logger.debug("Writing row of sensor data: {0}".format(sensor))
                db.add_row(sensor)
        except Exception as e:
            logger.logger.error("Could not write sensor data to database. Error: {0}".
                format(e))


def main(user_options):
    try:
        if(user_options["configure"]):
            SensorConfig.configure() # APDM sensors must be configured prior to streaming
            print("Remove the sensors from the docking station. Wait until the " +
                "sensors and the access point are all flashing green in unison " + 
                "before streaming.")
        elif(user_options["stream"]):
            if(user_options["--csv"]): # Stream data and write to a CSV
                get_sensor_data_and_write_to_csv()
            elif(user_options["--sql"]): # Stream data and write to SQL database
                get_sensor_data_and_write_to_sql()
        elif(user_options["visualize"]):
            pass
        else:
            logger.logger.error("Invalid menu choice from user. Args received: {0}".format(user_options))
            print("Error: Invalid menu choice from user. Check logfile for details.")
    except KeyboardInterrupt:
        print("Shutdown request. Exiting...")


if __name__ == '__main__':
    arguments = docopt(__doc__)
    main(arguments)

