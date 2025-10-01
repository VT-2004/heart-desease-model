# Heart Disease Prediction System

## Project Overview
This project delivers an end-to-end Heart Disease Prediction System, leveraging machine learning algorithms to assess a patient's risk of developing heart disease based on their health parameters. The system features a user-friendly Flask web application where individuals can input their health data and receive an immediate, detailed prediction report.

## Features
-   **Multi-Model Prediction:** Utilizes several machine learning algorithms (Logistic Regression, K-Nearest Neighbors, Support Vector Machine, Decision Tree, and Random Forest) to provide a comprehensive and robust prediction.
-   **User-Friendly Web Interface:** A Flask-based web application allows users to easily input health parameters through a clean and intuitive form.
-   **Detailed Prediction Report:** Generates a report that includes an overall heart disease risk percentage and individual predictions (High/Low Chance with probabilities) from each trained model.
-   **Robust Input Validation:** Implements both client-side (JavaScript) and server-side (Flask) validation to ensure data integrity and improve user experience.
-   **Informational Pages:** Includes "About Us" and "Disclaimer" pages to provide context, explain the project's technical stack, and clarify the non-medical nature of the predictions.
-   **Deployment Ready:** Configured for easy deployment to cloud platforms using `Gunicorn` and a `Procfile`.

## Machine Learning Models
The following models were trained and evaluated:
-   **Logistic Regression**
-   **K-Nearest Neighbors (KNN)**
-   **Support Vector Machine (SVM)**
-   **Decision Tree**
-   **Random Forest** (Achieved the highest accuracy during initial evaluation)

All trained models, along with the data preprocessors (StandardScaler, OneHotEncoder, and imputers), are saved using `pickle` for efficient loading into the Flask application.

## Technical Stack
-   **Backend:** Python 3.x
-   **Web Framework:** Flask
-   **Machine Learning:** Scikit-learn, Pandas, NumPy
-   **Web Server:** Gunicorn (for production deployment)
-   **Frontend:** HTML5, CSS3, JavaScript
-   **Development Environment:** Google Colab (for ML pipeline), Local Python Environment (for Flask app)

## Project Structure
heart_disease_prediction/
├── app.py # Main Flask application file
├── requirements.txt # List of Python dependencies
├── README.md # Project description, setup, and run instructions
├── trained_models/ # Directory to store all saved ML artifacts
│ ├── heart_disease_models.pkl # Contains all trained ML models (dict of pipelines)
│ ├── heart_disease_preprocessor.pkl # The fitted ColumnTransformer
│ ├── imputer_ca.pkl # Imputer for 'ca' column
│ └── imputer_thal.pkl # Imputer for 'thal' column
├── templates/ # Directory for HTML templates (Jinja2)
│ ├── base.html # Base template for consistent layout
│ ├── index.html # Homepage with input form
│ ├── result.html # Page to display prediction results
│ ├── about.html # About Us page
│ └── disclaimer.html # Disclaimer page
├── static/ # Directory for static assets (CSS, JS, images)
│ ├── css/
│ │ └── style.css # Custom CSS styles
│ └── js/
│ └── script.js # Client-side JavaScript for validation/UX
├── notebooks/ # (Optional) Directory for Jupyter/Colab notebooks
└── heart_disease_ml_pipeline.ipynb # Your Colab notebook with ML code
└── Procfile # Declares process types for deployment (e.g., Heroku, Render)
code
Code
## Setup and Local Development

### 1. Clone the Repository (After initial Git setup)
If you've already initialized your Git repository locally and you are viewing this `README.md`, you can skip this step. Otherwise, if you are downloading this project, treat it as the project root.

### 2. Create a Virtual Environment
It's highly recommended to use a virtual environment to manage project dependencies.
```bash
python -m venv venv
3. Activate the Virtual Environment
Windows PowerShell:
code
Powershell
.\venv\Scripts\Activate.ps1
Windows Command Prompt (cmd.exe):
code
Cmd
venv\Scripts\activate.bat
macOS/Linux/Git Bash:
code
Bash
source venv/bin/activate
(Your prompt should now show (venv) indicating the environment is active.)
4. Install Dependencies
Install all required libraries using the requirements.txt file.
code
Bash
pip install -r requirements.txt
5. Download ML Models and Preprocessors
The trained machine learning models and preprocessing pipelines are stored as .pkl files.
Ensure you have the trained_models directory in your project root, containing:
heart_disease_models.pkl
heart_disease_preprocessor.pkl
imputer_ca.pkl
imputer_thal.pkl
If you followed the ML pipeline development in Google Colab, you would have downloaded these files into this folder.
6. Run the Flask Application
Start the Flask development server.
code
Bash
python app.py
The application will typically run on http://127.0.0.1:5000. Open this URL in your web browser.
7. Run with Gunicorn (Production Test - Optional for Local)
To test how your application would run in a production environment (using Gunicorn), ensure Gunicorn is installed (pip install gunicorn) and run:
code
Bash
gunicorn app:app
This typically runs on http://127.0.0.1:8000.
Deployment
This application is configured for easy deployment to platforms like Heroku, Render, or Railway.
Ensure all changes are committed to a Git repository (e.g., GitHub).
Connect your repository to your chosen deployment platform.
The platform will use requirements.txt to install dependencies and Procfile (with web: gunicorn app:app) to start your application.
Usage
Navigate to the homepage (/).
Fill in the patient's health parameters in the input form.
Client-side validation will provide immediate feedback for invalid inputs.
Click "Get Prediction" to submit the data.
The system will display a detailed prediction report, including an overall risk percentage and individual model predictions.
Disclaimer
This Heart Disease Prediction System is for informational and educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for any medical concerns.
Contributing
(Optional section: Add instructions if you want others to contribute to your project)
License
(Optional section: Specify the license under which your project is released, e.g., MIT, Apache 2.0)
Contact
For any questions or feedback, please contact [Your Name/Email/GitHub Profile Link].