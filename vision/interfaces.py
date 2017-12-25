"""
Copy from Scrapy
"""
from zope.interface import Interface

class IDataReportLoader(Interface):

    def from_settings(settings):
        """Return an instance of the class for the given settings"""

    def load(data_report_name):
        """Return the Spider class for the given data report name. If the data report
        name is not found, it must raise a KeyError."""

    def list():
        """Return a list with the names of all data reports available in the
        project"""


# IDataReportManager is deprecated, don't use it!
# An alias is kept for backwards compatibility.
IDataReportManager = IDataReportLoader
