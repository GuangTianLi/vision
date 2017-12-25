"""
This module contains the default values for all settings used by Vision.

"""


DATA_REPORT_LOADER_CLASS = 'vision.datareportloader.DataReportLoader'

# create SVG file (disabled by default)
SVG_FILE = False

# default use mysql
USE_MYSQL = True

# file decode(GBK by default)
FILE_DECODE = "GBK"

#Log
LOG_ENABLED = True
LOG_ENCODING = 'utf-8'
LOG_FORMATTER = 'scrapy.logformatter.LogFormatter'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'
LOG_STDOUT = False
LOG_LEVEL = 'DEBUG'
LOG_FILE = None

#server
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 10001

# file modes(w+ by default)
FILE_MODES = 'w+'
#1  :  bar see: http://pygal.org/en/stable/documentation/types/bar.html
#2  :  pie see: http://pygal.org/en/stable/documentation/types/pie.html
#
SVG_STYLE = 1