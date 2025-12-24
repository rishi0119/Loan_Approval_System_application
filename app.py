import streamlit as st
import pandas as pd
import pickle as pk
import math

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Loan Approval System",
    page_icon="🏦",
    layout="wide"
)

# -------------------- CLEAN DARK UI CSS --------------------
st.markdown("""
<style>
.stApp {
    background-color: #0b0f14;
    color: #e5e7eb;
}

h1 {
    color: #f9fafb;
}

.section {
    background-color: #111827;
    padding: 24px;
    margin-bottom: 28px;
    border-radius: 10px;
    border: 1px solid #1f2937;
}

.section-header {
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 18px;
    color: #f9fafb;
}

.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border: none;
}

.metric {
    font-size: 18px;
    font-weight: 600;
}

.credit-good { color: #22c55e; }
.credit-mid { color: #facc15; }
.credit-bad { color: #ef4444; }
</style>
""", unsafe_allow_html=True)

# -------------------- TITLE --------------------
st.title("🏦 Smart Loan Approval System")
st.caption("Eligibility • EMI • Risk • Confidence • ML-Based Decision")
st.divider()

# -------------------- LOAD MODEL --------------------
model = pk.load(open("model.pkl", "rb"))
scaler = pk.load(open("scaler.pkl", "rb"))

# ==================== APPLICANT DETAILS ====================

st.markdown("<div class='section-header'>👤 Applicant Details</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    no_of_dep = st.slider("Dependents", 0, 5)
    grad = st.selectbox("Education", ["Graduated", "Not Graduated"])
    self_emp = st.selectbox("Self Employed?", ["Yes", "No"])

with col2:
    Annual_Income = st.slider("Annual Income (₹)", 0, 20000000)
    Assets = st.slider("Total Assets (₹)", 0, 20000000)
    Cibil = st.slider("CIBIL Score (Higher is Better)", 300, 900, 750)

# Credit indicator
st.progress((Cibil - 300) / 600)

if Cibil < 550:
    st.markdown("<span class='credit-bad'>🔴 Poor Credit</span>", unsafe_allow_html=True)
elif Cibil < 650:
    st.markdown("<span class='credit-mid'>🟡 Fair Credit</span>", unsafe_allow_html=True)
elif Cibil < 750:
    st.markdown("<span class='credit-mid'>🟡 Good Credit</span>", unsafe_allow_html=True)
else:
    st.markdown("<span class='credit-good'>🟢 Excellent Credit</span>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ==================== LOAN DETAILS ====================
st.markdown("<div class='section-header'>📄 Loan Details</div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    Loan_Amount = st.slider("Loan Amount (₹)", 0, 20000000)

with col4:
    Loan_Dur = st.slider("Loan Tenure (Years)", 1, 20)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------- ENCODING --------------------
grad_s = 0 if grad == "Graduated" else 1
emp_s = 0 if self_emp == "No" else 1

# -------------------- EMI CALCULATION --------------------
interest_rate = 0.10
monthly_rate = interest_rate / 12
months = Loan_Dur * 12

if Loan_Amount > 0:
    EMI = (Loan_Amount * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
else:
    EMI = 0

monthly_income = Annual_Income / 12

# ==================== ACTION ====================
st.divider()
if st.button("🔍 Evaluate Loan Application"):

    rejection_reasons = []

    if Annual_Income < 300000:
        rejection_reasons.append("Annual income below ₹3,00,000")

    if Cibil < 650:
        rejection_reasons.append("CIBIL score below 650")

    if Loan_Amount > Annual_Income * 5:
        rejection_reasons.append("Loan amount too high compared to income")

    if EMI > monthly_income * 0.4:
        rejection_reasons.append("EMI exceeds 40% of monthly income")

    # -------------------- REJECTION --------------------
    if rejection_reasons:
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>❌ Loan Rejected</div>", unsafe_allow_html=True)

        for r in rejection_reasons:
            st.write("•", r)

        st.info("💡 Improve credit score, reduce loan amount, or increase tenure")
        st.markdown("</div>", unsafe_allow_html=True)
        st.stop()

    # -------------------- ML PREDICTION --------------------
    input_data = pd.DataFrame(
        [[no_of_dep, grad_s, emp_s, Annual_Income, Loan_Amount, Loan_Dur, Cibil, Assets]],
        columns=[
            "no_of_dependents",
            "education",
            "self_employed",
            "income_annum",
            "loan_amount",
            "loan_term",
            "cibil_score",
            "Assets"
        ]
    )

    input_data = scaler.transform(input_data)
    prediction = model.predict(input_data)
    probability = model.predict_proba(input_data)
    confidence = probability[0][1] * 100

    # -------------------- RISK --------------------
    if Cibil >= 750 and EMI <= monthly_income * 0.3:
        risk = "🟢 Low Risk"
    elif Cibil >= 700:
        risk = "🟡 Medium Risk"
    else:
        risk = "🔴 High Risk"

    # -------------------- RESULT --------------------
    st.markdown("<div class='section'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>📊 Loan Decision</div>", unsafe_allow_html=True)

    if prediction[0] == 1:
        st.success("Loan Approved")
    else:
        st.warning("Manual Review Required")

    st.markdown(f"<div class='metric'>Approval Confidence: {confidence:.2f}%</div>", unsafe_allow_html=True)
    st.progress(confidence / 100)

    st.write(f"**Risk Level:** {risk}")
    st.write(f"**Estimated EMI:** ₹{int(EMI):,}")

    st.markdown("</div>", unsafe_allow_html=True)
