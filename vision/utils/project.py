"""
Copy from Scrapy
"""
import os
import warnings
from importlib import import_module

from six.moves import cPickle as pickle

from vision.settings import Settings
from vision.utils.conf import closest_vision_cfg, init_env

ENVVAR = 'VISION_SETTINGS_MODULE'
DATADIR_CFG_SECTION = 'datadir'


def inside_project():
    vision_module = os.environ.get(ENVVAR)
    if vision_module is not None:
        try:
            import_module(vision_module)
        except ImportError as exc:
            warnings.warn("Cannot import vision settings module %s: %s" % (vision_module, exc))
        else:
            return True
    return bool(closest_vision_cfg())


def get_project_settings():
    if ENVVAR not in os.environ:
        project = os.environ.get('VISION_PROJECT', 'default')
        init_env(project)

    settings = Settings()
    settings_module_path = os.environ.get(ENVVAR)
    if settings_module_path:
        settings.setmodule(settings_module_path, priority='project')

    # XXX: remove this hack
    pickled_settings = os.environ.get("VISION_PICKLED_SETTINGS_TO_OVERRIDE")
    if pickled_settings:
        settings.setdict(pickle.loads(pickled_settings), priority='project')

    # XXX: deprecate and remove this functionality
    env_overrides = {k[7:]: v for k, v in os.environ.items() if
                     k.startswith('VISION_')}
    if env_overrides:
        settings.setdict(env_overrides, priority='project')

    return settings
