from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)


def pull_data(): 
    query = supabase.table("earthquakes").select("*").execute()
    data = query.data
    return data

# Given data
data = pull_data()

# Convert data to DataFrame
df = pd.DataFrame(data)

# Convert 'date' and 'time' to datetime
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

# Extract relevant features
df['timestamp'] = df['datetime'].apply(lambda x: x.timestamp())

# Define features and target
X = df[['latitude', 'longitude', 'depth', 'timestamp']]
y = df[['latitude', 'longitude', 'depth', 'magnitude']]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a random forest regressor model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)


def predict_earthquake(potential_X): 
    pred = model.predict(potential_X)
    return {
        'latitude': pred[0][0],
        'longitude': pred[0][1],
        'depth': pred[0][2],
        'magnitude': pred[0][3], 
        'confidence': 100 - mse
    }