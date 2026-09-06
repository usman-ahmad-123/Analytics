import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
import joblib

# -----------------------------
# Load models safely
# -----------------------------

try:
    logistic_model = joblib.load("models/logistic_model.pkl")
except Exception as e:
    st.error(f"Error loading logistic model: {e}")
    logistic_model = None

try:
    rf_model = joblib.load("models/rf_model.pkl")
except Exception as e:
    st.error(f"Error loading random forest model: {e}")
    rf_model = None

try:
    xgb_model = joblib.load("models/xgb_model.pkl")
except Exception as e:
    st.error(f"Error loading XGBoost model: {e}")
    xgb_model = None
# -----------------------------
# Streamlit UI
# -----------------------------
tab1, tab2 = st.tabs(["Prediction", "Model Insights"])

if rf_model is not None:
    preprocessor = rf_model.named_steps["preprocessor"]
    rf_classifier = rf_model.named_steps["model"]

with tab1:
    st.title("Customer Churn Prediction App")
    st.write("Enter customer details to predict churn probability")

    model_choice = st.selectbox(
        "Choose Model",
        ["Logistic Regression", "Random Forest", "XGBoost"]
    )

    # Input fields
    gender = st.selectbox("Gender", ["Male","Female"])
    senior = st.selectbox("Senior Citizen", [0,1])
    partner = st.selectbox("Partner", ["Yes","No"])
    dependents = st.selectbox("Dependents", ["Yes","No"])
    tenure = st.slider("Tenure (months)",0,72)
    phoneservice = st.selectbox("Phone Service", ["Yes","No"])
    multiplelines = st.selectbox("Multiple Lines", ["Yes","No","No phone service"])
    internet = st.selectbox("Internet Service", ["DSL","Fiber optic","No"])
    onlinesecurity = st.selectbox("Online Security", ["Yes","No","No internet service"])
    onlinebackup = st.selectbox("Online Backup", ["Yes","No","No internet service"])
    deviceprotection = st.selectbox("Device Protection", ["Yes","No","No internet service"])
    techsupport = st.selectbox("Tech Support", ["Yes","No","No internet service"])
    streamingtv = st.selectbox("Streaming TV", ["Yes","No","No internet service"])
    streamingmovies = st.selectbox("Streaming Movies", ["Yes","No","No internet service"])
    contract = st.selectbox("Contract", ["Month-to-month","One year","Two year"])
    paperless = st.selectbox("Paperless Billing", ["Yes","No"])
    payment = st.selectbox(
        "Payment Method",
        ["Electronic check","Mailed check","Bank transfer (automatic)","Credit card (automatic)"]
    )
    monthly = st.number_input("Monthly Charges",0.0,200.0)
    total = st.number_input("Total Charges",0.0,10000.0)

    # Build dataframe with all expected columns
    data = pd.DataFrame({
        "Gender":[gender],
        "SeniorCitizen":[senior],
        "Partner":[partner],
        "Dependents":[dependents],
        "Tenure in Months":[tenure],
        "Phone Service":[phoneservice],
        "Multiple Lines":[multiplelines],
        "Internet Service":[internet],
        "Online Security":[onlinesecurity],
        "Online Backup":[onlinebackup],
        "Device Protection Plan":[deviceprotection],
        "Premium Tech Support":[techsupport],
        "Streaming TV":[streamingtv],
        "Streaming Movies":[streamingmovies],
        "Streaming Music":["No"],
        "Unlimited Data":["No"],
        "Contract":[contract],
        "Paperless Billing":[paperless],
        "Payment Method":[payment],
        "Monthly Charge":[monthly],
        "Total Charges":[total],
        "Age":[30],
        "Number of Dependents":[0],
        "Number of Referrals":[0],
        "Avg Monthly Long Distance Charges":[0],
        "Avg Monthly GB Download":[0],
        "Total Refunds":[0],
        "Total Extra Data Charges":[0],
        "Total Long Distance Charges":[0],
        "Total Revenue":[0],
        "Married":["No"],
        "Offer":["None"],
        "Internet Type":["Fiber"]
    })

    if model_choice == "Logistic Regression":
        model = logistic_model
    elif model_choice == "Random Forest":
        model = rf_model
    else:
        model = xgb_model

    if st.button("Predict Churn") and model is not None:
        prob = model.predict_proba(data)[0][1]
        st.metric("Churn Probability", f"{prob*100:.1f}%")
        st.progress(float(prob))

        if prob > 0.6:
            st.error("High Risk Customer")
        elif prob > 0.3:
            st.warning("Medium Risk Customer")
        else:
            st.success("Low Risk Customer")

        st.write(f"Model Used: **{model_choice}**")
        st.subheader("Prediction Explanation (SHAP)")

        if rf_model is not None:
            X_transformed = preprocessor.transform(data)
            feature_names = preprocessor.get_feature_names_out()
            X_transformed_df = pd.DataFrame(X_transformed, columns=feature_names)

            explainer = shap.Explainer(rf_classifier)
            shap_values = explainer(X_transformed_df)

            fig = plt.figure()
            shap.plots.waterfall(shap_values[0, :, 1], show=False)
            st.pyplot(fig)

