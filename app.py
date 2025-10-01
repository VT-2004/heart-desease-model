import os
import pickle
from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np

# --- Configuration & Global Variables ---
# Get the directory of the current script (app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Define the path to the trained_models directory
MODELS_DIR = os.path.join(BASE_DIR, 'trained_models')

# Define paths to saved artifacts
MODELS_FILE = os.path.join(MODELS_DIR, 'heart_disease_models.pkl')
PREPROCESSOR_FILE = os.path.join(MODELS_DIR, 'heart_disease_preprocessor.pkl')
IMPUTER_CA_FILE = os.path.join(MODELS_DIR, 'imputer_ca.pkl')
IMPUTER_THAL_FILE = os.path.join(MODELS_DIR, 'imputer_thal.pkl')

# Store feature names for consistent ordering during prediction
# This is critical because the preprocessor expects features in a specific order
feature_columns = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach',
    'exang', 'oldpeak', 'slope', 'ca', 'thal'
]

# Mappings for displaying categorical text (for result.html readability)
CP_MAP = {1: 'Typical Angina', 2: 'Atypical Angina', 3: 'Non-anginal Pain', 4: 'Asymptomatic'}
RESTECG_MAP = {0: 'Normal', 1: 'ST-T wave abnormality', 2: 'Probable/definite LV hypertrophy'}
SLOPE_MAP = {1: 'Upsloping', 2: 'Flat', 3: 'Downsloping'}
THAL_MAP = {3: 'Normal', 6: 'Fixed defect', 7: 'Reversible defect'}


# --- Load ML Artifacts ---
# Initialize variables to None. They will be populated if loading is successful.
trained_models = None
preprocessor = None
imputer_ca = None # Keeping these loaded for robustness, though preprocessor pipeline handles main transformation
imputer_thal = None

print("Loading machine learning models and preprocessors...")
try:
    with open(MODELS_FILE, 'rb') as f:
        trained_models = pickle.load(f)
    print(f"Loaded models: {list(trained_models.keys())}")

    with open(PREPROCESSOR_FILE, 'rb') as f:
        preprocessor = pickle.load(f)
    print("Loaded ColumnTransformer preprocessor.")

    with open(IMPUTER_CA_FILE, 'rb') as f:
        imputer_ca = pickle.load(f)
    print("Loaded imputer for 'ca'.")

    with open(IMPUTER_THAL_FILE, 'rb') as f:
        imputer_thal = pickle.load(f)
    print("Loaded imputer for 'thal'.")

except Exception as e:
    print(f"ERROR: Could not load ML artifacts. Please ensure 'trained_models' directory and all .pkl files are present and correct. Details: {e}")
    # Set to empty dict/None to prevent further errors if loading failed
    trained_models = {}
    preprocessor = None
    imputer_ca = None
    imputer_thal = None


# --- Flask Application Setup ---
app = Flask(__name__)


# --- Routes ---

@app.route('/')
def home():
    """Renders the homepage with the input form."""
    return render_template('index.html')

@app.route('/about')
def about():
    """Renders the About Us page."""
    return render_template('about.html')

@app.route('/disclaimer')
def disclaimer():
    """Renders the Disclaimer page."""
    return render_template('disclaimer.html')


