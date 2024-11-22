import pprint
import logging
import os


class AppException(Exception):
    pass


class System:
    @classmethod
    def is_logging(cls, min_level=logging.INFO):
        level = cls.get_log_level()

        if level > 0 and level <= min_level:
            return True

        return False

    @classmethod
    def get_log_level(cls):
        logger = logging.getLogger()
        level = logger.getEffectiveLevel()

        return level

    @classmethod
    def output_data(cls, title, data, level=logging.INFO, indent=2):
        formatted_data = pprint.pformat(data, indent=indent)
        cls.output_body(title, formatted_data, level=level)

    @classmethod
    def output_body(cls, title, data, level=logging.INFO):
        logging.log(level, title + ':\n' + data)

    @classmethod
    def line(cls, msg):
        print(msg)

    @classmethod
    def warn(cls, msg):
        print('\033[33m' + msg + '\033[0m')

    @classmethod
    def exit(cls, msg, error=0):
        if error == 0:
            cls.line(msg)
        else:
            cls.warn(msg)

        os._exit(error)