with tab2:
    if rf_model is not None:
        preprocessor = rf_model.named_steps["preprocessor"]
        feature_names = preprocessor.get_feature_names_out()
        rf_classifier = rf_model.named_steps["model"]
        feature_importance = rf_classifier.feature_importances_

        feat_imp = pd.DataFrame({
            "feature": feature_names,
            "importance": feature_importance
        }).sort_values("importance", ascending=False)

        top_features = feat_imp.head(15)
        fig, ax = plt.subplots(figsize=(10,6))
        ax.barh(top_features["feature"], top_features["importance"])
        ax.invert_yaxis()
        ax.set_title("Top Drivers of Customer Churn")
        st.pyplot(fig)

        st.subheader("SHAP Summary Plot")

        # Build sample_data with all expected columns
        sample_data = pd.DataFrame({
            "Age": np.random.randint(18, 80, size=50),
            "Number of Dependents": np.random.randint(0, 5, size=50),
            "Number of Referrals": np.random.randint(0, 10, size=50),
            "Tenure in Months": np.random.randint(0, 72, size=50),
            "Avg Monthly Long Distance Charges": np.random.uniform(0, 50, size=50),
            "Avg Monthly GB Download": np.random.uniform(0, 100, size=50),
            "Monthly Charge": np.random.uniform(20, 120, size=50),
            "Total Charges": np.random.uniform(100, 5000, size=50),
            "Total Refunds": np.random.uniform(0, 100, size=50),
            "Total Extra Data Charges": np.random.uniform(0, 200, size=50),
            "Total Long Distance Charges": np.random.uniform(0, 300, size=50),
            "Total Revenue": np.random.uniform(500, 10000, size=50),
            "Gender": np.random.choice(["Male", "Female"], size=50),
            "Married": np.random.choice(["Yes", "No"], size=50),
            "Offer": np.random.choice(["None", "Offer A", "Offer B"], size=50),
            "Phone Service": np.random.choice(["Yes", "No"], size=50),
            "Multiple Lines": np.random.choice(["Yes", "No"], size=50),
            "Internet Service": np.random.choice(["DSL", "Fiber optic", "No"], size=50),
            "Internet Type": np.random.choice(["Cable", "Fiber", "None"], size=50),
            "Online Security": np.random.choice(["Yes", "No"], size=50),
            "Online Backup": np.random.choice(["Yes", "No"], size=50),
            "Device Protection Plan": np.random.choice(["Yes", "No"], size=50),
            "Premium Tech Support": np.random.choice(["Yes", "No"], size=50),
            "Streaming TV": np.random.choice(["Yes", "No"], size=50),
            "Streaming Movies": np.random.choice(["Yes", "No"], size=50),
            "Streaming Music": np.random.choice(["Yes", "No"], size=50),
            "Unlimited Data": np.random.choice(["Yes", "No"], size=50),
            "Contract": np.random.choice(["Month-to-month", "One year", "Two year"], size=50),
            "Paperless Billing": np.random.choice(["Yes", "No"], size=50),
            "Payment Method": np.random.choice([
                "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
            ], size=50)
        })

        X_sample_transformed = preprocessor.transform(sample_data)
        X_sample_df = pd.DataFrame(X_sample_transformed, columns=feature_names)



        explainer = shap.Explainer(rf_classifier)
        shap_values = explainer(X_sample_df)

        fig = plt.figure()
        shap.plots.beeswarm(shap_values[:, :, 1], max_display=15, show=False)
        st.pyplot(fig)

        st.subheader("SHAP Feature Importance")
        fig = plt.figure()
        shap.plots.bar(shap_values[:, :, 1], max_display=15, show=False)
        st.pyplot(fig)

    performance_df = pd.DataFrame({
        "Model": ["Logistic Regression", "Random Forest", "XGBoost"],
        "ROC AUC": [0.86, 0.85, 0.85],
        "F1 Score": [0.64, 0.65, 0.63],
        "Precision": [0.52, 0.56, 0.55],
        "Recall": [0.84, 0.78, 0.75]
    })

    st.subheader("Model Performance")
    st.dataframe(performance_df)

    st.subheader("Business Insights")
    st.markdown("""
### Key Drivers of Customer Churn
- **Customer Tenure**: Shorter tenure → higher churn risk.
- **Contract Type**: Month-to-month contracts → highest churn.
- **Monthly Charges**: Higher charges → more likely to churn.
- **Internet Service Type**: Fiber optic users churn more than DSL.
- **Value-Added Services**: Lack of security/tech support increases churn.

### Recommendations
• Encourage long-term contracts with discounts.  
• Offer bundled services (security, tech support).  
• Provide retention offers for high-charge customers.  
• Focus campaigns on new customers with low tenure.
""")
