# About the database

This database stores data from APDM OPal wearable sensors. Data includes accelerometer, gyroscope, and magnetometer data from multiple APDM Opal sensors. Each time the program is run, a new trial with a new `trial_id` is started.

### APDM Opal sensor data usage in Python
The APDM Opal sensor data comes in as a 2D array of string values. The overall array contains one array for each APDM Opal sensor. All timestamps and numbers are initially strings and must be converted to integers or doubles.

### Tables
* `trials`
* `trial_data`

### `trials` table
* `trial_id` ID of the recording trial, AKA any new recording session of the sensors (integer)
* `start_time` Timestamp from when recording started (unix time millseconds)
* `device_ids` Device IDs from all APDM Opal sensors involved in this trial (Array of comma-delimited integers as a single string)

### `trial_data` table
* `trial_id` ID of the recording trial, matches `trial_id` in `trials` table
* `computer_timestamp` Time that the computer received this row of data from the APDM sensors (unix time milliseconds)
* `sensor_timestamp` Time that the APDM Opal sensor created/recorded the row of data (unix time microseconds)
* `sensor_id` ID of the APDM sensor, as given by the manufacturer (3-6 digit integer)
* `accel_x` Accelerometer X from sensor (radians).
* `accel_y` Accelerometer Y from sensor (radians).
* `accel_z` Accelerometer Z from sensor (radians).
* `gyro_x` Gyroscope X (m/s^2)
* `gyro_y` Gyroscope Y (m/s^2)
* `gyro_z` Gyroscope Z (m/s^2)
* `magnet_x` Magnetometer X from sensor (microteslas).
* `magnet_y` Magnetometer Y from sensor (microteslas).
* `magnet_z` Magnetometer Z from sensor (microteslas).