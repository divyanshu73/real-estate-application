import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Price Prediction")

with open("website\df.pkl", "rb") as file:
    df = pickle.load(file)
    
with open("website\pipeline.pkl", "rb") as file:
    pipeline = pickle.load(file)

st.header('Enter your input') 

# values fetching

property_type = st.selectbox('Property Type', ['flat', 'house'])
sector = st.selectbox('Sector', sorted(df['sector'].unique().tolist()))
bedrooms = float(st.selectbox('Number of Bedroom', sorted(df['bedRoom'].unique().tolist())))
bathrooms = float(st.selectbox('Number of Bathrooms', sorted(df['bathroom'].unique().tolist())))
balcony = st.selectbox('Number of Balconies', sorted(df['balcony'].unique().tolist()))
property_age = st.selectbox('Property Age', sorted(df['agePossession'].unique().tolist()))
built_up_area = float(st.number_input('Built Up Area (sq. feet)'))
servant_room = 1.0 if st.selectbox('Servant Room', [True, False]) else 0.0 
store_room = 1.0 if st.selectbox('Store Room', [True, False]) else 0.0
furnishing_type = st.selectbox('Furnishing Type', sorted(df['furnishing_type'].unique().tolist()))
luxury_category = st.selectbox('Luxury Category', sorted(df['luxury_category'].unique().tolist()))
floor_category = st.selectbox('Floor Category', sorted(df['floor_category'].unique().tolist()))

if st.button('Predict'):
    # form a dataframe
    data = [[property_type, sector, bedrooms, bathrooms, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony', 'agePossession', 'built_up_area', 'servant room', 'store room', 'furnishing_type', 'luxury_category', 'floor_category']
    
    # converting to DataFrame
    one_df = pd.DataFrame(data, columns=columns)
    #st.dataframe(one_df)
    
    # predecting the result
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.20
    high = base_price + 0.20
    
    # displaying the result
    st.text("The price of flat is between {} crores and {} crores".format(round(low,3), round(high,3)))
    