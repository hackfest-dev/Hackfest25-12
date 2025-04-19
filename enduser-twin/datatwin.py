import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import VotingClassifier
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import time
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from scipy import stats
import io
import glob
from matplotlib.dates import DateFormatter
import random

# Set page configuration
st.set_page_config(
    page_title="Health Digital Twin",
    page_icon="🏥",
    layout="wide"
)

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)
os.makedirs("profiles", exist_ok=True)
os.makedirs("wearable_data", exist_ok=True)

# Custom CSS to improve the UI with colorful light theme
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
        color: #333333;
    }
    .patient-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #4361ee;
    }
    .metric-container {
        background-color: #f0f7ff;
        border-radius: 5px;
        padding: 15px;
        margin-bottom: 10px;
        border-left: 3px solid #4cc9f0;
    }
    .high-risk {
        color: #f72585;
        font-weight: bold;
    }
    .low-risk {
        color: #4cc9f0;
        font-weight: bold;
    }
    .header {
        color: #4361ee;
        font-weight: bold;
    }
    .stButton button {
        background-color: #4361ee;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
    }
    .stButton button:hover {
        background-color: #3a0ca3;
    }
    h1, h2, h3 {
        color: #3a0ca3;
    }
    .stRadio > div {
        padding: 10px;
        background-color: #ffffff;
        border-radius: 5px;
        border: 1px solid #eaeaea;
    }
    .stSelectbox > div > div {
        background-color: #ffffff;
        color: #333333;
    }
    .css-145kmo2 {
        color: #333333;
    }
    .stTextInput > div > div > input {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #eaeaea;
    }
    .stNumberInput > div > div > input {
        background-color: #ffffff;
        color: #333333;
        border: 1px solid #eaeaea;
    }
    div[data-testid="stSidebar"] {
        background-color: #f0f7ff;
        background: linear-gradient(135deg, #f0f7ff 0%, #e6f2ff 100%);
        color: #333333;
    }
    div[data-testid="stSidebar"] .stRadio label {
        color: #333333;
    }
    .stDataFrame {
        background-color: #ffffff;
    }
    .stProgress > div > div > div > div {
        background-color: #4cc9f0;
        background: linear-gradient(90deg, #4cc9f0 0%, #4361ee 100%);
    }
    .stSuccess {
        background-color: #d9f2e6;
        color: #087f5b;
    }
    .stInfo {
        background-color: #e1ecf8;
        color: #3a6df0;
    }
    .stWarning {
        background-color: #fff3e0;
        color: #ff9800;
    }
    .stError {
        background-color: #ffebee;
        color: #f44336;
    }
    /* Add styling for all input field containers */
    div.stDateInput, div.stTimeInput, div.stFileUploader {
        background-color: #ffffff;
        color: #333333;
    }
    
    /* Ensure dropdown menus have light backgrounds */
    div[data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    
    /* Style for multiselect options */
    div[data-baseweb="popover"] div {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Override for any remaining dark elements */
    .st-bq, .st-aj, .st-c0, .st-c1, .st-c2, .st-c3, .st-c4, .st-c5, .st-c6, 
    .st-c7, .st-c8, .st-c9, .st-ca, .st-cb, .st-cc, .st-cd, .st-ce {
        background-color: #ffffff !important;
        color: #333333 !important;
    }
    
    /* Make sure code blocks and text areas are light too */
    .stCodeBlock, textarea, div[data-baseweb="textarea"] {
        background-color: #f8f9fa !important;
        color: #333333 !important;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("Individual Health Digital Twin")
    
    # Sidebar menu - reordered as requested
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3774/3774299.png", width=100)
        st.markdown("## Navigation")
        page = st.radio("Select Page", ["Patient Profiles", "Add New Patient", "Update Health Data", "Import Wearable Data"])
        
        st.markdown("---")
        st.markdown("### About")
        st.info("This application creates digital twins for individual patients to predict health risks.")
    
    if page == "Patient Profiles":
        show_patient_profiles()
    elif page == "Add New Patient":
        add_new_patient()
    elif page == "Update Health Data":
        update_health_data()
    elif page == "Import Wearable Data":
        import_wearable_data()

def show_patient_profiles():
    st.header("Patient Profiles")
    
    # Get list of patient profiles
    profiles = get_patient_profiles()
    
    if not profiles:
        st.info("No patient profiles found. Please add a new patient profile.")
        return
    
    # Let user select a patient by ID or name
    patient_options = [f"{p['patient_id']} - {p['name']}" for p in profiles]
    selected_patient_option = st.selectbox("Select Patient:", patient_options)
    
    selected_patient_id = selected_patient_option.split(" - ")[0]
    
    # Get patient data
    patient = next((p for p in profiles if p['patient_id'] == selected_patient_id), None)
    
    if patient:
        display_patient_profile(patient)
        
        # Run health predictions
        st.markdown("### Health Risk Assessment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="patient-card">', unsafe_allow_html=True)
            st.subheader("Diabetes Risk")
            diabetes_risk = predict_diabetes_risk(patient)
            display_risk_meter("Diabetes", diabetes_risk)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="patient-card">', unsafe_allow_html=True)
            st.subheader("Heart Disease Risk")
            heart_risk = predict_heart_risk(patient)
            display_risk_meter("Heart Disease", heart_risk)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show health trends
        st.markdown("### Health Parameter Trends")
        st.markdown('<div class="patient-card">', unsafe_allow_html=True)
        
        if 'history' in patient and len(patient['history']) > 1:
            parameter = st.selectbox("Select Parameter to View:", 
                                    [col for col in patient['history'][0].keys() 
                                     if col not in ['date', 'patient_id']])
            
            # Extract data for plotting
            dates = [entry['date'] for entry in patient['history']]
            values = [entry.get(parameter, 0) for entry in patient['history']]
            
            # Create plot
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(dates, values, marker='o', linestyle='-', color='#0d6efd')
            ax.set_title(f"{parameter} Over Time")
            ax.set_xlabel("Date")
            ax.set_ylabel(parameter)
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Rotate x-axis labels
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            st.pyplot(fig)
        else:
            st.info("Not enough historical data to show trends. Please update health data.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Health recommendations
        st.markdown("### Health Recommendations")
        st.markdown('<div class="patient-card">', unsafe_allow_html=True)
        
        if diabetes_risk > 50 or heart_risk > 50:
            st.warning("Based on your health parameters, we recommend:")
            recommendations = []
            
            if diabetes_risk > 50:
                recommendations.extend([
                    "Monitor blood glucose levels regularly",
                    "Reduce sugar and refined carbohydrate intake",
                    "Maintain regular physical activity (30 minutes, 5 days a week)"
                ])
            
            if heart_risk > 50:
                recommendations.extend([
                    "Monitor blood pressure regularly",
                    "Reduce sodium intake",
                    "Consider consulting with a cardiologist"
                ])
            
            for rec in recommendations:
                st.markdown(f"- {rec}")
        else:
            st.success("Your health parameters look good! Continue with:")
            st.markdown("- Regular exercise (150 minutes per week)")
            st.markdown("- Balanced diet rich in fruits and vegetables")
            st.markdown("- Regular health check-ups")
        
        st.markdown('</div>', unsafe_allow_html=True)

def add_new_patient():
    st.header("Add New Patient")
    
    st.markdown('<div class="patient-card">', unsafe_allow_html=True)
    
    # Basic information
    patient_id = st.text_input("Patient ID")
    name = st.text_input("Full Name")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=0.0, max_value=120.0, value=30.0)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    with col2:
        height = st.number_input("Height (cm)", min_value=0.0, max_value=300.0, value=170.0)
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=500.0, value=70.0)
    
    # Calculate BMI
    bmi = weight / ((height/100) ** 2) if height > 0 else 0
    st.info(f"Calculated BMI: {bmi:.2f}")
    
    # Health parameters
    st.subheader("Health Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        blood_glucose = st.number_input("Blood Glucose (mg/dL)", min_value=0.0, max_value=500.0, value=90.0)
        systolic_bp = st.number_input("Systolic BP (mmHg)", min_value=0.0, max_value=300.0, value=120.0)
    
    with col2:
        cholesterol = st.number_input("Total Cholesterol (mg/dL)", min_value=0.0, max_value=500.0, value=180.0)
        hdl = st.number_input("HDL (mg/dL)", min_value=0.0, max_value=200.0, value=50.0)
    
    with col3:
        triglycerides = st.number_input("Triglycerides (mg/dL)", min_value=0.0, max_value=1000.0, value=150.0)
        diastolic_bp = st.number_input("Diastolic BP (mmHg)", min_value=0.0, max_value=200.0, value=80.0)
    
    # Medical history
    st.subheader("Medical History")
    
    col1, col2 = st.columns(2)
    
    with col1:
        family_diabetes = st.checkbox("Family History of Diabetes")
        family_heart = st.checkbox("Family History of Heart Disease")
    
    with col2:
        smoking = st.checkbox("Smoker")
        physical_activity = st.selectbox("Physical Activity Level", ["Low", "Moderate", "High"])
    
    if st.button("Add Patient"):
        if patient_id and name:
            # Create patient data
            patient_data = {
                "patient_id": patient_id,
                "name": name,
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight,
                "bmi": bmi,
                "history": [{
                    "date": time.strftime("%Y-%m-%d"),
                    "patient_id": patient_id,
                    "blood_glucose": blood_glucose,
                    "systolic_bp": systolic_bp,
                    "diastolic_bp": diastolic_bp,
                    "cholesterol": cholesterol,
                    "hdl": hdl,
                    "triglycerides": triglycerides,
                    "weight": weight,
                    "bmi": bmi
                }],
                "medical_history": {
                    "family_diabetes": family_diabetes,
                    "family_heart": family_heart,
                    "smoking": smoking,
                    "physical_activity": physical_activity
                }
            }
            
            # Save patient data
            save_patient_data(patient_data)
            
            st.success(f"Patient {name} added successfully!")
        else:
            st.error("Patient ID and Name are required.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def update_health_data():
    st.header("Update Health Data")
    
    # Get list of patient profiles
    profiles = get_patient_profiles()
    
    if not profiles:
        st.info("No patient profiles found. Please add a new patient first.")
        return
    
    st.markdown('<div class="patient-card">', unsafe_allow_html=True)
    
    # Let user select a patient
    patient_options = [f"{p['patient_id']} - {p['name']}" for p in profiles]
    selected_patient_option = st.selectbox("Select Patient:", patient_options)
    
    selected_patient_id = selected_patient_option.split(" - ")[0]
    
    # Get patient data
    patient = next((p for p in profiles if p['patient_id'] == selected_patient_id), None)
    
    if patient:
        st.subheader(f"Update Health Data for {patient['name']}")
        
        # Get latest values for defaults
        latest = patient['history'][-1] if 'history' in patient and patient['history'] else {}
        
        # Health parameters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            blood_glucose = st.number_input("Blood Glucose (mg/dL)", 
                                         min_value=0.0, max_value=500.0, 
                                         value=float(latest.get('blood_glucose', 90)))
            systolic_bp = st.number_input("Systolic BP (mmHg)", 
                                       min_value=0.0, max_value=300.0, 
                                       value=float(latest.get('systolic_bp', 120)))
        
        with col2:
            cholesterol = st.number_input("Total Cholesterol (mg/dL)", 
                                       min_value=0.0, max_value=500.0, 
                                       value=float(latest.get('cholesterol', 180)))
            hdl = st.number_input("HDL (mg/dL)", 
                               min_value=0.0, max_value=200.0, 
                               value=float(latest.get('hdl', 50)))
        
        with col3:
            triglycerides = st.number_input("Triglycerides (mg/dL)", 
                                         min_value=0.0, max_value=1000.0, 
                                         value=float(latest.get('triglycerides', 150)))
            diastolic_bp = st.number_input("Diastolic BP (mmHg)", 
                                        min_value=0.0, max_value=200.0, 
                                        value=float(latest.get('diastolic_bp', 80)))
        
        col1, col2 = st.columns(2)
        
        with col1:
            weight = st.number_input("Weight (kg)", 
                                  min_value=0.0, max_value=500.0, 
                                  value=float(latest.get('weight', patient['weight'])))
        
        # Calculate BMI
        height = patient['height']
        bmi = weight / ((height/100) ** 2) if height > 0 else 0
        
        with col2:
            st.info(f"Calculated BMI: {bmi:.2f}")
        
        if st.button("Update Health Data"):
            # Create new health record
            new_record = {
                "date": time.strftime("%Y-%m-%d"),
                "patient_id": patient['patient_id'],
                "blood_glucose": blood_glucose,
                "systolic_bp": systolic_bp,
                "diastolic_bp": diastolic_bp,
                "cholesterol": cholesterol,
                "hdl": hdl,
                "triglycerides": triglycerides,
                "weight": weight,
                "bmi": bmi
            }
            
            # Add new record to history
            if 'history' not in patient:
                patient['history'] = []
            
            patient['history'].append(new_record)
            
            # Update weight and BMI in patient data
            patient['weight'] = weight
            patient['bmi'] = bmi
            
            # Save updated patient data
            save_patient_data(patient)
            
            st.success(f"Health data for {patient['name']} updated successfully!")
    
    st.markdown('</div>', unsafe_allow_html=True)

def display_patient_profile(patient):
    st.markdown('<div class="patient-card">', unsafe_allow_html=True)
    
    # Patient info header
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    
    with col2:
        st.markdown(f"## {patient['name']}")
        st.markdown(f"**Patient ID:** {patient['patient_id']}")
        st.markdown(f"**Age:** {patient['age']} years | **Gender:** {patient['gender']}")
    
    # Latest health metrics
    st.subheader("Current Health Status")
    
    if 'history' in patient and patient['history']:
        latest = patient['history'][-1]
        
        # Create 3 columns for metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f"<p class='header'>BMI</p>", unsafe_allow_html=True)
            bmi = latest.get('bmi', patient.get('bmi', 0))
            bmi_status = "High" if bmi >= 25 else "Normal" if bmi >= 18.5 else "Low"
            bmi_color = "high-risk" if bmi_status != "Normal" else "low-risk"
            st.markdown(f"<h3>{bmi:.1f} <span class='{bmi_color}'>({bmi_status})</span></h3>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f"<p class='header'>Blood Glucose</p>", unsafe_allow_html=True)
            glucose = latest.get('blood_glucose', 0)
            glucose_status = "High" if glucose > 140 else "Normal" if glucose >= 70 else "Low"
            glucose_color = "high-risk" if glucose_status != "Normal" else "low-risk"
            st.markdown(f"<h3>{glucose} mg/dL <span class='{glucose_color}'>({glucose_status})</span></h3>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f"<p class='header'>Blood Pressure</p>", unsafe_allow_html=True)
            systolic = latest.get('systolic_bp', 0)
            diastolic = latest.get('diastolic_bp', 0)
            bp_status = "High" if systolic > 130 or diastolic > 80 else "Normal"
            bp_color = "high-risk" if bp_status != "Normal" else "low-risk"
            st.markdown(f"<h3>{systolic}/{diastolic} mmHg <span class='{bp_color}'>({bp_status})</span></h3>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f"<p class='header'>Cholesterol</p>", unsafe_allow_html=True)
            chol = latest.get('cholesterol', 0)
            chol_status = "High" if chol > 200 else "Normal"
            chol_color = "high-risk" if chol_status != "Normal" else "low-risk"
            st.markdown(f"<h3>{chol} mg/dL <span class='{chol_color}'>({chol_status})</span></h3>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f"<p class='header'>HDL Cholesterol</p>", unsafe_allow_html=True)
            hdl = latest.get('hdl', 0)
            hdl_status = "Low" if hdl < 40 else "Normal"
            hdl_color = "high-risk" if hdl_status != "Normal" else "low-risk"
            st.markdown(f"<h3>{hdl} mg/dL <span class='{hdl_color}'>({hdl_status})</span></h3>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-container">', unsafe_allow_html=True)
            st.markdown(f"<p class='header'>Triglycerides</p>", unsafe_allow_html=True)
            trig = latest.get('triglycerides', 0)
            trig_status = "High" if trig > 150 else "Normal"
            trig_color = "high-risk" if trig_status != "Normal" else "low-risk"
            st.markdown(f"<h3>{trig} mg/dL <span class='{trig_color}'>({trig_status})</span></h3>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No health data available. Please update health data.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def predict_diabetes_risk(patient):
    """Predict diabetes risk based on patient data"""
    # Get latest health data
    if 'history' not in patient or not patient['history']:
        return 50  # Default risk
    
    latest = patient['history'][-1]
    
    # Simple risk calculation based on known diabetes risk factors
    risk = 0
    
    # BMI factor
    bmi = latest.get('bmi', patient.get('bmi', 0))
    if bmi >= 30:
        risk += 30
    elif bmi >= 25:
        risk += 20
    
    # Glucose factor
    glucose = latest.get('blood_glucose', 0)
    if glucose >= 126:
        risk += 40
    elif glucose >= 100:
        risk += 20
    
    # Age factor
    age = patient.get('age', 0)
    if age >= 45:
        risk += 15
    
    # Family history
    if patient.get('medical_history', {}).get('family_diabetes', False):
        risk += 15
    
    # Physical activity
    activity = patient.get('medical_history', {}).get('physical_activity', 'Moderate')
    if activity == 'Low':
        risk += 10
    
    # Cap risk at 100
    return min(risk, 100)

def predict_heart_risk(patient):
    """Predict heart disease risk based on patient data"""
    # Get latest health data
    if 'history' not in patient or not patient['history']:
        return 50  # Default risk
    
    latest = patient['history'][-1]
    
    # Simple risk calculation based on known heart disease risk factors
    risk = 0
    
    # Blood pressure factor
    systolic = latest.get('systolic_bp', 0)
    diastolic = latest.get('diastolic_bp', 0)
    if systolic >= 140 or diastolic >= 90:
        risk += 30
    elif systolic >= 130 or diastolic >= 80:
        risk += 20
    
    # Cholesterol factors
    cholesterol = latest.get('cholesterol', 0)
    hdl = latest.get('hdl', 0)
    triglycerides = latest.get('triglycerides', 0)
    
    if cholesterol >= 240:
        risk += 20
    elif cholesterol >= 200:
        risk += 10
    
    if hdl < 40:
        risk += 15
    
    if triglycerides >= 200:
        risk += 15
    
    # Age and gender factors
    age = patient.get('age', 0)
    gender = patient.get('gender', '')
    
    if gender == 'Male' and age >= 45:
        risk += 15
    elif gender == 'Female' and age >= 55:
        risk += 15
    
    # Smoking
    if patient.get('medical_history', {}).get('smoking', False):
        risk += 20
    
    # Family history
    if patient.get('medical_history', {}).get('family_heart', False):
        risk += 15
    
    # Cap risk at 100
    return min(risk, 100)

def display_risk_meter(condition, risk_percentage):
    """Display a visual risk meter"""
    # Determine risk category and color
    if risk_percentage >= 70:
        category = "High Risk"
        color = "#dc3545"  # Red
    elif risk_percentage >= 40:
        category = "Moderate Risk"
        color = "#ffc107"  # Yellow
    else:
        category = "Low Risk"
        color = "#198754"  # Green
    
    # Create a gauge-like visualization
    st.markdown(f"""
    <div style="text-align: center;">
        <h1 style="font-size: 3rem; margin-bottom: 0;">{risk_percentage}%</h1>
        <p style="color: {color}; font-weight: bold; font-size: 1.2rem;">{category}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a progress bar
    st.progress(risk_percentage / 100)
    
    # Add risk factors text
    if risk_percentage >= 40:
        st.markdown(f"**Key Risk Factors for {condition}:**")
        
        if condition == "Diabetes":
            if risk_percentage >= 70:
                factors = ["High blood glucose", "Elevated BMI", "Family history", "Insufficient physical activity"]
            else:
                factors = ["Slightly elevated blood glucose", "Above optimal BMI", "Age factor"]
        else:  # Heart Disease
            if risk_percentage >= 70:
                factors = ["High blood pressure", "Elevated cholesterol", "Smoking", "Family history"]
            else:
                factors = ["Slightly elevated blood pressure", "Borderline cholesterol levels", "Age factor"]
        
        for factor in factors:
            st.markdown(f"- {factor}")

def get_patient_profiles():
    """Load all patient profiles"""
    profiles = []
    
    if not os.path.exists("profiles"):
        return profiles
    
    for filename in os.listdir("profiles"):
        if filename.endswith(".pkl"):
            try:
                profile = joblib.load(os.path.join("profiles", filename))
                profiles.append(profile)
            except:
                pass
    
    return profiles

def save_patient_data(patient_data):
    """Save patient data to disk"""
    patient_id = patient_data['patient_id']
    filepath = os.path.join("profiles", f"{patient_id}.pkl")
    joblib.dump(patient_data, filepath)

def import_wearable_data():
    """Import wearable device data with timestamps from CSV files"""
    st.header("Import Wearable Device Data")
    
    # Get list of patient profiles
    profiles = get_patient_profiles()
    
    if not profiles:
        st.info("No patient profiles found. Please add a new patient first.")
        return
    
    st.markdown('<div class="patient-card">', unsafe_allow_html=True)
    
    # Let user select a patient
    patient_options = [f"{p['patient_id']} - {p['name']}" for p in profiles]
    selected_patient_option = st.selectbox("Select Patient:", patient_options)
    
    selected_patient_id = selected_patient_option.split(" - ")[0]
    
    # Get patient data
    patient = next((p for p in profiles if p['patient_id'] == selected_patient_id), None)
    
    if patient:
        st.subheader(f"Import Wearable Data for {patient['name']}")
        
        # File upload options
        upload_method = st.radio("Select Import Method:", ["Upload CSV File", "Use Sample Data"])
        
        if upload_method == "Upload CSV File":
            # File upload with clear instructions
            st.markdown("""
            ### Upload CSV Instructions
            1. Your CSV file must contain a 'timestamp' column in a datetime format (e.g., 'YYYY-MM-DD HH:MM:SS')
            2. Health parameters should be in separate columns (e.g., 'heart_rate', 'blood_glucose', etc.)
            3. Make sure all health metrics are numeric values
            """)
            
            uploaded_file = st.file_uploader("Upload CSV file with wearable device data", type=["csv"], help="CSV file must contain a timestamp column")
            
            if uploaded_file is not None:
                try:
                    # Read the CSV file
                    df = pd.read_csv(uploaded_file)
                    
                    # Display preview
                    st.write("Data Preview:")
                    st.dataframe(df.head())
                    
                    # Check if timestamp column exists
                    if 'timestamp' not in df.columns:
                        timestamp_col = st.selectbox("Select the timestamp column:", df.columns)
                        if timestamp_col != 'timestamp':
                            df = df.rename(columns={timestamp_col: 'timestamp'})
                    
                    # Data mapping
                    st.subheader("Map CSV Columns to Health Parameters")
                    
                    # Get available health parameters
                    health_params = ['blood_glucose', 'systolic_bp', 'diastolic_bp', 'heart_rate', 
                                    'steps', 'sleep', 'calories', 'oxygen_level']
                    
                    # Auto-detect matching columns
                    auto_mapping = {}
                    for param in health_params:
                        # Check for exact match
                        if param in df.columns:
                            auto_mapping[param] = param
                        # Check for partial match
                        else:
                            matches = [col for col in df.columns if param in col.lower()]
                            if matches:
                                auto_mapping[param] = matches[0]
                            else:
                                auto_mapping[param] = 'None'
                    
                    # Create mapping with auto-detection
                    col_mapping = {}
                    for param in health_params:
                        col_options = ['None'] + list(df.columns)
                        default_index = col_options.index(auto_mapping[param]) if auto_mapping[param] in col_options else 0
                        col_mapping[param] = st.selectbox(f"Map column for {param}:", 
                                                        col_options, 
                                                        index=default_index,
                                                        key=f"map_{param}")
                    
                    if st.button("Import Data"):
                        try:
                            wearable_records = []
                            
                            # Process each row in the CSV
                            for index, row in df.iterrows():
                                try:
                                    # Convert timestamp string to datetime object
                                    timestamp = pd.to_datetime(row['timestamp'])
                                    
                                    # Create record with timestamp
                                    record = {
                                        "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                                        "patient_id": patient['patient_id']
                                    }
                                    
                                    # Add mapped health parameters
                                    for param, col in col_mapping.items():
                                        if col != 'None' and col in df.columns:
                                            # Convert to float to ensure consistency
                                            try:
                                                record[param] = float(row[col])
                                            except:
                                                continue
                                    
                                    wearable_records.append(record)
                                except:
                                    continue
                            
                            # Initialize wearable_data if it doesn't exist
                            if 'wearable_data' not in patient:
                                patient['wearable_data'] = []
                            
                            # Add new wearable records
                            patient['wearable_data'].extend(wearable_records)
                            
                            # Save the updated patient data
                            save_patient_data(patient)
                            
                            # Also save as CSV for backup
                            wearable_df = pd.DataFrame(wearable_records)
                            wearable_df.to_csv(f"wearable_data/{patient['patient_id']}_wearable.csv", index=False)
                            
                            st.success(f"Successfully imported {len(wearable_records)} wearable data records for {patient['name']}.")
                            
                            # Show prediction results
                            show_wearable_predictions(patient)
                        except:
                            st.info("Please check your data format and try again.")
                
                except:
                    st.info("Please make sure your CSV file is formatted correctly with a timestamp column.")
        else:
            # Sample data option
            st.info("Using sample wearable data for demonstration purposes")
            
            # Generate sample data
            if st.button("Generate Sample Data"):
                try:
                    # Create sample dataframe with timestamp and health metrics
                    start_time = datetime.now() - timedelta(days=7)
                    times = [start_time + timedelta(hours=i*3) for i in range(56)]  # 7 days of data points every 3 hours
                    
                    # Generate some realistic sample data with trends
                    # Add some randomness to make it look realistic but with health patterns
                    is_diabetic = random.choice([True, False])
                    has_heart_issues = random.choice([True, False])
                    
                    heart_rates = []
                    blood_glucose = []
                    systolic_bp = []
                    diastolic_bp = []
                    oxygen_levels = []
                    steps = []
                    
                    for i in range(len(times)):
                        # Time of day effect (higher in morning, lower at night)
                        hour = times[i].hour
                        time_factor = 1.0 if 8 <= hour <= 20 else 0.8
                        
                        # Generate heart rate - higher if has heart issues
                        base_hr = 85 if has_heart_issues else 70
                        hr = base_hr * time_factor + random.randint(-10, 10)
                        heart_rates.append(max(50, min(120, hr)))
                        
                        # Generate blood glucose - higher if diabetic
                        base_glucose = 150 if is_diabetic else 90
                        glucose = base_glucose * time_factor + random.randint(-20, 20)
                        blood_glucose.append(max(70, min(200, glucose)))
                        
                        # Generate blood pressure - higher if has heart issues
                        base_sys = 140 if has_heart_issues else 120
                        sys = base_sys * time_factor + random.randint(-10, 10)
                        systolic_bp.append(max(100, min(160, sys)))
                        
                        base_dia = 90 if has_heart_issues else 80
                        dia = base_dia * time_factor + random.randint(-5, 5)
                        diastolic_bp.append(max(60, min(100, dia)))
                        
                        # Generate oxygen level - slightly lower if has heart issues
                        base_oxygen = 95 if has_heart_issues else 98
                        oxygen = base_oxygen + random.randint(-2, 2)
                        oxygen_levels.append(max(90, min(100, oxygen)))
                        
                        # Generate steps - more during the day
                        base_steps = 1000 if 8 <= hour <= 20 else 200
                        step = base_steps + random.randint(-200, 200)
                        steps.append(max(0, step))
                    
                    # Create dataframe
                    sample_df = pd.DataFrame({
                        'timestamp': [t.strftime("%Y-%m-%d %H:%M:%S") for t in times],
                        'heart_rate': heart_rates,
                        'blood_glucose': blood_glucose,
                        'systolic_bp': systolic_bp,
                        'diastolic_bp': diastolic_bp,
                        'oxygen_level': oxygen_levels,
                        'steps': steps
                    })
                    
                    # Display preview
                    st.write("Sample Data Preview:")
                    st.dataframe(sample_df.head())
                    
                    # Process sample data
                    wearable_records = []
                    for _, row in sample_df.iterrows():
                        record = {
                            "timestamp": row['timestamp'],
                            "patient_id": patient['patient_id'],
                            "heart_rate": float(row['heart_rate']),
                            "blood_glucose": float(row['blood_glucose']),
                            "systolic_bp": float(row['systolic_bp']),
                            "diastolic_bp": float(row['diastolic_bp']),
                            "oxygen_level": float(row['oxygen_level']),
                            "steps": float(row['steps'])
                        }
                        wearable_records.append(record)
                    
                    # Initialize wearable_data if it doesn't exist
                    if 'wearable_data' not in patient:
                        patient['wearable_data'] = []
                    
                    # Add new wearable records
                    patient['wearable_data'].extend(wearable_records)
                    
                    # Save the updated patient data
                    save_patient_data(patient)
                    
                    # Also save as CSV for backup
                    sample_df.to_csv(f"wearable_data/{patient['patient_id']}_wearable.csv", index=False)
                    
                    st.success(f"Successfully added {len(wearable_records)} sample wearable data records for {patient['name']}.")
                    
                    # Show prediction results
                    show_wearable_predictions(patient)
                except:
                    st.info("An issue occurred while generating sample data. Please try again.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_wearable_predictions(patient):
    """Show disease predictions based on wearable data"""
    if 'wearable_data' not in patient or not patient['wearable_data']:
        return
    
    # Convert to DataFrame for easier manipulation
    try:
        wearable_df = pd.DataFrame(patient['wearable_data'])
        
        # Convert timestamp to datetime objects
        wearable_df['timestamp'] = pd.to_datetime(wearable_df['timestamp'])
        
        # Sort by timestamp
        wearable_df = wearable_df.sort_values('timestamp')
        
        # Get the most recent data points
        latest_data = {}
        for col in wearable_df.columns:
            if col not in ['timestamp', 'patient_id']:
                if col in wearable_df.columns and not wearable_df[col].dropna().empty:
                    latest_data[col] = wearable_df[col].dropna().iloc[-1]
        
        st.markdown("## Health Prediction Based on Wearable Data")
        col1, col2 = st.columns(2)
        
        # Calculate diabetes risk based on wearable data
        with col1:
            st.markdown('<div class="patient-card">', unsafe_allow_html=True)
            st.subheader("Diabetes Risk Assessment")
            
            diabetes_risk = 0
            
            # Use blood glucose from wearable if available
            if 'blood_glucose' in latest_data:
                glucose = latest_data['blood_glucose']
                if glucose >= 126:
                    diabetes_risk += 40
                elif glucose >= 100:
                    diabetes_risk += 20
                
                st.markdown(f"<p>Blood Glucose: <strong>{glucose:.1f} mg/dL</strong></p>", unsafe_allow_html=True)
            
            # Use BMI from patient profile
            if 'bmi' in patient:
                bmi = patient['bmi']
                if bmi >= 30:
                    diabetes_risk += 30
                elif bmi >= 25:
                    diabetes_risk += 20
                
                st.markdown(f"<p>BMI: <strong>{bmi:.1f}</strong></p>", unsafe_allow_html=True)
            
            # Activity level based on steps
            if 'steps' in latest_data:
                avg_steps = wearable_df['steps'].mean()
                if avg_steps < 5000:
                    diabetes_risk += 10
                    st.markdown(f"<p>Average Steps: <strong>{avg_steps:.0f}</strong> (Low activity)</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p>Average Steps: <strong>{avg_steps:.0f}</strong></p>", unsafe_allow_html=True)
            
            # Add age factor
            if 'age' in patient:
                age = patient['age']
                if age >= 45:
                    diabetes_risk += 15
            
            # Cap risk at 100
            diabetes_risk = min(diabetes_risk, 100)
            
            # Display risk meter
            display_risk_meter("Diabetes", diabetes_risk)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Calculate heart disease risk based on wearable data
        with col2:
            st.markdown('<div class="patient-card">', unsafe_allow_html=True)
            st.subheader("Heart Disease Risk Assessment")
            
            heart_risk = 0
            
            # Use blood pressure from wearable if available
            if 'systolic_bp' in latest_data and 'diastolic_bp' in latest_data:
                systolic = latest_data['systolic_bp']
                diastolic = latest_data['diastolic_bp']
                
                if systolic >= 140 or diastolic >= 90:
                    heart_risk += 30
                elif systolic >= 130 or diastolic >= 80:
                    heart_risk += 20
                
                st.markdown(f"<p>Blood Pressure: <strong>{systolic:.0f}/{diastolic:.0f} mmHg</strong></p>", unsafe_allow_html=True)
            
            # Use heart rate from wearable if available
            if 'heart_rate' in latest_data:
                heart_rate = latest_data['heart_rate']
                if heart_rate > 100:
                    heart_risk += 15
                
                st.markdown(f"<p>Heart Rate: <strong>{heart_rate:.0f} bpm</strong></p>", unsafe_allow_html=True)
            
            # Use oxygen level from wearable if available
            if 'oxygen_level' in latest_data:
                oxygen = latest_data['oxygen_level']
                if oxygen < 95:
                    heart_risk += 20
                
                st.markdown(f"<p>Oxygen Level: <strong>{oxygen:.1f}%</strong></p>", unsafe_allow_html=True)
            
            # Add age and gender factors
            if 'age' in patient and 'gender' in patient:
                age = patient['age']
                gender = patient['gender']
                
                if gender == 'Male' and age >= 45:
                    heart_risk += 15
                elif gender == 'Female' and age >= 55:
                    heart_risk += 15
            
            # Cap risk at 100
            heart_risk = min(heart_risk, 100)
            
            # Display risk meter
            display_risk_meter("Heart Disease", heart_risk)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Health recommendations based on wearable data
        st.markdown('<div class="patient-card">', unsafe_allow_html=True)
        st.subheader("Personalized Health Recommendations")
        
        recommendations = []
        
        # Diabetes recommendations
        if diabetes_risk >= 70:
            recommendations.append("Your wearable data indicates high risk for diabetes. Consider consulting with an endocrinologist.")
            recommendations.append("Monitor your blood glucose levels carefully and maintain a consistent meal schedule.")
            recommendations.append("Consider adopting a low-glycemic diet with limited processed carbohydrates.")
        elif diabetes_risk >= 40:
            recommendations.append("Your wearable data shows moderate risk for diabetes. Consider increasing physical activity.")
            recommendations.append("Try to reduce intake of sugary foods and beverages.")
        
        # Heart disease recommendations
        if heart_risk >= 70:
            recommendations.append("Your wearable data indicates high risk for heart disease. Consider consulting with a cardiologist.")
            recommendations.append("Monitor your blood pressure regularly and consider stress reduction techniques.")
        elif heart_risk >= 40:
            recommendations.append("Your wearable data shows moderate risk for heart disease. Consider adding cardiovascular exercise to your routine.")
            recommendations.append("Focus on a heart-healthy diet with reduced sodium and saturated fats.")
        
        # Activity recommendations based on steps
        if 'steps' in latest_data:
            avg_steps = wearable_df['steps'].mean()
            if avg_steps < 5000:
                recommendations.append(f"Your average daily step count ({avg_steps:.0f}) is lower than recommended. Aim for at least 10,000 steps daily.")
        
        # Blood glucose recommendations
        if 'blood_glucose' in latest_data:
            glucose = latest_data['blood_glucose']
            if glucose > 140:
                recommendations.append(f"Your blood glucose level ({glucose:.1f} mg/dL) is elevated. Consider dietary changes to reduce sugar intake.")
        
        # Blood pressure recommendations
        if 'systolic_bp' in latest_data and 'diastolic_bp' in latest_data:
            systolic = latest_data['systolic_bp']
            diastolic = latest_data['diastolic_bp']
            if systolic > 130 or diastolic > 80:
                recommendations.append(f"Your blood pressure ({systolic:.0f}/{diastolic:.0f} mmHg) is higher than optimal. Consider reducing sodium intake.")
        
        # Display recommendations
        if recommendations:
            for rec in recommendations:
                st.markdown(f"- {rec}")
        else:
            st.success("Your health parameters look good based on wearable data! Continue with your healthy lifestyle.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
    except:
        pass

if __name__ == "__main__":
    main()
