from django.apps import AppConfig
from django.conf import settings
import os
import sys
import threading


class UsdaSyncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usda_sync'

    def ready(self):
        from . import sync                                                      # Import the sync module after the app is ready
        if 'runserver' not in sys.argv or not os.environ.get('RUN_MAIN'):
            return

        threading.Thread(target=sync.food_data_sync).start()