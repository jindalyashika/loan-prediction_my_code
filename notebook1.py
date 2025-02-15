import streamlit as st
import pickle
import os
from PIL import Image

# Title
st.title("Bank Loan Prediction using Machine Learning")

# Load and display logo
logo_path = "D:/lab_ml/SBI-Logo.png"  # Update this path if incorrect
if os.path.exists(logo_path):
    img1 = Image.open(logo_path)
    img1 = img1.resize((156, 145))
    st.image(img1, use_column_width=False)
else:
    st.warning("⚠️ Logo not found. Proceeding without displaying the logo.")

# Upload Model File
uploaded_file = st.file_uploader("D:\lab_ml\Model\ML_Model2.pkl", type="pkl")

# Load model after upload
if uploaded_file is not None:
    try:
        model = pickle.load(uploaded_file)
        st.success("✅ Model successfully loaded!")
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        model = None
else:
    st.warning("⚠️ No model loaded! Please upload a trained ML_Model2.pkl file.")
    model = None

# Loan Prediction Form
if model:
    account_no = st.text_input('Account Number')
    fn = st.text_input('Full Name')

    # User Inputs
    gen = st.selectbox("Gender", [0, 1], format_func=lambda x: ["Female", "Male"][x])
    mar = st.selectbox("Marital Status", [0, 1], format_func=lambda x: ["No", "Yes"][x])
    dep = st.selectbox("Dependents", [0, 1, 2, 3], format_func=lambda x: ["No", "One", "Two", "More than Two"][x])
    edu = st.selectbox("Education", [0, 1], format_func=lambda x: ["Not Graduate", "Graduate"][x])
    emp = st.selectbox("Employment Status", [0, 1], format_func=lambda x: ["Job", "Business"][x])
    prop = st.selectbox("Property Area", [0, 1, 2], format_func=lambda x: ["Rural", "Semi-Urban", "Urban"][x])
    cred = st.selectbox("Credit Score", [0, 1], format_func=lambda x: ["Between 300 to 500", "Above 500"][x])

    # Numeric Inputs
    mon_income = st.number_input("Applicant's Monthly Income($)", value=0)
    co_mon_income = st.number_input("Co-Applicant's Monthly Income($)", value=0)
    loan_amt = st.number_input("Loan Amount", value=0)

    # Loan Duration Mapping
    dur_display = ['2 Months', '6 Months', '8 Months', '1 Year', '16 Months']
    dur_mapping = {0: 60, 1: 180, 2: 240, 3: 360, 4: 480}
    dur = st.selectbox("Loan Duration", list(dur_mapping.keys()), format_func=lambda x: dur_display[x])
    duration = dur_mapping[dur]

    # Submit Button
    if st.button("Submit"):
        # Prepare input for model
        features = [[int(gen), int(mar), int(dep), int(edu), int(emp),
                     float(mon_income), float(co_mon_income), float(loan_amt),
                     int(duration), int(cred), int(prop)]]

        # Make Prediction
        prediction = model.predict(features)
        ans = int(prediction[0])

        # Display Result
        if ans == 0:
            st.error(f"❌ Hello {fn}, Account No: {account_no} — You will NOT get the loan.")
        else:
            st.success(f"🎉 Hello {fn}, Account No: {account_no} — Congratulations! You WILL get the loan.")

