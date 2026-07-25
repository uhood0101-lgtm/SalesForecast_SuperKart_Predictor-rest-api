import joblib
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app with a name
app = Flask("SalesForecast_SuperKart_Predictor")

# Load the trained churn prediction model
model = joblib.load("SalesForecast_SuperKart_Prediction_v1.0.joblib")

# Define a route for the home page
@app.get('/')
def home():
    return "Welcome to the SuperKart Sales Forecast Predictor API"

# Define an endpoint to predict Sales forecast for a product
@app.post('/v1/product')
def predict_sales():
    # Get JSON data from the request
    sales_data = request.get_json()

    # Extract relevant customer features from the input data
    sample = {
        'Product_Id': sales_data['Product_Id'],
        'Product_Weight': sales_data['Product_Weight'],
        'Product_Allocated_Area': sales_data['Product_Allocated_Area'],
        'Product_MRP': sales_data['Product_MRP'],
        'Store_Establishment_Year': sales_data['Store_Establishment_Year'],
        'Product_Sugar_Content': sales_data['Product_Sugar_Content'],
        'Product_Type': sales_data['Product_Type'],
        'Store_Id': sales_data['Store_Id'],
        'Store_Size': sales_data['Store_Size'],
        'Store_Location_City_Type': sales_data['Store_Location_City_Type'],
        'Store_Type': sales_data['Store_Type']
    }

    # Convert the extracted data into a DataFrame
    input_data = pd.DataFrame([sample])

    # remove Product_Id from data
    input_data = input_data.drop(columns=['Product_Id'])

    # Make a churn prediction using the trained model
    prediction = model.predict(input_data).tolist()[0]

    # Return the prediction as a JSON response
    return jsonify({'Prediction': prediction}) # Corrected key

# Define an endpoint to predict sales for a batch of products
@app.post('/v1/productbatch')
def predict_sales_batch():
    # Get the uploaded CSV file from the request
    file = request.files['file']

    # Read the file into a DataFrame
    input_data = pd.read_csv(file)

    # Store Product_Id for output mapping
    product_ids = input_data['Product_Id'].values.tolist()

    # remove Product_Id from data
    input_data = input_data.drop(columns=['Product_Id'])

    # Make predictions for the batch data
    predictions = model.predict(input_data).tolist()

    # Map predictions to Product_Id
    output_dict = dict(zip(product_ids, predictions))

    return output_dict

# Run the Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
