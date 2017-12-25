"""
Copy from Scrapy
"""
import os
import sys

from six.moves.configparser import SafeConfigParser


def arglist_to_dict(arglist):
    """Convert a list of arguments like ['arg1=val1', 'arg2=val2', ...] to a
    dict
    """
    return dict(x.split('=', 1) for x in arglist)


def closest_vision_cfg(path='.', prevpath=None):
    """Return the path to the closest vision.cfg file by traversing the current
    directory and its parents
    """
    if path == prevpath:
        return ''
    path = os.path.abspath(path)
    cfgfile = os.path.join(path, 'vision.cfg')
    if os.path.exists(cfgfile):
        return cfgfile
    return closest_vision_cfg(os.path.dirname(path), path)


def init_env(project='default', set_syspath=True):
    """Initialize environment to use command-line tool from inside a project
    dir. This sets the Vision settings module and modifies the Python path to
    be able to locate the project module.
    """
    cfg = get_config()
    if cfg.has_option('settings', project):
        os.environ['VISION_SETTINGS_MODULE'] = cfg.get('settings', project)
    closest = closest_vision_cfg()
    if closest:
        projdir = os.path.dirname(closest)
        if set_syspath and projdir not in sys.path:
            sys.path.append(projdir)


def get_config(use_closest=True):
    """Get Vision config file as a SafeConfigParser"""
    sources = get_sources(use_closest)
    cfg = SafeConfigParser()
    cfg.read(sources)
    return cfg


def get_sources(use_closest=True):
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or \
                      os.path.expanduser('~/.config')
    sources = ['/etc/vision.cfg', r'c:\vision\vision.cfg',
               xdg_config_home + '/vision.cfg',
               os.path.expanduser('~/.vision.cfg')]
    if use_closest:
        sources.append(closest_vision_cfg())
    return sources
