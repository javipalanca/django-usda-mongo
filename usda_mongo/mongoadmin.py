__author__ = 'jpalanca'

# Import the MongoAdmin base class
from mongonaut.sites import MongoAdmin

# Import your custom models
from .models import Food, FoodGroup, Weight, Nutrient, Footnote, DataDerivation, DataSource, Source, NutrientData

# Instantiate the MongoAdmin class
# Then attach the mongoadmin to your model
Food.mongoadmin = MongoAdmin()
FoodGroup.mongoadmin = MongoAdmin()
Weight.mongoadmin = MongoAdmin()
Nutrient.mongoadmin = MongoAdmin()
Footnote.mongoadmin = MongoAdmin()
DataSource.mongoadmin = MongoAdmin()
DataDerivation.mongoadmin = MongoAdmin()
Source.mongoadmin = MongoAdmin()
NutrientData.mongoadmin = MongoAdmin()
