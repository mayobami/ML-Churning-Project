import requests

# Customer data to test
customer = {
  'customerid': '8879-zkjof',
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

# Your LIVE AWS URL
url = 'http://churn-serving-env.eba-x267egaj.us-east-1.elasticbeanstalk.com/predict'

print(f"Testing ML Model at: {url}")
response = requests.post(url, json=customer)
print(f"Status Code: {response.status_code}")
print(f"Result: {response.json()}")
