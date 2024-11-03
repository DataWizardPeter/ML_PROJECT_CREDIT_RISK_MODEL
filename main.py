import streamlit as st
from prediction_helper import predict  # Ensure this is correctly linked to your prediction_helper.py
import base64

# Cache the image loading function to avoid reloading each time
@st.cache_data
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set the path to your local image file
background_image = r"risk-protection-eliminating-risk-top-view.jpg"  # Update with your actual file path
base64_background = get_base64_of_bin_file(background_image)

# Set the page configuration and title
st.set_page_config(page_title="Capital Crest Finance: Credit Risk Modelling", page_icon="📊")

# Adding title with light gray color
st.markdown(
    '<h1 style="color:white;">Capital Crest Finance: Credit Risk Modelling</h1>',
    unsafe_allow_html=True
)

# Add custom CSS for background image
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
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar navigation and static content (loads only once)
st.sidebar.header("Navigation")
st.sidebar.write("Use the options below to navigate through the app.")

# Main content container
with st.container():
    st.header("Credit Risk Assessment")
    st.markdown(
        '<p style="color:navy;font-weight:bold;">Fill in the details below to assess your credit risk.</p>',
        unsafe_allow_html=True
    )

    # Input section with a card-like appearance
    st.subheader("Input Parameters")
    input_card = st.container()

    with input_card:
        # Use rows of three columns each for input fields
        row1 = st.columns(3)
        row2 = st.columns(3)
        row3 = st.columns(3)
        row4 = st.columns(3)

        # Assign inputs to the first row with default values
        with row1[0]:
            age = st.number_input('Age', min_value=18, step=1, max_value=100, value=28)
        with row1[1]:
            income = st.number_input('Income (Annual)', min_value=0, value=1200000, format="%d")
        with row1[2]:
            loan_amount = st.number_input('Loan Amount', min_value=0, value=2560000, format="%d")

        # Calculate Loan to Income Ratio
        loan_to_income_ratio = loan_amount / income if income > 0 else 0
        with row2[0]:
            st.metric(label="Loan to Income Ratio", value=f"{loan_to_income_ratio:.2f}")

        # Remaining inputs
        with row2[1]:
            loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=36)
        with row2[2]:
            avg_dpd_per_delinquency = st.number_input('Avg Days Past Due (DPD)', min_value=0, value=20)

        with row3[0]:
            delinquency_ratio = st.number_input('Delinquency Ratio (%)', min_value=0, max_value=100, step=1, value=30)
        with row3[1]:
            credit_utilization_ratio = st.number_input('Credit Utilization Ratio (%)', min_value=0, max_value=100,
                                                       step=1, value=30)
        with row3[2]:
            num_open_accounts = st.number_input('Number of Open Loan Accounts', min_value=1, max_value=4, step=1,
                                                value=2)

        # Input controls for residence type, loan purpose, and loan type
        with row4[0]:
            residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])
        with row4[1]:
            loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
        with row4[2]:
            loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])

    # Cache the prediction function to avoid recalculating for same inputs
    @st.cache_data
    def get_prediction(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                       delinquency_ratio, credit_utilization_ratio, num_open_accounts,
                       residence_type, loan_purpose, loan_type):
        return predict(age, income, loan_amount, loan_tenure_months,
                       avg_dpd_per_delinquency, delinquency_ratio, credit_utilization_ratio, 
                       num_open_accounts, residence_type, loan_purpose, loan_type)

    # Button to calculate risk
    if st.button('Calculate Risk', key='calculate'):
        with st.spinner("Calculating..."):
            # Call the cached prediction function
            probability, credit_score, rating = get_prediction(age, income, loan_amount, loan_tenure_months,
                                                               avg_dpd_per_delinquency, delinquency_ratio, 
                                                               credit_utilization_ratio, num_open_accounts,
                                                               residence_type, loan_purpose, loan_type)

            # Display the results in a card format
            st.success("Calculation Complete!")
            st.subheader("Results")
            results_card = st.container()
            with results_card:
                st.metric(label="Default Probability", value=f"{probability:.2%}")
                st.metric(label="Credit Score", value=f"{credit_score}")
                st.metric(label="Rating", value=f"{rating}")

# Sidebar information about the application (static content)
st.sidebar.markdown("### About")
st.sidebar.write("This application is designed specifically for Capital Crest to assess credit risk for potential loan applicants. Using a custom-built model, the app evaluates various financial and demographic factors to provide a credit risk assessment. This model is fine-tuned to align with Capital Crest's unique lending criteria and risk management goals, ensuring a robust and tailored approach to decision-making.")
