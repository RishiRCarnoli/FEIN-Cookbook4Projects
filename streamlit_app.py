import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from io import StringIO
import os
import uuid
from datetime import datetime

# App configuration
st.set_page_config(
    page_title="DataWizard 🧙‍♂️",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for analytics
if 'analytics' not in st.session_state:
    st.session_state.analytics = {
        'files_processed': 0,
        'total_rows_processed': 0,
        'users': set(),
        'sessions': []
    }

# Generate unique user ID
if 'user_id' not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
    st.session_state.analytics['users'].add(st.session_state.user_id)
    st.session_state.analytics['sessions'].append({
        'user_id': st.session_state.user_id,
        'start_time': datetime.now(),
        'actions': []
    })

# Track user action
def track_action(action):
    st.session_state.analytics['sessions'][-1]['actions'].append({
        'time': datetime.now(),
        'action': action
    })

# Header with magic animation
st.title("DataWizard 🧙‍♂️")
st.markdown("### Your one-click solution for **data cleaning** and **Kaggle-style insights**")
st.write("Upload a CSV file and watch the magic happen!")

# File uploader with animation
with st.expander("✨ Upload your CSV file", expanded=True):
    uploaded_file = st.file_uploader("Drag & drop or click to browse", 
                                    type=["csv"],
                                    help="Supports files up to 200MB",
                                    key="file_uploader")
    
    if uploaded_file:
        track_action("File Uploaded")
        st.success(f"✅ Successfully uploaded {uploaded_file.name}")

# Main processing
if uploaded_file:
    # Read CSV with progress animation
    with st.spinner("🧠 Analyzing your data..."):
        time.sleep(1)  # Simulate processing time
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.analytics['files_processed'] += 1
            st.session_state.analytics['total_rows_processed'] += len(df)
            track_action("File Processed")
        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.stop()
    
    # Show original data preview
    st.subheader("🔍 Original Data Preview")
    st.dataframe(df.head(), height=210)
    
    # Data cleaning options in sidebar
    st.sidebar.header("🧹 Data Cleaning Options")
    clean_missing = st.sidebar.checkbox("Handle missing values", True)
    remove_duplicates = st.sidebar.checkbox("Remove duplicates", True)
    standardize_text = st.sidebar.checkbox("Standardize text columns", True)
    fix_data_types = st.sidebar.checkbox("Fix data types automatically", True)
    
    # Apply cleaning
    df_clean = df.copy()
    cleaning_log = []
    
    if clean_missing:
        # Smart imputation based on data type
        for col in df_clean.columns:
            if df_clean[col].isnull().sum() > 0:
                if df_clean[col].dtype == 'object':
                    df_clean[col].fillna('Unknown', inplace=True)
                    cleaning_log.append(f"Filled missing text in '{col}' with 'Unknown'")
                else:
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
                    cleaning_log.append(f"Filled missing numbers in '{col}' with median")
    
    if remove_duplicates:
        initial_count = len(df_clean)
        df_clean.drop_duplicates(inplace=True)
        duplicates_removed = initial_count - len(df_clean)
        if duplicates_removed > 0:
            cleaning_log.append(f"Removed {duplicates_removed} duplicate rows")
    
    if standardize_text:
        text_cols = df_clean.select_dtypes(include=['object']).columns
        for col in text_cols:
            # FIX: Handle mixed types
            try:
                df_clean[col] = df_clean[col].astype(str).str.strip().str.title()
            except:
                pass
        cleaning_log.append(f"Standardized text in {len(text_cols)} columns")
    
    if fix_data_types:
        # Auto-convert to datetime
        for col in df_clean.columns:
            if df_clean[col].dtype == 'object':
                try:
                    df_clean[col] = pd.to_datetime(df_clean[col])
                    cleaning_log.append(f"Converted '{col}' to datetime")
                except:
                    try:
                        # Try converting to numeric
                        df_clean[col] = pd.to_numeric(df_clean[col])
                        cleaning_log.append(f"Converted '{col}' to numeric")
                    except:
                        pass
    
    # Show cleaning results
    st.subheader("✨ Cleaning Report")
    if cleaning_log:
        st.success(f"**{len(cleaning_log)} transformations applied**")
        for log in cleaning_log:
            st.write(f"- {log}")
    else:
        st.info("No cleaning operations performed")
    
    # Show cleaned data preview
    st.subheader("🧼 Cleaned Data Preview")
    st.dataframe(df_clean.head(), height=210)
    
    # Kaggle-style metrics dashboard
    st.subheader("📊 Data Insights Dashboard")
    
    # Create tabs for different metrics
    tab1, tab2, tab3, tab4 = st.tabs([
        "Overview", 
        "Distributions", 
        "Correlations", 
        "Quality Report"
    ])
    
    with tab1:
        st.subheader("Data Overview")
        
        # Summary stats
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Rows", len(df_clean))
        col2.metric("Total Columns", len(df_clean.columns))
        col3.metric("Missing Values", df_clean.isnull().sum().sum())
        
        # Data types - FIXED
        st.write("### Data Types")
        
        # Convert dtypes to strings
        dtype_counts = df_clean.dtypes.astype(str).value_counts().reset_index()
        dtype_counts.columns = ['Data Type', 'Count']
        
        # Handle empty case
        if len(dtype_counts) > 0:
            fig = px.pie(dtype_counts, names='Data Type', values='Count', 
                         hole=0.4, color_discrete_sequence=px.colors.sequential.Blues_r)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data types detected")
    
    with tab2:
        st.subheader("Distributions")
        
        # Numerical distributions
        num_cols = df_clean.select_dtypes(include=np.number).columns
        if len(num_cols) > 0:
            num_col = st.selectbox("Select numerical column", num_cols)
            fig = px.histogram(df_clean, x=num_col, nbins=50, 
                              marginal="box", color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No numerical columns found")
        
        # Categorical distributions
        cat_cols = df_clean.select_dtypes(include=['object', 'category']).columns
        if len(cat_cols) > 0:
            cat_col = st.selectbox("Select categorical column", cat_cols)
            # FIX: Convert to string for safety
            value_counts = df_clean[cat_col].astype(str).value_counts().reset_index()
            value_counts.columns = ['Value', 'Count']
            fig = px.bar(value_counts, x='Value', y='Count', 
                         color='Count', color_continuous_scale='Blues')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No categorical columns found")
    
    with tab3:
        st.subheader("Correlations")
        
        if len(num_cols) > 1:
            # Correlation matrix
            corr_matrix = df_clean[num_cols].corr().round(2)
            fig = px.imshow(corr_matrix, 
                           text_auto=True, 
                           color_continuous_scale='Bluered',
                           aspect="auto")
            st.plotly_chart(fig, use_container_width=True)
            
            # Scatter plot
            col1, col2 = st.columns(2)
            x_axis = col1.selectbox("X-axis", num_cols)
            y_axis = col2.selectbox("Y-axis", num_cols, index=1)
            fig = px.scatter(df_clean, x=x_axis, y=y_axis, 
                            trendline="ols", 
                            marginal_x="histogram", 
                            marginal_y="histogram")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need at least 2 numerical columns for correlation analysis")
    
    with tab4:
        st.subheader("Data Quality Report")
        
        # Missing values analysis
        st.write("### Missing Values")
        missing_df = df_clean.isnull().sum().reset_index()
        missing_df.columns = ['Column', 'Missing Values']
        missing_df = missing_df[missing_df['Missing Values'] > 0]
        
        if len(missing_df) > 0:
            fig = px.bar(missing_df, x='Column', y='Missing Values', 
                         color='Missing Values', color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("🎉 No missing values found!")
        
        # Outlier detection
        st.write("### Potential Outliers")
        if len(num_cols) > 0:
            outlier_col = st.selectbox("Select column for outlier detection", num_cols)
            
            # Calculate outliers using IQR method
            q1 = df_clean[outlier_col].quantile(0.25)
            q3 = df_clean[outlier_col].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)
            
            outliers = df_clean[
                (df_clean[outlier_col] < lower_bound) | 
                (df_clean[outlier_col] > upper_bound)
            ]
            
            st.write(f"**{len(outliers)} potential outliers detected** (using IQR method)")
            st.dataframe(outliers.head(10))
        else:
            st.info("No numerical columns for outlier detection")
    
    # Download cleaned data
    st.subheader("📥 Export Results")
    csv = df_clean.to_csv(index=False).encode('utf-8')
    
    col1, col2 = st.columns(2)
    col1.download_button(
        label="Download Cleaned CSV",
        data=csv,
        file_name=f"cleaned_{uploaded_file.name}",
        mime='text/csv',
        help="Download your cleaned dataset"
    )
    
    # Show analytics to user (optional)
    st.sidebar.subheader("📈 Your Impact")
    st.sidebar.metric("Files Processed", st.session_state.analytics['files_processed'])
    st.sidebar.metric("Total Rows Cleaned", st.session_state.analytics['total_rows_processed'])
    st.sidebar.caption(f"Unique users: {len(st.session_state.analytics['users'])}")

# Empty state with animation
else:
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <lottie-player src="https://assets10.lottiefiles.com/packages/lf20_5tkzkblw.json" 
                       background="transparent" speed="1" 
                       style="width: 300px; height: 300px; margin: 0 auto;" 
                       loop autoplay>
        </lottie-player>
        <h3>Upload a CSV file to get started!</h3>
        <p>Your data will be processed securely and never stored</p>
    </div>
    """, unsafe_allow_html=True)

# Add Lottie animation component
st.markdown("""
<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>
""", unsafe_allow_html=True)

# Add analytics tracking to footer
st.sidebar.markdown("---")
st.sidebar.caption(f"Session ID: {st.session_state.user_id}")
