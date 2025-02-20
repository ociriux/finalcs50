from django.conf import settings
from io import BytesIO
from zipfile import ZipFile, BadZipFile
import json
import requests



def food_data_sync():
    """
    Diese Funktion übernimmt:
    1. Das Herunterladen der USDA-Daten (als ZIP).
    2. Entpacken der ZIP-Datei
    3. Das Umwandeln und Speichern der JSON-Daten in die SQL-Datenbank.
    """

    print("### Starte den USDA-Datenimport...")

    # Beispiel: URL, von der die USDA-Daten heruntergeladen werden.
    # Ersetze dies mit der korrekten URL.
    url = settings.FOUNDATION_FOODS_DOWNLOAD_URL
    print(f"### Downloading Food Data from {url}")
    
    try:
        # ZIP-Datei herunterladen
        response = requests.get(url)
        response.raise_for_status()
        
        # ZIP-Datei in Memory laden
        with BytesIO(response.content) as data_in_memory:
            with ZipFile(data_in_memory) as food_data_zip:
                json_filename = food_data_zip.namelist()[0]
                print(f"### Gefundene Datei im ZIP: {json_filename}")
        
                # JSON-Datei aus ZIP lesen
                with food_data_zip.open(json_filename) as json_file:
                    food_data = json.load(json_file)
                    print("### JSON erfolgreich geladen")

                    for food in food_data['FoundationFoods'][:5]:
                        #if food.get('description') == 'Almond butter, creamy':
                            print(food['description'])
                            for nutrient in food['foodNutrients']:
                                if nutrient['nutrient'].get('name') == 'Water':
                                    print(nutrient['nutrient']['id'], nutrient['nutrient']['name'], nutrient['amount'], nutrient['nutrient']['unitName'],'\n')
        
                        # Hier kommt Ihre Datenverarbeitung...
        
    except requests.RequestException as e:
        print("### Fehler beim Download:", e)
    except BadZipFile as e:
        print("### Fehler beim Entpacken der ZIP-Datei:", e)
    except json.JSONDecodeError as e:
        print("### Fehler beim Parsen der JSON-Datei:", e)