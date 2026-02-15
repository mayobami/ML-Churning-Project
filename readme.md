# Customer Churn Prediction Model

A machine learning project that predicts whether telecom customers will churn (leave the service), deployed as a REST API on AWS.

## What This Project Does

Ever wondered if you could predict which customers are about to cancel their subscription? This project does exactly that. It uses historical customer data to train a logistic regression model that predicts the likelihood of customer churn. The model is wrapped in a Flask web service and deployed to AWS Elastic Beanstalk, making it accessible from anywhere via a simple HTTP request.

**Live Demo:** The API is deployed at `http://churn-serving-env.eba-x267egaj.us-east-1.elasticbeanstalk.com/predict`

## Why I Built This

This project was part of my journey to learn:
- How to containerize ML models with Docker
- Deploying ML applications to the cloud
- Building production-ready APIs
- End-to-end ML workflow from training to deployment

## Tech Stack

- **Python 3.10** - Core programming language
- **Scikit-learn** - Model training (Logistic Regression)
- **Pandas & NumPy** - Data processing
- **Flask** - Web framework for the API
- **Waitress** - Production WSGI server
- **Docker** - Containerization
- **AWS Elastic Beanstalk** - Cloud deployment
- **WSL2** - Development environment

## Project Structure

```
ML-Churning-Project/
├── data-week-3.csv          # Training dataset
├── train.py                 # Model training script
├── predict.py               # Flask API service
├── Predict-test.py          # Local testing script
├── test-cloud.py            # AWS deployment test
├── test-web.html            # Web interface for testing
├── model_C=1.0.bin          # Trained model (pickled)
├── Dockerfile               # Container configuration
├── Pipfile & Pipfile.lock   # Python dependencies
└── readme.md                # This file
```

## How It Works

### 1. Data & Training

The model uses customer data including:
- Demographics (gender, senior citizen status)
- Account info (tenure, contract type)
- Services (phone, internet, streaming)
- Billing (monthly charges, payment method)

The training script (`train.py`) trains a logistic regression model with regularization parameter C=1.0, achieving about 84% accuracy.

### 2. The API

The Flask app (`predict.py`) exposes a `/predict` endpoint that:
- Accepts customer data as JSON
- Runs it through the trained model
- Returns churn probability and a yes/no prediction

### 3. Containerization

The entire application is packaged in a Docker container that:
- Uses Python 3.10 slim base image
- Installs all dependencies
- Trains the model during build (ensures version compatibility)
- Runs on port 80 for AWS compatibility

### 4. Cloud Deployment

Deployed to AWS Elastic Beanstalk which handles:
- Server provisioning
- Load balancing
- Auto-scaling
- Health monitoring

## Running Locally

### Prerequisites
- Python 3.10+
- Docker installed
- WSL2 (if on Windows)

### Option 1: Run with Python

```bash
# Install dependencies
pipenv install

# Activate virtual environment
pipenv shell

# Train the model
python train.py

# Start the server
python predict.py

# Test it (in another terminal)
python Predict-test.py
```

### Option 2: Run with Docker

```bash
# Start Docker daemon (WSL)
sudo dockerd &

# Build the image
docker build -t churn-prediction .

# Run the container
docker run -p 9696:9696 churn-prediction

# Test it
python Predict-test.py
```

## Using the API

### Example Request

```python
import requests

customer = {
    'gender': 'female',
    'seniorcitizen': 0,
    'partner': 'no',
    'dependents': 'no',
    'tenure': 41,
    'phoneservice': 'yes',
    'multiplelines': 'no',
    'internetservice': 'dsl',
    'onlinesecurity': 'yes',
    'onlinebackup': 'no',
    'deviceprotection': 'yes',
    'techsupport': 'yes',
    'streamingtv': 'yes',
    'streamingmovies': 'yes',
    'contract': 'one_year',
    'paperlessbilling': 'yes',
    'paymentmethod': 'bank_transfer_(automatic)',
    'monthlycharges': 79.85,
    'totalcharges': 3320.75
}

url = 'http://churn-serving-env.eba-x267egaj.us-east-1.elasticbeanstalk.com/predict'
response = requests.post(url, json=customer)
print(response.json())
```

### Example Response

```json
{
    "churn": false,
    "churn_probability": 0.06763086556091738
}
```

This means the customer has a 6.76% chance of churning (low risk).

### Web Interface Demo

I also built a simple web page (`test-web.html`) that lets you test the API without writing code:

**For local use:**
```bash
# Open the test page in your browser
Start-Process test-web.html
```

**For others to use:**
1. Clone this repo
2. Open `test-web.html` in any browser
3. Fill in customer details and click "Predict Churn"

