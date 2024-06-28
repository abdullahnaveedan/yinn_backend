import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt # Import matplotlib for plotting


# Load the dataset (assuming the file is named 'carbon_emissions.xlsx')
df = pd.read_excel('merged_data (2).xlsx')


# Preprocess the data
X = df.drop('CO2/kg', axis=1)
y = df['CO2/kg']

# Encode categorical variables
categorical_features = ['Category', 'item','Material']
numerical_features = []

# Handle unknown categories during transformation
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# Define the model
model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)

# Create a pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                           ('model', model)])

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
pipeline.fit(X_train, y_train)

# Make predictions
y_pred = pipeline.predict(X_test)


mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)


# Display results
print(f"XGBoost - MSE: {mse}, RMSE: {rmse}")