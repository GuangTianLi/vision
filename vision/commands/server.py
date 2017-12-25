from vision.commands import VisionCommand
from vision.exceptions import UsageError
from vision.server import Server
from vision.utils.conf import arglist_to_dict


class Command(VisionCommand):
    requires_project = True

    def syntax(self):
        return "[options]"

    def short_desc(self):
        return "run vision for server"

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
        self.server = Server(self.settings)
        self.server.start()
