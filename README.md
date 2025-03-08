# AMBROSIA - Optimizing Your Nutrition

#### Video Demo:  [URL HERE]

#### Description:

Project #finalcs50
├── ambrosia
│   ├── nutrition_matcher
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── matcher.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── templates
│   │   │   ├── index.html
│   │   │   ├── master.html
│   │   ├── static
│   │   │   ├── styles.css
│   ├── usda_sync
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── tasks.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── management
│   │   │   ├── commands
│   │   │   │   ├── sync_usda.py
│   ├── ambrosia
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── asgi.py
├── manage.py
├── README.md
├── requirements.txt


Ambrosia is a Food-Matching Web Application primarily implemented with Python, Django, HTML, Bootstrap, and JavaScript. The application allows users to input a set of nutrients, and it generates a selection of foods from the database that best cover the selected nutrients. Users can search for one nutrient or multiple nutrients, and the algorithm will provide the top 20 foods that offer the best chance of acquiring those nutrients.

The main page is designed to be fast, responsive, and dynamic. Users can click on any food item, and a comprehensive nutrient label is generated, showing all relevant information from the database. Additionally, users can browse the foods and their nutrients in the database independently of the matching algorithm.

One special feature of the database is the `usda_sync` app. This app allows users to set a URL to the latest downloadable data from the USDA's FoodData Central, ensuring that Ambrosia's database is updated automatically. `usda_sync` checks for a new URL every time the server starts. If a new URL is set in the settings and it is not already saved in the `LastUpdate` model, the data updating process begins. After importing food and nutrient data into the `Food` and `Nutrient` models, the data is used to build the `FoodSpec` model, which models the relationship between foods and nutrients. Each food and its nutrient are rated based on their relative concentration, with the highest nutrient amount between foods receiving a score of 100. This score is ultimately used to help the `nutrition_matcher` match foods to a nutrient selection.

#### Project Structure:
- `matcher.py`: Contains the core algorithm for finding the top food matches based on selected nutrients. The `find_top_matches` function filters foods by nutrient IDs, calculates total and average scores, and returns the top 20 foods.
- `usda_sync`: An app responsible for syncing the database with the latest data from the USDA's FoodData Central. It checks for new URLs, updates the database, and builds the `FoodSpec` model.
- `templates`: Contains HTML templates for the web application, including the main page and modal forms for user input.
- `static`: Contains static files such as CSS and JavaScript for styling and interactivity.

#### Design Choices:
1. **Algorithm for Matching Foods**: The algorithm in `matcher.py` was designed to prioritize foods based on their nutrient concentration. The decision to use both total and average scores ensures that foods with a high concentration of multiple nutrients are prioritized.
2. **Responsive Design**: The use of Bootstrap ensures that the web application is responsive and user-friendly across different devices and screen sizes.
3. **Automatic Database Updates**: The `usda_sync` app was implemented to automate the process of updating the database with the latest USDA data. This ensures that the application always has the most current information without manual intervention.
4. **User Interaction**: The main page and modal forms were designed to be intuitive and easy to use. Users can quickly input their nutrient goals and receive immediate feedback on the best food matches.

#### Future Enhancements:
- **User Authentication**: Implementing user authentication to allow users to save their preferences and nutrient goals.
- **Advanced Filtering**: Adding more advanced filtering options for users to refine their food searches based on dietary restrictions or preferences.
- **Enhanced Visualization**: Improving the visualization of nutrient data with charts and graphs to provide users with a better understanding of their nutritional intake.

Ambrosia aims to provide users with a powerful tool to optimize their nutrition by leveraging the latest data and advanced algorithms. We hope you find this project useful and informative.