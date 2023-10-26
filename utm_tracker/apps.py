from django.apps import AppConfig
from edx_django_utils.plugins import PluginURLs, PluginSettings

from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType

class UtmTrackerConfig(AppConfig):
    name = "utm_tracker"
    verbose_name = "UTM Session Tracker"
    # default_auto_field = "django.db.models.BigAutoField"

    plugin_app = {
        
        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.COMMON: {PluginSettings.RELATIVE_PATH: 'settings'},
            }
        }
    }

    def ready(self):
        from . import signals