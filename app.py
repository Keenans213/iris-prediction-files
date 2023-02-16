from flask import Flask, jsonify, request
import numpy as np
from joblib import load

# Initialize the app and set a secret_key.
app = Flask(__name__)
app.secret_key = 'something_secret'

# Load the joblib model
MODEL = load('rf_clf.joblib')

# Model features
FEATURES = ['sepal length', 'sepal width', 'petal length', 'petal width']

# Maps model prediction index to target name
idx_to_target = {0: 'setosa', 1: 'versicolor', 2: 'virginica'}

# Parses features from json request
def parse_args(requested_dict):
  x_list = []
  for feature in FEATURES:
    value = requested_dict.get(feature, None)
    if value: 
      x_list.append(value)
    else:
      x_list.append(0)
  return x_list

@app.route('/api', methods=['GET', 'POST'])
def api():
  """Handle request and output model score in json format."""
  # Handle empty requests.
  if not request.json:
    return jsonify({'error': 'no request received'})

  # Parse request args into feature array for prediction.
  x_list = parse_args(request.json)
  x_array = np.array([x_list])

  # Predict on x_array and return JSON response.
  pred = idx_to_target[MODEL.predict(x_array)[0]]
  response = dict(PREDICTION=pred)
  return jsonify(response)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)