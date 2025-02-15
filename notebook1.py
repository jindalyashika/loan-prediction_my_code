import streamlit as st
import pickle
import os
from PIL import Image

# ✅ Step 1: Ensure scikit-learn is installed
try:
    import sklearn
except ModuleNotFoundError:
    st.error("❌ Error: scikit-learn is not installed. Install it using `pip install scikit-learn`.")
    st.stop()

# ✅ Step 2: Upload Model File
st.title("🏦 Bank Loan Prediction using Machine Learning")

uploaded_file = st.file_uploader("📤 D:\lab_ml\Model\ML_Model2.pkl", type="pkl")

# Load model
model = None
if uploaded_file is not None:
    try:
        model = pickle.load(uploaded_file)
        st.success("✅ Model successfully loaded!")
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        model = None

# ✅ Step 3: Display Logo (with error handling)
logo_path = r"D:\lab_ml\SBI-Logo.png"

try:
    img = Image.open(logo_path)
    img = img.resize((156, 145))
    st.image(img, use_column_width=False)
except FileNotFoundError:
    st.warning("⚠️ Logo not found. Proceeding without displaying the logo.")

# ✅ Step 4: Collect User Inputs
account_no = st.text_input('📌 Account Number')
fn = st.text_input('👤 Full Name')

# Selection Inputs
gen = st.selectbox("👩‍💼 Gender", [0, 1], format_func=lambda x: ["Female", "Male"][x])
mar = st.selectbox("💍 Marital Status", [0, 1], format_func=lambda x: ["No", "Yes"][x])
dep = st.selectbox("👨‍👩‍👧 Dependents", [0, 1, 2, 3], format_func=lambda x: ["No", "One", "Two", "More than Two"][x])
edu = st.selectbox("🎓 Education", [0, 1], format_func=lambda x: ["Not Graduate", "Graduate"][x])
emp = st.selectbox("💼 Employment Status", [0, 1], format_func=lambda x: ["Job", "Business"][x])
prop = st.selectbox("🏠 Property Area", [0, 1, 2], format_func=lambda x: ["Rural", "Semi-Urban", "Urban"][x])
cred = st.selectbox("💳 Credit Score", [0, 1], format_func=lambda x: ["Between 300 to 500", "Above 500"][x])

# Numeric Inputs
mon_income = st.number_input("💰 Applicant's Monthly Income ($)", value=0)
co_mon_income = st.number_input("💰 Co-Applicant's Monthly Income ($)", value=0)
loan_amt = st.number_input("🏦 Loan Amount", value=0)

# Loan Duration Mapping
dur_display = ['2 Months', '6 Months', '8 Months', '1 Year', '16 Months']
dur_mapping = {0: 60, 1: 180, 2: 240, 3: 360, 4: 480}
dur = st.selectbox("⏳ Loan Duration", list(dur_mapping.keys()), format_func=lambda x: dur_display[x])
duration = dur_mapping[dur]

# ✅ Step 5: Submit and Predict
if st.button("🚀 Submit"):
    if model is None:
        st.error("❌ No model loaded! Please upload a trained `ML_Model2.pkl` file.")
    else:
        # Prepare input for model
        features = [[int(gen), int(mar), int(dep), int(edu), int(emp),
                     float(mon_income), float(co_mon_income), float(loan_amt),
                     int(duration), int(cred), int(prop)]]

        # Make Prediction
        prediction = model.predict(features)
        ans = int(prediction[0])

        # Display Result
        if ans == 0:
            st.error(f"❌ Hello, {fn} (Account No: {account_no})\n\n"
                     "Unfortunately, you **will NOT get the loan** based on our prediction.")
        else:
            st.success(f"🎉 Hello, {fn} (Account No: {account_no})\n\n"
                       "Congratulations! 🎊 You **will get the loan** based on our prediction.")

