import streamlit as st
from prediction_helper import predict  # Ensure this is correctly linked to your prediction_helper.py
import base64
import os

# Function to load the image and convert it to a base64 string
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set the path to your local image file
background_image_path = "risk-protection-eliminating-risk-top-view.jpg"  # Update with actual file path
if os.path.exists(background_image_path):
    base64_background = get_base64_of_bin_file(background_image_path)
else:
    base64_background = None

# Set the page configuration and title
st.set_page_config(page_title="Capital Crest Finance: Credit Risk Modelling", page_icon="📊")

# Add custom CSS for background image if available
if base64_background:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{base64_background}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        
        /* Responsive design for mobile */
        @media (max-width: 768px) {{
            .stApp {{
                background-size: contain;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Adding title with white color
st.markdown(
    '<h1 style="color:white;">Capital Crest Finance: Credit Risk Modelling</h1>',
    unsafe_allow_html=True
)

# Main content container for credit risk assessment
st.header("Credit Risk Assessment")
st.markdown(
    '<p style="color:navy;font-weight:bold;">Fill in the details below to assess your credit risk.</p>',
    unsafe_allow_html=True
)

# Input section
st.subheader("Input Parameters")
with st.container():
    age = st.number_input('Age', min_value=18, max_value=100, value=28)
    income = st.number_input('Income (Annual)', min_value=0, value=1200000, format="%d")
    loan_amount = st.number_input('Loan Amount', min_value=0, value=2560000, format="%d")
    
    # Loan to Income Ratio Calculation
    loan_to_income_ratio = loan_amount / income if income > 0 else 0
    st.metric(label="Loan to Income Ratio", value=f"{loan_to_income_ratio:.2f}")
    
    # Additional inputs
    loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=36)
    avg_dpd_per_delinquency = st.number_input('Avg Days Past Due (DPD)', min_value=0, value=20)
    delinquency_ratio = st.number_input('Delinquency Ratio (%)', min_value=0, max_value=100, step=1, value=30)
    credit_utilization_ratio = st.number_input('Credit Utilization Ratio (%)', min_value=0, max_value=100, step=1, value=30)
    num_open_accounts = st.number_input('Number of Open Loan Accounts', min_value=1, max_value=4, step=1, value=2)

    # Dropdowns for additional attributes
    residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])
    loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
    loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])

# Button to calculate risk
if st.button('Calculate Risk'):
    with st.spinner("Calculating..."):
        # Call the predict function from the helper module
        probability, credit_score, rating = predict(
            age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type
        )
        # Display the results
        st.success("Calculation Complete!")
        st.subheader("Results")
        with st.container():
            st.metric(label="Default Probability", value=f"{probability:.2%}")
            st.metric(label="Credit Score", value=f"{credit_score}")
            st.metric(label="Rating", value=f"{rating}")

# Sidebar content
st.sidebar.header("Navigation")
st.sidebar.write("Use the options below to navigate through the app.")
st.sidebar.markdown("### About")
st.sidebar.write("This app is designed for Capital Crest to assess credit risk for loan applicants, evaluating various financial and demographic factors.")
