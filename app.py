# Start by importing the relevant libraries and classes.
import streamlit as st
import pickle
import pandas as pd
# import numpy as np
# import xgboost
# from xgboost import XGBRegressor
# from sklearn.ensemble import RandomForestClassifier

# Import the ML model pipelines created under model_deployment.
pipe = pickle.load(open('pipe_first_innings.pkl', 'rb'))
pipe2 = pickle.load(open('pipe_second_innings.pkl', 'rb'))

# Define a list containing all team values.
teams = ['Australia',
         'England',
         'South Africa',
         'New Zealand',
         'West Indies',
         'India',
         'Bangladesh',
         'Sri Lanka',
         'Pakistan',
         'Zimbabwe',
         'Ireland',
         'Afghanistan']

# Define a list of all possible venues.
cities = ['Manchester',
          'Delhi',
          'Johannesburg',
          'Harare',
          'Centurion',
          'Barbados',
          'Mirpur',
          'Wellington',
          'Adelaide',
          'Dhaka',
          'London',
          'Southampton',
          'Pallekele',
          'Lauderhill',
          'Kolkata',
          'Christchurch',
          'Bangalore',
          'Chittagong',
          'St Kitts',
          'Colombo',
          'Cardiff',
          'Hambantota',
          'Melbourne',
          'St Lucia',
          'Lahore',
          'Cape Town',
          'Nagpur',
          'Sydney',
          'Mount Maunganui',
          'Abu Dhabi',
          'Dubai',
          'Sharjah',
          'Trinidad',
          'Auckland',
          'Mumbai',
          'Durban',
          'Guyana',
          'Chandigarh',
          'Greater Noida',
          'Nottingham',
          'Hamilton']

# Define a title for the webapp.
st.title('T20 Cricket Score & Win Predictor')

# We make two tabs - 1st innings and 2nd innings.
# For 1st innings, we want to predict the score.
# For 2nd innings, we want to predict the win percentage.
tab1, tab2 = st.tabs(["1st Innings", "2nd Innings"])

# Set up the Score Predictor for 1st Innings.
with tab1:
    st.write("Fill out the following fields to get a predicted score for the batting team.")
    # We first design drop down list for team selection.
    col1, col2 = st.columns(2)

    with col1:
        batting_team = st.selectbox('Select batting team', sorted(teams), key=1)
    with col2:
        bowling_team = st.selectbox('Select bowling team', sorted(teams), key=2)

    # Validate that the bowling and batting team are unique.
    is_error = batting_team == bowling_team

    # Display a message if there is an error in the team entry.
    if is_error:
        st.error("The bowling team cannot be the same as the batting team.")

    # Selection of Venue.
    city = st.selectbox('Select city', sorted(cities), key=3)

    # Input of current score, overs done, wickets out.
    col4, col5, col6 = st.columns(3)

    with col4:
        current_score = st.number_input('Current Score', step=1, min_value=0, key=4)
    with col5:
        overs = st.number_input('Overs', min_value=5, max_value=20, key=5)
    with col6:
        wickets = st.number_input('Wickets', min_value=0, max_value=10, key=6)

    # Last five overs runs scored.
    last_five = st.number_input('Runs scored in the last 5 overs', step=1, min_value=0, key=7)

    # Now we program the Predict Score button to use our trained model.
    if st.button('Predict Score', disabled=is_error):
        # Computation for entry to the model.
        balls_left = 120 - (overs*6)
        wickets_left = 10 - wickets
        crr = current_score/overs

        # Define a DataFrame for the input.
        input_df = pd.DataFrame({'batting_team': [batting_team],
                                 'bowling_team': [bowling_team],
                                 'city': [city],
                                 'current_score': [current_score],
                                 'balls_left': [balls_left],
                                 'wickets_left': [wickets_left],
                                 'crr': [crr],
                                 'last_five': [last_five]})

        # Use the model to make a prediction on the input
        result = pipe.predict(input_df)

        # Output the predicted score.
        st.header("Predicted Score - " + str(int(result[0])))

with tab2:
    st.write("Fill out the following fields to get a win probability for both teams.")
    # We first design drop down list for team selection.
    col8, col9 = st.columns(2)

    # The keys have been entered to help streamlit differentiate between similar widgets.
    with col8:
        batting_team = st.selectbox('Select batting team', sorted(teams), key=8)
    with col9:
        bowling_team = st.selectbox('Select bowling team', sorted(teams), key=9)

    # Validate that the bowling and batting team are unique.
    is_error = batting_team == bowling_team

    # Display a message if there is an error in the team entry.
    if is_error:
        st.error("The bowling team cannot be the same as the batting team.")

    # Selection of Venue.
    city = st.selectbox('Select city', sorted(cities), key=10)

    # Input of current score, overs done, wickets out.
    col11, col12, col13 = st.columns(3)

    with col11:
        current_score = st.number_input('Current Score', step=1, min_value=0, key=11)
    with col12:
        overs = st.number_input('Overs', min_value=5, max_value=20, key=12)
    with col13:
        wickets = st.number_input('Wickets', min_value=0, max_value=10, key=13)

    # Last five overs and target score.
    col14, col15 = st.columns(2)

    with col14:
        last_five = st.number_input('Runs scored in the last 5 overs', step=1, min_value=0, key=14)
    with col15:
        target_score = st.number_input('Target Score', step=1, min_value=0, key=15)

    # Now we program the Predict Win button to use our model to generate values.
    if st.button('Predict Win', disabled=is_error):
        # Computation for entry to the model.
        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        crr = current_score / overs

        # Define a DataFrame for the input.
        input_df = pd.DataFrame({'batting_team': [batting_team],
                                 'bowling_team': [bowling_team],
                                 'city': [city],
                                 'current_score': [current_score],
                                 'balls_left': [balls_left],
                                 'wickets_left': [wickets_left],
                                 'crr': [crr],
                                 'last_five': [last_five],
                                 'target_score': [target_score]})

        # Use the model to make a prediction on the input
        result = pipe2.predict_proba(input_df)

        # Output the predicted score.
        # st.header("Predicted Win - " + str(int(result[0])))
        st.header(batting_team + ": " + str(result[0][1]*100) + "%; " +
                  bowling_team + ": " + str(result[0][0]*100) + "%")
