import streamlit as st
from PIL import Image
import pickle
import os
pip install scikit-learn

# Function to load the model safely
def load_model(uploaded_file):
    try:
        return pickle.load(uploaded_file)
    except ModuleNotFoundError as e:
        st.error("Error loading model: scikit-learn is not installed. Install it using `pip install scikit-learn`.")
        return None
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

# Streamlit UI
st.title("🏦 Bank Loan Prediction using Machine Learning")

# Load and display logo (Handling missing logo file)
logo_path = r'D:\lab_ml\SBI-Logo.png'
if os.path.exists(logo_path):
    img1 = Image.open(logo_path).resize((156, 145))
    st.image(img1, use_column_width=True)
else:
    st.warning("⚠️ Logo not found. Proceeding without displaying the logo.")

# Model Upload
uploaded_file = st.file_uploader("📂 D:\lab_ml\Model\ML_Model2.pkl", type="pkl")
model = None
if uploaded_file is not None:
    model = load_model(uploaded_file)

# User Input Fields
account_no = st.text_input('🔢 Account Number')
fn = st.text_input('👤 Full Name')

gen = st.selectbox("⚥ Gender", [0, 1], format_func=lambda x: ["Female", "Male"][x])
mar = st.selectbox("💍 Marital Status", [0, 1], format_func=lambda x: ["No", "Yes"][x])
dep = st.selectbox("👶 Dependents", [0, 1, 2, 3], format_func=lambda x: ["No", "One", "Two", "More than Two"][x])
edu = st.selectbox("🎓 Education", [0, 1], format_func=lambda x: ["Not Graduate", "Graduate"][x])
emp = st.selectbox("💼 Employment Status", [0, 1], format_func=lambda x: ["Job", "Business"][x])
prop = st.selectbox("🏠 Property Area", [0, 1, 2], format_func=lambda x: ["Rural", "Semi-Urban", "Urban"][x])
cred = st.selectbox("💳 Credit Score", [0, 1], format_func=lambda x: ["Between 300 to 500", "Above 500"][x])

# Numeric Inputs
mon_income = st.number_input("💰 Applicant's Monthly Income ($)", value=0)
co_mon_income = st.number_input("💰 Co-Applicant's Monthly Income ($)", value=0)
loan_amt = st.number_input("🏦 Loan Amount ($)", value=0)

# Loan Duration Mapping
dur_display = ['2 Months', '6 Months', '8 Months', '1 Year', '16 Months']
dur_mapping = {0: 60, 1: 180, 2: 240, 3: 360, 4: 480}
dur = st.selectbox("⏳ Loan Duration", list(dur_mapping.keys()), format_func=lambda x: dur_display[x])
duration = dur_mapping[dur]

# Prediction Button
if st.button("🔍 Predict Loan Approval"):
    if model is None:
        st.error("❌ No model loaded! Please upload a trained ML_Model2.pkl file.")
    else:
        # Prepare input features
        features = [[int(gen), int(mar), int(dep), int(edu), int(emp),
                     float(mon_income), float(co_mon_income), float(loan_amt),
                     int(duration), int(cred), int(prop)]]

        try:
            # Make Prediction
            prediction = model.predict(features)
            ans = int(prediction[0])

            # Display Result
            if ans == 0:
                st.error(f"❌ Hello {fn} (Account: {account_no}), You are NOT eligible for the loan.")
            else:
                st.success(f"✅ Hello {fn} (Account: {account_no}), Congratulations! You are eligible for the loan.")
        except Exception as e:
            st.error(f"⚠️ Prediction Error: {e}")
