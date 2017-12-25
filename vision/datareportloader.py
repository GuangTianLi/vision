# -*- coding: utf-8 -*-
"""
Copy from Scrapy
"""

from __future__ import absolute_import

from zope.interface import implementer

from vision.interfaces import IDataReportLoader
from vision.utils.datareport import iter_data_report_classes
from vision.utils.misc import walk_modules


@implementer(IDataReportLoader)
class DataReportLoader(object):
    """
    DataReportLoader is a class which locates and loads Data Report
    in a data report project.
    """

    def __init__(self, settings):
        self.data_report_modules = settings.getlist('DATA_REPORT_MODULES')
        self._data_report = {}
        self._load_all_data_report()

    def _load_data_report(self, module):
        for drcls in iter_data_report_classes(module):
            self._data_report[drcls.name] = drcls

    def _load_all_data_report(self):
        for name in self.data_report_modules:
            for module in walk_modules(name):
                self._load_data_report(module)

    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def load(self, data_report_name):
        """
        Return the Data Report class for the given spider name. If the spider
        name is not found, raise a KeyError.
        """

        try:
            return self._data_report[data_report_name]
        except KeyError:
            raise KeyError("Data report not found: {}".format(data_report_name))

    def list(self):
        """
        Return a list with the names of all data report available in the project.
        """
        return list(self._data_report.keys())
