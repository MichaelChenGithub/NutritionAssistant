# NutritionAssistant
## Backgroud and Target
I am entering my fourth year of fitness, and I still haven't found a user-friendly diet tracking tool to help me manage my diet progress. Therefore, I am trying to create a web application that integrates AI for intelligent diet logging and management. It will be able to provide personalized dietary recommendations and automatically record your eating habits. Additionally, it includes a calendar and tracking charts to make it convenient for fitness enthusiasts to monitor their progress.

## Main Features

Based on the user's dietary needs, the AI assistant will provide:
1. Nutritional knowledge (e.g., nutritional requirements based on the user's training goals)
2. Restaurant meals (e.g., Subways, TGI Friday's)
3. Recipes (e.g., red wine-braised beef, poached chicken breast)

## Secondary Features

Assist users in recording and tracking their diet by providing:
1. Automatic food import functionality by the AI assistant
2. Calendar
3. Tracking chart

## Project Plan
### Phase 1 - Data collection and assistant API implementation
#### Data collection
- [ ]  Nutritional knowledge
- [x]  Foundation food
- [x]  Restaurant meals
- [ ]  Recipes
#### Assistant API implementation
- [x]  Nutrition assistant
- [x]  POC assistant through **streamlit**
- [ ]  Model evaluation
### Phase 2 - Integrate the nutrition assistant into the project app
- [x]  Frontend deployment - chatbot look page
- [ ]  Backend API deployment
- [ ]  Service deployment - GCP compute engine
### Phase 3 - Secondary features
- [ ]  Recording calendars
- [ ]  Tracking charts, and recommending diets.

## Data Source
* Foundation food : USDA: https://www.usda.gov/
* Restaurant meals : MenuStat: https://www.menustat.org/