'''
APDM Opal Simple Streaming Tool.

This is a barebones tool to record data from APDM Opal sensors
to a CSV file. APDM Opal sensors are radio-frequency sensors 
with an on-board inertial measurement unit (IMU). This tool 
collects and stores the gyroscope, accelerometer, and magnetometer 
data from these sensors.

NOTE:
  The `configure` command must be run before you can `stream`.
  See official documentation from APDM's SDK for more setup info.

Usage:
  main.py configure
  main.py stream
'''
import sys
import csv
from app_logger import AppLogger
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

def main(user_option):
    try:
        if user_option == "configure":
            SensorConfig.configure() # APDM sensors must be configured prior to streaming
            print("Remove the sensors from the docking station. Wait until the " +
                "sensors and the access point are all flashing green in unison " + 
                "before streaming.")
        elif user_option == "stream":
            get_sensor_data_and_write_to_csv()
        else:
            logger.logger.error("Invalid menu choice from user. Args received: {0}".format(user_options))
            print("Error: Invalid menu choice from user. Check logfile for details.")
    except KeyboardInterrupt:
        print("Shutdown request. Exiting...")

if __name__ == '__main__':
    user_option = sys.argv[1]
    if user_option == "configure" or user_option == "stream":
        main(user_option)
    else:
        logger.logger.error("Error: command `{0}` not recognized.".format(user_option))
        print(__doc__)

