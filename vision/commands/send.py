from vision.commands import VisionCommand
from vision.exceptions import UsageError
from vision.sender import SenderRunner
from vision.utils.conf import arglist_to_dict


class Command(VisionCommand):
    requires_project = True

    def syntax(self):
        return "[options] <data report>"

    def short_desc(self):
        return "send a data report by eamil"

    def add_options(self, parser):
        VisionCommand.add_options(self, parser)
        parser.add_option("-a", dest="spargs", action="append", default=[], metavar="NAME=VALUE",
                          help="set data report argument (may be repeated)")

    def process_options(self, args, opts):
        VisionCommand.process_options(self, args, opts)
        try:
            opts.spargs = arglist_to_dict(opts.spargs)
        except ValueError:
            raise UsageError("Invalid -a value, use -a NAME=VALUE", print_help=False)

    def run(self, args, opts):
        if len(args) < 1:
            raise UsageError()
        self.data_report_runner = SenderRunner(self.settings)

        for rname in args:
            self.data_report_runner.send(rname, **opts.spargs)
