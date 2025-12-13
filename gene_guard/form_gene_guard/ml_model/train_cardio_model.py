"""
Cardiovascular Disease Prediction ML Model Training Script
Trains a Random Forest classifier to predict cardiovascular disease risk.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_and_preprocess_data():
    """Load the cardiovascular dataset and preprocess it."""
    # Load the dataset (semicolon separated)
    df = pd.read_csv(os.path.join(SCRIPT_DIR, 'cardio_train.csv'), sep=';')
    
    print(f"Dataset loaded: {len(df)} records")
    print(f"Columns: {list(df.columns)}")
    
    # Convert age from days to years
    df['age_years'] = df['age'] / 365.25
    
    # Calculate BMI
    df['bmi'] = df['weight'] / ((df['height'] / 100) ** 2)
    
    # Clean outliers in blood pressure
    df = df[(df['ap_hi'] >= 80) & (df['ap_hi'] <= 250)]
    df = df[(df['ap_lo'] >= 40) & (df['ap_lo'] <= 200)]
    df = df[df['ap_hi'] > df['ap_lo']]
    
    # Clean BMI outliers
    df = df[(df['bmi'] >= 15) & (df['bmi'] <= 60)]
    
    print(f"After cleaning: {len(df)} records")
    
    return df

def train_model():
    """Train the cardiovascular disease prediction model."""
    print("=" * 50)
    print("Cardiovascular Disease Prediction Model Training")
    print("=" * 50)
    
    # Load and preprocess data
    print("\n1. Loading data...")
    df = load_and_preprocess_data()
    
    # Select features
    print("\n2. Selecting features...")
    feature_columns = ['age_years', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 
                       'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'bmi']
    
    X = df[feature_columns]
    y = df['cardio']
    
    # Split data
    print("\n3. Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Scale features
    print("\n4. Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest
    print("\n5. Training Random Forest model...")
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        min_samples_split=10,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    print("\n6. Evaluating model...")
    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nTest Accuracy: {accuracy * 100:.2f}%")
    
    # Feature importance
    print("\n7. Feature Importance:")
    importances = sorted(zip(feature_columns, model.feature_importances_), 
                        key=lambda x: x[1], reverse=True)
    for feature, importance in importances:
        print(f"  {feature}: {importance * 100:.2f}%")
    
    # Save model and scaler
    print("\n8. Saving model and scaler...")
    joblib.dump(model, os.path.join(SCRIPT_DIR, 'cardio_model.pkl'))
    joblib.dump(scaler, os.path.join(SCRIPT_DIR, 'cardio_scaler.pkl'))
    joblib.dump(feature_columns, os.path.join(SCRIPT_DIR, 'cardio_features.pkl'))
    
    print("\n" + "=" * 50)
    print("Training Complete!")
    print("=" * 50)
    print(f"\nFiles saved:")
    print(f"  - cardio_model.pkl")
    print(f"  - cardio_scaler.pkl")
    print(f"  - cardio_features.pkl")
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    
    return model, scaler, feature_columns

if __name__ == "__main__":
    train_model()
