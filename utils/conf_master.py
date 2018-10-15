"""
Configuration management utils.
# Usage example:
from wixcontrib.webapp.conf_master import config
settings = config({
    'default': {       # NOTE: this section is required
    },
    'production': {
    },
    'test': {
    },
    'patch': {
    }
})
# You need to specify APP_SETTINGS variable inside .yaml file in order to override setting for specific environment.
env_variables:
  APP_SETTINGS: 'production'
# You also could use APP_SETTINGS_OVERRIDE to temporary set up second level ov overriding.
env_variables:
  APP_SETTINGS: 'test'
  APP_SETTINGS_OVERRIDE: 'patch'
# override priority
1. APP_SETTINGS_OVERRIDE
2. APP_SETTINGS
3. 'default'
"""


import os
import json

from google.appengine.ext import ndb


class Setting(ndb.Expando):
    value = ndb.StringProperty(required=True)

    @property
    def name(self):
        return self.key.id()


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


def config(sets):
    settings = AttributeDict(sets['default'])

    for s in Setting.query().fetch():
        settings[s.name] = str(s.value)

    _env_id = os.getenv('APP_SETTINGS', None)
    if _env_id:
        settings.update(sets[_env_id])

    _env_over = os.getenv('APP_SETTINGS_OVERRIDE', None)
    if _env_over:
        settings.update(json.loads(_env_over))

    return settings
