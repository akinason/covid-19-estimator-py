import time
import logging
from flask import request, g


class __RequestFormatter(logging.Formatter):
    """
    Our request formatter to format request log to:
    POST    /api/v1/on-convid-19        200     20 ms
    POST    /api/v1/on-convid-19/xml    200     10 ms
    POST    /api/v1/on-convid-19/json   200     10 ms
    """
    def format(self, record):
        record.url_rule = request.url_rule
        record.method = request.method
        record.duration = "%.0f ms" % ((time.time() - g.start_time) * 1000)
        return super().format(record)


__formatter = __RequestFormatter('%(method)s   %(url_rule)s     %(message)s     %(duration)s')

__stream_handler = logging.StreamHandler()
__stream_handler.setFormatter(__formatter)

__file_handler = logging.FileHandler('src/access.log')
__file_handler.setFormatter(__formatter)
