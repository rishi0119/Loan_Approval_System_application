Loan Approval System using Machine Learning
-------------------------------------------

Project Overview:-
-----------------
This project is a Loan Approval System built using Machine Learning and Streamlit. The main goal of this project is to predict whether a loan should be approved or rejected based on applicant details such as income, credit score, loan amount, and other financial factors.

Objective of the Project:-
-------------------------
- To automate the loan approval decision process
- To reduce manual effort in loan eligibility checking
- To apply machine learning concepts in a real-world financial use case
- To build an interactive and user-friendly web application

The project works in two stages:-

1. Eligibility Check (Rule-Based)
Before using the machine learning model, the system checks basic eligibility rules such as:
- Minimum annual income requirement
- Minimum CIBIL score
- Loan amount compared to income
- EMI affordability (EMI should not exceed 40% of monthly income)
If any of these conditions fail, the loan is rejected with clear reasons.

2. Machine Learning Prediction
If the applicant passes the eligibility stage:
- The input data is preprocessed using a scaler
- The trained ML model predicts loan approval
- The system also shows:
  - Approval confidence
  - Risk level (Low / Medium / High)
  - Estimated monthly EMI

Technologies Used:-
------------------
-> Python
-> Streamlit (for web application)
-> Pandas & NumPy (data handling)
-> Scikit-learn (machine learning)
-> Pickle (model and scaler storage)

Input Parameters:-
------------------
The system takes the following inputs from the user:
- Number of dependents
- Education level
- Employment type
- Annual income
- Total assets
- CIBIL credit score
- Loan amount
- Loan tenure

Output:-
--------
<a href="https://loanapprovalsystemapplication-oyxk4gmzxlftumlyapp6yer.streamlit.app" target="_blank">Open Loan Approval System</a>

Future Enhancements:-
---------------------
- Adding existing loan EMI handling
- Age and employment stability checks
- Admin dashboard for loan officers
- Database integration
- PDF loan approval reports

