"""
Copy from Scrapy
"""
from __future__ import print_function

import cProfile
import inspect
import optparse
import sys

import pkg_resources

import vision
from vision.commands import VisionCommand
from vision.exceptions import UsageError
from vision.utils.misc import walk_modules
from vision.utils.project import inside_project, get_project_settings


def _iter_command_classes(module_name):
    # TODO: add `name` attribute to commands and and merge this function with
    # vision.utils.spider.iter_spider_classes
    for module in walk_modules(module_name):
        for obj in vars(module).values():
            if inspect.isclass(obj) and \
                    issubclass(obj, VisionCommand) and \
                            obj.__module__ == module.__name__:
                yield obj


def _get_commands_from_module(module, inproject):
    d = {}
    for cmd in _iter_command_classes(module):
        if inproject or not cmd.requires_project:
            cmdname = cmd.__module__.split('.')[-1]
            d[cmdname] = cmd()
    return d


def _get_commands_from_entry_points(inproject, group='vision.commands'):
    cmds = {}
    for entry_point in pkg_resources.iter_entry_points(group):
        obj = entry_point.load()
        if inspect.isclass(obj):
            cmds[entry_point.name] = obj()
        else:
            raise Exception("Invalid entry point %s" % entry_point.name)
    return cmds


def _get_commands_dict(settings, inproject):
    cmds = _get_commands_from_module('vision.commands', inproject)
    cmds.update(_get_commands_from_entry_points(inproject))
    cmds_module = settings['COMMANDS_MODULE']
    if cmds_module:
        cmds.update(_get_commands_from_module(cmds_module, inproject))
    return cmds


def _pop_command_name(argv):
    i = 0
    for arg in argv[1:]:
        if not arg.startswith('-'):
            del argv[i]
            return arg
        i += 1


def _print_header(settings, inproject):
    if inproject:
        print("Vision %s - project: %s\n" % (vision.__version__, \
                                             settings['BOT_NAME']))
    else:
        print("Vision %s - no active project\n" % vision.__version__)


def _print_commands(settings, inproject):
    _print_header(settings, inproject)
    print("Usage:")
    print("  Vision <command> [options] [args]\n")
    print("Available commands:")
    cmds = _get_commands_dict(settings, inproject)
    for cmdname, cmdclass in sorted(cmds.items()):
        print("  %-13s %s" % (cmdname, cmdclass.short_desc()))
    if not inproject:
        print()
        print("  [ more ]      More commands available when run from project directory")
    print()
    print('Use "vision <command> -h" to see more info about a command')


def _print_unknown_command(settings, cmdname, inproject):
    _print_header(settings, inproject)
    print("Unknown command: %s\n" % cmdname)
    print('Use "vision" to see available commands')


def _run_print_help(parser, func, *a, **kw):
    try:
        func(*a, **kw)
    except UsageError as e:
        if str(e):
            parser.error(str(e))
        if e.print_help:
            parser.print_help()
        sys.exit(2)


def execute(argv=None, settings=None):
    if argv is None:
        argv = sys.argv

    if settings is None:
        settings = get_project_settings()

    inproject = inside_project()
    cmds = _get_commands_dict(settings, inproject)
    cmdname = _pop_command_name(argv)
    parser = optparse.OptionParser(formatter=optparse.TitledHelpFormatter(), \
                                   conflict_handler='resolve')
    if not cmdname:
        _print_commands(settings, inproject)
        sys.exit(0)
    elif cmdname not in cmds:
        _print_unknown_command(settings, cmdname, inproject)
        sys.exit(2)

    cmd = cmds[cmdname]
    parser.usage = "vision %s %s" % (cmdname, cmd.syntax())
    parser.description = cmd.long_desc()
    settings.setdict(cmd.default_settings, priority='command')
    cmd.settings = settings
    cmd.add_options(parser)
    opts, args = parser.parse_args(args=argv[1:])
    _run_print_help(parser, cmd.process_options, args, opts)

    _run_print_help(parser, _run_command, cmd, args, opts)
    sys.exit(cmd.exitcode)


def _run_command(cmd, args, opts):
    if opts.profile:
        _run_command_profiled(cmd, args, opts)
    else:
        cmd.run(args, opts)


def _run_command_profiled(cmd, args, opts):
    if opts.profile:
        sys.stderr.write("vision: writing cProfile stats to %r\n" % opts.profile)
    loc = locals()
    p = cProfile.Profile()
    p.runctx('cmd.run(args, opts)', globals(), loc)
    if opts.profile:
        p.dump_stats(opts.profile)


if __name__ == '__main__':
    execute()
