import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

def create_model():
    print("Generating synthetic dataset for Crop Recommendation...")
    # Features: N, P, K, temperature, humidity, pH, rainfall
    np.random.seed(42)
    # Generate 100 random samples
    X = np.random.rand(100, 7) * 100 
    X[:, 3] = X[:, 3] * 0.4 + 10 # Temp 10-50
    X[:, 4] = X[:, 4] * 0.8 + 20 # Humidity 20-100
    X[:, 5] = X[:, 5] * 0.14 # pH 0-14
    X[:, 6] = X[:, 6] * 3 # Rainfall 0-300
    
    crops = ['Rice', 'Wheat', 'Maize', 'Lentil', 'Jute', 'Cotton', 'Sugarcane']
    y = np.random.choice(crops, size=100)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(X_scaled, y)
    
    # Save directory
    os.makedirs('model', exist_ok=True)
    
    # Save model and scaler
    with open('model/crop_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    with open('model/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
        
    print("Dummy Model and Scaler have been generated in the 'model' directory.")

if __name__ == '__main__':
    create_model()
