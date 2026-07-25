import streamlit as st
import pandas as pd
import requests

# Streamlit UI for Customer Churn Prediction
st.title("SalesForecast_SuperKart_Prediction App")
st.write("Predict SuperKart Sales Forecast based on product sold details. Please Enter information required.")

# Collect user input based on dataset columns
ProductId_input = st.text_input("Product Id (2 chars followed by 4 digits)", max_chars=6)
ProductWeight_input = st.number_input("Product Weight", min_value=0.0, value=0.0)
ProductSugarContent_input = st.selectbox("Product Sugar Content", ["Low Sugar", "No Sugar", "Regular", "reg"])
ProductAllocatedArea_input = st.number_input("Product Allocated Area", min_value=0.0, value=0.0)
ProductType_input = st.selectbox("Product Type", ["Fruits and Vegetables","Snack Foods","Frozen Foods","Dairy ","Household ","Baking Goods","Canned","Health and Hygiene","Meat","Soft Drinks","Breads","Hard Drinks","Others","Starchy Foods","Breakfast","Seafood"])
ProductMRP_input = st.number_input("Product MRP", min_value=0.0, value=0.0)
StoreId_input = st.selectbox("Store Id", ["OUT001", "OUT002", "OUT003", "OUT004"])
StoreEstablishmentYear_input = st.selectbox("Store Establishment Year", ["1987", "1988", "1989", "1990", "1991", "1992", "1993", "1994", "1995", "1996", "1997", "1998", "1999", "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009"]) # Corrected list format
StoreSize_input = st.selectbox("Store Size", ["Small", "Medium", "High"])
StoreLocationCityType_input = st.selectbox("Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"])
StoreType_input = st.selectbox("Store Type", ["Supermarket Type1", "Supermarket Type2", "Food Mart", "Departmental Store"])

product_data = {
    'Product_Id': ProductId_input,
    'Product_Weight': ProductWeight_input,
    'Product_Sugar_Content': ProductSugarContent_input,
    'Product_Allocated_Area': ProductAllocatedArea_input,
    'Product_Type': ProductType_input,
    'Product_MRP': ProductMRP_input,
    'Store_Id': StoreId_input,
    'Store_Establishment_Year': StoreEstablishmentYear_input,
    'Store_Size': StoreSize_input,
    'Store_Location_City_Type': StoreLocationCityType_input,
    'Store_Type': StoreType_input
}

if st.button("Predict", type='primary'):
    response = requests.post("http://backend:7860/v1/product", json=product_data)
    if response.status_code == 200:
        result = response.json()
        prediction = result["Prediction"]
        st.write(f"Based on the information provided, the product's (ID - {ProductId_input}) sales forecast is {prediction}.")
    else:
        st.error("Error in API request")

# Batch Prediction
st.subheader("Batch Prediction")

file = st.file_uploader("Upload CSV file", type=["csv"])
if file is not None:
    if st.button("Predict for Batch", type='primary'):
        response = requests.post("http://backend:7860/v1/productbatch", files={"file": file})    # enter user name and space name before running the cell
        if response.status_code == 200:
            result = response.json()
            st.header("Batch Prediction Results")
            st.write(result)
        else:
            st.error("Error in API request")
            st.write(response.text)
