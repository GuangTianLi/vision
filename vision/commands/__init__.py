"""
Copy from Scrapy
Base class for Vision commands
"""
import os
from optparse import OptionGroup


from vision.utils.conf import arglist_to_dict
from vision.exceptions import UsageError


class VisionCommand(object):

    requires_project = False
    data_report_process = None
    # default settings to be used for this command instead of global defaults
    default_settings = {}

    exitcode = 0

    def __init__(self):
        self.settings = None  # set in vision.cmdline

    def set_crawler(self, crawler):
        assert not hasattr(self, '_crawler'), "crawler already set"
        self._crawler = crawler

    def syntax(self):
        """
        Command syntax (preferably one-line). Do not include command name.
        """
        return ""

    def short_desc(self):
        """
        A short description of the command
        """
        return ""

    def long_desc(self):
        """A long description of the command. Return short description when not
        available. It cannot contain newlines, since contents will be formatted
        by optparser which removes newlines and wraps text.
        """
        return self.short_desc()

    def help(self):
        """An extensive help for the command. It will be shown when using the
        "help" command. It can contain newlines, since not post-formatting will
        be applied to its contents.
        """
        return self.long_desc()

    def add_options(self, parser):
        """
        Populate option parse with options available for this command
        """
        group = OptionGroup(parser, "Global Options")
        group.add_option("--profile", metavar="FILE", default=None,
            help="write python cProfile stats to FILE")
        group.add_option("-s", "--set", action="append", default=[], metavar="NAME=VALUE",
            help="set/override setting (may be repeated)")

        parser.add_option_group(group)

    def process_options(self, args, opts):
        try:
            self.settings.setdict(arglist_to_dict(opts.set),
                                  priority='cmdline')
        except ValueError:
            raise UsageError("Invalid -s value, use -s NAME=VALUE", print_help=False)



    def run(self, args, opts):
        """
        Entry point for running commands
        """
        raise NotImplementedError
