import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
col1, col2 = st.columns(2)

def jump_line():
    st.markdown(
    '''
    ''')

# Here we would like to add some controllers in order to ask the user to select the parameters of the ride
#1. Let's ask for:
#- date and time
#- pickup longitude
#- pickup latitude
#- dropoff longitude
#- dropoff latitude
#- passenger count

with st.sidebar:
    n = st.slider('Number of passengers', 1, 10, 1)

    d = st.date_input(
        "Pickup date",
        datetime.now()
        )

    t = st.time_input(
        'Pickup time',
        datetime.now()
        )

    ### Pickup
    pickup_address = st.text_input('Pickup address', 'Statue of Liberty, NY')
    ggeo_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    ggeo_params = {
        'address':pickup_address,
        'key': st.secrets.google_geocoding_api_key
    }
    if pickup_address != '':
        pickup_coords = requests.get(ggeo_url, params = ggeo_params).json().get('results', 'Please first enter a valid address')[0].get('geometry').get('location')
        p_lat = pickup_coords.get('lat', 'Please first enter a valid address')
        p_long = pickup_coords.get('lng', 'Please first enter a valid address')

    ### Dropoff
    dropoff_address = st.text_input('Dropoff address', 'Newark International Airport, NY')
    ggeo_url = 'https://maps.googleapis.com/maps/api/geocode/json'
    ggeo_params = {
        'address':dropoff_address,
        'key': st.secrets.google_geocoding_api_key
    }
    if dropoff_address != '':
        dropoff_coords = requests.get(ggeo_url, params = ggeo_params).json().get('results', 'Please first enter a valid address')[0].get('geometry').get('location')
        d_lat = dropoff_coords.get('lat', 'Please first enter a valid address')
        d_long = dropoff_coords.get('lng', 'Please first enter a valid address')

    persons = 'persons'
    if n == 1:
        persons = 'person'

jump_line()

with col1:
    '''
    # 🚕 Taxi Fare Prediction 🚕
    '''
    ## Welcome to the taxi fare prediction page!
    jump_line()
    st.markdown(
        '''
        *This webpage returns an evaluation of your taxi fare.*

        ⬅️ Just select your **pickup** and **dropoff** locations, a **date & time**, and the **number of people to transport**.
        ''')

    st.write('''### Here is your taxi drive summary:''')
    st.write('⚫ Taxi drive for',n,f'{persons} on',d,'at',t)
    st.write('⚫ Pickup location:', pickup_address)
    st.write('⚫ Dropoff location:', dropoff_address)

    if pickup_address != '' and dropoff_address != '':

        params = {
        'pickup_datetime': str(d) + ' ' + str(t),
        'pickup_longitude': p_long,
        'pickup_latitude': p_lat,
        'dropoff_longitude': d_long,
        'dropoff_latitude': d_lat,
        'passenger_count': n
        }

        url = 'https://taxifare.lewagon.ai/predict'
        jump_line()
        st.write('''**When you are ready:**''')
        if st.button('Evaluate my taxi fare'):
            pred = requests.get(url, params = params).json()
            st.write('### 💰 Your taxi fare is estimated to be', round(pred.get('fare'),2),'$')


# Once we have these, let's call our API in order to retrieve a prediction
# See ? No need to load a `model.joblib` file in this app, we do not even need to know anything about Data Science in order to retrieve a prediction...
# 🤔 How could we call our API ? Off course... The `requests` package 💡
#2. Let's build a dictionary containing the parameters for our API...
#3. Let's call our API using the `requests` package...
#4. Let's retrieve the prediction from the **JSON** returned by the API...
# Finally, we can display the prediction to the user


jump_line()

with col2:

    df = pd.DataFrame(
        [[p_lat,p_long],
        [d_lat,d_long]],
        columns=['lat', 'lon'])

    st.map(df)

#if url == 'https://taxifare.lewagon.ai/predict':
#    st.markdown('Maybe you want to use your own API for the prediction, not the one provided by Le Wagon...')
