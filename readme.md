# Machine Learning Model Deployment Flow

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