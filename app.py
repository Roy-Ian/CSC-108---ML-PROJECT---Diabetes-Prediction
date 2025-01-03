from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

app = Flask(__name__)

# Constants
DATA_PATH = 'diabetes.csv'  
MODEL_PATH = 'model.pkl'    

# Load and preprocess the dataset
data = pd.read_csv(DATA_PATH)  
X = data[['Glucose', 'BloodPressure', 'BMI']]
y = data['Outcome']

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

# Function to load or train the model
def load_or_train_model(model_path, X_train, y_train):
    if os.path.exists(model_path):
        return joblib.load(model_path)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    joblib.dump(model, model_path)
    return model

model = load_or_train_model(MODEL_PATH, X_train, y_train)

# Eval the model
accuracy = accuracy_score(y_test, model.predict(X_test))
accuracy_percentage = f"{accuracy * 100:.2f}" 

# Home route to render the frontend
@app.route('/')
def home():
    return render_template('index.html', accuracy=accuracy_percentage)  

# API route to make predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.json

        required_features = ['Glucose', 'BloodPressure', 'BMI']
        missing_or_empty = [f for f in required_features if not input_data.get(f)]
        if missing_or_empty:
            return jsonify({'error': f'Fill Everything'}), 400

        # Convert 
        new_data = pd.DataFrame([input_data])

        # Make prediction
        prediction = model.predict(new_data)
        result = 'Positive for diabetes' if prediction[0] == 1 else 'Negative for diabetes'
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
