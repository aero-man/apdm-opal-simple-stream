# About the CSV writing option

Each trial gets its own CSV (named `trial_<timestamp>.csv`), unlike the database, where all data for all trials lives in a single table.

### APDM Opal sensor data usage in Python
The APDM Opal sensor data comes in as a 2D array of string values. The overall array contains one array for each APDM Opal sensor. All timestamps and numbers are initially strings and must be converted to integers or doubles.

### Each CSV row contains
* `computer_unix_time_ms` The time that the computer received the APDM sensor data (milliseconds).
* `sensor_unix_time_us` The time that the APDM sensor produced the sensor data (microseconds).
* `sensor_id` The ID of the APDM sensor. A 3-6 digit integer.
* `accel_x` Accelerometer X from sensor (radians).
* `accel_y` Accelerometer Y from sensor (radians).
* `accel_z` Accelerometer Z from sensor (radians).
* `gyro_x` Gyroscope X from sensor (m/s^2).
* `gyro_y` Gyroscope Y from sensor (m/s^2).
* `gyro_z` Gyroscope Z from sensor (m/s^2).
* `magnet_x` Magnetometer X from sensor (microteslas).
* `magnet_y` Magnetometer Y from sensor (microteslas).
* `magnet_z` Magnetometer Z from sensor (microteslas).

### Example CSV row
`1596058691.56, 1596058691017290, 579, 1.226603365, 0.506366587, -9.689746785,   -0.002136296, 0.008801691, -0.008545183, -23.03440777, -5.664235115, -20.25405071`