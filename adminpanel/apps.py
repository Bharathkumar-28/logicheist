from django.apps import AppConfig


class AdminpanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adminpanel'
# adminpanel/apps.py

from django.apps import AppConfig

class AdminpanelConfig(AppConfig):
    name = 'adminpanel'

    def ready(self):
        import adminpanel.signals  # Import signals to ensure the handler is connected
