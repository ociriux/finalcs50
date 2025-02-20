from django.apps import AppConfig
from django.conf import settings
from . import sync
import os
import sys
import threading


class UsdaSyncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usda_sync'

    def ready(self):
        # Optional: Nur im Entwicklungsmodus oder bei runserver starten
        if 'runserver' not in sys.argv or not os.environ.get('RUN_MAIN'):
            return

        print("###########CUM###############")

        threading.Thread(target=sync.food_data_sync).start()