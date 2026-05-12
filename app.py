# Install required libraries (run once)
# !pip install streamlit plotly pandas numpy faker

import streamlit as st
import pandas as pd
import numpy as np
from faker import Faker
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import io
import zipfile

# Initialize Faker for synthetic data
fake = Faker()

# Set page config for Apple-like theme
st.set_page_config(
    page_title="Encube Ethicals | AI-Powered Insights",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Apple-like UI
st.markdown("""
    <style>
    /* Apple-like Fonts and Colors */
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500;600;700&family=SF+Pro+Text:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'SF Pro Text', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
        background-color: #f5f5f7;
        color: #1d1d1f;
    }

    /* Sidebar Styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #d2d2d7;
    }

    /* Main Content Styling */
    .main {
        background-color: #f5f5f7;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.1);
        border: 1px solid #d2d2d7;
        margin-bottom: 20px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1), 0 6px 12px rgba(0,0,0,0.08);
    }

    /* KPI Cards */
    .kpi-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #d2d2d7;
        margin-bottom: 15px;
    }

    /* Key Findings */
    .key-finding {
        background-color: #fff5f5;
        padding: 15px;
        border-left: 4px solid #ff3b30;
        border-radius: 0 8px 8px 0;
        margin: 15px 0;
        font-size: 14px;
        line-height: 1.5;
    }
    .key-finding::before {
        content: "🔍";
        margin-right: 8px;
    }

    /* Outlier Highlight */
    .outlier {
        background-color: #ffeeba;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        color: #ff9500;
    }

    /* Abnormal Value Highlight */
    .abnormal {
        background-color: #ffebee;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        color: #ff3b30;
    }

    /* Efficient Value Highlight */
    .efficient {
        background-color: #e8f5e9;
        padding: 2px 6px;
        border-radius: 4px;
        font-weight: 600;
        color: #34c759;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #ffffff;
        padding: 10px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        padding: 0 20px;
        background-color: transparent;
        border-radius: 8px;
        font-weight: 500;
        color: #86868b;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0071e3;
        color: #ffffff;
    }

    /* Filter Section */
    .filter-section {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #d2d2d7;
    }

    /* Header */
    .header {
        color: #1d1d1f;
        padding-bottom: 10px;
        border-bottom: 1px solid #d2d2d7;
        margin-bottom: 20px;
    }

    /* Chart Containers */
    .chart-container {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #d2d2d7;
    }

    /* Data Tables */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
    }

    /* Buttons */
    .stButton>button {
        background-color: #0071e3;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: 500;
    }
    .stButton>button:hover {
        background-color: #0061c7;
    }

    /* Date Picker */
    .stDateInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #d2d2d7;
    }

    /* Apple-like polish */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }
    h1 {
        font-family: 'SF Pro Display', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 44px;
        letter-spacing: 0;
        line-height: 1.05;
        margin-bottom: 4px;
    }
    [data-testid="stCaptionContainer"] {
        color: #6e6e73;
        font-size: 15px;
    }
    .kpi-card {
        min-height: 245px;
        border-radius: 18px;
        border: 1px solid rgba(210,210,215,0.75);
        box-shadow: 0 12px 34px rgba(0,0,0,0.06);
        animation: floatIn 520ms cubic-bezier(.2,.8,.2,1) both;
    }
    .kpi-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 18px 45px rgba(0,0,0,0.10);
    }
    .chart-shell {
        background: rgba(255,255,255,0.86);
        border: 1px solid rgba(210,210,215,0.72);
        border-radius: 20px;
        padding: 14px 16px 10px;
        margin: 10px 0 18px;
        box-shadow: 0 18px 50px rgba(0,0,0,0.07);
        backdrop-filter: blur(18px);
        animation: floatIn 620ms cubic-bezier(.2,.8,.2,1) both;
    }
    .business-finding {
        background: linear-gradient(135deg, #f5f5f7 0%, #ffffff 100%);
        border: 1px solid rgba(210,210,215,0.8);
        border-left: 4px solid #0071e3;
        border-radius: 14px;
        padding: 12px 14px;
        margin: 8px 0 18px;
        color: #1d1d1f;
        font-size: 13px;
        line-height: 1.45;
        box-shadow: 0 8px 22px rgba(0,0,0,0.04);
    }
    .business-finding b {
        color: #0071e3;
    }
    .header {
        border-bottom: 0;
        margin-top: 12px;
        margin-bottom: 4px;
        font-size: 30px;
    }
    .stTabs [data-baseweb="tab-list"] {
        position: sticky;
        top: 0;
        z-index: 2;
        border: 1px solid rgba(210,210,215,0.7);
        backdrop-filter: blur(20px);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 999px;
    }
    .stTabs [aria-selected="true"] {
        background: #1d1d1f;
        color: #ffffff;
    }
    [data-testid="stSidebar"] {
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(20px);
    }
    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid rgba(210,210,215,0.8);
    }
    @keyframes floatIn {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS FOR BUSINESS-RELEVANT SYNTHETIC DATA ---
def generate_batch_data(n=200):
    """Generate synthetic batch production data with outliers and inefficiencies"""
    products = ["Acne Cream 5%", "Pain Relief Gel 10%", "Eczema Ointment 2%", "Antifungal Lotion 1%", "Psoriasis Cream 3%"]
    lines = ["Norden-Line-1", "Norden-Line-2", "Filler-1", "Filler-2", "Mixer-1", "Mixer-2"]
    failure_reasons = ["Equipment Malfunction", "Human Error", "Raw Material Contamination", "Temperature Deviation", "Pressure Issue"]
    data = []
    for _ in range(n):
        batch_id = f"BATCH-{fake.ean8()}"
        product = random.choice(products)
        line = random.choice(lines)
        date = fake.date_between(start_date='-1y', end_date='today')
        # Introduce more failures for specific lines/products to highlight inefficiencies
        if line in ["Norden-Line-1", "Filler-1"] or product in ["Acne Cream 5%", "Psoriasis Cream 3%"]:
            status = random.choices(["Success", "Failure", "On Hold"], weights=[0.6, 0.3, 0.1])[0]
        else:
            status = random.choices(["Success", "Failure", "On Hold"], weights=[0.85, 0.1, 0.05])[0]

        # Calculate OEE components (for Manufacturing tab)
        availability = random.uniform(0.85, 0.98) if line != "Norden-Line-1" else random.uniform(0.6, 0.8)
        performance = random.uniform(0.9, 0.98) if line != "Filler-1" else random.uniform(0.7, 0.85)
        quality = random.uniform(0.95, 0.99) if product != "Acne Cream 5%" else random.uniform(0.8, 0.9)
        oee = availability * performance * quality

        if status == "Failure":
            failure_reason = random.choice(failure_reasons)
            financial_loss = round(np.random.uniform(5000, 150000), 2)
            if line == "Norden-Line-1" and product == "Acne Cream 5%":
                financial_loss = round(np.random.uniform(100000, 300000), 2)
            rft = 0  # Right First Time
        else:
            failure_reason = None
            financial_loss = 0
            rft = 1  # Right First Time

        # Add some on-hold batches with long delays
        if status == "On Hold":
            days_on_hold = random.randint(1, 30)
        else:
            days_on_hold = 0

        # Add cycle time (for Manufacturing tab)
        cycle_time = random.uniform(2, 8) if line != "Norden-Line-1" else random.uniform(8, 15)

        data.append({
            "Batch_ID": batch_id,
            "Product": product,
            "Line": line,
            "Date": date,
            "Status": status,
            "Failure_Reason": failure_reason,
            "Financial_Loss": financial_loss,
            "Days_On_Hold": days_on_hold,
            "OEE": oee,
            "RFT": rft,
            "Cycle_Time": cycle_time
        })
    return pd.DataFrame(data)

def generate_quality_data(n=150):
    """Generate synthetic quality deviation data with outliers"""
    products = ["Acne Cream 5%", "Pain Relief Gel 10%", "Eczema Ointment 2%", "Antifungal Lotion 1%"]
    parameters = ["pH", "Viscosity (cP)", "Weight (g)", "Purity (%)", "Microbial Count (CFU)", "Particle Size (μm)"]
    data = []
    for _ in range(n):
        deviation_id = f"DEV-{fake.ean8()}"
        batch_id = f"BATCH-{fake.ean8()}"
        product = random.choice(products)
        parameter = random.choice(parameters)
        # Set expected ranges based on parameter
        if parameter == "pH":
            expected = round(np.random.uniform(5.5, 6.5), 2)
        elif parameter == "Viscosity (cP)":
            expected = round(np.random.uniform(5000, 10000), 2)
        elif parameter == "Weight (g)":
            expected = round(np.random.uniform(48, 52), 2)
        elif parameter == "Purity (%)":
            expected = round(np.random.uniform(98, 100), 2)
        elif parameter == "Microbial Count (CFU)":
            expected = round(np.random.uniform(0, 10), 2)
        else:
            expected = round(np.random.uniform(10, 50), 2)
        # Introduce deviations, with some extreme outliers
        if product == "Acne Cream 5%" and parameter == "Viscosity (cP)":
            actual = round(expected + np.random.uniform(-3000, 5000), 2)
        else:
            actual = round(expected + np.random.uniform(-1, 1), 2)
        deviation = abs(actual - expected)
        # Classify risk based on deviation and parameter
        if parameter == "Microbial Count (CFU)" and actual > 10:
            risk_level = "Critical"
        elif deviation > expected * 0.2:
            risk_level = "High"
        elif deviation > expected * 0.1:
            risk_level = "Medium"
        else:
            risk_level = "Low"
        # Add some critical outliers
        if random.random() < 0.05:
            risk_level = "Critical"
            actual = expected * 2
        # Add CAPA closure time (for Quality tab)
        capa_closure_time = random.randint(5, 30) if risk_level in ["Critical", "High"] else random.randint(1, 10)
        data.append({
            "Deviation_ID": deviation_id,
            "Batch_ID": batch_id,
            "Product": product,
            "Parameter": parameter,
            "Expected": expected,
            "Actual": actual,
            "Deviation": deviation,
            "Risk_Level": risk_level,
            "CAPA_Closure_Time": capa_closure_time
        })
    return pd.DataFrame(data)

def generate_inventory_data(n=50):
    """Generate synthetic inventory data with stockouts and overstocks"""
    products = ["API-A (Retinoid)", "API-B (Steroid)", "Excipient-X (Emulsifier)", "Excipient-Y (Preservative)",
               "Packaging-Tube-30g", "Packaging-Tube-60g", "Packaging-Jar-100g", "Label-Acne", "Label-Eczema"]
    data = []
    for product in products:
        for _ in range(n // len(products)):
            current_stock = round(np.random.uniform(500, 20000), 0)
            reorder_level = round(np.random.uniform(1000, 5000), 0)
            lead_time = random.choice([7, 14, 21, 30])
            cost_per_unit = random.uniform(10, 100)
            # Introduce stockouts and overstocks
            if product in ["API-A (Retinoid)", "Packaging-Tube-30g"]:
                current_stock = round(np.random.uniform(200, 800), 0)
                status = "Shortage"
            elif product in ["Excipient-Y (Preservative)", "Label-Acne"]:
                current_stock = round(np.random.uniform(15000, 30000), 0)
                status = "Overstock"
            else:
                status = "Optimal"
            # Add some extreme outliers
            if product == "API-B (Steroid)" and random.random() < 0.1:
                current_stock = 50
                status = "Critical Shortage"
            # Calculate inventory turnover (for Supply Chain tab)
            annual_usage = round(np.random.uniform(5000, 50000), 0)
            turnover_ratio = annual_usage / ((current_stock + reorder_level) / 2) if (current_stock + reorder_level) > 0 else 0
            data.append({
                "Product": product,
                "Current_Stock": current_stock,
                "Reorder_Level": reorder_level,
                "Lead_Time": lead_time,
                "Status": status,
                "Cost_Per_Unit": cost_per_unit,
                "Annual_Usage": annual_usage,
                "Turnover_Ratio": turnover_ratio
            })
    return pd.DataFrame(data)

def generate_equipment_data(n=120):
    """Generate synthetic equipment downtime data with outliers"""
    equipment = ["Norden-Line-1", "Norden-Line-2", "Filler-1", "Filler-2", "Mixer-1", "Mixer-2", "Homogenizer-1"]
    reasons = ["Preventive Maintenance", "Breakdown", "Calibration", "Cleaning", "Operator Error"]
    data = []
    for _ in range(n):
        eq_id = random.choice(equipment)
        date = fake.date_between(start_date='-1y', end_date='today')
        # Introduce more downtime for specific equipment
        if eq_id in ["Norden-Line-1", "Filler-1"]:
            downtime_hours = round(np.random.uniform(2, 48), 2)
            reason = random.choices(reasons, weights=[0.2, 0.5, 0.1, 0.1, 0.1])[0]
        else:
            downtime_hours = round(np.random.uniform(1, 12), 2)
            reason = random.choice(reasons)
        # Calculate production loss (higher for critical equipment)
        if eq_id in ["Norden-Line-1", "Norden-Line-2"]:
            production_loss = round(downtime_hours * np.random.uniform(2000, 5000), 2)
        else:
            production_loss = round(downtime_hours * np.random.uniform(500, 2000), 2)
        # Add extreme outliers
        if eq_id == "Norden-Line-1" and random.random() < 0.05:
            downtime_hours = 72
            production_loss = 50000
        # Add downtime prediction accuracy (for Manufacturing tab)
        prediction_accuracy = random.uniform(0.7, 0.95) if eq_id != "Norden-Line-1" else random.uniform(0.4, 0.6)
        data.append({
            "Equipment": eq_id,
            "Date": date,
            "Downtime_Hours": downtime_hours,
            "Reason": reason,
            "Production_Loss": production_loss,
            "Prediction_Accuracy": prediction_accuracy
        })
    return pd.DataFrame(data)

def generate_forecast_data(n=12):
    """Generate synthetic demand forecast vs actual data with outliers"""
    products = ["Acne Cream 5%", "Pain Relief Gel 10%", "Eczema Ointment 2%", "Antifungal Lotion 1%"]
    months = pd.date_range(start=datetime.now() - timedelta(days=365), periods=n, freq='ME').strftime('%b %Y').tolist()
    data = []
    for month in months:
        product = random.choice(products)
        # Base forecast with seasonality
        if "Q1" in month or "Q4" in month:
            base_forecast = round(np.random.uniform(80000, 150000), 0)
        else:
            base_forecast = round(np.random.uniform(50000, 100000), 0)
        # Introduce forecasting errors
        if product == "Pain Relief Gel 10%":
            error_pct = round(np.random.uniform(-30, 40), 2)
        else:
            error_pct = round(np.random.uniform(-15, 20), 2)
        actual = round(base_forecast * (1 + error_pct/100), 0)
        # Add extreme outliers
        if month == "Mar 2025" and product == "Acne Cream 5%":
            actual = base_forecast * 2
            error_pct = 100
        data.append({
            "Month": month,
            "Product": product,
            "Forecast": base_forecast,
            "Actual": actual,
            "Error_Percent": error_pct
        })
    return pd.DataFrame(data)

def generate_compliance_data(n=30):
    """Generate synthetic compliance audit data with critical findings"""
    audit_types = ["FDA Inspection", "EMA Audit", "CDSCO Audit", "ICH Q7 Audit", "GMP Certification"]
    findings_types = ["Documentation", "Process Control", "Equipment", "Training", "Data Integrity"]
    data = []
    for _ in range(n):
        audit_id = f"AUDIT-{fake.ean8()}"
        audit_type = random.choice(audit_types)
        date = fake.date_between(start_date='-1y', end_date='today')
        # FDA audits tend to have more findings
        if audit_type == "FDA Inspection":
            num_findings = random.randint(3, 10)
        else:
            num_findings = random.randint(0, 5)
        # Classify risk
        if num_findings > 5:
            risk = "Critical"
        elif num_findings > 2:
            risk = "High"
        else:
            risk = "Low"
        # Add some critical outliers
        if audit_type == "FDA Inspection" and random.random() < 0.2:
            num_findings = 15
            risk = "Critical"
        status = "Open" if risk in ["Critical", "High"] else "Closed"
        # Add finding types
        findings = random.choices(findings_types, k=num_findings)
        # Add audit readiness score (for Compliance tab)
        readiness_score = random.uniform(60, 95) if risk != "Critical" else random.uniform(30, 60)
        data.append({
            "Audit_ID": audit_id,
            "Type": audit_type,
            "Date": date,
            "Findings": num_findings,
            "Risk_Level": risk,
            "Status": status,
            "Finding_Types": ", ".join(findings),
            "Readiness_Score": readiness_score
        })
    return pd.DataFrame(data)

def generate_tech_transfer_data(n=20):
    """Generate synthetic technology transfer data with delays"""
    products = ["Acne Cream 5%", "Pain Relief Gel 10%", "Eczema Ointment 2%", "New Anti-Aging Serum"]
    stages = ["Documentation Review", "Lab Testing", "Pilot Batch", "Scale-Up", "Validation", "Commercial Batch"]
    data = []
    for _ in range(n):
        transfer_id = f"TT-{fake.ean8()}"
        product = random.choice(products)
        # New products have longer transfers
        if product == "New Anti-Aging Serum":
            start_date = fake.date_between(start_date='-1y', end_date='-8M')
            base_delay = random.randint(60, 180)
        else:
            start_date = fake.date_between(start_date='-1y', end_date='-4M')
            base_delay = random.randint(0, 90)
        # Add delays
        delay_days = base_delay + random.randint(-30, 60)
        end_date = start_date + timedelta(days=delay_days + 90)  # Base 90 days + delay
        # Current stage
        if delay_days > 60:
            stage = "Validation"
        elif delay_days > 30:
            stage = "Scale-Up"
        else:
            stage = random.choice(stages[:3])
        # Add extreme outliers
        if product == "New Anti-Aging Serum" and random.random() < 0.3:
            delay_days = 200
        # Calculate success rate (for R&D tab)
        success = 1 if delay_days <= 30 else 0
        data.append({
            "Transfer_ID": transfer_id,
            "Product": product,
            "Stage": stage,
            "Start_Date": start_date,
            "End_Date": end_date,
            "Delay_Days": delay_days,
            "Success": success
        })
    return pd.DataFrame(data)

def generate_bottleneck_data(n=150):
    """Generate synthetic process bottleneck data with inefficiencies"""
    processes = ["Mixing", "Filling", "Packaging", "QC Testing", "Labeling", "Homogenization"]
    reasons = ["Equipment Failure", "Material Shortage", "Operator Error", "Process Variability", "Changeover Delay"]
    data = []
    for _ in range(n):
        process = random.choice(processes)
        date = fake.date_between(start_date='-1y', end_date='today')
        # Introduce more bottlenecks for specific processes
        if process in ["Filling", "Packaging"]:
            duration = round(np.random.uniform(2, 12), 2)
            bottleneck = random.choices(["Yes", "No"], weights=[0.4, 0.6])[0]
        else:
            duration = round(np.random.uniform(1, 6), 2)
            bottleneck = random.choices(["Yes", "No"], weights=[0.2, 0.8])[0]
        if bottleneck == "Yes":
            reason = random.choice(reasons)
            # Higher impact for critical processes
            if process in ["Filling", "Packaging"]:
                impact = round(np.random.uniform(5000, 50000), 2)
            else:
                impact = round(np.random.uniform(1000, 20000), 2)
            # Add extreme outliers
            if process == "Filling" and random.random() < 0.1:
                impact = 100000
        else:
            reason = None
            impact = 0
        data.append({
            "Process": process,
            "Date": date,
            "Duration_Hours": duration,
            "Bottleneck": bottleneck,
            "Reason": reason,
            "Impact": impact
        })
    return pd.DataFrame(data)

# --- LOAD SYNTHETIC DATA ---
@st.cache_data
def load_data():
    return {
        "batch": generate_batch_data(200),
        "quality": generate_quality_data(150),
        "inventory": generate_inventory_data(50),
        "equipment": generate_equipment_data(120),
        "forecast": generate_forecast_data(12),
        "compliance": generate_compliance_data(30),
        "tech_transfer": generate_tech_transfer_data(20),
        "bottleneck": generate_bottleneck_data(150)
    }

data = load_data()

required_columns = {
    "batch": {"Batch_ID", "Product", "Line", "Date", "Status", "OEE", "RFT", "Cycle_Time"},
    "quality": {"Deviation_ID", "Batch_ID", "Product", "Risk_Level", "CAPA_Closure_Time"},
    "inventory": {"Product", "Current_Stock", "Status", "Annual_Usage", "Turnover_Ratio"},
    "equipment": {"Equipment", "Date", "Downtime_Hours", "Prediction_Accuracy"},
    "forecast": {"Month", "Product", "Forecast", "Actual", "Error_Percent"},
    "compliance": {"Type", "Date", "Findings", "Risk_Level", "Readiness_Score"},
    "tech_transfer": {"Product", "Stage", "Delay_Days", "Success"},
    "bottleneck": {"Process", "Date", "Duration_Hours", "Impact"},
}

missing_columns = {
    name: sorted(columns - set(data[name].columns))
    for name, columns in required_columns.items()
    if name not in data or columns - set(data[name].columns)
}

if missing_columns:
    load_data.clear()
    data = load_data()
    missing_columns = {
        name: sorted(columns - set(data[name].columns))
        for name, columns in required_columns.items()
        if name not in data or columns - set(data[name].columns)
    }
    if missing_columns:
        st.error(f"Dashboard data schema is incomplete: {missing_columns}")
        st.stop()

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.image("https://via.placeholder.com/200x80/0071e3/ffffff?text=Encube+Ethicals", use_container_width=True)
    st.markdown("## 🔍 Filters")
    st.markdown("---")

    # Date Range Filter
    st.markdown("### 📅 Date Range")
    date_range = st.date_input(
        "Select Date Range",
        value=[datetime.now() - timedelta(days=365), datetime.now()],
        max_value=datetime.now(),
        min_value=datetime.now() - timedelta(days=730),
        key="date_range"
    )

    # Product Filter
    st.markdown("### 🏭 Product")
    all_products = sorted(set(data['batch']['Product'].unique()).union(set(data['quality']['Product'].unique())))
    selected_products = st.multiselect(
        "Select Products",
        options=all_products,
        default=all_products,
        key="product_filter"
    )

    # Line/Equipment Filter
    st.markdown("### 🏗️ Equipment/Line")
    all_equipment = sorted(set(data['equipment']['Equipment'].unique()).union(set(data['batch']['Line'].unique())))
    selected_equipment = st.multiselect(
        "Select Equipment/Line",
        options=all_equipment,
        default=all_equipment,
        key="equipment_filter"
    )

    # Status Filter
    st.markdown("### 📊 Batch Status")
    batch_statuses = st.multiselect(
        "Select Status",
        options=["Success", "Failure", "On Hold"],
        default=["Success", "Failure", "On Hold"],
        key="batch_status_filter"
    )

    # Risk Level Filter
    st.markdown("### ⚠️ Quality Risk Level")
    risk_levels = st.multiselect(
        "Select Risk Level",
        options=["Critical", "High", "Medium", "Low"],
        default=["Critical", "High", "Medium", "Low"],
        key="risk_filter"
    )

    # Inventory Status Filter
    st.markdown("### 📦 Inventory Status")
    inventory_statuses = st.multiselect(
        "Select Status",
        options=["Optimal", "Shortage", "Overstock", "Critical Shortage"],
        default=["Optimal", "Shortage", "Overstock", "Critical Shortage"],
        key="inventory_status_filter"
    )

    st.markdown("---")
    st.markdown("### 📥 Export Data")
    if st.button("📊 Download Dashboard Data"):
        # Create a combined CSV
        combined_data = {}
        for name, df in data.items():
            combined_data[name] = df.to_csv(index=False)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for name, csv_data in combined_data.items():
                zip_file.writestr(f"{name}.csv", csv_data)

        st.download_button(
            label="Download CSV ZIP",
            data=zip_buffer.getvalue(),
            file_name="encube_dashboard_data.zip",
            mime="application/zip"
        )


def filter_by_date(df, date_col="Date"):
    if date_col not in df.columns or len(date_range) != 2:
        return df
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    filtered = df.copy()
    filtered[date_col] = pd.to_datetime(filtered[date_col])
    return filtered[(filtered[date_col] >= start_date) & (filtered[date_col] <= end_date)]


def kpi_card(title, value, context, ai_opportunity, business_value):
    st.markdown(
        f"""
        <div class="kpi-card">
            <h4 style="margin: 0 0 6px 0;">{title}</h4>
            <div style="font-size: 30px; font-weight: 700; color: #0071e3; margin-bottom: 8px;">{value}</div>
            <div style="font-size: 13px; color: #515154; line-height: 1.45;"><b>What it measures:</b> {context}</div>
            <div style="font-size: 13px; color: #515154; line-height: 1.45; margin-top: 6px;"><b>AI opportunity:</b> {ai_opportunity}</div>
            <div style="font-size: 13px; color: #1d1d1f; line-height: 1.45; margin-top: 6px;"><b>Business value:</b> {business_value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_header(title, subtitle):
    st.markdown(f"<h2 class='header'>{title}</h2>", unsafe_allow_html=True)
    st.caption(subtitle)


APPLE_COLORS = ["#0071e3", "#34c759", "#ff9500", "#af52de", "#5ac8fa", "#ff3b30", "#5856d6", "#8e8e93"]
RISK_COLORS = {
    "Critical": "#ff3b30",
    "High": "#ff9500",
    "Medium": "#ffd60a",
    "Low": "#34c759",
    "Open": "#ff9500",
    "Closed": "#34c759",
    "Shortage": "#ff9500",
    "Critical Shortage": "#ff3b30",
    "Overstock": "#5856d6",
    "Optimal": "#34c759",
    "Forecast": "#0071e3",
    "Actual": "#34c759",
}


def style_chart(fig, height=390):
    fig.update_layout(
        height=height,
        template="plotly_white",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="SF Pro Text, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif", color="#1d1d1f"),
        title=dict(font=dict(size=18, color="#1d1d1f"), x=0.02, xanchor="left"),
        margin=dict(l=35, r=25, t=58, b=45),
        hoverlabel=dict(bgcolor="#1d1d1f", font_color="#ffffff", bordercolor="#1d1d1f"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        transition=dict(duration=450, easing="cubic-in-out"),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, tickfont=dict(color="#6e6e73"))
    fig.update_yaxes(gridcolor="rgba(210,210,215,0.55)", zeroline=False, tickfont=dict(color="#6e6e73"))
    return fig


def render_chart(fig, finding):
    st.markdown("<div class='chart-shell'>", unsafe_allow_html=True)
    st.plotly_chart(style_chart(fig), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='business-finding'><b>Key finding:</b> {finding}</div>", unsafe_allow_html=True)


def add_bar_highlight(fig, df, x_col, y_col, label_prefix="Outlier"):
    if df.empty:
        return fig
    row = df.loc[df[y_col].idxmax()]
    fig.add_scatter(
        x=[row[x_col]],
        y=[row[y_col]],
        mode="markers+text",
        marker=dict(size=18, color="#ff3b30", symbol="circle-open", line=dict(width=3)),
        text=[label_prefix],
        textposition="top center",
        showlegend=False,
        hovertemplate=f"{label_prefix}<br>{x_col}: %{{x}}<br>{y_col}: %{{y:.2f}}<extra></extra>",
    )
    return fig


def add_threshold_line(fig, y_value, label, color="#ff3b30"):
    fig.add_hline(
        y=y_value,
        line_dash="dot",
        line_color=color,
        annotation_text=label,
        annotation_position="top left",
        annotation_font_color=color,
    )
    return fig


def add_scatter_highlight(fig, df, x_col, y_col, label_prefix="Highest impact"):
    if df.empty:
        return fig
    row = df.loc[df[y_col].idxmax()]
    fig.add_scatter(
        x=[row[x_col]],
        y=[row[y_col]],
        mode="markers+text",
        marker=dict(size=22, color="#ff3b30", symbol="circle-open", line=dict(width=3)),
        text=[label_prefix],
        textposition="top center",
        showlegend=False,
        hovertemplate=f"{label_prefix}<br>{x_col}: %{{x:.2f}}<br>{y_col}: %{{y:.2f}}<extra></extra>",
    )
    return fig


# --- FILTER DATA ---
batch_df = filter_by_date(data["batch"])
batch_df = batch_df[
    batch_df["Product"].isin(selected_products)
    & batch_df["Line"].isin(selected_equipment)
    & batch_df["Status"].isin(batch_statuses)
]

quality_df = data["quality"][data["quality"]["Product"].isin(selected_products)]
quality_df = quality_df[quality_df["Risk_Level"].isin(risk_levels)]

inventory_df = data["inventory"][data["inventory"]["Status"].isin(inventory_statuses)]

equipment_df = filter_by_date(data["equipment"])
equipment_df = equipment_df[equipment_df["Equipment"].isin(selected_equipment)]

forecast_df = data["forecast"]
compliance_df = filter_by_date(data["compliance"])
tech_transfer_df = data["tech_transfer"]
bottleneck_df = filter_by_date(data["bottleneck"])


# --- DERIVED KPI VALUES ---
oee_pct = batch_df["OEE"].mean() * 100 if not batch_df.empty else 0
rft_pct = batch_df["RFT"].mean() * 100 if not batch_df.empty else 0
deviation_rate = len(quality_df) / max(batch_df["Batch_ID"].nunique(), 1) * 100
capa_days = quality_df["CAPA_Closure_Time"].mean() if not quality_df.empty else 0
cycle_time = batch_df["Cycle_Time"].mean() if not batch_df.empty else 0
forecast_accuracy = 100 - forecast_df["Error_Percent"].abs().mean() if not forecast_df.empty else 0
inventory_turnover = inventory_df["Turnover_Ratio"].mean() if not inventory_df.empty else 0
tech_transfer_success = tech_transfer_df["Success"].mean() * 100 if not tech_transfer_df.empty else 0
audit_readiness = compliance_df["Readiness_Score"].mean() if not compliance_df.empty else 0
downtime_prediction = equipment_df["Prediction_Accuracy"].mean() * 100 if not equipment_df.empty else 0


# --- MAIN DASHBOARD ---
st.markdown("# Encube Ethicals | AI-Powered Manufacturing Insights")
st.caption("Synthetic operating dashboard for pharma manufacturing, quality, supply chain, technology transfer, and compliance.")

tab_manufacturing, tab_quality, tab_supply, tab_tech, tab_compliance = st.tabs([
    "Manufacturing",
    "Quality",
    "Supply Chain",
    "Technology Transfer",
    "Compliance"
])

with tab_manufacturing:
    section_header("Manufacturing Performance", "Production efficiency, throughput, bottlenecks, and equipment reliability.")
    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_card(
            "OEE (Overall Equipment Effectiveness)",
            f"{oee_pct:.1f}%",
            "How effectively manufacturing equipment is utilized through availability, performance, and quality.",
            "Predictive maintenance, bottleneck analytics, and utilization optimization.",
            "Increased capacity, reduced downtime, and better asset utilization."
        )
    with col2:
        kpi_card(
            "Production Cycle Time",
            f"{cycle_time:.1f} hrs",
            "Total time required to manufacture a batch or product.",
            "Process mining, workflow optimization, delay prediction, and scheduling optimization.",
            "Faster production, higher throughput, and better customer fulfillment."
        )
    with col3:
        kpi_card(
            "Manufacturing Downtime Prediction Accuracy",
            f"{downtime_prediction:.1f}%",
            "Ability to predict production interruptions before they affect output.",
            "Sensor analytics, time-series anomaly detection, and predictive maintenance.",
            "Reduced unplanned stoppages and improved manufacturing continuity."
        )

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        oee_by_line = batch_df.groupby("Line", as_index=False)["OEE"].mean()
        oee_by_line["OEE"] = oee_by_line["OEE"] * 100
        fig = px.bar(oee_by_line, x="Line", y="OEE", color="Line", title="OEE by Manufacturing Line", color_discrete_sequence=APPLE_COLORS)
        fig.update_layout(showlegend=False, yaxis_title="OEE %")
        add_threshold_line(fig, 75, "OEE watch zone", "#ff9500")
        if not oee_by_line.empty:
            low_oee = oee_by_line.loc[oee_by_line["OEE"].idxmin()]
            fig.add_scatter(
                x=[low_oee["Line"]],
                y=[low_oee["OEE"]],
                mode="markers+text",
                marker=dict(size=18, color="#ff3b30", symbol="circle-open", line=dict(width=3)),
                text=["Lowest OEE"],
                textposition="top center",
                showlegend=False,
            )
        render_chart(
            fig,
            "The lowest-OEE line is the first candidate for bottleneck analytics because every availability or quality loss directly reduces usable manufacturing capacity."
        )
    with chart_col2:
        downtime_by_equipment = equipment_df.groupby("Equipment", as_index=False)["Downtime_Hours"].sum()
        fig = px.bar(downtime_by_equipment, x="Equipment", y="Downtime_Hours", color="Equipment", title="Downtime Hours by Equipment", color_discrete_sequence=APPLE_COLORS)
        fig.update_layout(showlegend=False)
        add_bar_highlight(fig, downtime_by_equipment, "Equipment", "Downtime_Hours", "Downtime outlier")
        render_chart(
            fig,
            "Equipment with concentrated downtime should move to predictive maintenance priority because it creates avoidable production loss and delivery risk."
        )

    bottleneck_summary = bottleneck_df.groupby("Process", as_index=False).agg(Duration_Hours=("Duration_Hours", "mean"), Impact=("Impact", "sum"))
    fig = px.scatter(
        bottleneck_summary,
        x="Duration_Hours",
        y="Impact",
        size="Impact",
        color="Process",
        title="Process Bottleneck Impact",
        color_discrete_sequence=APPLE_COLORS
    )
    add_scatter_highlight(fig, bottleneck_summary, "Duration_Hours", "Impact", "Highest loss")
    render_chart(
        fig,
        "The highest-impact bottleneck is the best target for scheduling optimization because small cycle-time reductions here release capacity across downstream steps."
    )

with tab_quality:
    section_header("Quality Intelligence", "Batch quality, deviations, and CAPA governance for topical formulation operations.")
    col1, col2, col3 = st.columns(3)
    with col1:
        kpi_card(
            "Batch Right-First-Time (RFT%)",
            f"{rft_pct:.1f}%",
            "Share of batches passing quality standards without rework.",
            "Batch risk prediction, process parameter analytics, and environmental anomaly detection.",
            "Reduced wastage, faster release cycles, and higher customer trust."
        )
    with col2:
        kpi_card(
            "Deviation Rate",
            f"{deviation_rate:.1f}%",
            "Frequency of manufacturing or quality deviations relative to produced batches.",
            "Anomaly detection, root cause analytics, pattern recognition, and predictive quality monitoring.",
            "Reduced compliance risk, faster investigations, and improved process control."
        )
    with col3:
        kpi_card(
            "CAPA Closure Time",
            f"{capa_days:.1f} days",
            "How quickly corrective and preventive actions are resolved.",
            "NLP-based deviation classification, CAPA recommendation engines, and similar-case retrieval.",
            "Faster issue resolution, reduced repeat incidents, and stronger quality governance."
        )

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        risk_counts = quality_df["Risk_Level"].value_counts().reset_index()
        risk_counts.columns = ["Risk_Level", "Count"]
        pull_values = [0.12 if risk == "Critical" else 0 for risk in risk_counts["Risk_Level"]]
        fig = px.pie(
            risk_counts,
            names="Risk_Level",
            values="Count",
            title="Deviation Risk Mix",
            color="Risk_Level",
            color_discrete_map=RISK_COLORS
        )
        fig.update_traces(hole=0.58, pull=pull_values, textinfo="percent+label", marker=dict(line=dict(color="#ffffff", width=2)))
        render_chart(
            fig,
            "Critical and high-risk deviations are the quality signals to classify first because they drive investigation load, release delays, and audit exposure."
        )
    with chart_col2:
        capa_by_product = quality_df.groupby("Product", as_index=False)["CAPA_Closure_Time"].mean()
        fig = px.bar(capa_by_product, x="Product", y="CAPA_Closure_Time", color="Product", title="Average CAPA Closure Time", color_discrete_sequence=APPLE_COLORS)
        fig.update_layout(showlegend=False, yaxis_title="Days")
        add_threshold_line(fig, 15, "Closure delay threshold", "#ff9500")
        add_bar_highlight(fig, capa_by_product, "Product", "CAPA_Closure_Time", "Slowest CAPA")
        render_chart(
            fig,
            "The slowest product-level CAPA cycle points to where similar-case retrieval and recommendation engines can reduce repeat investigations."
        )

    st.dataframe(quality_df.sort_values("CAPA_Closure_Time", ascending=False).head(20), use_container_width=True)

with tab_supply:
    section_header("Supply Chain Planning", "Demand planning, inventory efficiency, stock risk, and replenishment signals.")
    col1, col2 = st.columns(2)
    with col1:
        kpi_card(
            "Forecast Accuracy",
            f"{forecast_accuracy:.1f}%",
            "How accurately future demand is predicted versus actual demand.",
            "Time-series forecasting, demand sensing, and seasonal pattern analysis.",
            "Better inventory planning, lower working capital, and improved customer fulfillment."
        )
    with col2:
        kpi_card(
            "Inventory Turnover Ratio",
            f"{inventory_turnover:.2f}x",
            "How efficiently inventory is utilized across APIs, excipients, packaging, and labels.",
            "Inventory optimization, demand prediction, and smart replenishment systems.",
            "Reduced holding cost, lower wastage, and improved supply continuity."
        )

    forecast_long = forecast_df.melt(id_vars=["Month", "Product"], value_vars=["Forecast", "Actual"], var_name="Measure", value_name="Units")
    fig = px.line(
        forecast_long,
        x="Month",
        y="Units",
        color="Measure",
        markers=True,
        title="Forecast vs Actual Demand",
        color_discrete_map=RISK_COLORS
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    if not forecast_df.empty:
        forecast_df = forecast_df.copy()
        forecast_df["Abs_Error"] = forecast_df["Error_Percent"].abs()
        worst_forecast = forecast_df.loc[forecast_df["Abs_Error"].idxmax()]
        fig.add_scatter(
            x=[worst_forecast["Month"]],
            y=[worst_forecast["Actual"]],
            mode="markers+text",
            marker=dict(size=18, color="#ff3b30", symbol="circle-open", line=dict(width=3)),
            text=["Forecast miss"],
            textposition="top center",
            showlegend=False,
        )
    render_chart(
        fig,
        "The largest forecast miss should feed demand-sensing models because it can cause either stockouts or excess inventory before production planning catches up."
    )

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig = px.bar(
            inventory_df,
            x="Product",
            y="Current_Stock",
            color="Status",
            title="Inventory Position by Material",
            color_discrete_map=RISK_COLORS
        )
        add_bar_highlight(fig, inventory_df, "Product", "Current_Stock", "Stock outlier")
        render_chart(
            fig,
            "Overstocked and shortage materials need different actions, but both represent working-capital leakage and supply continuity risk."
        )
    with chart_col2:
        fig = px.scatter(
            inventory_df,
            x="Turnover_Ratio",
            y="Current_Stock",
            color="Status",
            size="Annual_Usage",
            hover_name="Product",
            title="Inventory Efficiency and Stock Exposure",
            color_discrete_map=RISK_COLORS
        )
        add_threshold_line(fig, inventory_df["Current_Stock"].median() if not inventory_df.empty else 0, "Median stock", "#8e8e93")
        add_scatter_highlight(fig, inventory_df, "Turnover_Ratio", "Current_Stock", "Exposure outlier")
        render_chart(
            fig,
            "High stock with weak turnover is the strongest replenishment optimization opportunity because it ties cash to materials that are not moving efficiently."
        )

with tab_tech:
    section_header("Technology Transfer", "Transfer execution risk, timeline visibility, and commercialization readiness.")
    kpi_card(
        "Technology Transfer Success Rate",
        f"{tech_transfer_success:.1f}%",
        "Success and efficiency of transferring formulations and processes between plants, regions, and manufacturing setups.",
        "Transfer risk prediction, timeline forecasting, process conformance analytics, and knowledge intelligence systems.",
        "Faster commercialization, reduced transfer delays, and better process standardization."
    )

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig = px.bar(
            tech_transfer_df,
            x="Product",
            y="Delay_Days",
            color="Stage",
            title="Transfer Delay by Product and Stage",
            color_discrete_sequence=APPLE_COLORS
        )
        add_threshold_line(fig, 60, "High transfer delay", "#ff3b30")
        add_bar_highlight(fig, tech_transfer_df, "Product", "Delay_Days", "Delay outlier")
        render_chart(
            fig,
            "Transfers beyond the delay threshold should receive risk prediction support because they slow commercialization and standardization across sites."
        )
    with chart_col2:
        stage_counts = tech_transfer_df["Stage"].value_counts().reset_index()
        stage_counts.columns = ["Stage", "Transfers"]
        max_stage = stage_counts["Transfers"].max() if not stage_counts.empty else 0
        fig = px.pie(stage_counts, names="Stage", values="Transfers", title="Current Transfer Stage Mix", color_discrete_sequence=APPLE_COLORS)
        fig.update_traces(
            hole=0.58,
            pull=[0.1 if value == max_stage else 0 for value in stage_counts["Transfers"]],
            textinfo="percent+label",
            marker=dict(line=dict(color="#ffffff", width=2))
        )
        render_chart(
            fig,
            "The most crowded transfer stage is the governance checkpoint where knowledge intelligence can reduce handoff friction and timeline uncertainty."
        )

    st.dataframe(tech_transfer_df.sort_values("Delay_Days", ascending=False), use_container_width=True)

with tab_compliance:
    section_header("Audit and Compliance", "Audit readiness, finding trends, and regulatory inspection risk.")
    kpi_card(
        "Audit Readiness / Compliance Score",
        f"{audit_readiness:.1f}%",
        "Operational compliance preparedness across audits, documentation, process control, training, and data integrity.",
        "Compliance dashboards, SOP intelligence copilots, automated evidence retrieval, and deviation trend monitoring.",
        "Reduced audit risk, faster inspections, better regulatory confidence, and reduced manual effort."
    )

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        fig = px.bar(
            compliance_df,
            x="Type",
            y="Findings",
            color="Risk_Level",
            title="Audit Findings by Audit Type",
            color_discrete_map=RISK_COLORS
        )
        add_threshold_line(fig, 5, "Inspection risk threshold", "#ff3b30")
        add_bar_highlight(fig, compliance_df, "Type", "Findings", "Finding outlier")
        render_chart(
            fig,
            "Audit types crossing the finding threshold should drive automated evidence retrieval and SOP readiness checks before inspection windows."
        )
    with chart_col2:
        fig = px.box(
            compliance_df,
            x="Risk_Level",
            y="Readiness_Score",
            color="Risk_Level",
            title="Readiness Score by Risk Level",
            color_discrete_map=RISK_COLORS,
            points="all"
        )
        add_threshold_line(fig, 70, "Readiness floor", "#ff9500")
        render_chart(
            fig,
            "Low readiness clusters reveal where compliance intelligence matters most: closing documentation gaps before they become regulatory observations."
        )

    st.dataframe(compliance_df.sort_values("Findings", ascending=False), use_container_width=True)
