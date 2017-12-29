"""
Base class for Vision DataReport
"""
from vision.utils.trackref import object_ref


class DataReport(object_ref):
    """Base class for Vision data report. All data report must inherit from this
    class.
    """

    name = None
    custom_settings = None

    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        self.use_mysql = False
        self.db_instance = None
        self.file_name = None

    @classmethod
    def from_data_report_center(cls, data_report_center, *args, **kwargs):
        data_report = cls(*args, **kwargs)
        data_report._set_data_report_center(data_report_center)
        return data_report

    def _set_data_report_center(self, data_report_center):
        self.data_report_center = data_report_center
        self.settings = data_report_center.settings

    def make_data_from_db(self):
        raise NotImplementedError

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(cls.custom_settings or {}, priority='spider')

    def __str__(self):
        return "<%s %r at 0x%0x>" % (type(self).__name__, self.name, id(self))

    __repr__ = __str__
