from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import joblib
from difflib import get_close_matches
import os
from django.templatetags.static import static
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
import pickle
from sklearn.preprocessing import OneHotEncoder
from fuzzywuzzy import fuzz, process
from xgboost import XGBRegressor


def index(request):
    return HttpResponse("Testing!")

# Load the dataset
dataset_path = os.path.join(settings.BASE_DIR, 'static', 'merged_data.xlsx')
df = pd.read_excel(dataset_path)

# Load the saved model
model_path = os.path.join(os.path.dirname(__file__), 'xgb_model.pkl')
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# Fit a new encoder on the 'Material' column
encoder = OneHotEncoder()
encoder.fit(df[['Material']])

# Function to find the closest match for the item name using fuzzywuzzy
def find_closest_match(item_name, df):
    items = df['item'].tolist()
    closest_match, _ = process.extractOne(item_name, items)
    return closest_match

# Function to predict CO2/kg based on materials and percentages
def predict_co2(materials, model, encoder):
    total_percentage = sum(materials.values())
    if total_percentage != 100:
        raise ValueError("Total percentage of materials must equal 100%")
    
    co2_values = []
    for material, percentage in materials.items():
        material_df = pd.DataFrame({'Material': [material]})
        material_encoded = encoder.transform(material_df)
        co2_value = model.predict(material_encoded)[0]
        co2_values.append(co2_value * (percentage / 100))
    
    weighted_co2 = sum(co2_values)
    return weighted_co2

class PredictEmissionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmissionInputSerializer(data=request.data)
        if serializer.is_valid():
            user_item = serializer.validated_data['product_name']
            materials_data = serializer.validated_data['materials']
            
            # Load dataset
            df = pd.read_excel(dataset_path)
            
            user_materials = {material['material']: material['percentage'] for material in materials_data}
            
            try:
                # Predict the CO2 emission based on user input
                predicted_co2 = predict_co2(user_materials, model, encoder)
                return Response({'predicted_emission_co2e': predicted_co2}, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
