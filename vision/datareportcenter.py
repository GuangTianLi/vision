import logging

import six
from zope.interface.verify import verifyClass, DoesNotImplement

from vision.interfaces import IDataReportLoader
from vision.settings import Settings
from vision.utils.log import LogCounterHandler, configure_logging, log_vision_info
from vision.utils.misc import load_object

logger = logging.getLogger(__name__)


class DataReportCenter(object):
    """
    This is a class to load DataReport by class's name
    """

    def __init__(self, settings=None):
        self.file_name = None
        if isinstance(settings, dict) or settings is None:
            settings = Settings(settings)
        self.settings = settings
        self.data_report_loader = _get_data_report_loader(settings)

        handler = LogCounterHandler(self, level=settings.get('LOG_LEVEL'))
        logging.root.addHandler(handler)
        # lambda is assigned to Crawler attribute because this way it is not
        # garbage collected after leaving __init__ scope
        self.__remove_handler = lambda: logging.root.removeHandler(handler)

        configure_logging(self.settings)
        log_vision_info(self.settings)

    def get_data_report(self, data_report):
        """
        Return a :class:`~vision.datareport.DataReport` object.

        """
        return self._create_data_report(data_report)

    def get_data_from_data_report(self, data_report):
        self.data_report = self.get_data_report(data_report)
        self.data_report.file_name = self.file_name
        self.file_dict = {}
        for data in self.data_report.make_data_from_db():
            csv_file_name = self.data_report.settings.get(
                "DATA_REPORT_FILE_NAME", self.data_report.settings.get(
                    "DATA_REPORT_CSV_FILE_NAME", self.data_report.name))
            svg_file_name = self.data_report.settings.get(
                "DATA_REPORT_FILE_NAME", self.data_report.settings.get(
                    "DATA_REPORT_SVG_FILE_NAME", self.data_report.name))
            self.csv_file = self.data_report.settings.get("DATA_REPORT_FILE_DIRECTORY_DEFAULT",
                                                          "") + csv_file_name + ".csv"
            self.svg_file = self.data_report.settings.get("DATA_REPORT_FILE_DIRECTORY_DEFAULT",
                                                          "") + svg_file_name + ".svg"

            self.file_dict[self.csv_file] = self.svg_file
            yield data

    def _create_data_report(self, data_report_cls):
        if isinstance(data_report_cls, six.string_types):
            data_report_cls = self.data_report_loader.load(data_report_cls)
        data_report_cls.update_settings(self.settings)
        return data_report_cls.from_data_report_center(self)


def _get_data_report_loader(settings):
    """ Get DataReportLoader instance from settings """
    cls_path = settings.get('DATA_REPORT_LOADER_CLASS')
    loader_cls = load_object(cls_path)
    try:
        verifyClass(IDataReportLoader, loader_cls)
    except DoesNotImplement:
        pass
    return loader_cls.from_settings(settings.frozencopy())
