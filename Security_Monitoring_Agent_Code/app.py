import streamlit as st
import pandas as pd
from log_collector import collect_logs
from log_compressor import compress_logs
from anomaly_detector import detect_anomalies

# Page Configuration
st.set_page_config(
    page_title="Security Monitoring Agent",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: black;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #1e1e1e;
        border-left: 5px solid #6c5ce7;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize Session State
if 'data_processed' not in st.session_state:
    st.session_state.data_processed = False

# Sidebar
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.markdown("---")
    st.write("**Agent Status:** 🟢 Online")
    
    if st.button("🚀 Run Security Scan", type="primary", use_container_width=True):
        with st.spinner("Ingesting & Compressing Logs..."):
            # 1. Log Ingestion
            raw_df = collect_logs()
            
            # 2. Compression
            compressed_df = compress_logs(raw_df)
            
            # 3. Anomaly Detection
            alerts, preds = detect_anomalies(compressed_df)
            
            # Store in session state
            st.session_state.raw_df = raw_df
            st.session_state.compressed_df = compressed_df
            st.session_state.alerts = alerts
            st.session_state.data_processed = True
            
    st.markdown("---")
    st.info("This agent compresses logs by ~80% to reduce processing costs.")

# Main Dashboard
st.title("🛡️ AI-Powered Security Monitoring Agent")
st.markdown("### Threat Intelligence & Log Compression Dashboard")

if st.session_state.data_processed:
    raw_df = st.session_state.raw_df
    compressed_df = st.session_state.compressed_df
    alerts = st.session_state.alerts
    
    # Metrics
    compression_ratio = (1 - len(compressed_df) / len(raw_df)) * 100
    
    st.markdown("#### System Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Raw Events", len(raw_df), delta="Ingested")
    col2.metric("Compressed Events", len(compressed_df), delta="-80% Volume", delta_color="inverse")
    col3.metric("Cost Savings", f"{compression_ratio:.0f}%", delta="Optimized")
    col4.metric("Threats Detected", len(alerts), delta="Anomalies", delta_color="inverse" if len(alerts) > 0 else "normal")
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📈 System Health", "🚨 Threat Intelligence", "💾 Data Inspector"])
    
    with tab1:
        st.subheader("Real-time System Metrics (Compressed)")
        st.area_chart(compressed_df[['cpu', 'memory', 'network']], color=["#FF4B4B", "#4B4BFF", "#4BFF4B"])
    
    with tab2:
        st.subheader("Detected Anomalies")
        if alerts:
            for alert in alerts:
                st.warning(f"⚠️ {alert}")
        else:
            st.success("✅ No anomalies detected.")
            
    with tab3:
        col_raw, col_comp = st.columns(2)
        with col_raw:
            st.subheader("Raw Logs")
            st.dataframe(raw_df.head(50), use_container_width=True)
        with col_comp:
            st.subheader("Compressed Logs")
            st.dataframe(compressed_df, use_container_width=True)

else:
    st.info("👈 Click 'Run Security Scan' in the sidebar to start.")
    # Placeholder visual
    st.bar_chart({"CPU": [0], "Memory": [0], "Network": [0]})