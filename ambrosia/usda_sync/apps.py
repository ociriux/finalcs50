from django.apps import AppConfig
import sys
import threading


class UsdaSyncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'usda_sync'

    def ready(self):
        # Prüfen, ob der Befehl "runserver" ausgeführt wird.
        # So läuft der Code nur, wenn du den Entwicklungsserver startest,
        # und nicht bei anderen Befehlen wie "migrate" oder "test".
        if 'runserver' not in sys.argv:
            return

        # Importiere hier die Funktion, die den Sync ausführt.
        # Der Import erfolgt erst hier, um eventuelle Zirkularreferenzen zu vermeiden.
        from . import sync

        # Starte den Synchronisationsprozess in einem separaten Thread,
        # damit der Serverstart nicht blockiert wird.
        threading.Thread(target=sync.food_data_sync).start()