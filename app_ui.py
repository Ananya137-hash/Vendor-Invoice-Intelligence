import streamlit as st
import pandas as pd
import numpy as np
import time
from inference.predict_invoice_flag import predict_invoice_flag
from inference.predict_freight import predict_freight_cost

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Vendor Invoice Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# DYNAMIC THEME STATE MANAGEMENT
# ==========================================
# Initialize the theme state on the very first load
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# Define Full Page Colors based on the current state
if st.session_state.dark_mode:
    page_bg = "#0E1117"      # Deep dark background
    sidebar_bg = "#262730"   # Slightly lighter dark for sidebar
    text_color = "#FAFAFA"   # White text
    title_color = "#60A5FA"  # Bright Blue (Pops on dark)
    sub_color = "#94A3B8"    # Light Grey
else:
    page_bg = "#F8FAFC"      # Very soft blue/white background
    sidebar_bg = "#FFFFFF"   # Pure white sidebar
    text_color = "#0F172A"   # Dark text
    title_color = "#1E3A8A"  # Deep Blue
    sub_color = "#475569"    # Medium Grey

# Injecting CSS to override Streamlit's entire page background
theme_css = f"""
<style>
    /* Hide Streamlit Defaults */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Force Full Page Main Background */
    [data-testid="stAppViewContainer"] {{
        background-color: {page_bg} !important;
    }}
    
    /* Force Sidebar Background */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
    }}

    /* Target ALL nested text components */
    .stMarkdown p, 
    .stMarkdown li, 
    .stNumberInput label p,
    [data-testid="stWidgetLabel"] p,  
    [role="radiogroup"] p,            
    summary p,                        
    h1, h2, h3, h4, h5, h6            
    {{
        color: {text_color} !important;
    }}

    /* Style the main title */
    .main-title {{
        font-size: 3.8rem !important; 
        font-weight: 800;
        color: {title_color} !important;
        margin-bottom: 0rem;
        line-height: 1.2;
    }}
    
    .sub-title {{
        font-size: 1.4rem;
        color: {sub_color} !important;
        margin-bottom: 2rem;
    }}
    
    /* Make the predict buttons stand out */
    div.stButton > button:first-child {{
        background-color: #0F172A !important;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
        width: 100%;
    }}
    
    /* Force predict button text to STAY white */
    div.stButton > button:first-child p {{
        color: #FFFFFF !important;
    }}

    div.stButton > button:first-child:hover {{
        background-color: #334155 !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }}
</style>
"""
st.markdown(theme_css, unsafe_allow_html=True)

# ==========================================
# HEADER SECTION & TOP-RIGHT TOGGLE
# ==========================================
# Create a layout with 85% width for the title, 15% width for the toggle
top_left, top_right = st.columns([0.85, 0.15])

with top_right:
    st.write("") # tiny spacer to push it down slightly
    # The label changes dynamically based on the current state!
    toggle_label = "🌙 Dark Mode" if st.session_state.dark_mode else "☀️ Light Mode"
    
    # By using key="dark_mode", Streamlit locks this widget to the session state
    st.toggle(toggle_label, key="dark_mode")

with top_left:
    st.markdown('<p class="main-title">Vendor Invoice Intelligence Portal ⚡</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">AI-Driven Freight Cost Prediction & Invoice Risk Flagging</p>', unsafe_allow_html=True)

with st.expander("ℹ️ About this Portal", expanded=False):
    st.markdown("""
    This internal analytics portal leverages machine learning to:
    - 🎯 **Forecast freight costs accurately**
    - 🛡️ **Detect risky or abnormal vendor invoices**
    - 📉 **Reduce financial leakage and manual workload**
    """)

st.divider()

