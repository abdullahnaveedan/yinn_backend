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
from .serializers import EmissionInputSerializer
import numpy as np
import pickle
from sklearn.preprocessing import OneHotEncoder
from fuzzywuzzy import fuzz, process 

def index(request):
    return HttpResponse("Hello World")

# Load the saved model
model_filename = os.path.join(os.path.dirname(__file__), 'xgb_model.pkl')
with open(model_filename, 'rb') as file:
    model = pickle.load(file)

# Function to load dataset from an Excel file
def load_dataset(filename):
    df = pd.read_excel(filename)
    return df

# Function to find closest match for an item name
def find_closest_item(item_name, dataset):
    choices = dataset['item'].tolist()
    closest_match, score = process.extractOne(item_name, choices, scorer=fuzz.token_sort_ratio)
    return closest_match

# Function to calculate weighted CO2
def calculate_weighted_co2(material_percentages, material_df):
    total_co2 = 0
    for material, percentage in material_percentages.items():
        # Fetch CO2 value for the material
        co2_value = material_df.loc[material_df['Material'] == material, 'CO2/kg']
        if not co2_value.empty:
            total_co2 += (co2_value.values[0] * (percentage / 100))
        else:
            # Handle the case where material is not found, maybe by setting a default CO2 value
            print(f"Warning: Material {material} not found in CO2 emissions data. Using 0 CO2/kg.")
            total_co2 += 0  # Or any default value you deem appropriate
    return total_co2

# Function to predict CO2 emission
def predict_co2_emission(item, material_percentages, dataset):
    # Find closest item match
    matched_item = find_closest_item(item, dataset)
    print(matched_item)
    if not matched_item:
        raise ValueError(f"No close match found for item '{item}' in the dataset.")
    
    # Calculate weighted CO2 based on user-entered percentages
    # Use the full dataset for material lookup instead of filtering by matched item
    material_df = dataset[['Material', 'CO2/kg']]  
    weighted_co2 = calculate_weighted_co2(material_percentages, material_df)
    
    return weighted_co2

class PredictEmissionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EmissionInputSerializer(data=request.data)
        if serializer.is_valid():
            user_item = serializer.validated_data['product_name']
            materials_data = serializer.validated_data['materials']
            print(user_item)
            # Load dataset
            dataset = os.path.join(settings.BASE_DIR, 'static', 'merged_data.xlsx')
            df = load_dataset(dataset)
            
            user_materials = {material['material']: material['percentage'] for material in materials_data}
            
            # Predict the CO2 emission based on user input
            predicted_co2 = predict_co2_emission(user_item, user_materials, df)
            
            return Response({'predicted_emission_co2e': predicted_co2}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