The page provides a form where you can:
- Enter customer details (gender, tenure, charges, etc.)
- Click "Predict Churn" button
- See results instantly from the live AWS API

**Try it out:** Change values like contract type from "Month-to-month" to "Two year" and watch the churn probability drop!

**Note:** The web demo requires the AWS API to be running. Make sure the environment is deployed before testing.

## Deploying to AWS

### Setup

1. **Install AWS EB CLI:**
```bash
pipenv install awsebcli --dev
```

2. **Configure AWS credentials:**
Create `~/.aws/credentials`:
```ini
[eb-cli]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

3. **Initialize EB application:**
```bash
pipenv run eb init -p docker churn-prediction --region us-east-1
```

### Deploy

```bash
# Create environment and deploy
pipenv run eb create churn-serving-env

# Check status
pipenv run eb status

# View logs
pipenv run eb logs

# Update after changes
pipenv run eb deploy
```

### Terminate (to stop charges)

```bash
pipenv run eb terminate churn-serving-env
```

## Challenges & Solutions

### Problem 1: WSL Issues
**Issue:** Docker Desktop wouldn't start due to outdated WSL version.

**Solution:** Installed Docker directly in WSL Ubuntu instead of using Docker Desktop. This actually works better for development.

### Problem 2: Model Version Mismatch
**Issue:** Model trained with scikit-learn 1.8.0 but container had 1.7.2.

**Solution:** Retrain the model during Docker build to ensure version compatibility. Added `RUN python train.py` to Dockerfile.

### Problem 3: Port Configuration
**Issue:** Container exposed port 9696 but AWS expects port 80.

**Solution:** Changed Dockerfile to use port 80 for production. For local development, you can still use 9696.

### Problem 4: CORS Errors
**Issue:** Web browser couldn't access API due to CORS restrictions.

**Solution:** Added flask-cors to allow cross-origin requests from web applications.

## What I Learned

1. **Docker isn't just for deployment** - It solved my dependency hell and made everything reproducible.

2. **Cloud deployment is tricky** - Port configurations, health checks, and environment variables matter more than you think.

3. **The model is only 20% of the work** - Most of the effort goes into packaging, deploying, and making it accessible.

4. **WSL is powerful** - Running Linux tools on Windows without dual-booting is game-changing for development.

5. **Always test in production-like environments** - What works locally might fail in the cloud for subtle reasons.

## Future Improvements

- [ ] Add a proper web frontend (React or Vue)
- [ ] Implement model versioning and A/B testing
- [ ] Add authentication/API keys
- [ ] Set up CI/CD pipeline
- [ ] Add monitoring and logging (CloudWatch)
- [ ] Retrain model periodically with new data
- [ ] Try different models (XGBoost, Random Forest)
- [ ] Add data validation and error handling

## Dataset

The dataset contains telecom customer information with features like:
- Customer demographics
- Service subscriptions
- Account information
- Churn label (target variable)

**Note:** This is a practice dataset used for learning purposes.

## License

This project is open source and available for educational purposes.

## Contact

Feel free to reach out if you have questions or want to collaborate!

---

**Note:** If you're running this project, remember to terminate your AWS environment when done to avoid charges: `pipenv run eb terminate churn-serving-env`

---

## Original Architecture Documentation

This project uses a **Client-Server architecture** to deploy a machine learning model as a web service. This setup separates the model logic from the testing environment, a standard pattern for production APIs.

---

## 🏗️ Architecture Components

### 1. `predict.py` (The Server)
* **Role:** Flask web service.
* **Functionality:** * Runs continuously, listening on `http://localhost:9696`.
    * Loads the pre-trained machine learning model.
    * **The POST Method:** It defines a specific "route" (endpoint) that is configured to only accept **POST** requests. It extracts the customer data from the body of this request.
    * Returns model predictions formatted as **JSON**.

### 2. `predict-test.py` (The Client)
* **Role:** Test script/Consumer.
* **Functionality:**
    * **The POST Method:** It uses a library (like `requests`) to "push" or **POST** customer data to the server's URL.
    * Receives the prediction response.
    * Prints the results to the console for verification.

---

## 💻 Code Snippets: Where POST Happens

### The Server Side (`predict.py`)
In Flask, we specify `methods=['POST']` to tell the server to listen for data being sent to it.

```python
from flask import Flask, request, jsonify

app = Flask('churn')

# We specify POST here because we are receiving data
@app.route('/predict', methods=['POST'])
def predict():
    customer = request.get_json()  # This gets the data sent by the POST request
    
    # ... (Model prediction logic happens here) ...
    
    result = {
        'churn_probability': 0.25,
        'churn': False
    }
    return jsonify(result)