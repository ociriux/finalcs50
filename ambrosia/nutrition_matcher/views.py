from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from usda_sync.models import Food, Nutrient, FoodSpec
from . import matcher

def index(request):
    template = loader.get_template('index.html')
    foods = Food.objects.all().order_by('description')
    nutrients = Nutrient.objects.all().order_by('description')
    foodspecs = FoodSpec.objects.all()
    context = {
        'foods' : foods, 'nutrients' : nutrients, 'foodspecs' : foodspecs,
    }
    return HttpResponse(template.render(context, request))

def nutrition_matcher(request):
    if request.method == "POST":
        target_nutrient_ids = request.POST.getlist("nutrient_target")
        target_nutrient_ids = [int(x) for x in target_nutrient_ids]
        matched_food = matcher.find_top_matches(target_nutrient_ids)
        context = {
            'matched_food' : matched_food, 'target_nutrient_ids' : target_nutrient_ids
        }
        return render(request, "matched.html", context)
    return HttpResponse("Invalid request", status=400)

def build_label(request):
    if request.method == "POST":
        selected = request.POST.get("id")
        if not selected:
            return HttpResponse("No id provided", status=400)
        selected = int(selected)
        selected_foodspecs = FoodSpec.objects.filter(food_id=selected).order_by('-score')

        calories = selected_foodspecs.filter(nutrient_id__in=[1008, 2047, 2048]).first()
        total_fat = selected_foodspecs.filter(nutrient_id__in=[1004, 1085]).first()
        saturated_fat = selected_foodspecs.filter(nutrient_id__in=[1258]).first()
        monounsaturated_fat = selected_foodspecs.filter(nutrient_id__in=[1292]).first()
        polyunsaturated_fat = selected_foodspecs.filter(nutrient_id__in=[1293]).first()
        trans_fat = selected_foodspecs.filter(nutrient_id__in=[1257]).first()
        cholesterol = selected_foodspecs.filter(nutrient_id__in=[1253]).first()
        sodium = selected_foodspecs.filter(nutrient_id__in=[1093]).first()
        total_carbohydrate = selected_foodspecs.filter(nutrient_id__in=[1005, 1050]).first()
        dietary_fiber = selected_foodspecs.filter(nutrient_id__in=[1079]).first()
        total_sugars = selected_foodspecs.filter(nutrient_id__in=[1063, 2000]).first()
        protein = selected_foodspecs.filter(nutrient_id__in=[1003]).first()
        nitrogen = selected_foodspecs.filter(nutrient_id__in=[1002]).first()
        water = selected_foodspecs.filter(nutrient_id__in=[1051]).first()
        ash = selected_foodspecs.filter(nutrient_id__in=[1007]).first()

        proximates_map = {
            1008: calories,
            1004: total_fat,
            1258: saturated_fat,
            1292: monounsaturated_fat,
            1293: polyunsaturated_fat,
            1257: trans_fat,
            1253: cholesterol,
            1093: sodium,
            1005: total_carbohydrate,
            1079: dietary_fiber,
            1063: total_sugars,
            1003: protein,
            1002: nitrogen,
            1051: water,
            1007: ash,
        }

        vitamins_map = {}
        minerals_map = {}
        fattyacids_map = {}
        sugars_map = {}
        aminos_map = {}
        others_map = {}

        proximates = [1008, 2047, 2048, 1004, 1085, 1258, 1292, 1293, 1257, 1253,
                        1093, 1005, 1050, 1079, 1063, 2000, 1003, 1002, 1051, 1007]
        
        vitamins = [1105, 1106, 1109, 1110, 1111, 1112, 1113, 1114, 1116,
                    1117, 1118, 1119, 1120, 1121, 1122, 1123, 1125, 1126, 
                    1127, 1128, 1129, 1130, 1131, 1162, 1165, 1166, 1167, 
                    1170, 1175, 1176, 1177, 1178, 1183, 1184, 1185, 1188, 
                    1191, 1192, 2059, 2066]

        minerals = [1087, 1089, 1090, 1091, 1092, 1094, 1095, 1097, 1098, 
                    1100, 1101, 1102, 1103, 1137, 1146]

        fattyacids = [1259, 1260, 1261, 1262, 1263, 1264, 1265, 1266, 1267, 
                        1268, 1269, 1270, 1271, 1272, 1273, 1276, 1277, 1278, 1279, 
                        1280, 1281, 1294, 1296, 1298, 1299, 1300, 1301, 1303, 1304, 
                        1305, 1306, 1311, 1312, 1313, 1314, 1315, 1316, 1317, 1321, 
                        1323, 1325, 1329, 1330, 1331, 1333, 1334, 1335, 1404, 1405, 
                        1406, 1409, 1411, 1414, 2003, 2004, 2005, 2006, 2007, 2008,
                        2009, 2010, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 
                        2020, 2021, 2022, 2023, 2024, 2025, 2026]
        
        sugars = [1009, 1010, 1011, 1012, 1013, 1014, 1075, 1076, 1077]

        aminos = [1210, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1218, 
                1219, 1220, 1221, 1222, 1223, 1224, 1225, 1226, 1227, 
                1228, 1232]

        for spec in selected_foodspecs:
            if spec.nutrient.id in proximates:
                continue
            elif spec.nutrient.id in vitamins:
                vitamins_map[spec.nutrient.id] = spec
            elif spec.nutrient.id in minerals:
                minerals_map[spec.nutrient.id] = spec
            elif spec.nutrient.id in fattyacids:
                fattyacids_map[spec.nutrient.id] = spec
            elif spec.nutrient.id in sugars:
                sugars_map[spec.nutrient.id] = spec
            elif spec.nutrient.id in aminos:
                aminos_map[spec.nutrient.id] = spec
            else:
                others_map[spec.nutrient.id] = spec

        context = {
            'proximates_map' : proximates_map, 'vitamins_map' : vitamins_map,  'minerals_map' : minerals_map,  'fattyacids_map' : fattyacids_map,  'sugars_map' : sugars_map,  'aminos_map' : aminos_map, 'others_map' : others_map,
        }
        return render(request, "label.html", context)
    return HttpResponse("Invalid request", status=400)

def food(request):
    food = Food.objects.all().order_by('description')
    template = loader.get_template('food.html')
    context = {
        'food' : food,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    food = Food.objects.get(id=id)
    foodspecs = FoodSpec.objects.filter(food_id=id).order_by('-score')
    template = loader.get_template('details.html')
    context = {
        'foodspecs' : foodspecs, 'food' : food,
    }
    return HttpResponse(template.render(context, request))

def nutrients(request):
    nutrients = Nutrient.objects.all().order_by('description')
    template = loader.get_template('nutrients.html')
    context = {
        'nutrients' : nutrients,
    }
    return HttpResponse(template.render(context, request))