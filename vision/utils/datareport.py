"""
Copy from Scrapy
"""
import inspect
import logging

import six

from vision.datareport import DataReport

logger = logging.getLogger(__name__)


def iter_data_report_classes(module):
    """Return an iterator over all Data Report classes defined in the given module
    that can be instantiated (ie. which have name)
    """
    # singleton in vision.datareport.DataReport
    from vision.datareport import DataReport

    for obj in six.itervalues(vars(module)):
        if inspect.isclass(obj) and \
                issubclass(obj, DataReport) and \
                        obj.__module__ == module.__name__ and \
                getattr(obj, 'name', None):
            yield obj


class DefaultSpider(DataReport):
    name = 'default'
