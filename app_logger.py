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
        sh.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)

