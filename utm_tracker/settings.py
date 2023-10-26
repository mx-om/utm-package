from django.conf import settings



UTM_TRACKER_CUSTOM_TAGS = ["tag1", "tag2"]
CUSTOM_TAGS = UTM_TRACKER_CUSTOM_TAGS
# list of custom args to extract from the querystring

def plugin_settings(settings):
    """
    Common settings for Announcements
    .. toggle_name: FEATURES['ENABLE_ANNOUNCEMENTS']
    .. toggle_implementation: SettingDictToggle
    .. toggle_default: False
    .. toggle_description: This feature can be enabled to show system wide announcements
       on the sidebar of the learner dashboard. Announcements can be created by Global Staff
       users on maintenance dashboard of studio. Maintenance dashboard can accessed at
       https://{studio.domain}/maintenance
    .. toggle_warnings: TinyMCE is needed to show an editor in the studio.
    .. toggle_use_cases: open_edx
    .. toggle_creation_date: 2017-11-08
    .. toggle_tickets: https://github.com/edx/edx-platform/pull/16496
    """
    #settings.INSTALLED_APPS.append("mx_catalog")
    
    
    UTM_MIDDLEWARE = [
        "utm_tracker.middleware.UtmSessionMiddleware",
        "utm_tracker.middleware.LeadSourceMiddleware"
        ]
    
    settings.MIDDLEWARE.extend(UTM_MIDDLEWARE)
