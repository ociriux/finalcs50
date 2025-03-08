# AMBROSIA - Optimizing Your Nutrition

#### Video Demo: [URL HERE]

## Overview
Ambrosia is a dynamic web application that helps users optimize their nutrition by matching foods to their specific nutrient needs. Built primarily with Django, JavaScript and Bootstrap, it leverages the USDA's FoodData Central "Foundation Foods" database to provide accurate, up-to-date nutritional information.

## Key Features
- **Smart Nutrient Matching**: Input any combination of nutrients, and Ambrosia finds the top 20 foods that best    satisfy those requirements
- **Interactive Nutrient Labels**: Click any food to view its comprehensive nutritional profile
- **Fast And Dynamic Dashboard**: Use the nutrition matcher and quickly look through food-nutrient data without reloading the page
- **Semi-Automatic Database Updates**: Synchronization System, that runs on server start when provided a new URL
- **Scoring System**: Foods are ranked based on their relative nutrient concentrations between other foods. When using the nutrition matcher, foods get picked based on average score between selected nutrients in a food
- **Food Browser**: Browse and search through the complete food and nutrient database

## Technical Architecture

### Core Structure
```bash
Project #finalcs50
└── ambrosia
    ├── ambrosia
    |   └── settings.py         # FOUNDATION_FOODS_DOWNLOAD_URL is used by food_data_sync()
    ├── nutrition_matcher       # Main app that handles core functions
    │   ├── static
    │   │   └── styles.css      # CSS for navbar transparancy 
    │   ├── templates           
    │   │   ├── master.html     # General web app template
    │   │   ├── index.htmlw     # Dashboard with core functionality
    │   │   ├── matched.html    # Renders top matches given by find_top_matches()
    │   │   └── label.html      # Renders the dynamic nutrition label
    │   ├── matcher.py          # Contains the core matching algorithm
    │   └── views.py            # Handles web requests and data presentation
    ├── usda_sync               # App that handles data synchronization
    │   ├── apps.py             # Runs food_data_sync() on server start
    │   ├── models.py           # Defines Food, Nutrient, and FoodSpec models
    │   └── sync.py             # Checks for a new URL in settings.py, downloads data, feeds data into models, rates food-nutrient combinations
    └── requirements.txt        # Install dependencies with pip install -r requirements.txt
```

## How It Works

### Core Functionality Flow
1. **Initial User Input**
   - Click "Get Started" to open the nutrient selection modal
   - Choose one or more nutrients from the comprehensive list
   - Submit selection to trigger the matching process

2. **Food Matching Process**
   ```python
   # matcher.py handles the core matching logic
   def find_top_matches(nutrient_ids):
       return Food.objects.filter(foodspec__nutrient__id__in=nutrient_ids)
           .annotate(
               average_score=1.0 * Sum('foodspec__score') / Count('foodspec__nutrient')
           )
           .order_by('-average_score')[:20]
   ```
   - Backend receives nutrient IDs via POST to `/nutrition_matcher/`
   - `find_top_matches()` calculates optimal foods based on:
     - Presence of selected nutrients
     - Average nutrient concentration scores
     - Returns top 20 matches

3. **Dynamic Results Display**
   - JavaScript handles the matching response
   - Renders food matches as interactive buttons
   - Updates the dashboard without page reload

4. **Nutrition Label Generation**
   - Click any food to view detailed nutrition information
   - System sends food ID via POST to `/build_label/`
   - Backend organizes nutrient data into categorical maps
   - JavaScript handles the map response
   - Renders food specs as FDA style nutrition label
   - Updates the dashboard without page reload

5. **Additional Features**
   - Food browser accessible when clicking on food description over the nutriton label
   - Each food selection triggers automatic label update
   - All interactions handled asynchronously for smooth UX

## Installation

```bash
# Clone the repository
git clone https://github.com/ociriux/finalcs50.git

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windowws
source .venv/bin/activate   # Unix/MacOS

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

## Design Decisions

### Why Django?
Django was chosen for its:
- Robust ORM for complex database operations
- Built-in admin interface for data management
- Excellent documentation and community support
- Strong security features
- Learning a new back-end web framework besides flask

### Scoring System
The scoring system (0-100) was implemented to:
- Normalize nutrient concentrations across different measurement units
- Provide meaningful comparisons between foods
- Support the ranking in the matching algorithm

### Database Structure
- **Food**: Basic food information
- **Nutrient**: Nutrient definitions and units
- **FoodSpec**: Many-to-many relationship with calculated scores
- **LastUpdate**: Storing the last used URL to prevent food_data_sync() from running on every server start
This structure is a result of the nested and repetitive nature of the Data provided by the USDA FoodData Central. It allows for efficient querying and flexible nutrient matching.

### USDA Sync
This App was implemented to:
- Seperate the Project from the data, resulting in a smaller file size of the repositor
- Allow for automatic synchronization of new food data
- Only run updates when new data is provided by the user
- Handle the integration of new data into the database

## Concideration For Future Enhancements
- Improving the find_top_matches() algorithm to get better at handling a lot of nutrients
- Expanding the functionality to allow for kcal, macro- and micro-nutrient goals, thus functioning as a full-fledged nutrition coach
- Building an own database, providing comprehensive and standardised food-data
- User accounts for saving preferences and tracking progress
- Custom diet profiles (vegan, keto, etc.)
- Meal planning suggestions
- Mobile app development