@app.route('/predict', methods=['POST'])
def predict():
    # Initial check if ML artifacts are loaded (or if previous loading failed)
    if not trained_models or not preprocessor: # Check if dict is empty or preprocessor is None
        return render_template('result.html',
                               overall_prediction_percentage=0,
                               detailed_predictions={},
                               user_input={},
                               error_message="Server error: Machine learning models or preprocessors not loaded. Please check server logs.")

    user_input_raw = {} # To store raw form data for display
    validation_errors = [] # List to collect all validation errors

    # 1. Get raw input data from form and initial type conversion
    try:
        user_input_raw = {
            'age': float(request.form['age']),
            'sex': float(request.form['sex']),
            'cp': float(request.form['cp']),
            'trestbps': float(request.form['trestbps']),
            'chol': float(request.form['chol']),
            'fbs': float(request.form['fbs']),
            'restecg': float(request.form['restecg']),
            'thalach': float(request.form['thalach']),
            'exang': float(request.form['exang']),
            'oldpeak': float(request.form['oldpeak']),
            'slope': float(request.form['slope']),
            'ca': float(request.form['ca']),
            'thal': float(request.form['thal'])
        }
    except ValueError as e:
        print(f"ValueError in form data: {e}")
        return render_template('result.html',
                               overall_prediction_percentage=0,
                               detailed_predictions={},
                               user_input={},
                               error_message=f"Invalid input format. Please ensure all fields are correctly filled (numbers where expected). Details: {e}")
    except KeyError as e:
        print(f"KeyError in form data: Missing field {e}")
        return render_template('result.html',
                               overall_prediction_percentage=0,
                               detailed_predictions={},
                               user_input={},
                               error_message=f"Missing required input field. Please fill all fields. Missing: {e}")
    except Exception as e:
        print(f"Unexpected error getting form data: {e}")
        return render_template('result.html',
                               overall_prediction_percentage=0,
                               detailed_predictions={},
                               user_input={},
                               error_message=f"An unexpected error occurred processing your input. Details: {e}")

    # --- 2. Server-side Validation of Input Ranges/Values ---
    validation_rules = {
        'age': {'min': 1, 'max': 120}, # Realistic human age
        'sex': {'allowed': [0.0, 1.0]},
        'cp': {'allowed': [1.0, 2.0, 3.0, 4.0]},
        'trestbps': {'min': 80, 'max': 200}, # Common healthy to very high BP
        'chol': {'min': 100, 'max': 600},    # Common healthy to very high cholesterol
        'fbs': {'allowed': [0.0, 1.0]},
        'restecg': {'allowed': [0.0, 1.0, 2.0]},
        'thalach': {'min': 60, 'max': 220},  # Common max heart rate range
        'exang': {'allowed': [0.0, 1.0]},
        'oldpeak': {'min': 0.0, 'max': 6.2}, # Based on dataset max
        'slope': {'allowed': [1.0, 2.0, 3.0]},
        'ca': {'allowed': [0.0, 1.0, 2.0, 3.0]},
        'thal': {'allowed': [3.0, 6.0, 7.0]}
    }

    for feature, value in user_input_raw.items():
        rules = validation_rules.get(feature)
        if rules:
            if 'min' in rules and value < rules['min']:
                validation_errors.append(f"{feature.replace('_', ' ').title()} is too low (min: {rules['min']}).")
            if 'max' in rules and value > rules['max']:
                validation_errors.append(f"{feature.replace('_', ' ').title()} is too high (max: {rules['max']}).")
            if 'allowed' in rules and value not in rules['allowed']:
                # Handle floats in allowed lists
                if not any(np.isclose(value, allowed_val) for allowed_val in rules['allowed']):
                     validation_errors.append(f"{feature.replace('_', ' ').title()} has an invalid value ({int(value) if value.is_integer() else value}). Allowed values: {rules['allowed']}.")


    if validation_errors:
        print(f"Validation errors: {validation_errors}")
        return render_template('result.html',
                               overall_prediction_percentage=0,
                               detailed_predictions={},
                               user_input=user_input_raw, # Pass raw input to display
                               error_message="<br>".join(validation_errors)) # Join errors for display


    # Convert to DataFrame for consistent processing - now confident data is valid
    input_df = pd.DataFrame([user_input_raw], columns=feature_columns)

    # 3. Make predictions with all models
    detailed_predictions = {}
    probabilities = []
    has_true_prob_models = 0

    for model_name, model_pipeline in trained_models.items():
        prediction = None
        prob_positive = None
        try:
            prediction = model_pipeline.predict(input_df)[0]

            if hasattr(model_pipeline, 'predict_proba') and callable(getattr(model_pipeline, 'predict_proba')):
                prob_positive = model_pipeline.predict_proba(input_df)[0][1]
                probabilities.append(prob_positive)
                has_true_prob_models += 1
            else:
                print(f"Warning: {model_name} does not support predict_proba or it's not callable. Using hard prediction as probability for display.")
                prob_positive = float(prediction)
                probabilities.append(prob_positive)

        except Exception as e:
            print(f"Error during prediction for {model_name}: {e}")
            prediction = 0
            prob_positive = 0.5
            probabilities.append(prob_positive)

        detailed_predictions[model_name] = {
            'prediction': int(prediction),
            'probability': prob_positive
        }

    # 4. Calculate overall prediction percentage
    if has_true_prob_models > 0:
        true_probabilities_only = [p for p, model_name in zip(probabilities, trained_models.keys())
                                   if hasattr(trained_models[model_name], 'predict_proba') and callable(getattr(trained_models[model_name], 'predict_proba'))]
        overall_prediction_percentage = np.mean(true_probabilities_only) * 100 if true_probabilities_only else 0
    else:
        overall_prediction_percentage = np.mean([d['prediction'] for d in detailed_predictions.values()]) * 100

    # 5. Prepare user input for display on result page
    user_input_display = user_input_raw.copy()
    user_input_display['cp_text'] = CP_MAP.get(user_input_raw['cp'], 'Unknown')
    user_input_display['restecg_text'] = RESTECG_MAP.get(user_input_raw['restecg'], 'Unknown')
    user_input_display['slope_text'] = SLOPE_MAP.get(user_input_raw['slope'], 'Unknown')
    user_input_display['thal_text'] = THAL_MAP.get(user_input_raw['thal'], 'Unknown')

    final_error_message = None

    return render_template('result.html',
                           overall_prediction_percentage=overall_prediction_percentage,
                           detailed_predictions=detailed_predictions,
                           user_input=user_input_display,
                           error_message=final_error_message)


# --- Run the Flask App ---
if __name__ == '__main__':
    # For development, enable debug mode.
    # For deployment, this should be False.
    app.run(debug=False) # Changed from True to False