# ==========================================
# SIDEBAR
# ==========================================
with st.sidebar:
    st.write("") # Spacer 
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135679.png", width=60) 
    
    st.markdown(f"**<span style='color:{text_color}; font-size:1.2rem;'>Module Selection</span>**", unsafe_allow_html=True)
    
    selected_model = st.radio(
        "Active Workflow:",
        ["Freight Cost Prediction", "Invoice Manual Approval Flag"],
        label_visibility="collapsed"
    )
    
    st.divider()
    st.markdown(f"**<span style='color:{title_color}; font-size:1.1rem;'>📈 Business Impact</span>**", unsafe_allow_html=True)
    st.info("✓ Improved cost forecasting\n\n✓ Reduced invoice fraud\n\n✓ Faster finance operations")

# ==========================================
# MODULE 1: FREIGHT COST PREDICTION
# ==========================================
if selected_model == "Freight Cost Prediction":
    st.subheader("📦 Freight Cost Predictor")
    st.caption("Forecast expected freight charges based on invoice volume and total value.")
    
    # Wrap form in a clean UI card
    with st.container(border=True):
        with st.form("freight_form"):
            col1, col2 = st.columns(2)
            with col1:
                quantity = st.number_input("Total Quantity", min_value=1, value=1200, step=10)
            with col2:
                dollars = st.number_input("Invoice Dollars ($)", min_value=1.0, value=18500.0, step=100.0)
            
            st.write("") # Spacer
            submit_freight = st.form_submit_button("Predict Freight Cost")
            
    # Process Results
    if submit_freight:
        with st.spinner("Calculating optimal freight cost..."):
            time.sleep(0.7) # Smooth UI delay
            
            input_data = {
                "Quantity": [quantity],
                "Dollars": [dollars]
            }
            
            prediction = predict_freight_cost(input_data)['Predicted_Freight']
            
            st.toast("Prediction successful!", icon="✅")
            
            st.success("Analysis Complete.")
            st.metric(
                label="Estimated Freight Cost",
                value=f"${prediction[0]:,.2f}",
                delta="Algorithm Confidence: High",
                delta_color="normal"
            )

# ==========================================
# MODULE 2: INVOICE FLAG PREDICTION
# ==========================================
else:
    st.subheader("🛡️ Anomaly Detection & Risk Flagging")
    st.caption("Identify abnormal vendor invoices requiring manual audit.")
    
    with st.container(border=True):
        with st.form("invoice_flag_form"):
            st.markdown("**Invoice Details**")
            col1, col2, col3 = st.columns(3)
            with col1:
                invoice_quantity = st.number_input("Invoice Quantity", min_value=1, value=50)
                freight = st.number_input("Freight Cost ($)", min_value=0.0, value=1.73)
            with col2:
                invoice_dollars = st.number_input("Invoice Dollars ($)", min_value=1.0, value=352.95)
                total_item_quantity = st.number_input("Total Item Quantity", min_value=1, value=162)
            with col3:
                total_item_dollars = st.number_input("Total Item Dollars ($)", min_value=1.0, value=2476.0)
            
            st.write("") # Spacer
            submit_flag = st.form_submit_button("Evaluate Risk")

    # Process Results
    if submit_flag:
        with st.spinner("Analyzing historical patterns..."):
            time.sleep(0.8) # Smooth UI delay
            
            input_data = {
                "invoice_quantity": invoice_quantity,
                "invoice_dollars": invoice_dollars,
                "Freight": freight,
                "total_item_quantity": total_item_quantity,
                "total_item_dollars": total_item_dollars
            }
            
            flag_prediction = predict_invoice_flag(input_data)['predicted_invoice_flag']
            is_flagged = bool(flag_prediction[0])
            
        if is_flagged:
            st.toast("Anomaly Detected!", icon="🚨")
            st.error("### 🛑 MANUAL APPROVAL REQUIRED\nThis invoice exhibits irregular patterns and has been flagged for financial review.")
        else:
            st.toast("Invoice Verified", icon="✅")
            st.success("### ✅ SAFE FOR AUTOMATIC PROCESSING\nThis invoice aligns with standard vendor historical data.")