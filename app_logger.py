'''
Write logs to file specified in `settings.py`
'''
import logging
import settings


class AppLogger():
    def __init__(self, module_name):
        self.logger = logging.getLogger(module_name)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(settings.MAIN_LOG_FILENAME)
        fh.setLevel(logging.DEBUG)
        sh = logging.StreamHandler()
        sh.setLevel(logging.INFO)
        logfile_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        user_facing_formatter = logging.Formatter('%(message)s')
        fh.setFormatter(logfile_formatter)
        sh.setFormatter(user_facing_formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

