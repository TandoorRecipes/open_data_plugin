from django.apps import AppConfig


class OpenDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes.plugins.open_data_plugin'
    verbose_name = 'Tandoor Open Data'
    base_url = 'open-data/'
    bundle_name = 'OPEN-DATA'
