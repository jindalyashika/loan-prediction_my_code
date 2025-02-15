import streamlit as st
from PIL import Image
import pickle
import numpy as np
import os

# Load Model with Error Handling
def load_model():
    uploaded_file = st.file_uploader("📂 D:\lab_ml\Model\ML_Model2.pkl", type="pkl")
    if uploaded_file is not None:
        try:
            model = pickle.load(uploaded_file)
            st.success("✅ Model loaded successfully!")
            return model
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            return None
    else:
        st.warning("⚠ No model loaded! Please upload a trained ML_Model2.pkl file.")
        return None

# Load Logo with Error Handling
def load_logo():
    try:
        img = Image.open("SBI-Logo.png")
        img = img.resize((156, 145))
        st.image(img, use_column_width=False)
    except FileNotFoundError:
        st.warning("⚠ Logo not found. Proceeding without displaying the logo.")

# Run the Streamlit App
def run():
    st.title("🏦 Bank Loan Prediction using Machine Learning")
    
    # Display Logo
    load_logo()

    # Load the Model
    model = load_model()
    
    if model is None:
        return  # Stop execution if model isn't loaded
    
    # User Inputs
    account_no = st.text_input('📌 Account Number')
    fn = st.text_input('👤 Full Name')

    # Categorical Inputs
    gen = st.selectbox("🧑‍🤝‍🧑 Gender", [0, 1], format_func=lambda x: ["Female", "Male"][x])
    mar = st.selectbox("💍 Marital Status", [0, 1], format_func=lambda x: ["No", "Yes"][x])
    dep = st.selectbox("👨‍👩‍👧‍👦 Dependents", [0, 1, 2, 3], format_func=lambda x: ["No", "One", "Two", "More than Two"][x])
    edu = st.selectbox("🎓 Education", [0, 1], format_func=lambda x: ["Not Graduate", "Graduate"][x])
    emp = st.selectbox("💼 Employment Status", [0, 1], format_func=lambda x: ["Job", "Business"][x])
    cred = st.selectbox("💳 Credit Score", [0, 1], format_func=lambda x: ["Between 300 to 500", "Above 500"][x])
    prop = st.selectbox("🏡 Property Area", [0, 1, 2], format_func=lambda x: ["Rural", "Semi-Urban", "Urban"][x])

    # NEW: Loan History (Missing Feature)
    loan_history = st.selectbox("📜 Loan History", [0, 1], format_func=lambda x: ["No", "Yes"][x])

    # Numeric Inputs
    mon_income = st.number_input("💰 Applicant's Monthly Income ($)", value=0)
    co_mon_income = st.number_input("💰 Co-Applicant's Monthly Income ($)", value=0)
    loan_amt = st.number_input("💵 Loan Amount", value=0)

    # Loan Duration Mapping
    dur_display = ['2 Months', '6 Months', '8 Months', '1 Year', '16 Months']
    dur_mapping = {0: 60, 1: 180, 2: 240, 3: 360, 4: 480}
    dur = st.selectbox("🕒 Loan Duration", list(dur_mapping.keys()), format_func=lambda x: dur_display[x])
    duration = dur_mapping[dur]

    # Submit Button
    if st.button("🚀 Predict Loan Approval"):
        # Prepare input for model (Now 12 Features!)
        features = np.array([[gen, mar, dep, edu, emp, mon_income, co_mon_income, loan_amt, duration, cred, prop, loan_history]])
        
        # Check Feature Mismatch
        expected_features = model.n_features_in_
        if features.shape[1] != expected_features:
            st.error(f"❌ Feature mismatch! Model expects {expected_features} features, but received {features.shape[1]}.")
            return
        
        try:
            # Make Prediction
            prediction = model.predict(features)
            
            # Ensure prediction is not empty
            if prediction is None or len(prediction) == 0:
                st.error("❌ Error: Model returned an empty prediction.")
                return
            
            ans = int(prediction[0])  # Convert prediction to integer safely
            
            # Display Result
            if ans == 0:
                st.error(f"❌ Sorry, {fn} ({account_no}), you are NOT eligible for the loan.")
            else:
                st.success(f"🎉 Congratulations, {fn} ({account_no})! You are eligible for the loan.")
        
        except Exception as e:
            st.error(f"❌ Error making prediction: {str(e)}")

# Run the app
run()
