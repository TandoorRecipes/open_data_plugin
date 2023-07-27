from django.apps import AppConfig


class OpenDataConfig(AppConfig):
    VERSION = '0.2.0'

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes.plugins.open_data_plugin'
    verbose_name = 'Tandoor Open Data'
    base_url = 'open-data/'
    bundle_name = 'OPEN-DATA'
    # name of DRF router in urls.py that should be included by the base router (make sure to give all objects a plugin prefix to avoid collisions)
    api_router_name = 'open_data_router'
    # name of template to include in the main nav section
    nav_main = ''  # not implemented yet
    # name of template to include in the dropdown nav section
    nav_dropdown = 'open_data_dropdown_nav.html'

    disabled = False
