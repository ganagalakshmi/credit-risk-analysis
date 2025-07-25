import streamlit as st
import joblib
import numpy as np

# Load the best model
best_model = joblib.load('best_model.joblib')

# Custom CSS to style the Analyze button
st.markdown(
    """
    <style>
    div.stButton > button {
        background-color: indigo;
        color: white;
        border-radius: 10px;
        padding: 10px;
        font-size: 16px;
    }
    div.stButton > button:hover {
        background-color: #4b0082;  /* Darker indigo when hovered */
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app layout
#st.title("Credit Risk Analysis App 🚀")

# Custom title with indigo background
st.markdown(
    '<h1 style="background-color: indigo; color: white; padding: 10px; text-align: center;">Credit Risk Analysis App 🚀</h1>',
    unsafe_allow_html=True
)

# Input fields based on your dataset columns
person_age = st.number_input('Age of the borrower', min_value=18, max_value=100)
person_income = st.number_input('Annual Income of the borrower', min_value=0)
person_home_ownership = st.selectbox('Home Ownership', ['Mortgage', 'Own', 'Rent'])
person_emp_length = st.number_input('Length of Employment (years)', min_value=0)
loan_intent = st.selectbox('Loan Intent', ['Education', 'Home Improvement', 'Debt Consolidation', 'Medical', 'Personal', 'Venture'])
loan_grade = st.selectbox('Loan Grade', ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
loan_amnt = st.number_input('Loan Amount', min_value=0)
loan_int_rate = st.number_input('Interest Rate (%)', min_value=0.0, max_value=100.0)

# Automatically calculate loan percent of income
if person_income > 0:
    loan_percent_income = (loan_amnt / person_income) * 100
else:
    loan_percent_income = 0.0  # Set loan percent income to 0 if person_income is 0

# Display the calculated loan percent of income
st.write(f'Loan Percent of Income: {loan_percent_income:.2f}%')

cb_person_default_on_file = st.selectbox('Previous Defaults on File', ['Yes', 'No'])
cb_person_cred_hist_length = st.number_input('Credit History Length (years)', min_value=0)

# Convert categorical variables to numerical (example of label encoding)
person_home_ownership_encoded = 1 if person_home_ownership == 'Own' else 0
loan_intent_encoded = {'Education': 0, 'Home Improvement': 1, 'Debt Consolidation': 2, 'Medical': 3, 'Personal': 4, 'Venture': 5}[loan_intent]
loan_grade_encoded = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}[loan_grade]
cb_person_default_on_file_encoded = 1 if cb_person_default_on_file == 'Yes' else 0

# Create input data in the format the model expects
input_data = np.array([[person_age, person_income, person_home_ownership_encoded, person_emp_length, loan_intent_encoded, loan_grade_encoded, 
                        loan_amnt, loan_int_rate, loan_percent_income, cb_person_default_on_file_encoded, cb_person_cred_hist_length]])

# Ensure input data is numerical (remove NaN values)
input_data = np.nan_to_num(input_data)


# Function to display colored text based on risk level
def display_colored_risk(risk_label):
    if risk_label == 'Low risk of default':
        st.markdown(f'<div style="background-color: #90EE90; padding: 10px;">{risk_label}</div>', unsafe_allow_html=True)  # Green background
    elif risk_label == 'Medium risk of default':
        st.markdown(f'<div style="background-color: #FFFF00; padding: 10px;">{risk_label}</div>', unsafe_allow_html=True)  # Yellow background
    else:
        st.markdown(f'<div style="background-color: #FF6347; padding: 10px;">{risk_label}</div>', unsafe_allow_html=True)  # Red background

# Make prediction
if st.button('Analyze 🔍'):
    prediction_proba = best_model.predict_proba(input_data)

    # Get the probability of default (class 1)
    default_probability = prediction_proba[0][1]

    # Map prediction to risk categories based on the new probability thresholds
    if default_probability < 0.5:
        risk_label = 'Low risk of default'
    elif 0.5 <= default_probability < 0.7:
        risk_label = 'Medium risk of default'
    else:
        risk_label = 'High risk of default'
    
     # Display prediction with color-coded risk levels
    display_colored_risk(risk_label)
     
     
    #st.write(f'Prediction: {risk_label}')
