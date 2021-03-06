"""
Copy from Scrapy
"""
"""
Vision core exceptions

These exceptions are documented in docs/topics/exceptions.rst. Please don't add
new exceptions here without documenting them there.
"""


# Commands

class NotConfigured(Exception):
    """Indicates a missing configuration situation"""
    pass


class NotData(Exception):
    """Indicates a missing configuration situation"""
    pass


class UsageError(Exception):
    """To indicate a command-line usage error"""

    def __init__(self, *a, **kw):
        self.print_help = kw.pop('print_help', True)
        super(UsageError, self).__init__(*a, **kw)
