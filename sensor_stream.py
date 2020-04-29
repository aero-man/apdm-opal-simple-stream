'''
This class configures and gets data from the APDM Opal sensors
'''
import apdm
from time import time
from app_logger import AppLogger


logger = AppLogger(__name__)

class SensorStream:
    def __init__(self):
        self.context = None
        self.device_ids = []

    def start(self):
        '''
        Start the sensors. The intention is for the sensors to
        be started, then to run `sensors.get_next()` on a loop 
        to continuously get sensor data.

        Virtually all code in this function is APDM SDK example code
        '''
        try:
            num_aps = apdm.uintArray(1)
            apdm.apdm_ap_get_num_access_points_on_host1(num_aps)

            # Create sensor "context"
            self.context = apdm.apdm_ctx_allocate_new_context()
            if self.context == None:
                logger.logger.error("Unable to allocate new context")
                raise Exception("Unable to allocate new context")
            
            # Open access points
            open_access_points = apdm.apdm_ctx_open_all_access_points(self.context)
            if open_access_points != apdm.APDM_OK:
                logger.logger.error("Unable to open all access points")
                raise Exception("Unable to open all access points")
            
            # Sync sensors and access points together
            sync_records = apdm.apdm_ctx_sync_record_list_head(self.context)
            if sync_records != apdm.APDM_OK:
                logger.logger.error("Unable to sync record head list")
                raise Exception("Unable to sync record head list")
            
            # Get device IDs for all sensors currently active.
            num_sensors = apdm.uintArray(1)
            apdm.apdm_ctx_get_expected_number_of_sensors2(self.context, num_sensors)
            for i in range(num_sensors[0]):
                self.device_ids.append(apdm.apdm_ctx_get_device_id_by_index(self.context, i))
                
        except Exception as e:
            logger.logger.error("Access points and sensors could not be started: {0}".format(e))   

    def get_next(self):
        '''
        Get next record for each foot from the sensors (2 records total)
        Returns:
            A 2D list, one row for each active sensor. Each row has the following data:
                - Computer time in milliseconds
                - Unix time in milliseconds
                - Device/sensor serial number
                - Accelerometer X, Y, and Z
                - Gyroscope X, Y, and Z
                - Magnetometer X, Y, and Z
        NOTE: A record is not always returned as there may not be data available to 
              read each time if reading faster than the sampling rate
        '''
        raw_record = self._get_next_record_from_sensor()
        logger.logger.debug("Raw record received: {0}".format(raw_record))
        clean_record = self._raw_record_to_gyro_accel_and_mag(raw_record)
        logger.logger.debug("Clean record: {0}".format(clean_record))
        self._calc_sensor_latency(clean_record[0][0], clean_record[0][1]) # [0][0] = sensor timestamp
        return clean_record

    def stop(self):
        '''
        Stop data streaming
        '''
        apdm.apdm_ctx_disconnect(self.context) 
        apdm.apdm_ctx_free_context(self.context)

    def _get_next_record_from_sensor(self):
        '''
        Helper function to get next raw record from sensor
        '''
        return_code = apdm.apdm_ctx_get_next_access_point_record_list(self.context)
        if return_code != apdm.APDM_OK:
            if return_code == apdm.APDM_NO_MORE_DATA:
                logger.logger.warn("No more data available from sensors.")
            else:
                logger.logger.error("Error code received from APDM system: {0}".format(return_code))
            apdm.apdm_usleep(16666) # microseconds
        raw_record = apdm.apdm_record_t()
        return raw_record

    def _raw_record_to_gyro_accel_and_mag(self, raw_record):
        '''
        Helper function to format raw record into list of:
            - Unix time in milliseconds
            - Device/sensor serial number
            - Accelerometer X, Y, and Z
            - Gyroscope X, Y, and Z
            - Magnetometer X, Y, and Z
        '''
        sensor_data = []
        for device_id in self.device_ids:
            return_code = apdm.apdm_ctx_extract_data_by_device_id(self.context, device_id, raw_record)
            single_device_data = [
                        str(time()), # Computer's Unix time in milliseconds
                        str(raw_record.v2_sync_val64_us), # APDM sensors' Unix time in milliseconds
                        str(raw_record.device_info_serial_number),
                        str(raw_record.accl_x_axis_si),
                        str(raw_record.accl_y_axis_si),
                        str(raw_record.accl_z_axis_si),
                        str(raw_record.gyro_x_axis_si),
                        str(raw_record.gyro_y_axis_si),
                        str(raw_record.gyro_z_axis_si),
                        str(raw_record.mag_x_axis_si),
                        str(raw_record.mag_y_axis_si),
                        str(raw_record.mag_z_axis_si)]
            sensor_data.append(single_device_data)
        return sensor_data

    def _calc_sensor_latency(self, computer_timestamp, sensor_timestamp):
        '''
        Calculate latency for APDM Opal sensors in seconds
        '''
        sensor_latency = float(computer_timestamp) - float(sensor_timestamp)/1000000
        logger.logger.debug("Current sensor latency (s): {0}, Sensor Timestamp: {1}"
            .format(sensor_latency, sensor_timestamp))
        return sensor_latency
