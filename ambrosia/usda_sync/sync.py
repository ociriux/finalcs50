from django.conf import settings
from django.db.models import Max
from io import BytesIO
from .models import Food, Nutrient, FoodSpec, LastUpdate
from zipfile import ZipFile, BadZipFile
import json
import requests
import sys
import time


def food_data_sync():
    print("Starting food-data synchronization...")
    url = settings.FOUNDATION_FOODS_DOWNLOAD_URL            # Load the URL from the settings.py file
    if LastUpdate.objects.filter(url=url).exists():         # Check if the URL was already used
        print("No new url found, food-data is up-to-date")
        return
    
    LastUpdate.objects.all().delete()                       # Delete the previous URL
    LastUpdate(url=url).save()                              # Save the new URL as the last update

    print(f"Downloading data from {url}")
    
    try:
        response = requests.get(url)                        # Send a GET request to the URL
        response.raise_for_status()                         # Raise an exception if the status code is not 200
        
        with BytesIO(response.content) as data_in_memory:           # Load the content of the response into a BytesIO object
            with ZipFile(data_in_memory) as food_data_zip:          # Load the BytesIO object into a ZipFile object
                json_filename = food_data_zip.namelist()[0]
                print(f"Found food-data in ZIP: {json_filename}")
        
                with food_data_zip.open(json_filename) as json_file:        # Open the JSON file in the ZIP file
                    food_data = json.load(json_file)                        # Load the JSON file into a Python dictionary   
                    print("Successfully loaded JSON")
                    
                    print("Updating data...")
                    created_entries = 0

                    for food in food_data['FoundationFoods']:                       # Iterate over the 'FoundationFoods' list in food_data
                        
                        conv_factors = food.get('nutrientConversionFactors', [])
                        if not conv_factors:
                            conv_factors = [{'proteinValue': 4.0, 'fatValue': 9.0, 'carbValue': 4.0}]                        

                        food_item, created = Food.objects.update_or_create(         # Update or create a Food object
                            id = food.get('ndbNumber', ''),
                            defaults = {                                                # Only search for the ndbNumber, if it doesn't exist, create a new object with the following attributes:
                                'description' : food.get('description', ''),
                                'category' : food.get('foodCategory', {}).get('description', ''),
                                'calorie_conversion_factor_protein' : conv_factors[0].get('proteinValue', '4.0'),
                                'calorie_conversion_factor_fat' : conv_factors[0].get('fatValue', '9.0'),
                                'calorie_conversion_factor_carbs' : conv_factors[0].get('carbohydrateValue', '4.0'),
                            }
                        )

                        for nutrient in food['foodNutrients']:
                            nutrient_item, created = Nutrient.objects.update_or_create(
                                id = nutrient.get('nutrient', {}).get('id', ''),
                                defaults = {
                                    'description' : nutrient.get('nutrient', {}).get('name', ''),
                                    'unit' : nutrient.get('nutrient', {}).get('unitName', ''),
                                }
                            )

                            food_spec_item, created = FoodSpec.objects.update_or_create(
                                food = food_item,
                                nutrient = nutrient_item,
                                defaults = {
                                    'amount' : nutrient.get('amount', 0),
                                }
                            )

                    if created:
                        created_entries += 1
                    print(f"{created_entries} new entries created")

        food_count = Food.objects.count()
        nutrient_count = Nutrient.objects.count()
        print(f"Successfully updated data! {food_count} food items and {nutrient_count} nutrients are currently stored in the database")


        ### Calculate Scores for every Nutrient amount in a Food Item relative to the amount in other Food Items ###

        foodspec_count = FoodSpec.objects.count()
        score_updates = 0

        for nutrient in Nutrient.objects.all():
            result = FoodSpec.objects.filter(nutrient=nutrient).aggregate(max_amount=Max('amount'))
            max_amount = result.get('max_amount') or 0

            if max_amount == 0:
                continue

            foodspecs = FoodSpec.objects.filter(nutrient=nutrient)

            for foodspec in foodspecs:
                new_score = round((foodspec.amount / max_amount) * 100, 2)
                foodspec.score = new_score
                foodspec.save()
                score_updates += 1

                sys.stdout.write(f"\rFood-Nutrient scores calculated: {score_updates} / {foodspec_count}")
                sys.stdout.flush()

        ignored = foodspec_count - score_updates

        print(f"\n{score_updates} food-nutrient combinations rated / {ignored} food-nutrient combinations ignored because of insufficient data")
        print("Synchonization process successful!")
        
    except requests.RequestException as e:
        print("Error while downloading food-data:", e)
    except BadZipFile as e:
        print("Error while extracting files from Zip:", e)
    except json.JSONDecodeError as e:
        print("Error while parsing through JSON file:", e)
