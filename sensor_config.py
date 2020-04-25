'''
This is the example code from APDM's Python SDK 
with some settings and logging features added
'''
import apdm
import settings
from app_logger import AppLogger


logger = AppLogger(__name__)

class SensorConfig:
    @staticmethod
    def configure():
        context = apdm.apdm_ctx_allocate_new_context()
        try:
            apdm.apdm_ctx_open_all_access_points(context)
            streaming_config = apdm.apdm_streaming_config_t()
            apdm.apdm_init_streaming_config(streaming_config)
            streaming_config.enable_accel = settings.ENABLE_ACCEL
            streaming_config.enable_gyro = settings.ENABLE_GYRO
            streaming_config.enable_mag = settings.ENABLE_MAG
            streaming_config.wireless_channel_number = settings.WIRELESS_CHANNEL
            streaming_config.output_rate_hz = settings.SENSOR_OUTPUT_RATE_HZ
            r = apdm.apdm_ctx_autoconfigure_devices_and_accesspoint_streaming(context, streaming_config)
            if r != apdm.APDM_OK:
                error_msg = "Unable to autoconfigure system: {0}".format(apdm.apdm_strerror(r))
                logger.logger.error(error_msg)
                raise Exception(error_msg)
        finally:
            apdm.apdm_ctx_disconnect(context) 
            apdm.apdm_ctx_free_context(context)

