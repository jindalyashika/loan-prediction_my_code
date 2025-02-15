import streamlit as st
import numpy as np
import pickle
from PIL import Image
import os

# Function to load the model safely
def load_model(uploaded_file):
    try:
        if uploaded_file is not None:
            model = pickle.load(uploaded_file)
            return model
        else:
            st.error("❌ No model loaded! Please upload a trained ML_Model2.pkl file.")
            return None
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        return None

# Streamlit UI
def run():
    st.title("🏦 Bank Loan Prediction using Machine Learning")

    # Load and display logo
    logo_path = "D:/lab_ml/SBI-Logo.png"  # Update this path if necessary
    if os.path.exists(logo_path):
        img1 = Image.open(logo_path).resize((156, 145))
        st.image(img1, use_column_width=False)
    else:
        st.warning("⚠️ Logo not found. Proceeding without displaying the logo.")

    # Upload model file
    uploaded_file = st.file_uploader("📂 D:\lab_ml\Model\ML_Model2.pkl", type="pkl")
    model = load_model(uploaded_file)

    # Ensure the model is loaded before proceeding
    if model is None:
        return

    # User Inputs
    account_no = st.text_input("📌 Account Number")
    fn = st.text_input("🧑 Full Name")

    # Dropdown selections for categorical features
    gen = st.selectbox("👤 Gender", [0, 1], format_func=lambda x: ["Female", "Male"][x])
    mar = st.selectbox("💍 Marital Status", [0, 1], format_func=lambda x: ["No", "Yes"][x])
    dep = st.selectbox("👶 Dependents", [0, 1, 2, 3], format_func=lambda x: ["No", "One", "Two", "More than Two"][x])
    edu = st.selectbox("🎓 Education", [0, 1], format_func=lambda x: ["Not Graduate", "Graduate"][x])
    emp = st.selectbox("💼 Employment Status", [0, 1], format_func=lambda x: ["Job", "Business"][x])
    prop = st.selectbox("🏠 Property Area", [0, 1, 2], format_func=lambda x: ["Rural", "Semi-Urban", "Urban"][x])
    cred = st.selectbox("💳 Credit Score", [0, 1], format_func=lambda x: ["Between 300 to 500", "Above 500"][x])

    # **🆕 Missing Feature Added: Self-Employed**
    self_emp = st.selectbox("👔 Self Employed", [0, 1], format_func=lambda x: ["No", "Yes"][x])  # New Feature

    # Numeric Inputs
    mon_income = st.number_input("💰 Applicant's Monthly Income ($)", min_value=0)
    co_mon_income = st.number_input("💰 Co-Applicant's Monthly Income ($)", min_value=0)
    loan_amt = st.number_input("💵 Loan Amount", min_value=0)

    # Loan Duration Selection
    dur_display = ["2 Months", "6 Months", "8 Months", "1 Year", "16 Months"]
    dur_mapping = {0: 60, 1: 180, 2: 240, 3: 360, 4: 480}
    dur = st.selectbox("⏳ Loan Duration", list(dur_mapping.keys()), format_func=lambda x: dur_display[x])
    duration = dur_mapping[dur]

    # Submit Button
    if st.button("🚀 Submit"):
        # Prepare input for model (NOW 12 FEATURES!)
        features = np.array([[gen, mar, dep, edu, emp, self_emp, mon_income, co_mon_income, loan_amt, duration, cred, prop]])

        # Check if model expects more features
        expected_features = getattr(model, "n_features_in_", None)
        if expected_features and features.shape[1] != expected_features:
            st.error(f"❌ Feature mismatch! Model expects {expected_features} features, but received {features.shape[1]}.")
            return

        # Debugging Information
        st.write("🛠 **Debug - Features going into the model:**")
        st.dataframe(features)

        # Make Prediction
        try:
            prediction = model.predict(features)
            ans = int(prediction[0])

            # Display Result
            if ans == 0:
                st.error(f"❌ Hello {fn} (Account No: {account_no}) – You will NOT get the loan from the bank.")
            else:
                st.success(f"🎉 Congratulations {fn} (Account No: {account_no}) – You WILL get the loan from the bank.")
        except Exception as e:
            st.error(f"❌ Error making prediction: {e}")

# Run the Streamlit app
if __name__ == "__main__":
    run()
