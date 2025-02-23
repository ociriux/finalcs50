import json
import requests
from io import BytesIO
from zipfile import ZipFile, BadZipFile

from django.conf import settings
from .models import Food, Nutrient, FoodSpecs



def food_data_sync():
    print("Starting food-data synchronization...")
    url = settings.FOUNDATION_FOODS_DOWNLOAD_URL
    print(f"Downloading data from {url}")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with BytesIO(response.content) as data_in_memory:
            with ZipFile(data_in_memory) as food_data_zip:
                json_filename = food_data_zip.namelist()[0]
                print(f"Found food-data in ZIP: {json_filename}")
        
                with food_data_zip.open(json_filename) as json_file:
                    food_data = json.load(json_file)
                    print("Successfully loaded JSON")

                    for food in food_data['FoundationFoods']:
                        food, created = Food.objects.get_or_create(
                            id=food.get('ndbNumber', ''),
                            description=food.get('description', ''),
                            category=food.get('foodCategory', {}).get('description', ''),
                        )
                                    
        

        
    except requests.RequestException as e:
        print("Error while downloading food-data:", e)
    except BadZipFile as e:
        print("Error while extracting files from Zip:", e)
    except json.JSONDecodeError as e:
        print("Error while parsing through JSON file:", e)