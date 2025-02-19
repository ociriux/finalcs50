from django.apps import AppConfig
from django.conf import settings
import sys
import threading


class UsdaSyncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usda_sync'

    def ready(self):
        # Optional: Nur im Entwicklungsmodus oder bei runserver starten
        if 'runserver' not in sys.argv:
            return

        # Optional: Auch eine Einstellung in den Settings berücksichtigen
        if not getattr(settings, 'USDA_SYNC_ENABLED', True):
            return

        from . import sync
        threading.Thread(target=sync.food_data_sync).start()