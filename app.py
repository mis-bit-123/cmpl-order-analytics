import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_loader import OrderDataLoader
from config import DASHBOARD_TITLE, CURRENCY, BRUSH_SHEET_NAME
import numpy as np
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="CMPL Order Analytics Pro",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# PROFESSIONAL GLOBAL CSS
# ==========================================
st.markdown("""
<style>
/* Main Header - Crystal Clear & Blur-Free */
.main-header { 
    font-size: 2.8rem; 
    font-weight: 800; 
    color: #ffffff;
    background: transparent;
    text-align: center;
    padding: 25px 20px;
    margin-bottom: 25px;
    position: relative;
    z-index: 1;
}

/* Container with gradient background - NO BLUR */
.main-header-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 5px;
    margin-bottom: 30px;
    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
    position: relative;
    overflow: hidden;
}

/* Inner container for clean edges */
.main-header-inner {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 30px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Alternative: Solid background approach (NO blur effects) */
.main-header-solid {
    font-size: 2.8rem; 
    font-weight: 800; 
    color: #ffffff;
    text-align: center;
    padding: 30px;
    margin-bottom: 25px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    border: none;
}

/* Simple and clean - NO blur, NO gradient text */
.main-header-clean {
    font-size: 2.8rem; 
    font-weight: 800; 
    color: #667eea;
    text-align: center;
    padding-bottom: 15px;
    margin-bottom: 20px;
    border-bottom: 4px solid #667eea;
    text-shadow: none;
    background: none;
    -webkit-text-fill-color: #667eea;
}

/* Dark mode optimized */
@media (prefers-color-scheme: dark) {
    .main-header-clean {
        color: #a8b9f0;
        border-bottom-color: #a8b9f0;
        -webkit-text-fill-color: #a8b9f0;
    }
}

/* Light mode optimized */
@media (prefers-color-scheme: light) {
    .main-header-clean {
        color: #4c63d2;
        border-bottom-color: #4c63d2;
        -webkit-text-fill-color: #4c63d2;
    }
}

/* RECOMMENDED: Glass effect without blur issues */
.main-header-glass {
    font-size: 2.8rem; 
    font-weight: 800; 
    color: #ffffff;
    text-align: center;
    padding: 30px;
    margin-bottom: 25px;
    background: rgba(102, 126, 234, 0.95);
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
    border: 1px solid rgba(255, 255, 255, 0.18);
    text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* With accent line */
.main-header-accent {
    font-size: 2.8rem; 
    font-weight: 800; 
    color: #f8fafc;
    text-align: center;
    padding: 25px 30px;
    margin-bottom: 25px;
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    border-radius: 16px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    position: relative;
}

.main-header-accent::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 50%;
    transform: translateX(-50%);
    width: 100px;
    height: 4px;
    background: linear-gradient(90deg, #667eea, #764ba2);
    border-radius: 2px;
}

    .subheader { 
        font-size: 1.5rem; 
        font-weight: 600; 
        color: #2c3e50;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .metric-card { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px; 
        border-radius: 15px; 
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }

    .filter-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-bottom: 20px;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4 !important;
        color: white !important;
    }

    /* Side Radio Buttons */
    .stRadio > div {
        background-color: #101a24;
        border-radius: 10px;
        padding: 0.5rem;
        margin-top: 0.5rem;
    }
    .stRadio label {
        font-weight: 500 !important;
        padding: 0.4rem 0.6rem !important;
        border-radius: 6px !important;
        margin: 0.2rem 0 !important;
        transition: all 0.2s;
    }
    .stRadio label:hover {
        background-color: #e9ecef;
        transform: translateX(3px);
    }
    .stRadio [aria-selected="true"] {
        background-color: #1f77b4 !important;
        color: black !important;
        font-weight: 600 !important;
    }
    
    /* Brush Dashboard Specific Styles */
    .brush-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 20px;
    }
    
    .urgency-overdue { background-color: #ffebee; color: #c62828; padding: 4px 8px; border-radius: 12px; font-weight: bold; }
    .urgency-week { background-color: #fff3e0; color: #ef6c00; padding: 4px 8px; border-radius: 12px; font-weight: bold; }
    .urgency-month { background-color: #fffde7; color: #f9a825; padding: 4px 8px; border-radius: 12px; font-weight: bold; }
    .urgency-future { background-color: #e8f5e9; color: #2e7d32; padding: 4px 8px; border-radius: 12px; font-weight: bold; }

</style>
""", unsafe_allow_html=True)


# ==========================================
# DATA INITIALIZATION
# ==========================================
@st.cache_resource
def get_loader():
    return OrderDataLoader()

loader = get_loader()

# ==========================================
# LOAD DATA FIRST (Before Sidebar)
# ==========================================
@st.cache_data(ttl=300)
def load_data():
    try:
        return loader.fetch_data()
    except Exception as e:
        return None

df = load_data()

# Calculate stats safely
if df is not None and not df.empty:
    record_count = len(df)
    stats = loader.get_stats(df)
else:
    record_count = 0
# ==========================================
# SIDEBAR HEADER (Now df is defined)
# ==========================================
st.sidebar.markdown(f"""
<div style="text-align: center; padding: 1.5rem 0.5rem; background: linear-gradient(135deg, #1f77b4 0%, #ff7f0e 100%); border-radius: 15px; margin-bottom: 1.5rem; color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    <div style="font-size: 3rem; margin-bottom: 0.5rem;">📊</div>
    <div style="font-size: 1.4rem; font-weight: 800; margin-bottom: 0.3rem; letter-spacing: 0.5px;">CMPL Analytics</div>
    <div style="font-size: 0.95rem; opacity: 0.95; margin-bottom: 0.8rem; font-weight: 500;">Order Management System</div>
    <div style="font-size: 0.8rem; background: rgba(255,255,255,0.25); padding: 0.4rem 1rem; border-radius: 20px; display: inline-block; font-weight: 600; backdrop-filter: blur(10px);">
        🟢 System Online • {record_count:,} records
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGATION (NO CATEGORY TITLES)
# ==========================================

report_categories = {
    "📊 Overview": ["🏠 Executive Dashboard", "📈 Performance Metrics"],
    "🗺️ Geographic": ["🗺️ State-wise Deep Dive", "🗺️ State vs Product Matrix", "🗺️ Regional Comparison", "🗺️ Map Analytics"],
    "💰 Financial": ["💰 Revenue Trends", "💰 Year-wise Analysis", "💰 Monthly Insights", "💰 Top Revenue Sources"],
    "🔧 Products": ["🔧 Product Performance", "🔧 Product Trends", "🔧 Best Sellers by State"],
    "🏢 Companies": ["🏢 Company Analysis", "🏢 Customer Segmentation"],
    "⚡ Operations": ["⚡ Lead Time Analysis"],
    "🧹 Brush System": ["🧹 Brush Follow-up Dashboard"],  # NEW SECTION
    "📥 Export": ["📋 Raw Data Explorer"]
}

# Flatten into single radio list
all_reports = []
for reports in report_categories.values():
    all_reports.extend(reports)

# RADIO BUTTON ONLY
report = st.sidebar.radio("📌 Select Report", all_reports)


# ==========================================
# LOAD DATA WITH ERROR HANDLING
# ==========================================
@st.cache_data(ttl=300)
def load_data():
    try:
        return loader.fetch_data()
    except Exception as e:
        st.error(f"Data load error: {e}")
        return None

df = load_data()

if df is None:
    st.error("❌ Failed to connect to Google Sheets!")
    st.info("🔧 Troubleshooting:\n1. Check credentials/service_account.json\n2. Verify Sheet ID in config.py\n3. Ensure sharing with service account")
    st.stop()

if df.empty:
    st.warning("⚠️ No data found in sheet")
    st.stop()

# Stats
stats = loader.get_stats(df)

# Filters
years = sorted(df['Year'].unique(), reverse=True)
months = ["All"] + list(df['Month_Name'].unique())


# ==========================================
# MAIN HEADER
# ==========================================
st.markdown(f"<h1 class='main-header'>{DASHBOARD_TITLE}</h1>", unsafe_allow_html=True)
st.caption(f"🔄 Live Data | 📊 {len(df):,} records | 🕒 Updated: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
st.markdown("---")

# ==========================================
# REPORT: BRUSH FOLLOW-UP DASHBOARD (NEW)
# ==========================================
if report == "🧹 Brush Follow-up Dashboard":
    st.markdown("""
    <div class="brush-header">
        <h2>🧹 Broomer / Sweeper / Brush Set - Follow-up System</h2>
        <p>Track brush set purchases and manage 3-month replacement follow-ups</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Process brush data
    brush_df = loader.identify_brush_products(df)
    
    if brush_df.empty:
        st.warning("No Broomer, Sweeper, or Brush products found in the current dataset.")
        st.stop()
    
    # Calculate follow-up dates
    brush_df = loader.calculate_followup_dates(brush_df)
    brush_stats = loader.get_brush_summary_stats(brush_df)
    
    # ==================== MINI DASHBOARD METRICS ====================
    st.markdown("### 📊 Quick Overview")
    
    metric_cols = st.columns(5)
    with metric_cols[0]:
        st.metric("🧹 Total Units", f"{brush_stats['total_units']:,}")
    with metric_cols[1]:
        st.metric("💰 Total Revenue", f"{CURRENCY}{brush_stats['total_revenue']:,.0f}")
    with metric_cols[2]:
        st.metric("🏢 Unique Companies", f"{brush_stats['unique_companies']}")
    with metric_cols[3]:
        st.metric("⚠️ Overdue Follow-ups", f"{brush_stats['overdue_count']}", 
                 delta="Action Needed" if brush_stats['overdue_count'] > 0 else None,
                 delta_color="inverse")
    with metric_cols[4]:
        st.metric("📅 Due This Month", f"{brush_stats['upcoming_count']}")
    
    st.markdown("---")
    
    # ==================== TABS FOR ORGANIZATION ====================
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Follow-up Reminders", "📈 Analytics", "🔍 Search & Filter", "💾 Data Management"])
    
    # ==================== TAB 1: FOLLOW-UP REMINDERS ====================
    with tab1:
        st.markdown("### 📋 Follow-up Reminder Table")
        st.info("Brush sets need replacement after 90 days. Below is the automatic follow-up schedule based on purchase dates.")
        
        # Create display table
        display_df = brush_df[[
            'Date', 'Company', 'Client_Name', 'Product', 'State', 
            'Follow_Up_Date', 'Days_Until_Followup', 'Urgency', 'Inquiry_No'
        ]].copy()
        
        # Rename columns for display
        display_df.columns = [
            'Purchase Date', 'Company Name', 'Client Name', 'Product', 'State',
            'Follow-up Date', 'Days Left', 'Status', 'Inquiry No'
        ]
        
        # Format dates
        display_df['Purchase Date'] = display_df['Purchase Date'].dt.strftime('%d-%m-%Y')
        display_df['Follow-up Date'] = display_df['Follow-up Date'].dt.strftime('%d-%m-%Y')
        
        # Sort by urgency (overdue first)
        urgency_order = {'🔴 Overdue': 0, '🟠 Due This Week': 1, '🟡 Due This Month': 2, '🟢 Future': 3}
        display_df['Sort_Priority'] = brush_df['Urgency'].map(urgency_order)
        display_df = display_df.sort_values('Sort_Priority').drop('Sort_Priority', axis=1)
        
        # Filter options
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.multiselect("Filter by Status:", 
                                          options=display_df['Status'].unique(),
                                          default=display_df['Status'].unique())
        with col2:
            search_company = st.text_input("Search Company:", placeholder="Type company name...")
        
        # Apply filters
        filtered_display = display_df[display_df['Status'].isin(status_filter)]
        if search_company:
            filtered_display = filtered_display[filtered_display['Company Name'].str.contains(search_company, case=False)]
        
        # Display styled table
        if not filtered_display.empty:
            # Color coding for status
            def color_status(val):
                if '🔴' in val:
                    return 'background-color: #ffebee; color: #c62828; font-weight: bold;'
                elif '🟠' in val:
                    return 'background-color: #fff3e0; color: #ef6c00; font-weight: bold;'
                elif '🟡' in val:
                    return 'background-color: #fffde7; color: #f9a825; font-weight: bold;'
                else:
                    return 'background-color: #e8f5e9; color: #2e7d32; font-weight: bold;'
            
            styled_df = filtered_display.style.applymap(color_status, subset=['Status'])
            st.dataframe(styled_df, use_container_width=True, height=500)
            
            # Summary for filtered view
            st.caption(f"Showing {len(filtered_display)} of {len(display_df)} total records")
        else:
            st.warning("No records match your filter criteria.")
    
    # ==================== TAB 2: ANALYTICS ====================
    with tab2:
        st.markdown("### 📈 Brush Product Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Urgency Distribution
            st.markdown("#### ⏰ Follow-up Status Distribution")
            urgency_data = brush_df['Urgency'].value_counts().reset_index()
            urgency_data.columns = ['Status', 'Count']
            
            fig_urgency = px.pie(urgency_data, values='Count', names='Status', 
                                color_discrete_map={
                                    '🔴 Overdue': '#c62828',
                                    '🟠 Due This Week': '#ef6c00',
                                    '🟡 Due This Month': '#f9a825',
                                    '🟢 Future': '#2e7d32'
                                },
                                hole=0.4)
            fig_urgency.update_traces(textinfo='percent+label', textposition='outside')
            st.plotly_chart(fig_urgency, use_container_width=True)
        
        with col2:
            # Top Products
            st.markdown("#### 🏆 Top Brush Products")
            top_products = brush_df['Product'].value_counts().head(10).reset_index()
            top_products.columns = ['Product', 'Units Sold']
            
            fig_products = px.bar(top_products, y='Product', x='Units Sold', 
                                 orientation='h', color='Units Sold',
                                 color_continuous_scale='Viridis')
            fig_products.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_products, use_container_width=True)
        
        # Timeline view
        st.markdown("#### 📅 Follow-up Timeline")
        timeline_df = brush_df.copy()
        timeline_df['Month'] = timeline_df['Follow_Up_Date'].dt.strftime('%Y-%m')
        monthly_followups = timeline_df.groupby(['Month', 'Urgency']).size().reset_index(name='Count')
        
        fig_timeline = px.bar(monthly_followups, x='Month', y='Count', color='Urgency',
                             color_discrete_map={
                                 '🔴 Overdue': '#c62828',
                                 '🟠 Due This Week': '#ef6c00',
                                 '🟡 Due This Month': '#f9a825',
                                 '🟢 Future': '#2e7d32'
                             },
                             barmode='stack')
        fig_timeline.update_layout(xaxis_title="Follow-up Month", yaxis_title="Number of Follow-ups")
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # State-wise analysis
        st.markdown("#### 🗺️ State-wise Brush Sales")
        state_brush = brush_df.groupby('State').agg({
            'Total_Amount': 'sum',
            'Company': 'nunique',
            'Inquiry_No': 'count'
        }).reset_index()
        state_brush.columns = ['State', 'Revenue', 'Companies', 'Units']
        
        fig_state = px.scatter(state_brush, x='Companies', y='Revenue', size='Units',
                              color='Revenue', hover_name='State',
                              color_continuous_scale='Plasma')
        fig_state.update_layout(xaxis_title="Number of Companies", yaxis_title=f"Revenue ({CURRENCY})")
        st.plotly_chart(fig_state, use_container_width=True)
    
    # ==================== TAB 3: SEARCH & FILTER ====================
    with tab3:
        st.markdown("### 🔍 Advanced Search")
        
        # Advanced filters
        col1, col2, col3 = st.columns(3)
        with col1:
            filter_state = st.multiselect("Select States:", options=sorted(brush_df['State'].unique()))
        with col2:
            filter_product = st.multiselect("Select Products:", options=sorted(brush_df['Product'].unique()))
        with col3:
            date_range = st.date_input("Purchase Date Range:", 
                                      [brush_df['Date'].min(), brush_df['Date'].max()])
        
        # Apply advanced filters
        search_result = brush_df.copy()
        if filter_state:
            search_result = search_result[search_result['State'].isin(filter_state)]
        if filter_product:
            search_result = search_result[search_result['Product'].isin(filter_product)]
        if len(date_range) == 2:
            search_result = search_result[(search_result['Date'] >= pd.Timestamp(date_range[0])) & 
                                         (search_result['Date'] <= pd.Timestamp(date_range[1]))]
        
        if not search_result.empty:
            st.success(f"Found {len(search_result)} records matching your criteria")
            st.dataframe(search_result[[
                'Date', 'Company', 'Client_Name', 'Product', 'State', 
                'Total_Amount', 'Follow_Up_Date', 'Urgency'
            ]].style.format({
                'Date': lambda x: x.strftime('%d-%m-%Y'),
                'Follow_Up_Date': lambda x: x.strftime('%d-%m-%Y'),
                'Total_Amount': lambda x: f"{CURRENCY}{x:,.0f}"
            }), use_container_width=True)
            
            # Export option for filtered data
            csv = search_result.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv,
                file_name=f"brush_followups_{datetime.now().strftime('%Y%m%d')}.csv",
                mime='text/csv'
            )
        else:
            st.warning("No records found matching your criteria.")
    
    # ==================== TAB 4: DATA MANAGEMENT ====================
    with tab4:
        st.markdown("### 💾 Store to Google Sheets")
        st.info(f"This will store all {len(brush_df)} brush product records to the '{BRUSH_SHEET_NAME}' sheet in your Google Spreadsheet.")
        
        # Show preview of what will be stored
        with st.expander("👁️ Preview Data to be Stored"):
            preview_df = brush_df[[
                'Date', 'Inquiry_No', 'Company', 'Client_Name', 'Product', 
                'State', 'Total_Amount', 'Follow_Up_Date', 'Urgency'
            ]].copy()
            preview_df['Date'] = preview_df['Date'].dt.strftime('%d-%m-%Y')
            preview_df['Follow_Up_Date'] = preview_df['Follow_Up_Date'].dt.strftime('%d-%m-%Y')
            st.dataframe(preview_df.head(10), use_container_width=True)
            st.caption(f"Showing first 10 of {len(brush_df)} records")
        
        # Store button
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("🚀 Store to Sheet", type="primary", use_container_width=True):
                with st.spinner("Storing data to Google Sheets..."):
                    success, message = loader.store_to_brush_sheet(brush_df)
                    if success:
                        st.success(message)
                        st.balloons()
                    else:
                        st.error(message)
        
        with col2:
            # Check existing data
            existing_data = loader.fetch_existing_brush_data()
            if existing_data is not None and not existing_data.empty:
                st.info(f"ℹ️ Sheet currently contains {len(existing_data)} records. Storing will update with latest data from Order Confirmation sheet.")
            else:
                st.info("ℹ️ No existing data found in the sheet. This will create a new entry.")
        
        # Show existing data if available
        if existing_data is not None and not existing_data.empty:
            st.markdown("### 📋 Currently Stored Data")
            st.dataframe(existing_data, use_container_width=True, height=300)

# ==========================================
# REPORT 1: EXECUTIVE DASHBOARD
# ==========================================
elif report == "🏠 Executive Dashboard":
    st.markdown("## 🎯 Executive Overview")
    
    # Top filters
    with st.container():
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            selected_year = st.selectbox("📅 Select Year:", ["All"] + [str(y) for y in years])
        with col_f2:
            selected_state = st.selectbox("🗺️ Select State:", ["All"] + sorted(df['State'].unique().tolist()))
        with col_f3:
            selected_product = st.selectbox("🔧 Select Product:", ["All"] + sorted(df['Product'].unique().tolist()))
    
    # Filter data
    filtered_df = df.copy()
    if selected_year != "All":
        filtered_df = filtered_df[filtered_df['Year'] == int(selected_year)]
    if selected_state != "All":
        filtered_df = filtered_df[filtered_df['State'] == selected_state]
    if selected_product != "All":
        filtered_df = filtered_df[filtered_df['Product'] == selected_product]
    
    # KPI Cards with gradient
    cols = st.columns(4)
    metrics = [
        ("💰 Total Revenue", f"{CURRENCY}{filtered_df['Total_Amount'].sum():,.0f}", f"{len(filtered_df)} Orders"),
        ("📦 Total Quantity", f"{filtered_df['Qty'].sum():,.0f}", "Units Sold"),
        ("📊 Avg Order Value", f"{CURRENCY}{filtered_df['Total_Amount'].mean():,.0f}", "Per Order"),
        ("🏆 Top Product", filtered_df.groupby('Product')['Total_Amount'].sum().idxmax() if not filtered_df.empty else "N/A", "Best Seller")
    ]
    
    for col, (label, value, delta) in zip(cols, metrics):
        with col:
            st.metric(label=label, value=value, delta=delta)
    
    st.markdown("---")
    
    # Charts Row 1
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 💵 Revenue by State (Top 8)")
        state_data = filtered_df.groupby('State')['Total_Amount'].sum().nlargest(8).reset_index()
        fig = px.bar(state_data, x='State', y='Total_Amount', color='Total_Amount',
                    color_continuous_scale='Viridis', text=state_data['Total_Amount'].apply(lambda x: f'{CURRENCY}{x/100000:.1f}L'))
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.markdown("### 🔥 Top 5 Products by Revenue")
        prod_data = filtered_df.groupby('Product')['Total_Amount'].sum().nlargest(5).reset_index()
        fig = px.pie(prod_data, values='Total_Amount', names='Product', hole=0.5,
                    color_discrete_sequence=px.colors.qualitative.Set3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    # Charts Row 2
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📈 Monthly Revenue Trend")
        monthly = filtered_df.groupby(filtered_df['Date'].dt.to_period('M'))['Total_Amount'].sum()
        monthly.index = monthly.index.to_timestamp()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly.index, y=monthly.values, fill='tozeroy', 
                                line=dict(color='#1f77b4', width=3), name='Revenue'))
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.markdown("### 🏢 Top 8 Companies")
        comp_data = filtered_df.groupby('Company')['Total_Amount'].sum().nlargest(8).reset_index()
        fig = px.bar(comp_data, y='Company', x='Total_Amount', orientation='h', color='Total_Amount',
                    color_continuous_scale='Blues')
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# REPORT 2: PERFORMANCE METRICS (PROFESSIONAL EDITION)
# ==========================================
elif report == "📈 Performance Metrics":
    
    # Premium Styling
    st.markdown("""
        <style>
        .metric-hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 30px;
            border-radius: 20px;
            color: white;
            text-align: center;
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
            margin-bottom: 30px;
        }
        .metric-card-pro {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border-left: 5px solid #667eea;
            transition: transform 0.3s ease;
        }
        .metric-card-pro:hover {
            transform: translateY(-5px);
        }
        .trend-up { color: #10b981; font-weight: 600; }
        .trend-down { color: #ef4444; font-weight: 600; }
        .insight-badge {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-block;
            margin: 5px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<div class="metric-hero">', unsafe_allow_html=True)
    st.markdown("## 📈 Performance Analytics Center")
    st.markdown("### Real-time Business Intelligence & KPI Monitoring")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Ensure datetime
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter
    df['Week'] = df['Date'].dt.isocalendar().week
    df['DayOfWeek'] = df['Date'].dt.day_name()
    df['YearMonth'] = df['Date'].dt.to_period('M')
    
    available_years = sorted(df['Year'].unique())
    
    # Control Panel
    st.markdown("### 🎛️ Analysis Controls")
    col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns([1, 1, 1, 1])
    
    with col_ctrl1:
        year_filter = st.selectbox("📅 Period:", ["All Years"] + [str(y) for y in available_years])
    
    with col_ctrl2:
        comparison_mode = st.selectbox("📊 Comparison:", ["None", "Previous Period", "Year-over-Year"])
    
    with col_ctrl3:
        metric_focus = st.selectbox("🎯 Focus:", ["Revenue", "Orders", "Quantity", "Efficiency"])
    
    with col_ctrl4:
        granularity = st.selectbox("⏱️ Granularity:", ["Daily", "Weekly", "Monthly", "Quarterly"])
    
    # Filter data
    if year_filter != "All Years":
        analysis_df = df[df['Year'] == int(year_filter)].copy()
        period_label = f"FY {year_filter}"
    else:
        analysis_df = df.copy()
        period_label = "All Time"
    
    # Core Calculations
    total_revenue = analysis_df['Total_Amount'].sum()
    total_orders = analysis_df['Inquiry_No'].nunique()
    total_quantity = analysis_df['Qty'].sum()
    total_transactions = len(analysis_df)
    unique_states = analysis_df['State'].nunique()
    unique_products = analysis_df['Product'].nunique()
    unique_customers = analysis_df['Company'].nunique()
    
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    avg_qty_per_order = total_quantity / total_orders if total_orders > 0 else 0
    revenue_per_state = total_revenue / unique_states if unique_states > 0 else 0
    revenue_per_product = total_revenue / unique_products if unique_products > 0 else 0
    
    # Time-based metrics
    date_range = (analysis_df['Date'].max() - analysis_df['Date'].min()).days + 1
    revenue_per_day = total_revenue / date_range if date_range > 0 else 0
    orders_per_day = total_orders / date_range if date_range > 0 else 0
    
    # ==================== HERO METRICS SECTION ====================
    st.markdown("### 🎯 Key Performance Indicators")
    
    # Determine metric colors based on focus
    if metric_focus == "Revenue":
        primary_color = "#667eea"
        secondary_color = "#764ba2"
    elif metric_focus == "Orders":
        primary_color = "#f093fb"
        secondary_color = "#f5576c"
    elif metric_focus == "Quantity":
        primary_color = "#4facfe"
        secondary_color = "#00f2fe"
    else:
        primary_color = "#43e97b"
        secondary_color = "#38f9d7"
    
    col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5, col_kpi6 = st.columns(6)
    
    with col_kpi1:
        st.markdown(f"""
            <div class="metric-card-pro" style="border-left-color: {primary_color};">
                <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">TOTAL REVENUE</p>
                <h2 style="color: {primary_color}; margin: 10px 0; font-size: 1.8rem;">{CURRENCY}{total_revenue/1e6:.2f}M</h2>
                <p style="font-size: 0.8rem; color: #6b7280;">{period_label}</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_kpi2:
        st.markdown(f"""
            <div class="metric-card-pro" style="border-left-color: {secondary_color};">
                <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">TOTAL ORDERS</p>
                <h2 style="color: {secondary_color}; margin: 10px 0; font-size: 1.8rem;">{total_orders:,}</h2>
                <p style="font-size: 0.8rem; color: #6b7280;">{total_transactions:,} transactions</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_kpi3:
        st.markdown(f"""
            <div class="metric-card-pro" style="border-left-color: #10b981;">
                <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">AVG ORDER VALUE</p>
                <h2 style="color: #10b981; margin: 10px 0; font-size: 1.8rem;">{CURRENCY}{avg_order_value:,.0f}</h2>
                <p style="font-size: 0.8rem; color: #6b7280;">Per transaction</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_kpi4:
        st.markdown(f"""
            <div class="metric-card-pro" style="border-left-color: #f59e0b;">
                <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">TOTAL QUANTITY</p>
                <h2 style="color: #f59e0b; margin: 10px 0; font-size: 1.8rem;">{total_quantity/1e3:.1f}K</h2>
                <p style="font-size: 0.8rem; color: #6b7280;">Units sold</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_kpi5:
        st.markdown(f"""
            <div class="metric-card-pro" style="border-left-color: #ef4444;">
                <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">ACTIVE MARKETS</p>
                <h2 style="color: #ef4444; margin: 10px 0; font-size: 1.8rem;">{unique_states}</h2>
                <p style="font-size: 0.8rem; color: #6b7280;">{unique_products} products</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col_kpi6:
        st.markdown(f"""
            <div class="metric-card-pro" style="border-left-color: #8b5cf6;">
                <p style="color: #6b7280; font-size: 0.85rem; margin: 0;">CUSTOMER BASE</p>
                <h2 style="color: #8b5cf6; margin: 10px 0; font-size: 1.8rem;">{unique_customers:,}</h2>
                <p style="font-size: 0.8rem; color: #6b7280;">Unique companies</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    
# ==========================================
# REPORT 3: STATE-WISE DEEP DIVE (ENHANCED & FIXED)
# ==========================================
elif report == "🗺️ State-wise Deep Dive":
    st.markdown("## 🗺️ Comprehensive State Analysis")
    st.markdown("---")
    
    # Ensure Date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])
    
    # Extract Year for filtering
    df['Year'] = df['Date'].dt.year
    
    # Validate available years
    available_years = sorted(df['Year'].unique())
    target_years = [2024, 2025, 2026]
    valid_years = [year for year in target_years if year in available_years]
    
    if not valid_years:
        st.error("No data available for years 2024-2026. Please check your data.")
        st.stop()
    
    # Year Selector - Horizontal layout
    col_year, col_metric = st.columns([1, 2])
    with col_year:
        selected_years = st.multiselect(
            "📅 Select Years:", 
            valid_years, 
            default=valid_years,
            help="Compare performance across multiple years"
        )
    
    if not selected_years:
        st.warning("⚠️ Please select at least one year")
        st.stop()
    
    # Filter data by selected years
    year_filtered_df = df[df['Year'].isin(selected_years)]
    
    with col_metric:
        comparison_metric = st.radio(
            "📊 Comparison Metric:",
            ["Revenue (Total_Amount)", "Quantity (Qty)", "Orders (Count)"],
            horizontal=True,
            help="Choose metric for state comparisons"
        )
    
    # State selector with search and multi-select
    states = sorted(year_filtered_df['State'].unique())
    
    col_state, col_view = st.columns([2, 1])
    with col_state:
        selected_states = st.multiselect(
            "🗺️ Select States to Compare:", 
            states, 
            default=states[:min(5, len(states))],
            help="Select multiple states for comparative analysis"
        )
    
    if not selected_states:
        st.warning("⚠️ Please select at least one state")
        st.stop()
    
    with col_view:
        view_type = st.selectbox(
            "👁️ View Mode:",
            ["Combined View", "Year-over-Year", "Side-by-Side"],
            help="Choose how to visualize multi-year data"
        )
    
    # Filter data
    filtered = year_filtered_df[year_filtered_df['State'].isin(selected_states)]
    
    # Create tabs for different analysis views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview & Rankings", 
        "📈 Trends & Growth", 
        "🎯 Product Breakdown", 
        "🔥 Year-wise Heatmap"
    ])
    
    # Metric mapping for dynamic calculations
    metric_map = {
        "Revenue (Total_Amount)": ("Total_Amount", "sum", CURRENCY),
        "Quantity (Qty)": ("Qty", "sum", ""),
        "Orders (Count)": ("Inquiry_No", "count", "")
    }
    
    metric_col, agg_func, currency_symbol = metric_map[comparison_metric]
    
    with tab1:
        st.markdown("### 📊 State Performance Overview")
        
        if view_type == "Combined View":
            # Aggregate across all selected years
            state_summary = filtered.groupby('State').agg({
                'Total_Amount': 'sum',
                'Qty': 'sum',
                'Inquiry_No': 'count',
                'Year': 'nunique'
            }).rename(columns={
                'Inquiry_No': 'Orders', 
                'Year': 'Active_Years'
            }).reset_index()
            
            # Calculate averages per year
            state_summary['Avg_Revenue_Per_Year'] = state_summary['Total_Amount'] / state_summary['Active_Years']
            
            col_chart, col_table = st.columns([3, 2])
            
            with col_chart:
                # Dual-axis bar chart
                fig = go.Figure()
                
                # Determine which column to use based on metric
                if metric_col == 'Inquiry_No':
                    y_values = state_summary['Orders']
                elif metric_col == 'Qty':
                    y_values = state_summary['Qty']
                else:
                    y_values = state_summary['Total_Amount']
                
                # Primary metric bars
                fig.add_trace(go.Bar(
                    name=comparison_metric.split('(')[0].strip(),
                    x=state_summary['State'],
                    y=y_values,
                    marker_color='royalblue',
                    opacity=0.8
                ))
                
                # Secondary metric line (Revenue always shown as reference)
                if metric_col != 'Total_Amount':
                    fig.add_trace(go.Scatter(
                        name='Revenue Trend',
                        x=state_summary['State'],
                        y=state_summary['Total_Amount'],
                        mode='lines+markers',
                        yaxis='y2',
                        line=dict(color='firebrick', width=3),
                        marker=dict(size=8)
                    ))
                
                fig.update_layout(
                    title=f'State Comparison: {comparison_metric}',
                    xaxis_title="State",
                    yaxis_title=comparison_metric,
                    yaxis2=dict(
                        title="Revenue",
                        overlaying='y',
                        side='right',
                        showgrid=False
                    ),
                    barmode='group',
                    height=500,
                    template='plotly_white',
                    legend=dict(orientation="h", yanchor="bottom", y=1.02)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with col_table:
                st.markdown("### 🏆 State Rankings")
                
                # Determine ranking column
                if metric_col == 'Inquiry_No':
                    rank_col = 'Orders'
                elif metric_col == 'Qty':
                    rank_col = 'Qty'
                else:
                    rank_col = 'Total_Amount'
                
                state_summary['Rank'] = state_summary[rank_col].rank(ascending=False)
                
                # Format display
                display_df = state_summary.sort_values(rank_col, ascending=False)
                
                def highlight_top3(row):
                    if row['Rank'] == 1:
                        return ['background-color: gold'] * len(row)
                    elif row['Rank'] == 2:
                        return ['background-color: silver'] * len(row)
                    elif row['Rank'] == 3:
                        return ['background-color: #CD7F32'] * len(row)  # Bronze
                    return [''] * len(row)
                
                st.dataframe(
                    display_df.style.format({
                        'Total_Amount': lambda x: f"{CURRENCY}{x:,.0f}",
                        'Qty': lambda x: f"{x:,.0f}",
                        'Orders': lambda x: f"{x:,.0f}",
                        'Avg_Revenue_Per_Year': lambda x: f"{CURRENCY}{x:,.0f}"
                    }).apply(highlight_top3, axis=1),
                    use_container_width=True,
                    height=400
                )
        
        elif view_type == "Year-over-Year":
            # FIXED: Proper aggregation for year-over-year comparison
            if metric_col == 'Inquiry_No':
                # For count, use size() and reset index properly
                yearly_state = filtered.groupby(['State', 'Year']).size().reset_index(name='Value')
            else:
                # For sum operations
                yearly_state = filtered.groupby(['State', 'Year'])[metric_col].sum().reset_index(name='Value')
            
            # Create the line chart
            fig = px.line(
                yearly_state, 
                x='Year', 
                y='Value', 
                color='State',
                markers=True,
                title=f'Year-over-Year {comparison_metric} Comparison',
                template='plotly_white',
                labels={'Value': comparison_metric.split('(')[0].strip()}
            )
            
            # Ensure x-axis shows only selected years as integers
            fig.update_layout(
                height=500, 
                xaxis=dict(
                    tickmode='array', 
                    tickvals=selected_years,
                    dtick=1
                )
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Growth rate calculation
            if len(selected_years) > 1:
                st.markdown("### 📈 Growth Analysis")
                growth_data = []
                
                for state in selected_states:
                    state_data = yearly_state[yearly_state['State'] == state].sort_values('Year')
                    if len(state_data) > 1:
                        first_val = state_data.iloc[0]['Value']
                        last_val = state_data.iloc[-1]['Value']
                        growth = ((last_val - first_val) / first_val * 100) if first_val != 0 else 0
                        growth_data.append({
                            'State': state,
                            'First_Year': int(state_data.iloc[0]['Year']),
                            'Last_Year': int(state_data.iloc[-1]['Year']),
                            'First_Value': first_val,
                            'Last_Value': last_val,
                            'Growth_Rate': f"{growth:+.1f}%",
                            'Trend': '📈' if growth > 0 else '📉' if growth < 0 else '➡️'
                        })
                
                if growth_data:
                    growth_df = pd.DataFrame(growth_data)
                    st.dataframe(
                        growth_df.style.format({
                            'First_Value': lambda x: f"{x:,.0f}",
                            'Last_Value': lambda x: f"{x:,.0f}"
                        }),
                        use_container_width=True
                    )
        
        else:  # Side-by-Side
            cols = st.columns(len(selected_years))
            for idx, year in enumerate(selected_years):
                with cols[idx]:
                    st.markdown(f"### {year}")
                    year_data = filtered[filtered['Year'] == year].groupby('State').agg({
                        'Total_Amount': 'sum',
                        'Qty': 'sum',
                        'Inquiry_No': 'count'
                    }).rename(columns={'Inquiry_No': 'Orders'})
                    
                    # Determine y-axis column
                    if metric_col == 'Inquiry_No':
                        y_col = 'Orders'
                    elif metric_col == 'Qty':
                        y_col = 'Qty'
                    else:
                        y_col = 'Total_Amount'
                    
                    fig = px.bar(
                        year_data.reset_index(), 
                        x='State', 
                        y=y_col,
                        color='State',
                        title=f'{year} Performance',
                        template='plotly_white',
                        labels={y_col: comparison_metric.split('(')[0].strip()}
                    )
                    fig.update_layout(showlegend=False, height=300)
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### 📈 Temporal Trends Analysis")
        
        # Determine metric for top states calculation
        if metric_col == 'Inquiry_No':
            calc_col = 'Inquiry_No'
            calc_agg = 'count'
        else:
            calc_col = metric_col
            calc_agg = 'sum'
        
        # Get top 3 states based on selected metric
        if calc_agg == 'count':
            top_states = filtered.groupby('State')[calc_col].count().nlargest(3).index.tolist()
        else:
            top_states = filtered.groupby('State')[calc_col].sum().nlargest(3).index.tolist()
        
        col_trend, col_seasonal = st.columns([2, 1])
        
        with col_trend:
            st.markdown("#### Monthly Trends (Top 3 States)")
            
            for state in top_states:
                state_df = filtered[filtered['State'] == state]
                
                # Aggregate monthly data
                if calc_agg == 'count':
                    monthly = state_df.groupby(state_df['Date'].dt.to_period('M')).size().reset_index(name='Value')
                else:
                    monthly = state_df.groupby(state_df['Date'].dt.to_period('M'))[calc_col].sum().reset_index(name='Value')
                
                monthly['Date'] = monthly['Date'].dt.to_timestamp()
                
                # Create filled area chart
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=monthly['Date'],
                    y=monthly['Value'],
                    fill='tozeroy',
                    name=state,
                    line=dict(width=2),
                    mode='lines'
                ))
                
                fig.update_layout(
                    title=f"{state} - Monthly {comparison_metric}",
                    height=250,
                    template='plotly_white',
                    showlegend=False,
                    margin=dict(l=20, r=20, t=40, b=20),
                    xaxis_title="Month",
                    yaxis_title=comparison_metric.split('(')[0].strip()
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col_seasonal:
            st.markdown("#### 🎯 Quick Insights")
            
            # Calculate metrics for insights
            total_revenue = filtered['Total_Amount'].sum()
            total_orders = filtered['Inquiry_No'].nunique()
            avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
            
            st.metric("Total Revenue (Selected)", f"{CURRENCY}{total_revenue:,.0f}")
            st.metric("Total Orders", f"{total_orders:,}")
            st.metric("Avg Order Value", f"{CURRENCY}{avg_order_value:,.0f}")
            
            # Best performing state
            best_state = filtered.groupby('State')['Total_Amount'].sum().idxmax()
            best_revenue = filtered.groupby('State')['Total_Amount'].sum().max()
            st.success(f"🏆 Top State: **{best_state}**  \nRevenue: {CURRENCY}{best_revenue:,.0f}")
    
    with tab3:
        st.markdown("### 🎯 Product Distribution Analysis")
        
        col_prod1, col_prod2 = st.columns([1, 2])
        
        with col_prod1:
            selected_state_detail = st.selectbox(
                "🔍 Select State for Deep Dive:", 
                selected_states,
                help="Choose one state to analyze product performance"
            )
            
            analysis_type = st.radio(
                "Chart Type:",
                ["Sunburst", "Treemap", "Bar Chart"],
                help="Choose visualization type for product hierarchy"
            )
        
        if selected_state_detail:
            state_products = filtered[filtered['State'] == selected_state_detail].groupby(['Product', 'Year']).agg({
                'Total_Amount': 'sum',
                'Qty': 'sum',
                'Inquiry_No': 'count'
            }).reset_index()
            
            with col_prod2:
                if analysis_type == "Sunburst":
                    # Sunburst chart with Year and Product hierarchy
                    fig = px.sunburst(
                        state_products,
                        path=['Year', 'Product'],
                        values='Total_Amount',
                        color='Total_Amount',
                        color_continuous_scale='RdYlBu',
                        title=f'Product Hierarchy in {selected_state_detail} (by Revenue)',
                        template='plotly_white'
                    )
                    fig.update_layout(height=600)
                    
                elif analysis_type == "Treemap":
                    fig = px.treemap(
                        state_products,
                        path=[px.Constant(selected_state_detail), 'Year', 'Product'],
                        values='Total_Amount',
                        color='Qty',
                        color_continuous_scale='Viridis',
                        title=f'Product Distribution in {selected_state_detail}',
                        template='plotly_white'
                    )
                    fig.update_traces(root_color="lightgrey")
                    fig.update_layout(height=600)
                    
                else:  # Bar Chart
                    top_products = state_products.groupby('Product')['Total_Amount'].sum().nlargest(15).reset_index()
                    fig = px.bar(
                        top_products,
                        x='Total_Amount',
                        y='Product',
                        orientation='h',
                        color='Total_Amount',
                        color_continuous_scale='Blues',
                        title=f'Top 15 Products in {selected_state_detail}',
                        template='plotly_white',
                        labels={'Total_Amount': f'Revenue ({CURRENCY})'}
                    )
                    fig.update_layout(height=600, yaxis=dict(autorange="reversed"))
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Product performance table
            st.markdown("#### 📋 Detailed Product Performance")
            product_summary = filtered[filtered['State'] == selected_state_detail].groupby('Product').agg({
                'Total_Amount': 'sum',
                'Qty': 'sum',
                'Inquiry_No': 'count',
                'Year': lambda x: ', '.join(map(str, sorted(x.unique())))
            }).rename(columns={
                'Inquiry_No': 'Orders',
                'Year': 'Active_Years'
            }).sort_values('Total_Amount', ascending=False).head(15)
            
            st.dataframe(
                product_summary.style.format({
                    'Total_Amount': lambda x: f"{CURRENCY}{x:,.0f}",
                    'Qty': lambda x: f"{x:,.0f}",
                    'Orders': lambda x: f"{x:,.0f}"
                }),
                use_container_width=True
            )
    
    with tab4:
        st.markdown("### 🔥 Year-wise Performance Heatmap")
        
        # Create pivot table for heatmap
        heatmap_data = filtered.groupby(['State', 'Year'])['Total_Amount'].sum().reset_index()
        heatmap_pivot = heatmap_data.pivot(index='State', columns='Year', values='Total_Amount').fillna(0)
        
        # Ensure all selected years are present
        for year in selected_years:
            if year not in heatmap_pivot.columns:
                heatmap_pivot[year] = 0
        
        # Sort columns to ensure chronological order
        heatmap_pivot = heatmap_pivot[sorted(selected_years)]
        
        fig = px.imshow(
            heatmap_pivot,
            labels=dict(x="Year", y="State", color="Revenue"),
            x=[str(year) for year in sorted(selected_years)],
            y=heatmap_pivot.index,
            color_continuous_scale="YlOrRd",
            aspect="auto",
            title="Revenue Heatmap: States vs Years",
            template='plotly_white'
        )
        
        # Add text annotations
        fig.update_traces(
            text=[[f"{CURRENCY}{val:,.0f}" for val in row] for row in heatmap_pivot.values],
            texttemplate="%{text}",
            textfont={"size": 10}
        )
        
        fig.update_layout(height=max(400, len(selected_states) * 40))
        st.plotly_chart(fig, use_container_width=True)
        
        # Year-over-Year growth heatmap
        if len(selected_years) > 1:
            st.markdown("### 📊 Year-over-Year Growth Rates (%)")
            
            # Calculate percentage change
            growth_pivot = heatmap_pivot.pct_change(axis=1) * 100
            growth_pivot = growth_pivot.iloc[:, 1:]  # Remove first year (NaN)
            
            if not growth_pivot.empty and not growth_pivot.isna().all().all():
                fig_growth = px.imshow(
                    growth_pivot,
                    labels=dict(x="Year", y="State", color="Growth %"),
                    color_continuous_scale="RdYlGn",
                    color_continuous_midpoint=0,
                    aspect="auto",
                    title="YoY Growth Rate Heatmap (%)",
                    template='plotly_white'
                )
                
                # Add percentage text
                fig_growth.update_traces(
                    text=[[f"{val:.1f}%" if not pd.isna(val) else "N/A" for val in row] for row in growth_pivot.values],
                    texttemplate="%{text}",
                    textfont={"size": 10}
                )
                
                fig_growth.update_layout(height=max(400, len(selected_states) * 40))
                st.plotly_chart(fig_growth, use_container_width=True)
            else:
                st.info("Insufficient data for growth calculation")

# ==========================================
# REPORT 4: STATE VS PRODUCT MATRIX
# ==========================================
elif report == "🗺️ State vs Product Matrix":
    st.markdown("## 🗺️ State-Product Correlation Matrix")
    
    # Create pivot table
    pivot = df.pivot_table(values='Total_Amount', index='Product', columns='State', aggfunc='sum', fill_value=0)
    
    # Filter options
    min_revenue = st.slider("💰 Minimum Revenue Threshold:", 0, int(df['Total_Amount'].max()), 100000)
    
    # Filter pivot
    pivot_filtered = pivot[pivot.sum(axis=1) > min_revenue]
    
    # Heatmap
    fig = px.imshow(pivot_filtered, 
                    labels=dict(x="State", y="Product", color="Revenue"),
                    aspect="auto",
                    color_continuous_scale='YlOrRd')
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("### 📊 Top State-Product Combinations")
    top_combos = df.groupby(['State', 'Product'])['Total_Amount'].sum().nlargest(20).reset_index()
    st.dataframe(top_combos, use_container_width=True)

# ==========================================
# REPORT 5: REGIONAL COMPARISON (ENHANCED)
# ==========================================
elif report == "🗺️ Regional Comparison":
    st.markdown("## 🗺️ Multi-State Comparison Tool")
    st.markdown("---")
    
    # Ensure Date column is datetime and extract Year
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    
    # Get available years
    available_years = sorted(df['Year'].unique())
    
    # Year Selection with "All Years" option
    col_year, col_metric = st.columns([1, 2])
    with col_year:
        year_option = st.selectbox(
            "📅 Select Year:",
            ["All Years"] + [str(y) for y in available_years],
            help="Compare states across specific year or all time"
        )
    
    # Filter data based on year selection
    if year_option == "All Years":
        filtered_df = df.copy()
        selected_year_label = "All Years"
    else:
        selected_year = int(year_option)
        filtered_df = df[df['Year'] == selected_year]
        selected_year_label = str(selected_year)
    
    with col_metric:
        comparison_metric = st.radio(
            "📊 Comparison Metric:",
            ["Revenue (Total_Amount)", "Quantity (Qty)", "Orders (Count)"],
            horizontal=True,
            key="regional_metric"
        )
    
    # State Selection with swap button
    st.markdown("### 🗺️ Select States to Compare")
    
    col_s1, col_swap, col_s2 = st.columns([2, 0.5, 2])
    
    states_list = sorted(filtered_df['State'].unique())
    
    with col_s1:
        state1 = st.selectbox(
            "State 1:", 
            states_list, 
            index=0,
            key="state1_select"
        )
    
    with col_swap:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄", help="Swap States"):
            # Store in session state to swap
            if 'state1_select' in st.session_state and 'state2_select' in st.session_state:
                st.session_state.state1_select, st.session_state.state2_select = \
                    st.session_state.state2_select, st.session_state.state1_select
                st.rerun()
    
    with col_s2:
        # Filter out state1 from options for state2 to prevent same state comparison
        state2_options = [s for s in states_list if s != state1]
        default_index = 0 if len(state2_options) > 0 else 0
        state2 = st.selectbox(
            "State 2:", 
            state2_options, 
            index=default_index,
            key="state2_select"
        )
    
    # Get data for both states
    s1_data = filtered_df[filtered_df['State'] == state1]
    s2_data = filtered_df[filtered_df['State'] == state2]
    
    # Metric calculations
    metric_map = {
        "Revenue (Total_Amount)": ("Total_Amount", "sum"),
        "Quantity (Qty)": ("Qty", "sum"),
        "Orders (Count)": ("Inquiry_No", "count")
    }
    metric_col, agg_func = metric_map[comparison_metric]
    
    # Calculate metrics
    def calculate_metrics(data):
        if data.empty:
            return {
                'revenue': 0,
                'orders': 0,
                'quantity': 0,
                'avg_order': 0,
                'top_product': "N/A",
                'top_product_revenue': 0,
                'unique_products': 0,
                'active_months': 0
            }
        
        metrics = {
            'revenue': data['Total_Amount'].sum(),
            'orders': data['Inquiry_No'].nunique(),
            'quantity': data['Qty'].sum(),
            'avg_order': data['Total_Amount'].mean(),
            'unique_products': data['Product'].nunique(),
            'active_months': data['Date'].dt.to_period('M').nunique()
        }
        
        # Top product
        top_prod = data.groupby('Product')['Total_Amount'].sum()
        metrics['top_product'] = top_prod.idxmax() if not top_prod.empty else "N/A"
        metrics['top_product_revenue'] = top_prod.max() if not top_prod.empty else 0
        
        return metrics
    
    s1_metrics = calculate_metrics(s1_data)
    s2_metrics = calculate_metrics(s2_data)
    
    # Display Metrics Cards with Delta Comparison
    st.markdown(f"### 📊 Performance Overview - {selected_year_label}")
    
    cols = st.columns(2)
    
    # Color scheme - Professional contrasting colors
    colors = {
        'state1': '#2563EB',  # Royal Blue
        'state2': '#DC2626',  # Red
        'state1_light': '#DBEAFE',
        'state2_light': '#FEE2E2'
    }
    
    for idx, (state, data, metrics) in enumerate([
        (state1, s1_data, s1_metrics), 
        (state2, s2_data, s2_metrics)
    ]):
        with cols[idx]:
            # Header with color indicator
            header_color = colors['state1'] if idx == 0 else colors['state2']
            st.markdown(
                f"<h3 style='color: {header_color}; border-bottom: 3px solid {header_color}; padding-bottom: 10px;'>"
                f"🏴 {state}</h3>", 
                unsafe_allow_html=True
            )
            
            # Main metrics in styled containers
            with st.container():
                col_m1, col_m2 = st.columns(2)
                
                with col_m1:
                    # Primary metric based on selection
                    if metric_col == 'Total_Amount':
                        st.metric(
                            "Total Revenue", 
                            f"{CURRENCY}{metrics['revenue']:,.0f}",
                            delta=None
                        )
                    elif metric_col == 'Qty':
                        st.metric(
                            "Total Quantity", 
                            f"{metrics['quantity']:,.0f}",
                            delta=None
                        )
                    else:
                        st.metric(
                            "Total Orders", 
                            f"{metrics['orders']:,}",
                            delta=None
                        )
                
                with col_m2:
                    st.metric(
                        "Avg Order Value", 
                        f"{CURRENCY}{metrics['avg_order']:,.0f}",
                        delta=None
                    )
                
                col_m3, col_m4 = st.columns(2)
                with col_m3:
                    st.metric("Unique Products", f"{metrics['unique_products']}")
                with col_m4:
                    st.metric("Active Months", f"{metrics['active_months']}")
                
                # Top product info
                st.info(f"**Top Product:** {metrics['top_product']}  \n"
                       f"Revenue: {CURRENCY}{metrics['top_product_revenue']:,.0f}")
    
    # Winner Banner
    st.markdown("---")
    winner_col, diff_col = st.columns([1, 2])
    
    with winner_col:
        if metric_col == 'Total_Amount':
            s1_score = s1_metrics['revenue']
            s2_score = s2_metrics['revenue']
        elif metric_col == 'Qty':
            s1_score = s1_metrics['quantity']
            s2_score = s2_metrics['quantity']
        else:
            s1_score = s1_metrics['orders']
            s2_score = s2_metrics['orders']
        
        if s1_score > s2_score:
            winner = state1
            winner_color = colors['state1']
            margin = ((s1_score - s2_score) / s2_score * 100) if s2_score > 0 else 0
        elif s2_score > s1_score:
            winner = state2
            winner_color = colors['state2']
            margin = ((s2_score - s1_score) / s1_score * 100) if s1_score > 0 else 0
        else:
            winner = "Tie"
            winner_color = "#6B7280"
            margin = 0
        
        if winner != "Tie":
            st.markdown(
                f"<div style='background-color: {winner_color}; color: white; padding: 15px; "
                f"border-radius: 10px; text-align: center;'>"
                f"<h2>🏆 Winner</h2>"
                f"<h1>{winner}</h1>"
                f"<p>Leading by {margin:.1f}%</p>"
                f"</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='background-color: {winner_color}; color: white; padding: 15px; "
                f"border-radius: 10px; text-align: center;'>"
                f"<h2>⚖️ Tie</h2>"
                f"<p>Both states are equal</p>"
                f"</div>",
                unsafe_allow_html=True
            )
    
    with diff_col:
        # Comparison metrics table
        comparison_metrics = pd.DataFrame({
            'Metric': ['Revenue', 'Orders', 'Quantity', 'Avg Order Value', 'Unique Products'],
            state1: [
                f"{CURRENCY}{s1_metrics['revenue']:,.0f}",
                f"{s1_metrics['orders']:,}",
                f"{s1_metrics['quantity']:,.0f}",
                f"{CURRENCY}{s1_metrics['avg_order']:,.0f}",
                f"{s1_metrics['unique_products']}"
            ],
            state2: [
                f"{CURRENCY}{s2_metrics['revenue']:,.0f}",
                f"{s2_metrics['orders']:,}",
                f"{s2_metrics['quantity']:,.0f}",
                f"{CURRENCY}{s2_metrics['avg_order']:,.0f}",
                f"{s2_metrics['unique_products']}"
            ],
            'Difference': [
                f"{CURRENCY}{s1_metrics['revenue'] - s2_metrics['revenue']:+,.0f}",
                f"{s1_metrics['orders'] - s2_metrics['orders']:+,.0f}",
                f"{s1_metrics['quantity'] - s2_metrics['quantity']:+,.0f}",
                f"{CURRENCY}{s1_metrics['avg_order'] - s2_metrics['avg_order']:+,.0f}",
                f"{s1_metrics['unique_products'] - s2_metrics['unique_products']:+d}"
            ]
        })
        
        st.markdown("#### 📋 Detailed Comparison")
        st.dataframe(comparison_metrics, use_container_width=True, hide_index=True)
    
    # Visualizations
    st.markdown("---")
    st.markdown("### 📈 Visual Analytics")
    
    tab1, tab2, tab3 = st.tabs(["Product Comparison", "Monthly Trends", "Category Breakdown"])
    
    with tab1:
        # Product-wise comparison with selected metric
        if metric_col == 'Inquiry_No':
            s1_prod = s1_data.groupby('Product').size().reset_index(name='Value')
            s2_prod = s2_data.groupby('Product').size().reset_index(name='Value')
        else:
            s1_prod = s1_data.groupby('Product')[metric_col].sum().reset_index(name='Value')
            s2_prod = s2_data.groupby('Product')[metric_col].sum().reset_index(name='Value')
        
        # Merge for comparison
        prod_comparison = pd.merge(
            s1_prod.rename(columns={'Value': state1}),
            s2_prod.rename(columns={'Value': state2}),
            on='Product',
            how='outer'
        ).fillna(0)
        
        # Sort by total
        prod_comparison['Total'] = prod_comparison[state1] + prod_comparison[state2]
        prod_comparison = prod_comparison.sort_values('Total', ascending=False).head(15)
        
        # Chart type selector
        chart_type = st.radio(
            "Chart Type:",
            ["Grouped Bar", "Stacked Bar", "Radar Chart"],
            horizontal=True,
            key="prod_chart_type"
        )
        
        if chart_type == "Grouped Bar":
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name=state1, 
                x=prod_comparison['Product'], 
                y=prod_comparison[state1],
                marker_color=colors['state1'],
                text=prod_comparison[state1].apply(lambda x: f'{x:,.0f}'),
                textposition='auto'
            ))
            fig.add_trace(go.Bar(
                name=state2, 
                x=prod_comparison['Product'], 
                y=prod_comparison[state2],
                marker_color=colors['state2'],
                text=prod_comparison[state2].apply(lambda x: f'{x:,.0f}'),
                textposition='auto'
            ))
            fig.update_layout(
                barmode='group',
                title=f'Top Products Comparison ({comparison_metric.split("(")[0].strip()})',
                xaxis_tickangle=-45,
                height=500,
                template='plotly_white',
                legend=dict(orientation="h", yanchor="bottom", y=1.02)
            )
            
        elif chart_type == "Stacked Bar":
            fig = go.Figure()
            fig.add_trace(go.Bar(
                name=state1, 
                x=prod_comparison['Product'], 
                y=prod_comparison[state1],
                marker_color=colors['state1']
            ))
            fig.add_trace(go.Bar(
                name=state2, 
                x=prod_comparison['Product'], 
                y=prod_comparison[state2],
                marker_color=colors['state2']
            ))
            fig.update_layout(
                barmode='stack',
                title=f'Product Distribution - Stacked View',
                xaxis_tickangle=-45,
                height=500,
                template='plotly_white'
            )
            
        else:  # Radar Chart
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=prod_comparison[state1].tolist() + [prod_comparison[state1].iloc[0]],
                theta=prod_comparison['Product'].tolist() + [prod_comparison['Product'].iloc[0]],
                fill='toself',
                name=state1,
                line_color=colors['state1']
            ))
            fig.add_trace(go.Scatterpolar(
                r=prod_comparison[state2].tolist() + [prod_comparison[state2].iloc[0]],
                theta=prod_comparison['Product'].tolist() + [prod_comparison['Product'].iloc[0]],
                fill='toself',
                name=state2,
                line_color=colors['state2']
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True)),
                showlegend=True,
                title="Product Performance Radar",
                height=600,
                template='plotly_white'
            )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Monthly trends comparison
        col_monthly, col_stats = st.columns([3, 1])
        
        with col_monthly:
            # Prepare monthly data
            s1_monthly = s1_data.groupby(s1_data['Date'].dt.to_period('M')).agg({
                'Total_Amount': 'sum',
                'Qty': 'sum',
                'Inquiry_No': 'count'
            }).reset_index()
            s1_monthly['Date'] = s1_monthly['Date'].dt.to_timestamp()
            
            s2_monthly = s2_data.groupby(s2_data['Date'].dt.to_period('M')).agg({
                'Total_Amount': 'sum',
                'Qty': 'sum',
                'Inquiry_No': 'count'
            }).reset_index()
            s2_monthly['Date'] = s2_monthly['Date'].dt.to_timestamp()
            
            # Determine y-axis column
            if metric_col == 'Inquiry_No':
                y_col = 'Inquiry_No'
                y_label = 'Orders'
            elif metric_col == 'Qty':
                y_col = 'Qty'
                y_label = 'Quantity'
            else:
                y_col = 'Total_Amount'
                y_label = 'Revenue'
            
            fig = go.Figure()
            
            # State 1 line
            fig.add_trace(go.Scatter(
                x=s1_monthly['Date'],
                y=s1_monthly[y_col],
                mode='lines+markers',
                name=state1,
                line=dict(color=colors['state1'], width=3),
                marker=dict(size=8)
            ))
            
            # State 2 line
            fig.add_trace(go.Scatter(
                x=s2_monthly['Date'],
                y=s2_monthly[y_col],
                mode='lines+markers',
                name=state2,
                line=dict(color=colors['state2'], width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title=f'Monthly {y_label} Trends',
                xaxis_title="Month",
                yaxis_title=y_label,
                height=450,
                template='plotly_white',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col_stats:
            st.markdown("#### 📊 Trend Stats")
            
            # Calculate growth rates
            if len(s1_monthly) > 1:
                s1_growth = ((s1_monthly[y_col].iloc[-1] - s1_monthly[y_col].iloc[0]) / 
                            s1_monthly[y_col].iloc[0] * 100)
                st.metric(f"{state1} Growth", f"{s1_growth:+.1f}%")
            
            if len(s2_monthly) > 1:
                s2_growth = ((s2_monthly[y_col].iloc[-1] - s2_monthly[y_col].iloc[0]) / 
                            s2_monthly[y_col].iloc[0] * 100)
                st.metric(f"{state2} Growth", f"{s2_growth:+.1f}%")
            
            # Peak months
            if not s1_monthly.empty:
                s1_peak = s1_monthly.loc[s1_monthly[y_col].idxmax()]
                st.info(f"**{state1} Peak:**  \n"
                       f"{s1_peak['Date'].strftime('%b %Y')}  \n"
                       f"{CURRENCY if y_col == 'Total_Amount' else ''}{s1_peak[y_col]:,.0f}")
            
            if not s2_monthly.empty:
                s2_peak = s2_monthly.loc[s2_monthly[y_col].idxmax()]
                st.info(f"**{state2} Peak:**  \n"
                       f"{s2_peak['Date'].strftime('%b %Y')}  \n"
                       f"{CURRENCY if y_col == 'Total_Amount' else ''}{s2_peak[y_col]:,.0f}")
    
    with tab3:
        # Product category analysis (if you have categories, otherwise use first letter grouping)
        st.markdown("#### 🏷️ Product Category Analysis")
        
        # Create pseudo-categories from product names (first word)
        s1_data_copy = s1_data.copy()
        s2_data_copy = s2_data.copy()
        
        s1_data_copy['Category'] = s1_data_copy['Product'].str.split().str[0]
        s2_data_copy['Category'] = s2_data_copy['Product'].str.split().str[0]
        
        if metric_col == 'Inquiry_No':
            s1_cat = s1_data_copy.groupby('Category').size().reset_index(name='Value')
            s2_cat = s2_data_copy.groupby('Category').size().reset_index(name='Value')
        else:
            s1_cat = s1_data_copy.groupby('Category')[metric_col].sum().reset_index(name='Value')
            s2_cat = s2_data_copy.groupby('Category')[metric_col].sum().reset_index(name='Value')
        
        cat_comparison = pd.merge(
            s1_cat.rename(columns={'Value': state1}),
            s2_cat.rename(columns={'Value': state2}),
            on='Category',
            how='outer'
        ).fillna(0)
        
        # Create sunburst chart
        fig = go.Figure()
        
        # Donut charts side by side
        from plotly.subplots import make_subplots
        
        fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                           subplot_titles=(state1, state2))
        
        fig.add_trace(go.Pie(
            labels=cat_comparison['Category'],
            values=cat_comparison[state1],
            name=state1,
            hole=0.4,
            marker_colors=px.colors.sequential.Blues_r
        ), row=1, col=1)
        
        fig.add_trace(go.Pie(
            labels=cat_comparison['Category'],
            values=cat_comparison[state2],
            name=state2,
            hole=0.4,
            marker_colors=px.colors.sequential.Reds_r
        ), row=1, col=2)
        
        fig.update_layout(
            title_text="Category Distribution Comparison",
            height=500,
            template='plotly_white',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Category comparison table
        cat_comparison['Difference'] = cat_comparison[state1] - cat_comparison[state2]
        cat_comparison = cat_comparison.sort_values('Difference', ascending=False)
        
        st.markdown("#### 📋 Category Breakdown")
        st.dataframe(
            cat_comparison.style.format({
                state1: lambda x: f"{x:,.0f}",
                state2: lambda x: f"{x:,.0f}",
                'Difference': lambda x: f"{x:+,.0f}"
            }).apply(lambda x: ['background-color: rgba(37, 99, 235, 0.1)' if x['Difference'] > 0 else 'background-color: rgba(220, 38, 38, 0.1)' if x['Difference'] < 0 else '' for _ in x], axis=1),
            use_container_width=True,
            hide_index=True
        )


        # 5.2  here new added the Map wise anlaysis for the states wise
        # -----------------------------------------------------------------------------------------------------------------
        #  =========================================================================================================
          # ==========================================
# ==========================================
# REPORT: MAP ANALYTICS (GEOGRAPHIC INTELLIGENCE)
# ==========================================
# HOW TO ADD THIS TO YOUR app.py:
# ─────────────────────────────────────────
# 1. Find this line in your app.py (around the Regional Comparison section):
#
#       elif report == "🗺️ Map Analytics":
#
# 2. DELETE everything from that line down to (but NOT including) the next
#    top-level elif, which starts:
#
#       elif report == "💰 Revenue Trends":
#
# 3. PASTE this entire file's contents in that gap.
#    The indentation must be at the TOP LEVEL (no extra spaces before elif).
# ─────────────────────────────────────────

elif report == "🗺️ Map Analytics":

    # ── Styling (same pattern as your other pages) ───────────────────────────
    st.markdown("""
        <style>
        .map-header {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            padding: 30px;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 15px 35px rgba(17,153,142,0.3);
        }
        .map-stats {
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
            border-left: 5px solid #11998e;
        }
        .state-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 12px;
            margin: 10px 0;
            box-shadow: 0 8px 20px rgba(102,126,234,0.3);
        }
        </style>
        <div class="map-header">
            <h1 style="margin:0; font-size:2.5rem;">🗺️ Geographic Intelligence</h1>
            <p style="margin:10px 0 0 0; font-size:1.1rem; opacity:0.9;">
                State-wise Order Distribution & Market Analytics
            </p>
        </div>
    """, unsafe_allow_html=True)

    # ── Ensure datetime / Year column ────────────────────────────────────────
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year

    available_years = sorted(df['Year'].unique())

    # ── Controls ─────────────────────────────────────────────────────────────
    st.markdown("### 🎛️ Map Controls")
    col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns([1, 1, 1, 1])

    with col_ctrl1:
        year_select = st.selectbox(
            "📅 Select Year:",
            ["All Years"] + [str(y) for y in available_years],
            help="Filter orders by year",
            key="map_year_select"
        )
    with col_ctrl2:
        metric_type = st.selectbox(
            "📊 Metric:",
            ["Revenue", "Order Count", "Quantity", "Average Order Value"],
            help="Choose metric to visualise",
            key="map_metric_type"
        )
    with col_ctrl3:
        map_style = st.selectbox(
            "🗺️ Map Style:",
            ["Choropleth (India Map)", "Bubble Chart", "State Rankings Table"],
            help="Visualisation style",
            key="map_style"
        )
    with col_ctrl4:
        top_n_states = st.slider(
            "🏆 Top States:", 5, 30, 15,
            help="Number of top states to highlight",
            key="map_top_n"
        )

    # ── Filter ────────────────────────────────────────────────────────────────
    if year_select != "All Years":
        map_df = df[df['Year'] == int(year_select)].copy()
        period_label = f"FY {year_select}"
    else:
        map_df = df.copy()
        period_label = "All Time"

    if map_df.empty:
        st.error("⚠️ No data available for selected filters")
        st.stop()

    # ── Aggregate per state ───────────────────────────────────────────────────
    metric_map = {
        "Revenue":             ("Total_Amount", "sum"),
        "Order Count":         ("Inquiry_No",   "nunique"),
        "Quantity":            ("Qty",          "sum"),
        "Average Order Value": ("Total_Amount", "mean"),
    }
    metric_col, agg_func = metric_map[metric_type]

    if agg_func == "nunique":
        state_metrics = map_df.groupby('State')[metric_col].nunique().reset_index()
    elif agg_func == "mean":
        state_metrics = map_df.groupby('State')[metric_col].mean().reset_index()
    else:
        state_metrics = map_df.groupby('State')[metric_col].sum().reset_index()
    state_metrics.columns = ['State', 'Value']

    # Extra detail columns
    state_details = map_df.groupby('State').agg(
        Revenue=('Total_Amount', 'sum'),
        AvgOrder=('Total_Amount', 'mean'),
        Transactions=('Total_Amount', 'count'),
        TotalQty=('Qty', 'sum'),
        Orders=('Inquiry_No', 'nunique'),
        Customers=('Company', 'nunique'),
        Products=('Product', 'nunique'),
    ).round(2).reset_index()

    state_metrics = state_metrics.merge(state_details, on='State', how='left')
    state_metrics = state_metrics.sort_values('Value', ascending=False).reset_index(drop=True)

    total_value = state_metrics['Value'].sum()
    state_metrics['Percentage'] = (state_metrics['Value'] / total_value * 100).round(2)
    state_metrics['CumulativePct'] = state_metrics['Percentage'].cumsum().round(2)

    # ── India GeoJSON (cached) ────────────────────────────────────────────────
    @st.cache_data(ttl=86400, show_spinner=False)
    def _load_india_geojson():
        """Load India state boundaries from GitHub mirror."""
        try:
            import requests as _req
            url = (
                "https://raw.githubusercontent.com/geohacker/india/"
                "master/state/india_telengana.geojson"
            )
            r = _req.get(url, timeout=12)
            r.raise_for_status()
            return r.json()
        except Exception:
            return None

    # ── MAP VISUALISATION ─────────────────────────────────────────────────────
    plot_data = state_metrics.head(top_n_states).copy()

    if map_style == "Choropleth (India Map)":
        st.markdown(f"### 🗺️ India Heat Map — {metric_type} ({period_label})")

        geojson = _load_india_geojson()

        if geojson is not None:
            # ── Find the property key that holds the state name ───────────────
            name_key = "NAME_1"   # default for geohacker dataset
            if geojson.get("features"):
                props = geojson["features"][0].get("properties", {})
                for k in ("NAME_1", "ST_NM", "name", "NAME"):
                    if k in props:
                        name_key = k
                        break

            fig_map = px.choropleth(
                plot_data,
                geojson=geojson,
                locations="State",
                featureidkey=f"properties.{name_key}",
                color="Value",
                hover_name="State",
                hover_data={
                    "State":      False,
                    "Value":      True,
                    "Percentage": True,
                    "Orders":     True,
                    "Customers":  True,
                },
                color_continuous_scale=[
                    [0.0, "#E8F5E9"],
                    [0.2, "#81C784"],
                    [0.4, "#4CAF50"],
                    [0.6, "#2E7D32"],
                    [1.0, "#1B5E20"],
                ],
                labels={"Value": metric_type, "Percentage": "Share (%)"},
                title=f"Top {top_n_states} States — {metric_type}",
            )
            fig_map.update_geos(fitbounds="locations", visible=False)
            fig_map.update_layout(
                height=600,
                margin=dict(l=0, r=0, t=40, b=0),
                coloraxis_colorbar=dict(title=metric_type),
                template="plotly_white",
            )
            st.plotly_chart(fig_map, use_container_width=True)

        else:
            # ── Fallback: treemap (works offline, no external deps) ───────────
            st.info("ℹ️ Map tiles unavailable (network issue). Showing treemap instead.")
            fig_tree = px.treemap(
                plot_data,
                path=[px.Constant("India"), "State"],
                values="Value",
                color="Value",
                color_continuous_scale="RdYlGn",
                title=f"State-wise {metric_type} Distribution ({period_label})",
            )
            fig_tree.update_traces(
                texttemplate="<b>%{label}</b><br>%{value:,.0f}",
            )
            fig_tree.update_layout(height=600)
            st.plotly_chart(fig_tree, use_container_width=True)

    elif map_style == "Bubble Chart":
        st.markdown(f"### 🫧 Bubble Chart — Market Concentration ({period_label})")

        fig_bubble = px.scatter(
            plot_data,
            x="Customers",
            y="Value",
            size="Orders",
            color="Revenue",
            hover_name="State",
            text="State",
            size_max=60,
            title=f"State Analysis: {metric_type} vs Customer Base",
            labels={
                "Customers": "Number of Customers",
                "Value":     f"{metric_type}",
                "Orders":    "Total Orders",
                "Revenue":   f"Total Revenue ({CURRENCY})",
            },
            color_continuous_scale="Plasma",
        )
        fig_bubble.update_traces(
            textposition="top center",
            textfont=dict(size=10, color="black"),
            marker=dict(line=dict(width=2, color="DarkSlateGrey")),
        )
        fig_bubble.update_layout(height=550, template="plotly_white")
        st.plotly_chart(fig_bubble, use_container_width=True)

    else:  # State Rankings Table
        st.markdown(f"### 📋 State Rankings ({period_label})")

        disp = plot_data.copy()
        disp.insert(0, "Rank", range(1, len(disp) + 1))
        disp["Revenue"]     = disp["Revenue"].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        disp["AvgOrder"]    = disp["AvgOrder"].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        disp["Percentage"]  = disp["Percentage"].apply(lambda x: f"{x:.2f}%")
        disp["CumulativePct"] = disp["CumulativePct"].apply(lambda x: f"{x:.2f}%")
        disp = disp[["Rank", "State", "Value", "Percentage", "CumulativePct",
                     "Revenue", "Orders", "Customers", "Products", "AvgOrder"]]

        def _highlight_top3(row):
            if row["Rank"] == 1:
                return ["background: linear-gradient(90deg,#FFD700,#FFA500)"] * len(row)
            elif row["Rank"] == 2:
                return ["background: linear-gradient(90deg,#C0C0C0,#E8E8E8)"] * len(row)
            elif row["Rank"] == 3:
                return ["background: linear-gradient(90deg,#CD7F32,#D4AF37)"] * len(row)
            return [""] * len(row)

        st.dataframe(
            disp.style.apply(_highlight_top3, axis=1),
            use_container_width=True,
            height=500,
        )

    # ── KPI Cards ─────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(f"### 📊 Geographic Intelligence ({period_label})")

    col_geo1, col_geo2, col_geo3 = st.columns(3)
    top_state = state_metrics.iloc[0]

    with col_geo1:
        val_prefix = CURRENCY if metric_type in ("Revenue", "Average Order Value") else ""
        st.markdown(f"""
            <div class="state-card">
                <h4 style="margin:0;">🏆 #1 State</h4>
                <h2 style="margin:10px 0; font-size:1.8rem;">{top_state['State']}</h2>
                <p style="font-size:1.3rem; font-weight:600;">{val_prefix}{top_state['Value']:,.0f}</p>
                <p>{top_state['Percentage']:.1f}% of total {metric_type.lower()}</p>
                <hr style="border-color:rgba(255,255,255,0.3); margin:10px 0;">
                <small>📦 {int(top_state['Orders'])} orders &nbsp;•&nbsp; 🏢 {int(top_state['Customers'])} customers</small>
            </div>
        """, unsafe_allow_html=True)

    with col_geo2:
        top5_share = state_metrics.head(5)['Percentage'].sum()
        st.markdown(f"""
            <div class="map-stats" style="border-left-color:#f093fb;">
                <h4 style="margin:0; color:#6b7280;">📍 Market Concentration</h4>
                <h2 style="margin:15px 0; font-size:2rem; color:#f093fb;">{top5_share:.1f}%</h2>
                <p style="color:#6b7280;">Top 5 states contribution</p>
                <hr style="margin:15px 0;">
                <p style="margin:0;"><b>Active Markets:</b> {len(state_metrics)} states</p>
                <p style="margin:5px 0 0 0;"><b>Total Customers:</b> {int(state_metrics['Customers'].sum())}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_geo3:
        avg_rev = state_metrics['Revenue'].mean()
        best_aov_state   = state_metrics.loc[state_metrics['AvgOrder'].idxmax(), 'State']
        most_cust_state  = state_metrics.loc[state_metrics['Customers'].idxmax(), 'State']
        st.markdown(f"""
            <div class="map-stats" style="border-left-color:#4facfe;">
                <h4 style="margin:0; color:#6b7280;">📈 Avg Performance</h4>
                <h2 style="margin:15px 0; font-size:2rem; color:#4facfe;">{CURRENCY}{avg_rev:,.0f}</h2>
                <p style="color:#6b7280;">Revenue per state (avg)</p>
                <hr style="margin:15px 0;">
                <p style="margin:0;"><b>Best AOV:</b> {best_aov_state}</p>
                <p style="margin:5px 0 0 0;"><b>Most Customers:</b> {most_cust_state}</p>
            </div>
        """, unsafe_allow_html=True)

    # ── Pareto Chart ──────────────────────────────────────────────────────────
    st.markdown("#### 📈 Pareto Analysis (80/20 Rule)")

    pareto_data = state_metrics.head(15)
    x_vals = list(range(len(pareto_data)))

    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Bar(
        x=x_vals,
        y=pareto_data['Value'],
        name=metric_type,
        marker_color='royalblue',
        text=pareto_data['Value'].apply(
            lambda v: f"{CURRENCY}{v/1e6:.1f}M" if v >= 1e6
            else (f"{CURRENCY}{v/1e3:.0f}K" if v >= 1e3 else f"{v:.0f}")
        ),
        textposition='auto',
    ))
    fig_pareto.add_trace(go.Scatter(
        x=x_vals,
        y=pareto_data['CumulativePct'],
        name='Cumulative %',
        yaxis='y2',
        line=dict(color='red', width=3),
        marker=dict(size=8, symbol='diamond'),
    ))
    fig_pareto.add_hline(
        y=80, line_dash="dash", line_color="green",
        annotation_text="80% Threshold", yref='y2',
    )
    fig_pareto.update_layout(
        title=f"Top 15 States — {metric_type} Contribution",
        xaxis=dict(
            tickmode='array',
            tickvals=x_vals,
            ticktext=[
                (s[:12] + "…") if len(s) > 12 else s
                for s in pareto_data['State']
            ],
            tickangle=-30,
        ),
        yaxis=dict(
            title=f"{metric_type} ({CURRENCY if metric_type in ('Revenue','Average Order Value') else ''})",
            side='left',
        ),
        yaxis2=dict(
            title='Cumulative %', side='right', overlaying='y',
            range=[0, 100], ticksuffix='%',
        ),
        height=450,
        template='plotly_white',
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    st.plotly_chart(fig_pareto, use_container_width=True)

    states_80 = state_metrics[state_metrics['CumulativePct'] <= 80]
    if not states_80.empty:
        st.success(
            f"🎯 **Pareto Insight:** Top **{len(states_80)} states** "
            f"({len(states_80)/len(state_metrics)*100:.1f}% of markets) "
            f"generate **80%** of total {metric_type.lower()}."
        )

    # ── State Deep Dive ───────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🔍 State Deep Dive")

    selected_state_map = st.selectbox(
        "Select State for Detailed Analysis:",
        options=state_metrics['State'].tolist(),
        index=0,
        key="map_deep_dive_state",
    )

    if selected_state_map:
        state_data_map = map_df[map_df['State'] == selected_state_map].copy()

        col_detail1, col_detail2 = st.columns([2, 1])

        with col_detail1:
            st.markdown(f"#### 📊 {selected_state_map} — Performance Metrics")

            monthly_state = (
                state_data_map
                .groupby(state_data_map['Date'].dt.to_period('M'))
                .agg(Revenue=('Total_Amount', 'sum'), Orders=('Inquiry_No', 'nunique'))
                .reset_index()
            )
            monthly_state['Date'] = monthly_state['Date'].dt.to_timestamp()

            fig_state_trend = go.Figure()
            fig_state_trend.add_trace(go.Scatter(
                x=monthly_state['Date'],
                y=monthly_state['Revenue'],
                mode='lines+markers',
                name='Revenue',
                line=dict(width=3, color='#11998e'),
                fill='tozeroy',
                fillcolor='rgba(17,153,142,0.2)',
            ))
            fig_state_trend.update_layout(
                title=f"Monthly Revenue Trend — {selected_state_map}",
                xaxis_title="Month",
                yaxis_title=f"Revenue ({CURRENCY})",
                height=350,
                template='plotly_white',
            )
            st.plotly_chart(fig_state_trend, use_container_width=True)

        with col_detail2:
            st.markdown("#### 🏆 Top Customers")
            top_cust_map = (
                state_data_map
                .groupby('Company')
                .agg(Revenue=('Total_Amount', 'sum'), Orders=('Inquiry_No', 'nunique'))
                .sort_values('Revenue', ascending=False)
                .head(5)
            )
            top_cust_map['Revenue'] = top_cust_map['Revenue'].apply(
                lambda x: f"{CURRENCY}{x:,.0f}"
            )
            st.dataframe(top_cust_map, use_container_width=True)

            st.markdown("#### 🏷️ Top Products")
            top_prod_map = (
                state_data_map
                .groupby('Product')['Total_Amount']
                .sum()
                .sort_values(ascending=False)
                .head(5)
            )
            st.bar_chart(top_prod_map)

    # ── Export ──────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📥 Export Geographic Data")

    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        st.download_button(
            "📊 Export State Metrics (CSV)",
            state_metrics.to_csv(index=False).encode('utf-8'),
            f"state_metrics_{period_label.replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col_exp2:
        st.download_button(
            "📍 Export All Orders with State (CSV)",
            map_df.to_csv(index=False).encode('utf-8'),
            f"orders_by_state_{period_label.replace(' ', '_')}.csv",
            mime="text/csv",
            use_container_width=True,
        )

# ── END OF MAP ANALYTICS BLOCK ────────────────────────────────────────────────

# ==========================================
# REPORT 6: REVENUE TRENDS (ENHANCED)
# ==========================================
elif report == "💰 Revenue Trends":
    st.markdown("## 💰 Advanced Revenue Trends & Quarterly Analysis")
    
    # Year selection
    selected_year = st.selectbox("📅 Select Year:", ["All"] + [str(y) for y in years])
    
    trend_df = df.copy()
    if selected_year != "All":
        trend_df = trend_df[trend_df['Year'] == int(selected_year)]
        available_years = [int(selected_year)]
    else:
        available_years = sorted(trend_df['Year'].unique())
    
    # ==========================================
    # MONTHLY TREND ANALYSIS (Enhanced)
    # ==========================================
    st.markdown("### 📈 Monthly Trend Analysis")
    
    monthly_data = trend_df.groupby([trend_df['Date'].dt.year.rename('Year'), 
                                     trend_df['Date'].dt.month.rename('Month')]).agg({
        'Total_Amount': 'sum',
        'Inquiry_No': 'count',
        'Qty': 'sum'
    }).reset_index()
    
    # Create proper date column
    monthly_data['Period'] = pd.to_datetime(monthly_data[['Year', 'Month']].assign(day=1))
    monthly_data = monthly_data.sort_values('Period')
    
    # Calculate MoM Growth
    monthly_data['Revenue_Growth'] = monthly_data['Total_Amount'].pct_change() * 100
    monthly_data['Orders_Growth'] = monthly_data['Inquiry_No'].pct_change() * 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue Trend with Growth Indicators
        fig_rev = go.Figure()
        
        fig_rev.add_trace(go.Scatter(
            x=monthly_data['Period'], 
            y=monthly_data['Total_Amount'],
            mode='lines+markers+text',
            name='Revenue',
            line=dict(color='#2E86AB', width=3),
            marker=dict(size=8),
            text=monthly_data['Total_Amount'].apply(lambda x: f'{CURRENCY}{x/100000:.1f}L'),
            textposition='top center',
            textfont=dict(size=9),
            fill='tozeroy',
            fillcolor='rgba(46, 134, 171, 0.2)'
        ))
        
        fig_rev.update_layout(
            title="Monthly Revenue Trend",
            xaxis_title="Month",
            yaxis_title=f"Revenue ({CURRENCY})",
            height=400,
            hovermode='x unified',
            showlegend=False
        )
        st.plotly_chart(fig_rev, use_container_width=True)
    
    with col2:
        # Order Count with Secondary Trend
        fig_ord = go.Figure()
        
        fig_ord.add_trace(go.Bar(
            x=monthly_data['Period'], 
            y=monthly_data['Inquiry_No'],
            name='Orders',
            marker_color='#A23B72',
            text=monthly_data['Inquiry_No'].astype(int),
            textposition='outside'
        ))
        
        # Add trend line
        fig_ord.add_trace(go.Scatter(
            x=monthly_data['Period'], 
            y=monthly_data['Inquiry_No'],
            mode='lines',
            name='Trend',
            line=dict(color='#F18F01', width=2, dash='dash')
        ))
        
        fig_ord.update_layout(
            title="Monthly Order Count",
            xaxis_title="Month",
            yaxis_title="Number of Orders",
            height=400,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig_ord, use_container_width=True)
    
    # Monthly Growth Metrics
    if len(monthly_data) > 1:
        st.markdown("#### 📊 Monthly Growth Metrics")
        latest_month = monthly_data.iloc[-1]
        prev_month = monthly_data.iloc[-2]
        
        m_cols = st.columns(4)
        with m_cols[0]:
            rev_growth = latest_month['Revenue_Growth']
            st.metric(
                "Revenue Growth (MoM)",
                f"{rev_growth:+.1f}%" if pd.notna(rev_growth) else "N/A",
                f"{CURRENCY}{latest_month['Total_Amount'] - prev_month['Total_Amount']:,.0f}" if pd.notna(rev_growth) else "",
                delta_color="normal" if pd.notna(rev_growth) and rev_growth > 0 else "inverse" if pd.notna(rev_growth) else "off"
            )
        with m_cols[1]:
            ord_growth = latest_month['Orders_Growth']
            st.metric(
                "Orders Growth (MoM)",
                f"{ord_growth:+.1f}%" if pd.notna(ord_growth) else "N/A",
                f"{int(latest_month['Inquiry_No'] - prev_month['Inquiry_No'])} orders" if pd.notna(ord_growth) else "",
                delta_color="normal" if pd.notna(ord_growth) and ord_growth > 0 else "inverse" if pd.notna(ord_growth) else "off"
            )
        with m_cols[2]:
            st.metric(
                "Avg Monthly Revenue",
                f"{CURRENCY}{monthly_data['Total_Amount'].mean():,.0f}",
                f"Peak: {CURRENCY}{monthly_data['Total_Amount'].max():,.0f}"
            )
        with m_cols[3]:
            best_month = monthly_data.loc[monthly_data['Total_Amount'].idxmax(), 'Period']
            st.metric(
                "Best Month",
                best_month.strftime('%b %Y'),
                f"{CURRENCY}{monthly_data['Total_Amount'].max():,.0f}"
            )
    
    # ==========================================
    # QUARTERLY ANALYSIS (Enhanced)
    # ==========================================
    st.markdown("---")
    st.markdown("### 📊 Quarterly Performance Deep Dive")
    
    # Create Quarter labels
    trend_df['Year_Quarter'] = trend_df['Date'].dt.to_period('Q')
    trend_df['Quarter'] = trend_df['Date'].dt.quarter
    trend_df['Year'] = trend_df['Date'].dt.year
    
    quarterly = trend_df.groupby(['Year', 'Quarter']).agg({
        'Total_Amount': 'sum',
        'Inquiry_No': 'count',
        'Qty': 'sum'
    }).reset_index()
    
    quarterly['Quarter_Label'] = 'Q' + quarterly['Quarter'].astype(str) + ' ' + quarterly['Year'].astype(str)
    quarterly['Avg_Order_Value'] = quarterly['Total_Amount'] / quarterly['Inquiry_No']
    
    # Sort properly
    quarterly = quarterly.sort_values(['Year', 'Quarter'])
    
    # Calculate QoQ Growth
    quarterly['QoQ_Revenue_Growth'] = quarterly['Total_Amount'].pct_change() * 100
    quarterly['QoQ_Orders_Growth'] = quarterly['Inquiry_No'].pct_change() * 100
    
    # Quarterly KPI Cards
    st.markdown("#### 🎯 Quarterly Key Metrics")
    
    # Create columns for each quarter found
    q_cols = st.columns(len(quarterly))
    for idx, (_, row) in enumerate(quarterly.iterrows()):
        with q_cols[idx]:
            st.markdown(f"**{row['Quarter_Label']}**")
            st.metric(
                "Revenue",
                f"{CURRENCY}{row['Total_Amount']:,.0f}",
                None
            )
            st.metric(
                "Orders",
                f"{int(row['Inquiry_No'])}",
                None
            )
            st.metric(
                "AOV",
                f"{CURRENCY}{row['Avg_Order_Value']:,.0f}",
                None
            )
    
    # Quarter-over-Quarter Analysis
    if len(quarterly) > 1:
        st.markdown("#### 📈 Quarter-over-Quarter Growth")
        
        qoq_cols = st.columns(min(len(quarterly)-1, 4))
        for i in range(1, len(quarterly)):
            if i-1 < len(qoq_cols):
                with qoq_cols[i-1]:
                    curr = quarterly.iloc[i]
                    prev = quarterly.iloc[i-1]
                    rev_growth = curr['QoQ_Revenue_Growth']
                    
                    st.metric(
                        label=f"{prev['Quarter_Label']} → {curr['Quarter_Label']}",
                        value=f"{rev_growth:+.1f}%" if pd.notna(rev_growth) else "N/A",
                        delta=f"{CURRENCY}{curr['Total_Amount'] - prev['Total_Amount']:,.0f}" if pd.notna(rev_growth) else "",
                        delta_color="normal" if pd.notna(rev_growth) and rev_growth > 0 else "inverse"
                    )
    
    # Quarterly Visualizations
    st.markdown("#### 📊 Quarterly Visualizations")
    
    col_q1, col_q2 = st.columns(2)
    
    with col_q1:
        # Quarterly Revenue Trend
        fig_qtr = go.Figure()
        
        colors_q = px.colors.qualitative.Prism[:len(quarterly)]
        
        fig_qtr.add_trace(go.Bar(
            x=quarterly['Quarter_Label'],
            y=quarterly['Total_Amount'],
            marker_color=colors_q,
            text=quarterly['Total_Amount'].apply(lambda x: f'{CURRENCY}{x/100000:.1f}L'),
            textposition='outside'
        ))
        
        # Add trend line
        fig_qtr.add_trace(go.Scatter(
            x=quarterly['Quarter_Label'],
            y=quarterly['Total_Amount'],
            mode='lines+markers',
            line=dict(color='red', width=2),
            marker=dict(size=10),
            name='Trend'
        ))
        
        fig_qtr.update_layout(
            title="Quarterly Revenue Trend",
            xaxis_title="Quarter",
            yaxis_title=f"Revenue ({CURRENCY})",
            height=400,
            showlegend=False,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig_qtr, use_container_width=True)
    
    with col_q2:
        # Quarterly Orders vs AOV
        fig_q_combo = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig_q_combo.add_trace(
            go.Bar(
                x=quarterly['Quarter_Label'],
                y=quarterly['Inquiry_No'],
                name="Orders",
                marker_color='lightblue',
                text=quarterly['Inquiry_No'].astype(int),
                textposition='outside'
            ),
            secondary_y=False
        )
        
        fig_q_combo.add_trace(
            go.Scatter(
                x=quarterly['Quarter_Label'],
                y=quarterly['Avg_Order_Value'],
                name="AOV",
                mode='lines+markers',
                line=dict(color='darkred', width=3),
                marker=dict(size=10)
            ),
            secondary_y=True
        )
        
        fig_q_combo.update_layout(
            title="Orders vs Average Order Value by Quarter",
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            xaxis_tickangle=-45
        )
        fig_q_combo.update_yaxes(title_text="Number of Orders", secondary_y=False)
        fig_q_combo.update_yaxes(title_text=f"Avg Order Value ({CURRENCY})", secondary_y=True)
        
        st.plotly_chart(fig_q_combo, use_container_width=True)
    
    # Quarterly Comparison Table
    st.markdown("#### 📋 Quarterly Performance Table")
    
    # Prepare display table
    display_qtr = quarterly[['Quarter_Label', 'Total_Amount', 'Inquiry_No', 'Avg_Order_Value', 'QoQ_Revenue_Growth']].copy()
    display_qtr.columns = ['Quarter', 'Revenue', 'Orders', 'AOV', 'QoQ Growth']
    
    # Format columns
    display_qtr['Revenue'] = display_qtr['Revenue'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
    display_qtr['Orders'] = display_qtr['Orders'].apply(lambda x: f"{int(x)}")
    display_qtr['AOV'] = display_qtr['AOV'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
    display_qtr['QoQ Growth'] = display_qtr['QoQ Growth'].apply(lambda x: f"{x:+.1f}%" if pd.notna(x) else "-")
    
    st.table(display_qtr.set_index('Quarter'))
    
    # Year-over-Year Quarterly Comparison (if multiple years selected)
    if len(available_years) > 1:
        st.markdown("#### 🔄 Year-over-Year Quarterly Comparison")
        
        # Pivot for comparison
        qtr_pivot = quarterly.pivot(index='Quarter', columns='Year', values='Total_Amount').fillna(0)
        
        fig_yoy = go.Figure()
        
        colors_yoy = px.colors.qualitative.Set2[:len(available_years)]
        for idx, year in enumerate(available_years):
            if year in qtr_pivot.columns:
                fig_yoy.add_trace(go.Bar(
                    name=str(year),
                    x=['Q1', 'Q2', 'Q3', 'Q4'],
                    y=qtr_pivot[year],
                    marker_color=colors_yoy[idx],
                    text=qtr_pivot[year].apply(lambda x: f'{CURRENCY}{x/100000:.1f}L' if x > 0 else ''),
                    textposition='outside'
                ))
        
        fig_yoy.update_layout(
            title="Quarterly Revenue Comparison Across Years",
            xaxis_title="Quarter",
            yaxis_title=f"Revenue ({CURRENCY})",
            barmode='group',
            height=450,
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        st.plotly_chart(fig_yoy, use_container_width=True)
        
        # YoY Growth by Quarter
        if len(available_years) == 2:
            y1, y2 = available_years
            if y1 in qtr_pivot.columns and y2 in qtr_pivot.columns:
                st.markdown(f"**{y1} vs {y2} Quarterly Growth:**")
                yoy_cols = st.columns(4)
                for q in [1, 2, 3, 4]:
                    if q in qtr_pivot.index:
                        val_prev = qtr_pivot.loc[q, y1]
                        val_curr = qtr_pivot.loc[q, y2]
                        if val_prev > 0:
                            growth = ((val_curr - val_prev) / val_prev * 100)
                            with yoy_cols[q-1]:
                                st.metric(
                                    f"Q{q} Growth",
                                    f"{growth:+.1f}%",
                                    f"{CURRENCY}{val_curr - val_prev:,.0f}",
                                    delta_color="normal" if growth > 0 else "inverse"
                                )
    
    # Quarterly Insights Summary
    st.markdown("#### 🎯 Quarterly Insights")
    
    best_qtr = quarterly.loc[quarterly['Total_Amount'].idxmax()]
    worst_qtr = quarterly.loc[quarterly['Total_Amount'].idxmin()]
    avg_qtr_revenue = quarterly['Total_Amount'].mean()
    
    insight_cols = st.columns(3)
    with insight_cols[0]:
        st.metric(
            "🏆 Best Quarter",
            best_qtr['Quarter_Label'],
            f"{CURRENCY}{best_qtr['Total_Amount']:,.0f}"
        )
    with insight_cols[1]:
        st.metric(
            "📉 Lowest Quarter",
            worst_qtr['Quarter_Label'],
            f"{CURRENCY}{worst_qtr['Total_Amount']:,.0f}"
        )
    with insight_cols[2]:
        st.metric(
            "📊 Quarterly Average",
            f"{CURRENCY}{avg_qtr_revenue:,.0f}",
            f"Total: {CURRENCY}{quarterly['Total_Amount'].sum():,.0f}"
        )
    
    # Cumulative Trend
    st.markdown("#### 📈 Cumulative Revenue Trend")
    quarterly['Cumulative_Revenue'] = quarterly['Total_Amount'].cumsum()
    
    fig_cum = go.Figure()
    fig_cum.add_trace(go.Scatter(
        x=quarterly['Quarter_Label'],
        y=quarterly['Cumulative_Revenue'],
        mode='lines+markers+text',
        fill='tozeroy',
        line=dict(color='green', width=3),
        marker=dict(size=10),
        text=quarterly['Cumulative_Revenue'].apply(lambda x: f'{CURRENCY}{x/100000:.1f}L'),
        textposition='top center'
    ))
    
    fig_cum.update_layout(
        height=400,
        xaxis_title="Quarter",
        yaxis_title=f"Cumulative Revenue ({CURRENCY})",
        showlegend=False,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_cum, use_container_width=True)

# ==========================================
# REPORT 7: YEAR-WISE ANALYSIS
# ==========================================
elif report == "💰 Year-wise Analysis":
    st.markdown("## 💰 Year-over-Year Growth Analysis")
    
    # Get available years
    available_years = sorted(df['Year'].unique())
    
    if len(available_years) < 1:
        st.warning("No year data available")
        st.stop()
    
    # Year selection dropdowns
    col1, col2 = st.columns(2)
    with col1:
        base_year = st.selectbox("📅 Select Base Year:", available_years, index=0)
    with col2:
        compare_years = [y for y in available_years if y != base_year]
        if compare_years:
            comparison_year = st.selectbox("📅 Compare With Year:", compare_years, index=len(compare_years)-1 if len(compare_years) > 0 else 0)
        else:
            comparison_year = None
            st.info("Only one year available in dataset")
    
    # Calculate yearly stats
    yearly_stats = df.groupby('Year').agg({
        'Total_Amount': ['sum', 'mean', 'count'],
        'Qty': 'sum',
        'Company': 'nunique'
    }).round(2)
    
    yearly_stats.columns = ['Total_Revenue', 'Avg_Order_Value', 'Total_Orders', 'Total_Qty', 'Unique_Customers']
    
    # Display stats for selected years
    if base_year in yearly_stats.index:
        base_data = yearly_stats.loc[base_year]
        
        st.markdown(f"### 📊 {base_year} Performance")
        cols = st.columns(5)
        with cols[0]:
            st.metric("💰 Revenue", f"{CURRENCY}{base_data['Total_Revenue']:,.0f}")
        with cols[1]:
            st.metric("📦 Orders", f"{int(base_data['Total_Orders'])}")
        with cols[2]:
            st.metric("📊 Avg Order", f"{CURRENCY}{base_data['Avg_Order_Value']:,.0f}")
        with cols[3]:
            st.metric("🏭 Quantity", f"{int(base_data['Total_Qty'])}")
        with cols[4]:
            st.metric("🏢 Customers", f"{int(base_data['Unique_Customers'])}")
    
    # Year-to-Year Comparison
    if comparison_year and comparison_year in yearly_stats.index:
        st.markdown("---")
        st.markdown(f"### 📈 {base_year} vs {comparison_year} - Growth Analysis")
        
        comp_data = yearly_stats.loc[comparison_year]
        
        # Calculate differences
        revenue_diff = base_data['Total_Revenue'] - comp_data['Total_Revenue']
        orders_diff = base_data['Total_Orders'] - comp_data['Total_Orders']
        qty_diff = base_data['Total_Qty'] - comp_data['Total_Qty']
        
        # Calculate growth percentages
        revenue_growth = ((base_data['Total_Revenue'] / comp_data['Total_Revenue']) - 1) * 100 if comp_data['Total_Revenue'] > 0 else 0
        orders_growth = ((base_data['Total_Orders'] / comp_data['Total_Orders']) - 1) * 100 if comp_data['Total_Orders'] > 0 else 0
        qty_growth = ((base_data['Total_Qty'] / comp_data['Total_Qty']) - 1) * 100 if comp_data['Total_Qty'] > 0 else 0
        avg_order_growth = ((base_data['Avg_Order_Value'] / comp_data['Avg_Order_Value']) - 1) * 100 if comp_data['Avg_Order_Value'] > 0 else 0
        
        # Comparison Table
        comparison_data = {
            'Metric': ['Total Revenue', 'Total Orders', 'Quantity Sold', 'Avg Order Value', 'Active Customers'],
            base_year: [
                f"{CURRENCY}{base_data['Total_Revenue']:,.0f}",
                f"{int(base_data['Total_Orders'])}",
                f"{int(base_data['Total_Qty'])}",
                f"{CURRENCY}{base_data['Avg_Order_Value']:,.0f}",
                f"{int(base_data['Unique_Customers'])}"
            ],
            comparison_year: [
                f"{CURRENCY}{comp_data['Total_Revenue']:,.0f}",
                f"{int(comp_data['Total_Orders'])}",
                f"{int(comp_data['Total_Qty'])}",
                f"{CURRENCY}{comp_data['Avg_Order_Value']:,.0f}",
                f"{int(comp_data['Unique_Customers'])}"
            ],
            'Difference': [
                f"{CURRENCY}{revenue_diff:,.0f}",
                f"{int(orders_diff)}",
                f"{int(qty_diff)}",
                f"{CURRENCY}{base_data['Avg_Order_Value'] - comp_data['Avg_Order_Value']:,.0f}",
                f"{int(base_data['Unique_Customers'] - comp_data['Unique_Customers'])}"
            ],
            'Growth %': [
                f"{revenue_growth:+.2f}%",
                f"{orders_growth:+.2f}%",
                f"{qty_growth:+.2f}%",
                f"{avg_order_growth:+.2f}%",
                f"{((base_data['Unique_Customers']/comp_data['Unique_Customers'])-1)*100:+.2f}%" if comp_data['Unique_Customers'] > 0 else "N/A"
            ]
        }
        
        comp_df = pd.DataFrame(comparison_data)
        st.table(comp_df.set_index('Metric'))
        
        # Growth indicators
        st.markdown("### 📊 Growth Indicators")
        cols = st.columns(4)
        
        with cols[0]:
            delta_color = "normal" if revenue_growth > 0 else "inverse"
            st.metric(label="💰 Revenue Growth", value=f"{revenue_growth:+.2f}%", delta=f"{CURRENCY}{revenue_diff:,.0f}", delta_color=delta_color)
        
        with cols[1]:
            delta_color = "normal" if orders_growth > 0 else "inverse"
            st.metric(label="📦 Orders Growth", value=f"{orders_growth:+.2f}%", delta=f"{int(orders_diff)} orders", delta_color=delta_color)
        
        with cols[2]:
            delta_color = "normal" if qty_growth > 0 else "inverse"
            st.metric(label="🏭 Quantity Growth", value=f"{qty_growth:+.2f}%", delta=f"{int(qty_diff)} units", delta_color=delta_color)
        
        with cols[3]:
            delta_color = "normal" if avg_order_growth > 0 else "inverse"
            st.metric(label="📊 AOV Growth", value=f"{avg_order_growth:+.2f}%", delta=f"{CURRENCY}{base_data['Avg_Order_Value'] - comp_data['Avg_Order_Value']:,.0f}", delta_color=delta_color)
        
        # Visual indicator
        if revenue_growth > 0:
            st.success(f"✅ Growth of {revenue_growth:.2f}% from {comparison_year} to {base_year}")
        else:
            st.error(f"⚠️ Decline of {abs(revenue_growth):.2f}% from {comparison_year} to {base_year}")
    
    elif len(available_years) == 1:
        # Only one year available - show detailed breakdown
        st.info(f"📊 Only {available_years[0]} data available. Showing detailed breakdown...")
        
        # Monthly breakdown for single year
        year_df = df[df['Year'] == available_years[0]]
        monthly = year_df.groupby(year_df['Date'].dt.month).agg({
            'Total_Amount': 'sum',
            'Inquiry_No': 'count',
            'Qty': 'sum'
        }).round(2)
        monthly.columns = ['Revenue', 'Orders', 'Quantity']
        monthly.index = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][:len(monthly)]
        
        st.markdown(f"### 📅 {available_years[0]} Monthly Breakdown")
        st.table(monthly.style.format({
            'Revenue': lambda x: f"{CURRENCY}{x:,.0f}",
            'Orders': lambda x: f"{int(x)}",
            'Quantity': lambda x: f"{int(x)}"
        }))
    
    # All Years Line Chart
    if len(available_years) >= 2:
        st.markdown("---")
        st.markdown("### 📈 All Years Growth Trend")
        
        # Calculate growth for all years
        yearly_growth = yearly_stats.copy()
        yearly_growth['Revenue_Growth_Pct'] = yearly_growth['Total_Revenue'].pct_change() * 100
        yearly_growth['Orders_Growth_Pct'] = yearly_growth['Total_Orders'].pct_change() * 100
        
        # Create two charts side by side
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Revenue Trend (All Years)")
            fig1 = go.Figure()
            
            fig1.add_trace(go.Scatter(
                x=yearly_growth.index,
                y=yearly_growth['Total_Revenue'],
                mode='lines+markers+text',
                name='Revenue',
                text=yearly_growth['Total_Revenue'].apply(lambda x: f'{CURRENCY}{x/100000:.0f}L'),
                textposition='top center',
                line=dict(color='#1f77b4', width=3),
                marker=dict(size=10)
            ))
            
            fig1.update_layout(
                height=400,
                xaxis_title="Year",
                yaxis_title=f"Revenue ({CURRENCY})",
                showlegend=False,
                xaxis=dict(tickmode='linear', tick0=min(available_years), dtick=1)
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown("#### 📊 Year-over-Year Growth %")
            fig2 = go.Figure()
            
            # Filter out first year (no growth data)
            growth_data = yearly_growth[yearly_growth['Revenue_Growth_Pct'].notna()]
            
            colors = ['green' if x > 0 else 'red' for x in growth_data['Revenue_Growth_Pct']]
            
            fig2.add_trace(go.Bar(
                x=growth_data.index,
                y=growth_data['Revenue_Growth_Pct'],
                marker_color=colors,
                text=growth_data['Revenue_Growth_Pct'].apply(lambda x: f'{x:+.1f}%'),
                textposition='outside'
            ))
            
            fig2.add_hline(y=0, line_dash="dash", line_color="gray")
            
            fig2.update_layout(
                height=400,
                xaxis_title="Year",
                yaxis_title="Growth %",
                showlegend=False,
                xaxis=dict(tickmode='linear', tick0=min(available_years), dtick=1)
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Summary statistics for all years
        st.markdown("#### 📋 Year-over-Year Summary")
        summary_df = pd.DataFrame({
            'Year': yearly_growth.index,
            'Revenue': yearly_growth['Total_Revenue'].apply(lambda x: f"{CURRENCY}{x:,.0f}"),
            'Growth vs Previous': yearly_growth['Revenue_Growth_Pct'].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "Base Year"),
            'Orders': yearly_growth['Total_Orders'].astype(int),
            'Order Growth': yearly_growth['Orders_Growth_Pct'].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "-")
        })
        st.table(summary_df.set_index('Year'))

# ==========================================
# REPORT 8: MONTHLY INSIGHTS (FIXED)
# ==========================================
elif report == "💰 Monthly Insights":
    st.markdown("## 💰 Monthly Deep Dive & Seasonal Analysis")
    
    # Select multiple years for comparison
    selected_years = st.multiselect(
        "📅 Select Years to Compare:", 
        sorted(years), 
        default=sorted(years)[-2:] if len(years) >= 2 else years,
        help="Select multiple years to compare month-wise trends"
    )
    
    # State filter
    state_options = ["All States"] + sorted(df['State'].unique().tolist())
    selected_state_monthly = st.selectbox("🗺️ Filter by State:", state_options)
    
    if not selected_years:
        st.warning("Please select at least one year")
        st.stop()
    
    # Filter data
    filtered_df = df[df['Year'].isin(selected_years)]
    if selected_state_monthly != "All States":
        filtered_df = filtered_df[filtered_df['State'] == selected_state_monthly]
    
    # Prepare month-wise data
    month_order = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    monthly_data = filtered_df.groupby(['Year', 'Month_Name']).agg({
        'Total_Amount': 'sum',
        'Inquiry_No': 'count',
        'Qty': 'sum'
    }).reset_index()
    
    # ==========================================
    # MONTH-WISE TREND CHARTS
    # ==========================================
    st.markdown(f"### 📈 Month-wise Trend Comparison - {selected_state_monthly}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 💰 Revenue by Month")
        
        fig_revenue = go.Figure()
        colors = px.colors.qualitative.Set2[:len(selected_years)]
        
        for idx, year in enumerate(selected_years):
            year_data = monthly_data[monthly_data['Year'] == year]
            if not year_data.empty:
                # Sort by month order
                year_data['Month_Num'] = year_data['Month_Name'].apply(lambda x: month_order.index(x) if x in month_order else 0)
                year_data = year_data.sort_values('Month_Num')
                
                fig_revenue.add_trace(go.Scatter(
                    x=year_data['Month_Name'],
                    y=year_data['Total_Amount'],
                    mode='lines+markers+text',
                    name=str(year),
                    line=dict(color=colors[idx], width=3),
                    marker=dict(size=8),
                    text=year_data['Total_Amount'].apply(lambda x: f'{CURRENCY}{x/100000:.1f}L'),
                    textposition='top center',
                    textfont=dict(size=9)
                ))
        
        fig_revenue.update_layout(
            height=450,
            xaxis_title="Month",
            yaxis_title=f"Revenue ({CURRENCY})",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(categoryorder='array', categoryarray=month_order),
            hovermode='x unified',
            margin=dict(l=50, r=50, t=80, b=50)
        )
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Order Count by Month")
        
        fig_orders = go.Figure()
        
        for idx, year in enumerate(selected_years):
            year_data = monthly_data[monthly_data['Year'] == year]
            if not year_data.empty:
                year_data['Month_Num'] = year_data['Month_Name'].apply(lambda x: month_order.index(x) if x in month_order else 0)
                year_data = year_data.sort_values('Month_Num')
                
                fig_orders.add_trace(go.Bar(
                    x=year_data['Month_Name'],
                    y=year_data['Inquiry_No'],
                    name=str(year),
                    marker_color=colors[idx],
                    text=year_data['Inquiry_No'].astype(int),
                    textposition='outside'
                ))
        
        fig_orders.update_layout(
            height=450,
            xaxis_title="Month",
            yaxis_title="Number of Orders",
            barmode='group',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(categoryorder='array', categoryarray=month_order),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        st.plotly_chart(fig_orders, use_container_width=True)
    
    # ==========================================
    # COMPARISON TABLE
    # ==========================================
    st.markdown("---")
    st.markdown("### 📋 Month-wise Comparison Table")
    
    # Create pivot table
    pivot_revenue = monthly_data.pivot(index='Month_Name', columns='Year', values='Total_Amount').fillna(0)
    pivot_orders = monthly_data.pivot(index='Month_Name', columns='Year', values='Inquiry_No').fillna(0)
    
    # Reindex to ensure correct month order
    pivot_revenue = pivot_revenue.reindex([m for m in month_order if m in pivot_revenue.index])
    pivot_orders = pivot_orders.reindex([m for m in month_order if m in pivot_orders.index])
    
    # Display tabs for Revenue and Orders
    tab1, tab2 = st.tabs(["💰 Revenue", "📦 Orders"])
    
    with tab1:
        # Format for display
        display_rev = pivot_revenue.copy()
        for year in selected_years:
            if year in display_rev.columns:
                display_rev[year] = display_rev[year].apply(lambda x: f"{CURRENCY}{x:,.0f}" if x > 0 else "-")
        
        # Add YoY Growth column if 2+ years selected
        if len(selected_years) == 2:
            y1, y2 = sorted(selected_years)
            if y1 in pivot_revenue.columns and y2 in pivot_revenue.columns:
                growth = ((pivot_revenue[y2] - pivot_revenue[y1]) / pivot_revenue[y1] * 100).round(1)
                display_rev['Growth %'] = growth.apply(lambda x: f"{x:+.1f}%" if pd.notna(x) and x != 0 else "-")
        
        st.table(display_rev)
        
        # Total row
        totals = pivot_revenue.sum()
        st.markdown("**Total:**")
        cols = st.columns(len(selected_years) + (1 if len(selected_years) == 2 else 0))
        for idx, year in enumerate(selected_years):
            with cols[idx]:
                st.metric(f"{year}", f"{CURRENCY}{totals[year]:,.0f}")

    # ==========================================
    # YEAR-WISE SUMMARY SECTION
    # ==========================================
    st.markdown("---")
    st.markdown("### 🗓️ Year-wise Performance Summary")
    
    # Calculate year-wise totals
    yearly_summary = filtered_df.groupby('Year').agg({
        'Total_Amount': 'sum',
        'Inquiry_No': 'count',
        'Qty': 'sum'
    }).reset_index()
    
    # Calculate additional metrics
    yearly_summary['Avg_Order_Value'] = yearly_summary['Total_Amount'] / yearly_summary['Inquiry_No']
    yearly_summary = yearly_summary.sort_values('Year')
    
    # Year-wise KPI Cards
    st.markdown("#### 📊 Key Metrics by Year")
    year_cols = st.columns(len(selected_years))
    
    for idx, row in yearly_summary.iterrows():
        with year_cols[idx]:
            st.markdown(f"**{int(row['Year'])}**")
            st.metric(
                label="Total Revenue",
                value=f"{CURRENCY}{row['Total_Amount']:,.0f}",
                delta=None
            )
            st.metric(
                label="Total Orders",
                value=f"{int(row['Inquiry_No'])}",
                delta=None
            )
            st.metric(
                label="Avg Order Value",
                value=f"{CURRENCY}{row['Avg_Order_Value']:,.0f}",
                delta=None
            )
    
    # Year-over-Year Growth Calculation
    if len(yearly_summary) > 1:
        st.markdown("#### 📈 Year-over-Year Growth")
        
        yoy_data = yearly_summary.copy()
        yoy_data['Revenue_Growth'] = yoy_data['Total_Amount'].pct_change() * 100
        yoy_data['Orders_Growth'] = yoy_data['Inquiry_No'].pct_change() * 100
        yoy_data['AOV_Growth'] = yoy_data['Avg_Order_Value'].pct_change() * 100
        
        # Display YoY metrics
        yoy_cols = st.columns(3)
        
        # Get the latest comparison (last year vs previous)
        latest_yoy = yoy_data.iloc[-1]
        prev_year = yoy_data.iloc[-2]['Year']
        curr_year = latest_yoy['Year']
        
        with yoy_cols[0]:
            rev_growth = latest_yoy['Revenue_Growth']
            st.metric(
                label=f"Revenue Growth ({int(prev_year)} → {int(curr_year)})",
                value=f"{rev_growth:+.1f}%",
                delta=f"{CURRENCY}{latest_yoy['Total_Amount'] - yoy_data.iloc[-2]['Total_Amount']:,.0f}",
                delta_color="normal" if rev_growth > 0 else "inverse"
            )
        
        with yoy_cols[1]:
            ord_growth = latest_yoy['Orders_Growth']
            st.metric(
                label=f"Orders Growth ({int(prev_year)} → {int(curr_year)})",
                value=f"{ord_growth:+.1f}%",
                delta=f"{int(latest_yoy['Inquiry_No'] - yoy_data.iloc[-2]['Inquiry_No'])} orders",
                delta_color="normal" if ord_growth > 0 else "inverse"
            )
        
        with yoy_cols[2]:
            aov_growth = latest_yoy['AOV_Growth']
            st.metric(
                label=f"AOV Growth ({int(prev_year)} → {int(curr_year)})",
                value=f"{aov_growth:+.1f}%",
                delta=f"{CURRENCY}{latest_yoy['Avg_Order_Value'] - yoy_data.iloc[-2]['Avg_Order_Value']:,.0f}",
                delta_color="normal" if aov_growth > 0 else "inverse"
            )
    
    # ==========================================
    # YEAR-WISE COMPARISON TABLE
    # ==========================================
    st.markdown("#### 📋 Year-wise Detailed Comparison")
    
    # Prepare display table
    display_yearly = yearly_summary.copy()
    display_yearly.columns = ['Year', 'Total Revenue', 'Total Orders', 'Total Qty', 'Avg Order Value']
    
    # Format for display
    for col in ['Total Revenue', 'Avg Order Value']:
        display_yearly[col] = display_yearly[col].apply(lambda x: f"{CURRENCY}{x:,.0f}")
    display_yearly['Total Orders'] = display_yearly['Total Orders'].apply(lambda x: f"{int(x)}")
    display_yearly['Total Qty'] = display_yearly['Total Qty'].apply(lambda x: f"{int(x)}")
    
    # Add YoY Growth columns if multiple years
    if len(yearly_summary) > 1:
        for i in range(1, len(yearly_summary)):
            prev_rev = yearly_summary.iloc[i-1]['Total_Amount']
            curr_rev = yearly_summary.iloc[i]['Total_Amount']
            growth = ((curr_rev - prev_rev) / prev_rev * 100)
            display_yearly.loc[i, 'YoY Growth'] = f"{growth:+.1f}%"
    
    st.table(display_yearly.set_index('Year').transpose())
    
    # ==========================================
    # YEAR-WISE VISUAL TRENDS
    # ==========================================
    st.markdown("#### 📊 Year-wise Trend Visualization")
    
    col_y1, col_y2 = st.columns(2)
    
    with col_y1:
        # Year-wise Revenue Bar Chart
        fig_year_rev = go.Figure()
        
        colors_years = px.colors.qualitative.Bold[:len(yearly_summary)]
        
        fig_year_rev.add_trace(go.Bar(
            x=yearly_summary['Year'].astype(str),
            y=yearly_summary['Total_Amount'],
            marker_color=colors_years,
            text=yearly_summary['Total_Amount'].apply(lambda x: f'{CURRENCY}{x/100000:.1f}L'),
            textposition='outside'
        ))
        
        # Add trend line if 2+ years
        if len(yearly_summary) > 1:
            fig_year_rev.add_trace(go.Scatter(
                x=yearly_summary['Year'].astype(str),
                y=yearly_summary['Total_Amount'],
                mode='lines+markers',
                line=dict(color='red', width=2, dash='dash'),
                marker=dict(size=10),
                name='Trend'
            ))
        
        fig_year_rev.update_layout(
            title="Annual Revenue Trend",
            xaxis_title="Year",
            yaxis_title=f"Revenue ({CURRENCY})",
            height=400,
            showlegend=False,
            margin=dict(l=50, r=50, t=50, b=50)
        )
        st.plotly_chart(fig_year_rev, use_container_width=True)
    
    with col_y2:
        # Year-wise Orders & AOV Combo Chart
        fig_year_combo = go.Figure()
        
        # Bar chart for Orders
        fig_year_combo.add_trace(go.Bar(
            x=yearly_summary['Year'].astype(str),
            y=yearly_summary['Inquiry_No'],
            name='Orders',
            marker_color='lightblue',
            yaxis='y',
            text=yearly_summary['Inquiry_No'].astype(int),
            textposition='outside'
        ))
        
        # Line chart for AOV
        fig_year_combo.add_trace(go.Scatter(
            x=yearly_summary['Year'].astype(str),
            y=yearly_summary['Avg_Order_Value'],
            name='Avg Order Value',
            mode='lines+markers',
            line=dict(color='darkred', width=3),
            marker=dict(size=10),
            yaxis='y2'
        ))
        
        fig_year_combo.update_layout(
            title="Orders vs Avg Order Value",
            xaxis_title="Year",
            yaxis=dict(
                title="Number of Orders",
                side="left"
            ),
            yaxis2=dict(
                title=f"Avg Order Value ({CURRENCY})",
                side="right",
                overlaying="y",
                showgrid=False
            ),
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=50, r=50, t=80, b=50)
        )
        st.plotly_chart(fig_year_combo, use_container_width=True)

    # ==========================================
    # SEASONAL INSIGHTS
    # ==========================================
    st.markdown("---")
    st.markdown("### 🎯 Seasonal Insights")
    
    if len(selected_years) > 0:
        # Find peak months across all selected years
        all_months = monthly_data.groupby('Month_Name')['Total_Amount'].sum().sort_values(ascending=False)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🏆 Peak Month", all_months.index[0], f"{CURRENCY}{all_months.iloc[0]:,.0f}")
        with col2:
            st.metric("📉 Lowest Month", all_months.index[-1], f"{CURRENCY}{all_months.iloc[-1]:,.0f}")
        with col3:
            avg_monthly = all_months.mean()
            st.metric("📊 Avg Monthly", f"{CURRENCY}{avg_monthly:,.0f}")
        
        # Top 3 months
        st.markdown("**Top 3 Performing Months:**")
        for i, (month, revenue) in enumerate(all_months.head(3).items(), 1):
            pct = (revenue / all_months.sum()) * 100
            st.write(f"{i}. **{month}**: {CURRENCY}{revenue:,.0f} ({pct:.1f}% of total)")

# ==========================================
# REPORT 9: TOP REVENUE SOURCES (ENHANCED WITH YEAR FILTER)
# ==========================================
elif report == "💰 Top Revenue Sources":
    st.markdown("## 💰 Revenue Contribution & Distribution Analysis")
    
    # Ensure Date column is datetime and extract Year
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    
    # Get available years for dropdown
    available_years = sorted(df['Year'].unique())
    
    # Year selection dropdown
    col_year, col_view = st.columns([1, 2])
    
    with col_year:
        year_option = st.selectbox(
            "📅 Select Year:",
            ["All Years"] + [str(y) for y in available_years],
            help="Filter data by specific year or view all time"
        )
    
    with col_view:
        view_mode = st.selectbox(
            "👁️ View Mode:",
            ["Summary View", "Detailed Analysis", "Trend View"],
            help="Choose display mode"
        )
    
    # Filter data based on year selection
    if year_option != "All Years":
        selected_year = int(year_option)
        analysis_df = df[df['Year'] == selected_year].copy()
        period_label = f" ({selected_year})"
    else:
        analysis_df = df.copy()
        period_label = ""
    
    # Calculate contributions
    total_revenue = analysis_df['Total_Amount'].sum()
    
    # State contribution
    state_revenue = analysis_df.groupby('State').agg({
        'Total_Amount': ['sum', 'count', 'mean'],
        'Qty': 'sum'
    }).round(2)
    state_revenue.columns = ['Revenue', 'Orders', 'Avg_Order', 'Quantity']
    state_revenue = state_revenue.sort_values('Revenue', ascending=False)
    state_revenue['Revenue_Pct'] = (state_revenue['Revenue'] / total_revenue * 100).round(2)
    state_revenue['Cumulative_Pct'] = state_revenue['Revenue_Pct'].cumsum().round(2)
    
    # Product contribution
    product_revenue = analysis_df.groupby('Product').agg({
        'Total_Amount': ['sum', 'count'],
        'Qty': 'sum',
        'State': 'nunique'
    }).round(2)
    product_revenue.columns = ['Revenue', 'Orders', 'Quantity', 'States_Presence']
    product_revenue = product_revenue.sort_values('Revenue', ascending=False)
    product_revenue['Revenue_Pct'] = (product_revenue['Revenue'] / total_revenue * 100).round(2)
    product_revenue['Cumulative_Pct'] = product_revenue['Revenue_Pct'].cumsum().round(2)
    
    # Customer contribution (NEW FEATURE)
    customer_revenue = analysis_df.groupby('Company').agg({
        'Total_Amount': ['sum', 'count', 'mean'],
        'Qty': 'sum',
        'State': 'nunique',
        'Product': 'nunique'
    }).round(2)
    customer_revenue.columns = ['Revenue', 'Orders', 'Avg_Order', 'Quantity', 'States', 'Products']
    customer_revenue = customer_revenue.sort_values('Revenue', ascending=False)
    customer_revenue['Revenue_Pct'] = (customer_revenue['Revenue'] / total_revenue * 100).round(2)
    customer_revenue['Cumulative_Pct'] = customer_revenue['Revenue_Pct'].cumsum().round(2)
    
    # TOP SUMMARY CARDS
    st.markdown(f"### 📊 Market Overview{period_label}")
    cols = st.columns(4)
    with cols[0]:
        st.metric("🗺️ Total States", len(state_revenue))
    with cols[1]:
        st.metric("🔧 Total Products", len(product_revenue))
    with cols[2]:
        top_state = state_revenue.index[0]
        st.metric("🏆 Top State", top_state, f"{state_revenue.iloc[0]['Revenue_Pct']:.1f}%")
    with cols[3]:
        top_product = product_revenue.index[0]
        st.metric("⭐ Top Product", top_product[:20] + "..." if len(top_product) > 20 else top_product, 
                 f"{product_revenue.iloc[0]['Revenue_Pct']:.1f}%")
    
    st.markdown("---")
    
    # View mode content
    if view_mode == "Summary View":
        # Your original visualization code
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🗺️ Top 10 States")
            fig_states = px.bar(
                state_revenue.head(10).reset_index(),
                x='Revenue',
                y='State',
                orientation='h',
                color='Revenue_Pct',
                color_continuous_scale='Viridis',
                text=state_revenue.head(10)['Revenue'].apply(lambda x: f'{CURRENCY}{x/1000:.0f}K')
            )
            fig_states.update_traces(textposition='outside')
            fig_states.update_layout(yaxis=dict(autorange="reversed"), height=400)
            st.plotly_chart(fig_states, use_container_width=True)
        
        with col2:
            st.markdown("#### 🔧 Top 10 Products")
            fig_products = px.bar(
                product_revenue.head(10).reset_index(),
                x='Revenue',
                y='Product',
                orientation='h',
                color='Revenue_Pct',
                color_continuous_scale='Plasma',
                text=product_revenue.head(10)['Revenue'].apply(lambda x: f'{CURRENCY}{x/1000:.0f}K')
            )
            fig_products.update_traces(textposition='outside')
            fig_products.update_layout(yaxis=dict(autorange="reversed"), height=400)
            st.plotly_chart(fig_products, use_container_width=True)
    
    elif view_mode == "Detailed Analysis":
        # Detailed tables with formatting
        col_det1, col_det2 = st.columns(2)
        
        with col_det1:
            st.markdown(f"#### 📋 State Details{period_label}")
            display_state = state_revenue.head(15).copy()
            display_state['Revenue'] = display_state['Revenue'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
            display_state['Avg_Order'] = display_state['Avg_Order'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
            display_state['Revenue_Pct'] = display_state['Revenue_Pct'].apply(lambda x: f"{x:.2f}%")
            display_state['Cumulative_Pct'] = display_state['Cumulative_Pct'].apply(lambda x: f"{x:.2f}%")
            st.dataframe(display_state, use_container_width=True, height=400)
        
        with col_det2:
            st.markdown(f"#### 📋 Product Details{period_label}")
            display_product = product_revenue.head(15).copy()
            display_product['Revenue'] = display_product['Revenue'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
            display_product['Revenue_Pct'] = display_product['Revenue_Pct'].apply(lambda x: f"{x:.2f}%")
            display_product['Cumulative_Pct'] = display_product['Cumulative_Pct'].apply(lambda x: f"{x:.2f}%")
            st.dataframe(display_product, use_container_width=True, height=400)
        
        # NEW: Top Customers section
        st.markdown("---")
        st.markdown(f"#### 👥 Top 10 Customers{period_label}")
        display_customer = customer_revenue.head(10).copy()
        display_customer['Revenue'] = display_customer['Revenue'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        display_customer['Avg_Order'] = display_customer['Avg_Order'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        display_customer['Revenue_Pct'] = display_customer['Revenue_Pct'].apply(lambda x: f"{x:.2f}%")
        st.dataframe(display_customer, use_container_width=True)
    
    else:  # Trend View
        # Monthly trend analysis
        st.markdown(f"#### 📈 Monthly Revenue Trend{period_label}")
        
        monthly_trend = analysis_df.groupby(analysis_df['Date'].dt.to_period('M')).agg({
            'Total_Amount': 'sum',
            'Inquiry_No': 'count'
        }).reset_index()
        monthly_trend['Date'] = monthly_trend['Date'].dt.to_timestamp()
        monthly_trend.columns = ['Month', 'Revenue', 'Orders']
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=monthly_trend['Month'],
            y=monthly_trend['Revenue'],
            mode='lines+markers',
            name='Revenue',
            line=dict(width=3, color='royalblue'),
            fill='tozeroy'
        ))
        
        fig_trend.update_layout(
            title=f"Revenue Trend{period_label}",
            xaxis_title="Month",
            yaxis_title=f"Revenue ({CURRENCY})",
            height=450,
            template='plotly_white'
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Show monthly data table
        st.markdown(f"#### 📊 Monthly Breakdown{period_label}")
        monthly_display = monthly_trend.copy()
        monthly_display['Revenue'] = monthly_display['Revenue'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        monthly_display['Month'] = monthly_display['Month'].dt.strftime('%b %Y')
        st.dataframe(monthly_display, use_container_width=True, hide_index=True)
    
    # Export section
    st.markdown("---")
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    
    with col_exp1:
        st.download_button(
            "📥 Export States",
            state_revenue.to_csv().encode('utf-8'),
            f"state_revenue{period_label.replace(' ', '_')}.csv"
        )
    
    with col_exp2:
        st.download_button(
            "📥 Export Products",
            product_revenue.to_csv().encode('utf-8'),
            f"product_revenue{period_label.replace(' ', '_')}.csv"
        )
    
    with col_exp3:
        st.download_button(
            "📥 Export Customers",
            customer_revenue.to_csv().encode('utf-8'),
            f"customer_revenue{period_label.replace(' ', '_')}.csv"
        )

    
    #9-10 Between but diffrent 
    # ==========================================
    # STATE-WISE CONTRIBUTION (ENHANCED)
    # ==========================================
    st.markdown("### 🗺️ State-wise Revenue Contribution")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Top 10 States Table with Rankings
        top_states = state_revenue.head(10).copy()
        top_states['Rank'] = range(1, len(top_states) + 1)
        
        # Format for display
        display_states = pd.DataFrame({
            'Rank': top_states['Rank'],
            'State': top_states.index,
            'Revenue': top_states['Revenue'].apply(lambda x: f"{CURRENCY}{x:,.0f}"),
            'Market Share': top_states['Revenue_Pct'].apply(lambda x: f"{x:.2f}%"),
            'Orders': top_states['Orders'].astype(int),
            'Avg Order': top_states['Avg_Order'].apply(lambda x: f"{CURRENCY}{x:,.0f}"),
            'Cumulative %': top_states['Cumulative_Pct'].apply(lambda x: f"{x:.1f}%")
        })
        
        st.table(display_states.set_index('Rank'))
        
        # State tier classification
        st.markdown("#### 🏅 State Performance Tiers")
        tier_cols = st.columns(3)
        
        # Classify states
        star_states = state_revenue[state_revenue['Revenue_Pct'] >= 10]  # >10% share
        growth_states = state_revenue[(state_revenue['Revenue_Pct'] >= 5) & (state_revenue['Revenue_Pct'] < 10)]
        emerging_states = state_revenue[state_revenue['Revenue_Pct'] < 5]
        
        with tier_cols[0]:
            st.markdown(f"**⭐ Star States (≥10%)**\n\n{len(star_states)} states")
            for state in star_states.head(3).index:
                st.write(f"• {state}")
        
        with tier_cols[1]:
            st.markdown(f"**📈 Growth States (5-10%)**\n\n{len(growth_states)} states")
            for state in growth_states.head(3).index:
                st.write(f"• {state}")
        
        with tier_cols[2]:
            st.markdown(f"**🌱 Emerging (<5%)**\n\n{len(emerging_states)} states")
            st.write(f"Total: {len(emerging_states)} states")
    
    with col2:
        # Enhanced Pie Chart with details
        st.markdown("#### Revenue Distribution")
        
        # Show top 8 + others
        top_8_states = state_revenue.head(8)
        others_revenue = state_revenue.iloc[8:]['Revenue'].sum()
        
        pie_data = pd.DataFrame({
            'State': list(top_8_states.index) + ['Others'],
            'Revenue': list(top_8_states['Revenue']) + [others_revenue]
        })
        
        fig = px.pie(pie_data, values='Revenue', names='State', hole=0.5,
                    color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_traces(textinfo='percent+label', textposition='outside', 
                         textfont_size=11, pull=[0.05 if i == 0 else 0 for i in range(len(pie_data))])
        fig.update_layout(height=500, showlegend=False,
                         annotations=[dict(text=f'Top 8<br>States', x=0.5, y=0.5, font_size=14, showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # ==========================================
    # PRODUCT-WISE CONTRIBUTION (NUMERIC FOCUS)
    # ==========================================
    st.markdown("### 🔧 Product Revenue Contribution")
    
    # Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        show_top_n = st.slider("Show Top N Products:", 5, 30, 10)
    with col_f2:
        min_revenue_prod = st.number_input("Min Revenue:", value=0, step=100000)
    
    filtered_products = product_revenue[product_revenue['Revenue'] >= min_revenue_prod].head(show_top_n)
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.markdown(f"#### Top {show_top_n} Products Ranking")
        
        # Detailed product table
        prod_display = pd.DataFrame({
            'Rank': range(1, len(filtered_products) + 1),
            'Product': filtered_products.index,
            'Revenue': filtered_products['Revenue'].apply(lambda x: f"{CURRENCY}{x:,.0f}"),
            'Market Share': filtered_products['Revenue_Pct'].apply(lambda x: f"{x:.2f}%"),
            'Orders': filtered_products['Orders'].astype(int),
            'States': filtered_products['States_Presence'].astype(int)
        })
        
        st.table(prod_display.set_index('Rank'))
        
        # Product market share summary
        total_prod_share = filtered_products['Revenue_Pct'].sum()
        st.info(f"**Top {show_top_n} products contribute {total_prod_share:.1f}% of total revenue**")
    
    with col2:
        st.markdown("#### Product Performance Metrics")
        
        # Horizontal bar chart with numbers
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=filtered_products.index[::-1],
            x=filtered_products['Revenue'][::-1],
            orientation='h',
            marker=dict(
                color=filtered_products['Revenue_Pct'][::-1],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Market Share %")
            ),
            text=filtered_products.apply(
                lambda x: f"{CURRENCY}{x['Revenue']/100000:.1f}L ({x['Revenue_Pct']:.1f}%)", 
                axis=1
            )[::-1],
            textposition='outside',
            textfont=dict(size=10)
        ))
        
        fig.update_layout(
            height=500,
            xaxis_title=f"Revenue ({CURRENCY})",
            yaxis=dict(autorange="reversed"),
            margin=dict(l=150, r=100, t=30, b=30)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Product concentration analysis
    st.markdown("#### 📊 Product Concentration Analysis")
    
    # Calculate how many products make up 80% of revenue
    product_revenue_sorted = product_revenue.sort_values('Revenue', ascending=False)
    product_revenue_sorted['Cumulative_Revenue'] = product_revenue_sorted['Revenue'].cumsum()
    product_revenue_sorted['Cumulative_Pct'] = (product_revenue_sorted['Cumulative_Revenue'] / total_revenue * 100)
    
    # Find Pareto point (80%)
    pareto_80_idx = product_revenue_sorted[product_revenue_sorted['Cumulative_Pct'] <= 80].index
    pareto_90_idx = product_revenue_sorted[product_revenue_sorted['Cumulative_Pct'] <= 90].index
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("🎯 Top 20% Products", f"{int(len(product_revenue) * 0.2)}", 
                 f"{(product_revenue_sorted.head(int(len(product_revenue) * 0.2))['Revenue_Pct'].sum()):.1f}% revenue")
    with cols[1]:
        st.metric("⭐ 80% Revenue Covered By", f"{len(pareto_80_idx)} products", 
                 f"{len(pareto_80_idx)/len(product_revenue)*100:.1f}% of catalog")
    with cols[2]:
        st.metric("💎 90% Revenue Covered By", f"{len(pareto_90_idx)} products")
    with cols[3]:
        st.metric("📦 Long Tail Products", f"{len(product_revenue) - len(pareto_80_idx)}", 
                 f"{(product_revenue_sorted.tail(len(product_revenue) - len(pareto_80_idx))['Revenue_Pct'].sum()):.1f}% revenue")

# ==========================================
# REPORT 10: PRODUCT PERFORMANCE (NUMERIC FOCUS)
# ==========================================
elif report == "🔧 Product Performance":
    st.markdown("## 🔧 Product Performance Analytics")
    
    # Calculate comprehensive metrics
    product_stats = df.groupby('Product').agg({
        'Total_Amount': ['sum', 'mean', 'count', 'std'],
        'Qty': ['sum', 'mean'],
        'Company': 'nunique',
        'State': 'nunique'
    }).round(2)
    
    product_stats.columns = [
        'Total_Revenue', 'Avg_Order_Value', 'Total_Orders', 'Revenue_StdDev',
        'Total_Qty', 'Avg_Qty_Per_Order', 'Unique_Customers', 'States_Present'
    ]
    
    # Calculate additional metrics
    total_market_revenue = product_stats['Total_Revenue'].sum()
    product_stats['Market_Share_Pct'] = (product_stats['Total_Revenue'] / total_market_revenue * 100).round(2)
    product_stats['Revenue_Per_Customer'] = (product_stats['Total_Revenue'] / product_stats['Unique_Customers']).round(2)
    
    # Sort by revenue
    product_stats = product_stats.sort_values('Total_Revenue', ascending=False)
    
    # TOP SUMMARY CARDS
    st.markdown("### 📊 Market Overview")
    cols = st.columns(5)
    with cols[0]:
        st.metric("Total Products", len(product_stats))
    with cols[1]:
        st.metric("Top Product", product_stats.index[0], f"{CURRENCY}{product_stats.iloc[0]['Total_Revenue']:,.0f}")
    with cols[2]:
        st.metric("Market Leader Share", f"{product_stats.iloc[0]['Market_Share_Pct']:.1f}%")
    with cols[3]:
        st.metric("Avg Order Value", f"{CURRENCY}{product_stats['Avg_Order_Value'].mean():,.0f}")
    with cols[4]:
        st.metric("Total Units Sold", f"{product_stats['Total_Qty'].sum():,.0f}")
    
    st.markdown("---")
    
    # TOP 10 RANKING TABLE (Main View)
    st.markdown("### 🏆 Top 10 Products - Detailed Ranking")
    
    top_10 = product_stats.head(10).copy()
    top_10['Rank'] = range(1, 11)
    top_10['Total_Revenue_Fmt'] = top_10['Total_Revenue'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
    top_10['Avg_Order_Fmt'] = top_10['Avg_Order_Value'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
    top_10['Market_Share_Fmt'] = top_10['Market_Share_Pct'].apply(lambda x: f"{x:.1f}%")
    
    # Reorder columns for display
    display_cols = [
        'Rank', 'Total_Revenue_Fmt', 'Market_Share_Fmt', 'Total_Orders', 
        'Total_Qty', 'Avg_Order_Fmt', 'Unique_Customers', 'States_Present'
    ]
    
    st.table(top_10[display_cols].rename(columns={
        'Total_Revenue_Fmt': 'Revenue',
        'Market_Share_Fmt': 'Market Share',
        'Total_Orders': 'Orders',
        'Total_Qty': 'Units',
        'Avg_Order_Fmt': 'Avg Order',
        'Unique_Customers': 'Customers',
        'States_Present': 'States'
    }))
    
    st.markdown("---")
    
    # COMPARISON SECTION - Select products to compare
    st.markdown("### 🔍 Product Comparison Tool")
    
    col1, col2 = st.columns(2)
    with col1:
        prod1 = st.selectbox("Select Product 1:", product_stats.index, index=0)
    with col2:
        prod2 = st.selectbox("Select Product 2:", product_stats.index, index=1 if len(product_stats) > 1 else 0)
    
    if prod1 and prod2:
        p1_data = product_stats.loc[prod1]
        p2_data = product_stats.loc[prod2]
        
        comparison_df = pd.DataFrame({
            'Metric': ['Revenue', 'Market Share %', 'Orders', 'Units Sold', 'Avg Order Value', 'Customers', 'States'],
            prod1: [
                f"{CURRENCY}{p1_data['Total_Revenue']:,.0f}",
                f"{p1_data['Market_Share_Pct']:.2f}%",
                f"{int(p1_data['Total_Orders'])}",
                f"{int(p1_data['Total_Qty'])}",
                f"{CURRENCY}{p1_data['Avg_Order_Value']:,.0f}",
                f"{int(p1_data['Unique_Customers'])}",
                f"{int(p1_data['States_Present'])}"
            ],
            prod2: [
                f"{CURRENCY}{p2_data['Total_Revenue']:,.0f}",
                f"{p2_data['Market_Share_Pct']:.2f}%",
                f"{int(p2_data['Total_Orders'])}",
                f"{int(p2_data['Total_Qty'])}",
                f"{CURRENCY}{p2_data['Avg_Order_Value']:,.0f}",
                f"{int(p2_data['Unique_Customers'])}",
                f"{int(p2_data['States_Present'])}"
            ],
            'Difference': [
                f"{CURRENCY}{p1_data['Total_Revenue'] - p2_data['Total_Revenue']:,.0f}",
                f"{p1_data['Market_Share_Pct'] - p2_data['Market_Share_Pct']:.2f}%",
                f"{int(p1_data['Total_Orders'] - p2_data['Total_Orders'])}",
                f"{int(p1_data['Total_Qty'] - p2_data['Total_Qty'])}",
                f"{CURRENCY}{p1_data['Avg_Order_Value'] - p2_data['Avg_Order_Value']:,.0f}",
                f"{int(p1_data['Unique_Customers'] - p2_data['Unique_Customers'])}",
                f"{int(p1_data['States_Present'] - p2_data['States_Present'])}"
            ]
        })
        
        st.table(comparison_df.set_index('Metric'))
    
    st.markdown("---")
    
    # ONLY 1 CHART - Top 10 Revenue (Horizontal Bar for quick visual reference)
    st.markdown("### 📊 Quick Visual Reference (Top 10)")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=top_10.index[::-1],
        x=top_10['Total_Revenue'][::-1],
        orientation='h',
        marker_color='royalblue',
        text=top_10['Total_Revenue'][::-1].apply(lambda x: f'{x/100000:.1f}L'),
        textposition='outside'
    ))
    fig.update_layout(
        height=400,
        xaxis_title=f"Revenue ({CURRENCY})",
        showlegend=False,
        margin=dict(l=200, r=50, t=30, b=30)
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # FULL DATA TABLE (Expandable)
    with st.expander("📋 View All Products Data"):
        st.dataframe(
            product_stats.style.format({
                'Total_Revenue': lambda x: f"{CURRENCY}{x:,.0f}",
                'Avg_Order_Value': lambda x: f"{CURRENCY}{x:,.0f}",
                'Revenue_Per_Customer': lambda x: f"{CURRENCY}{x:,.0f}",
                'Market_Share_Pct': lambda x: f"{x:.2f}%"
            }),
            use_container_width=True,
            height=500
        )
# ==========================================
# REPORT 11: PRODUCT TRENDS (ENHANCED)
# ==========================================
elif report == "🔧 Product Trends":
    st.markdown("## 🔧 Product Trends Over Time")
    st.markdown("---")
    
    # Ensure Date column is datetime and extract Year
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter
    df['Month_Name'] = df['Date'].dt.strftime('%b')
    df['Year_Month'] = df['Date'].dt.to_period('M')
    
    # Get available years
    available_years = sorted(df['Year'].unique())
    
    # Header controls
    col_year, col_metric, col_period = st.columns([1, 1, 1])
    
    with col_year:
        year_option = st.selectbox(
            "📅 Select Period:",
            ["All Years"] + [str(y) for y in available_years],
            help="Analyze trends across specific time period"
        )
    
    with col_metric:
        trend_metric = st.selectbox(
            "📊 Metric:",
            ["Revenue", "Quantity", "Orders", "Market Share"],
            help="Choose metric for trend analysis"
        )
    
    with col_period:
        time_period = st.selectbox(
            "⏱️ Time Grouping:",
            ["Monthly", "Quarterly", "Yearly"],
            help="Aggregate data by time period"
        )
    
    # Filter data based on year
    if year_option != "All Years":
        selected_year = int(year_option)
        analysis_df = df[df['Year'] == selected_year].copy()
        period_label = f" ({selected_year})"
    else:
        analysis_df = df.copy()
        period_label = " (All Time)"
    
    # Metric mapping
    metric_map = {
        "Revenue": ("Total_Amount", "sum"),
        "Quantity": ("Qty", "sum"),
        "Orders": ("Inquiry_No", "count"),
        "Market Share": ("Total_Amount", "sum")  # Special calculation
    }
    metric_col, agg_func = metric_map[trend_metric]
    
    # Product selection with categories
    st.markdown("### 🏷️ Product Selection")
    
    # Get top products by selected metric
    if agg_func == "count":
        product_ranking = analysis_df.groupby('Product')['Inquiry_No'].count().sort_values(ascending=False)
    else:
        product_ranking = analysis_df.groupby('Product')[metric_col].sum().sort_values(ascending=False)
    
    top_products = product_ranking.head(20).index.tolist()
    
    col_prod1, col_prod2 = st.columns([3, 1])
    
    with col_prod1:
        selected_products = st.multiselect(
            "🔧 Select Products to Compare:", 
            top_products, 
            default=top_products[:5] if len(top_products) >= 5 else top_products,
            help="Choose multiple products to compare trends"
        )
    
    with col_prod2:
        select_all = st.checkbox("Select All Top 20", value=False)
        if select_all:
            selected_products = top_products
    
    if not selected_products:
        st.warning("⚠️ Please select at least one product")
        st.stop()
    
    # Prepare time series data
    def prepare_time_series(data, products, period):
        """Prepare time series data based on selected period"""
        result = {}
        
        for product in products:
            prod_df = data[data['Product'] == product].copy()
            
            if period == "Monthly":
                grouped = prod_df.groupby(prod_df['Date'].dt.to_period('M'))
            elif period == "Quarterly":
                grouped = prod_df.groupby([prod_df['Year'], prod_df['Quarter']])
            else:  # Yearly
                grouped = prod_df.groupby('Year')
            
            if agg_func == "count":
                series = grouped.size()
            else:
                series = grouped[metric_col].sum()
            
            # Convert index to datetime for consistent plotting
            if period == "Monthly":
                series.index = series.index.to_timestamp()
            elif period == "Quarterly":
                series.index = pd.to_datetime(
                    series.index.map(lambda x: f"{x[0]}-{x[1]*3-2:02d}-01")
                )
            else:
                series.index = pd.to_datetime(series.index, format='%Y')
            
            result[product] = series
        
        return result
    
    time_series_data = prepare_time_series(analysis_df, selected_products, time_period)
    
    # Create DataFrame for easier manipulation
    trend_df = pd.DataFrame(time_series_data).fillna(0)
    
    # Calculate market share if selected
    if trend_metric == "Market Share":
        total_by_period = trend_df.sum(axis=1)
        trend_df = trend_df.div(total_by_period, axis=0) * 100
    
    # Main visualization tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Trend Lines", 
        "📊 Comparative Analysis", 
        "🎯 Growth Metrics", 
        "🔍 Seasonality"
    ])
    
    with tab1:
        st.markdown(f"#### 📈 {trend_metric} Trends{period_label}")
        
        chart_type = st.radio(
            "Chart Type:",
            ["Line Chart", "Area Chart", "Stacked Area", "Candlestick Style"],
            horizontal=True,
            key="trend_chart_type"
        )
        
        fig = go.Figure()
        
        colors = px.colors.qualitative.Set1 + px.colors.qualitative.Set2 + px.colors.qualitative.Set3
        
        for idx, product in enumerate(selected_products):
            color = colors[idx % len(colors)]
            
            if chart_type == "Line Chart":
                fig.add_trace(go.Scatter(
                    x=trend_df.index,
                    y=trend_df[product],
                    mode='lines+markers',
                    name=product,
                    line=dict(width=3, color=color),
                    marker=dict(size=8, color=color)
                ))
            
            elif chart_type == "Area Chart":
                fig.add_trace(go.Scatter(
                    x=trend_df.index,
                    y=trend_df[product],
                    fill='tozeroy',
                    name=product,
                    line=dict(width=2, color=color),
                    fillcolor=color.replace(')', ', 0.3)').replace('rgb', 'rgba')
                ))
            
            elif chart_type == "Stacked Area":
                fig.add_trace(go.Scatter(
                    x=trend_df.index,
                    y=trend_df[product],
                    stackgroup='one',
                    name=product,
                    line=dict(width=1, color=color),
                    fillcolor=color
                ))
            
            else:  # Candlestick Style (showing min, max, start, end for grouped periods)
                # For simplicity, show range as filled area
                fig.add_trace(go.Scatter(
                    x=trend_df.index,
                    y=trend_df[product],
                    fill='tozeroy',
                    name=product,
                    line=dict(width=2, color=color)
                ))
        
        # Add trend line for total if multiple products
        if len(selected_products) > 1 and chart_type != "Stacked Area":
            total_line = trend_df.sum(axis=1)
            fig.add_trace(go.Scatter(
                x=total_line.index,
                y=total_line.values,
                mode='lines',
                name='TOTAL',
                line=dict(width=4, color='black', dash='dash'),
                opacity=0.7
            ))
        
        y_axis_title = f"{trend_metric} ({'%' if trend_metric == 'Market Share' else CURRENCY if trend_metric == 'Revenue' else 'Units'})"
        
        fig.update_layout(
            title=f'{trend_metric} Trends - {time_period} View',
            xaxis_title="Time Period",
            yaxis_title=y_axis_title,
            height=550,
            template='plotly_white',
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary statistics
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        
        with col_stat1:
            total_value = trend_df.sum().sum()
            prefix = CURRENCY if trend_metric == "Revenue" else ""
            suffix = "%" if trend_metric == "Market Share" else ""
            st.metric(
                f"Total {trend_metric}",
                f"{prefix}{total_value:,.0f}{suffix}"
            )
        
        with col_stat2:
            avg_period = trend_df.sum(axis=1).mean()
            st.metric(
                f"Avg per {time_period[:-2]}",
                f"{prefix}{avg_period:,.0f}{suffix}"
            )
        
        with col_stat3:
            peak_period = trend_df.sum(axis=1).idxmax()
            st.metric(
                "Peak Period",
                peak_period.strftime('%b %Y') if hasattr(peak_period, 'strftime') else str(peak_period)
            )
    
    with tab2:
        st.markdown("#### 📊 Comparative Performance Matrix")
        
        # Calculate performance metrics for each product
        comparison_metrics = []
        
        for product in selected_products:
            series = trend_df[product]
            
            metrics = {
                'Product': product,
                'Total': series.sum(),
                'Average': series.mean(),
                'Peak': series.max(),
                'Min': series.min(),
                'Std_Dev': series.std(),
                'Growth_Rate': ((series.iloc[-1] - series.iloc[0]) / series.iloc[0] * 100) if len(series) > 1 and series.iloc[0] != 0 else 0,
                'Volatility': (series.std() / series.mean() * 100) if series.mean() != 0 else 0
            }
            comparison_metrics.append(metrics)
        
        comp_df = pd.DataFrame(comparison_metrics).sort_values('Total', ascending=False)
        
        # Display as table
        display_comp = comp_df.copy()
        prefix = CURRENCY if trend_metric == "Revenue" else ""
        suffix = "%" if trend_metric == "Market Share" else ""
        
        for col in ['Total', 'Average', 'Peak', 'Min']:
            display_comp[col] = display_comp[col].apply(lambda x: f"{prefix}{x:,.0f}{suffix}")
        
        display_comp['Std_Dev'] = display_comp['Std_Dev'].apply(lambda x: f"{prefix}{x:,.0f}")
        display_comp['Growth_Rate'] = display_comp['Growth_Rate'].apply(lambda x: f"{x:+.1f}%")
        display_comp['Volatility'] = display_comp['Volatility'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(display_comp, use_container_width=True, hide_index=True)
        
        # Radar chart comparison
        st.markdown("#### 🕸️ Multi-Dimensional Comparison")
        
        # Normalize metrics for radar chart (0-100 scale)
        radar_metrics = ['Total', 'Average', 'Peak', 'Growth_Rate']
        radar_df = comp_df[['Product'] + radar_metrics].copy()
        
        # Normalize to 0-100 scale
        for metric in radar_metrics:
            min_val = radar_df[metric].min()
            max_val = radar_df[metric].max()
            if max_val > min_val:
                radar_df[metric] = ((radar_df[metric] - min_val) / (max_val - min_val)) * 100
            else:
                radar_df[metric] = 50
        
        fig_radar = go.Figure()
        
        for idx, row in radar_df.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[row[m] for m in radar_metrics] + [row[radar_metrics[0]]],
                theta=radar_metrics + [radar_metrics[0]],
                fill='toself',
                name=row['Product'],
                opacity=0.6
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=True,
            title="Performance Comparison (Normalized)",
            height=500,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with tab3:
        st.markdown("#### 🎯 Growth & Momentum Analysis")
        
        # Calculate month-over-month or period-over-period growth
        growth_df = trend_df.pct_change() * 100
        
        col_growth1, col_growth2 = st.columns(2)
        
        with col_growth1:
            st.markdown("**📈 Period-over-Period Growth Rate (%)**")
            
            fig_growth = go.Figure()
            
            for idx, product in enumerate(selected_products):
                fig_growth.add_trace(go.Bar(
                    name=product,
                    x=growth_df.index,
                    y=growth_df[product],
                    marker_color=colors[idx % len(colors)]
                ))
            
            fig_growth.update_layout(
                barmode='group',
                title=f'{time_period} Growth Rate',
                yaxis_title="Growth %",
                height=400,
                template='plotly_white',
                showlegend=True
            )
            
            fig_growth.add_hline(y=0, line_dash="dash", line_color="black")
            
            st.plotly_chart(fig_growth, use_container_width=True)
        
        with col_growth2:
            st.markdown("**🎢 Cumulative Growth**")
            
            # Calculate cumulative growth from first period
            cumulative_df = ((trend_df / trend_df.iloc[0] - 1) * 100) if len(trend_df) > 0 else trend_df
            
            fig_cum = go.Figure()
            
            for idx, product in enumerate(selected_products):
                fig_cum.add_trace(go.Scatter(
                    x=cumulative_df.index,
                    y=cumulative_df[product],
                    mode='lines',
                    name=product,
                    line=dict(width=3, color=colors[idx % len(colors)]),
                    stackgroup=None
                ))
            
            fig_cum.update_layout(
                title='Cumulative Growth from Start',
                yaxis_title="Cumulative Growth %",
                height=400,
                template='plotly_white',
                hovermode='x unified'
            )
            
            fig_cum.add_hline(y=0, line_dash="dash", line_color="black")
            
            st.plotly_chart(fig_cum, use_container_width=True)
        
        # Growth insights
        st.markdown("#### 💡 Growth Insights")
        
        # Best and worst performers
        total_growth = {}
        for product in selected_products:
            series = trend_df[product]
            if len(series) >= 2 and series.iloc[0] != 0:
                growth = ((series.iloc[-1] - series.iloc[0]) / series.iloc[0]) * 100
                total_growth[product] = growth
        
        if total_growth:
            best_product = max(total_growth, key=total_growth.get)
            worst_product = min(total_growth, key=total_growth.get)
            
            col_ins1, col_ins2 = st.columns(2)
            
            with col_ins1:
                st.success(f"🏆 **Best Performer:** {best_product}  \n"
                          f"Total Growth: {total_growth[best_product]:+.1f}%")
            
            with col_ins2:
                if total_growth[worst_product] < 0:
                    st.error(f"📉 **Needs Attention:** {worst_product}  \n"
                            f"Total Growth: {total_growth[worst_product]:+.1f}%")
                else:
                    st.info(f"📊 **Slowest Growth:** {worst_product}  \n"
                           f"Total Growth: {total_growth[worst_product]:+.1f}%")
    
    with tab4:
        st.markdown("#### 🔍 Seasonality Patterns")
        
        if time_period == "Monthly" and len(analysis_df) > 0:
            # Aggregate by month across all years
            seasonality_df = analysis_df[analysis_df['Product'].isin(selected_products)].copy()
            
            monthly_pattern = seasonality_df.groupby(['Product', 'Month']).agg({
                metric_col: agg_func if agg_func != 'count' else 'size'
            }).reset_index()
            
            # Pivot for heatmap
            pivot_seasonal = monthly_pattern.pivot(index='Product', columns='Month', values=metric_col).fillna(0)
            
            # Reorder columns to start from January
            pivot_seasonal = pivot_seasonal[[i for i in range(1, 13) if i in pivot_seasonal.columns]]
            
            fig_heatmap = px.imshow(
                pivot_seasonal,
                labels=dict(x="Month", y="Product", color=trend_metric),
                x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][:len(pivot_seasonal.columns)],
                y=pivot_seasonal.index,
                color_continuous_scale="RdYlGn",
                aspect="auto",
                title=f"Seasonal Heatmap - {trend_metric} by Month",
                template='plotly_white'
            )
            
            fig_heatmap.update_layout(height=max(400, len(selected_products) * 40))
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Seasonal index calculation
            st.markdown("#### 📊 Seasonal Index (Average = 100)")
            
            seasonal_index = pivot_seasonal.div(pivot_seasonal.mean(axis=1), axis=0) * 100
            
            fig_index = go.Figure()
            
            for product in selected_products:
                if product in seasonal_index.index:
                    fig_index.add_trace(go.Scatter(
                        x=list(range(1, 13)),
                        y=seasonal_index.loc[product].values,
                        mode='lines+markers',
                        name=product,
                        line=dict(width=2)
                    ))
            
            fig_index.add_hline(y=100, line_dash="dash", line_color="black", 
                               annotation_text="Average")
            
            fig_index.update_layout(
                title="Seasonal Index by Month",
                xaxis=dict(
                    tickmode='array',
                    tickvals=list(range(1, 13)),
                    ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                ),
                yaxis_title="Index (100 = Average)",
                height=450,
                template='plotly_white',
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_index, use_container_width=True)
            
            # Peak season identification
            st.markdown("#### 🎯 Peak Season Insights")
            
            for product in selected_products:
                if product in seasonal_index.index:
                    peak_month = seasonal_index.loc[product].idxmax()
                    low_month = seasonal_index.loc[product].idxmin()
                    peak_value = seasonal_index.loc[product].max()
                    low_value = seasonal_index.loc[product].min()
                    
                    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                             'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                    
                    col_peak1, col_peak2 = st.columns(2)
                    with col_peak1:
                        st.success(f"**{product}**  \n"
                                  f"🔥 Peak: {months[peak_month-1]} ({peak_value:.0f} index)  \n"
                                  f"❄️ Low: {months[low_month-1]} ({low_value:.0f} index)")
        
        else:
            st.info("ℹ️ Switch to 'Monthly' time grouping to view seasonality analysis")
    
    # Data table at bottom
    with st.expander("📋 View Raw Trend Data"):
        display_trend = trend_df.copy()
        if trend_metric != "Market Share":
            prefix = CURRENCY if trend_metric == "Revenue" else ""
            display_trend = display_trend.applymap(lambda x: f"{prefix}{x:,.0f}")
        else:
            display_trend = display_trend.applymap(lambda x: f"{x:.1f}%")
        
        st.dataframe(display_trend, use_container_width=True)
        
        # Export option
        csv = trend_df.to_csv().encode('utf-8')
        st.download_button(
            label="📥 Export Trend Data (CSV)",
            data=csv,
            file_name=f"product_trends_{year_option.replace(' ', '_')}.csv",
            mime='text/csv'
        )
# ==========================================
# REPORT 12: BEST SELLERS BY STATE (ENHANCED & FIXED)
# ==========================================
elif report == "🔧 Best Sellers by State":
    st.markdown("## 🔧 Best Selling Products by State")
    st.markdown("---")
    
    # Ensure Date column is datetime and extract Year
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    
    # Get available years
    available_years = sorted(df['Year'].unique())
    
    # Filters row
    col_state, col_year, col_metric = st.columns([2, 1, 1])
    
    with col_state:
        selected_state = st.selectbox(
            "🗺️ Select State:", 
            sorted(df['State'].unique()),
            help="Choose a state to analyze top products"
        )
    
    with col_year:
        year_options = ["All Years"] + [str(y) for y in available_years]
        selected_year_option = st.selectbox(
            "📅 Year:", 
            year_options,
            help="Filter by specific year or view all time data"
        )
    
    with col_metric:
        ranking_metric = st.selectbox(
            "📊 Rank By:",
            ["Revenue", "Quantity", "Orders"],
            help="Choose metric to rank products"
        )
    
    # Filter data
    state_df = df[df['State'] == selected_state].copy()
    
    if selected_year_option != "All Years":
        selected_year = int(selected_year_option)
        state_df = state_df[state_df['Year'] == selected_year]
        year_label = f" ({selected_year})"
    else:
        year_label = " (All Time)"
    
    if state_df.empty:
        st.warning(f"⚠️ No data available for {selected_state}{year_label}")
        st.stop()
    
    # Calculate metrics based on selection
    if ranking_metric == "Revenue":
        metric_col = 'Total_Amount'
        agg_func = 'sum'
        currency_prefix = CURRENCY
        chart_color_scale = 'Viridis'
    elif ranking_metric == "Quantity":
        metric_col = 'Qty'
        agg_func = 'sum'
        currency_prefix = ""
        chart_color_scale = 'Plasma'
    else:  # Orders
        metric_col = 'Inquiry_No'
        agg_func = 'count'
        currency_prefix = ""
        chart_color_scale = 'Inferno'
    
    # Aggregate data - FIXED: Check available columns first
    agg_dict = {
        'Total_Amount': 'sum',
        'Qty': 'sum',
        'Inquiry_No': 'count'
    }
    
    # Only add Unit_Price if it exists
    if 'Unit_Price' in state_df.columns:
        agg_dict['Unit_Price'] = 'mean'
    
    product_stats = state_df.groupby('Product').agg(agg_dict).rename(columns={'Inquiry_No': 'Orders'})
    
    # Calculate additional metrics
    product_stats['Avg_Order_Value'] = product_stats['Total_Amount'] / product_stats['Orders']
    
    # Calculate market share based on selected metric
    if ranking_metric == "Orders":
        total_metric = product_stats['Orders'].sum()
        product_stats['Market_Share'] = (product_stats['Orders'] / total_metric * 100)
    elif ranking_metric == "Quantity":
        total_metric = product_stats['Qty'].sum()
        product_stats['Market_Share'] = (product_stats['Qty'] / total_metric * 100)
    else:
        total_metric = product_stats['Total_Amount'].sum()
        product_stats['Market_Share'] = (product_stats['Total_Amount'] / total_metric * 100)
    
    # Sort by selected metric
    if ranking_metric == "Orders":
        sort_col = 'Orders'
    elif ranking_metric == "Quantity":
        sort_col = 'Qty'
    else:
        sort_col = 'Total_Amount'
    
    top_products = product_stats.sort_values(sort_col, ascending=False).head(20)
    
    # Header with metrics
    st.markdown(f"### 📈 Top Performing Products in **{selected_state}**{year_label}")
    
    # KPI Cards
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    
    with col_kpi1:
        total_revenue = state_df['Total_Amount'].sum()
        st.metric(
            "Total Revenue", 
            f"{CURRENCY}{total_revenue:,.0f}",
            help="Total revenue for selected state and period"
        )
    
    with col_kpi2:
        total_orders = state_df['Inquiry_No'].nunique()
        st.metric("Total Orders", f"{total_orders:,}")
    
    with col_kpi3:
        top_product = top_products.index[0] if not top_products.empty else "N/A"
        st.metric("Top Product", top_product[:20] + "..." if len(str(top_product)) > 20 else top_product)
    
    with col_kpi4:
        top_product_share = top_products.iloc[0]['Market_Share'] if not top_products.empty else 0
        st.metric("Top Product Share", f"{top_product_share:.1f}%")
    
    st.markdown("---")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏆 Rankings", 
        "📊 Visual Analysis", 
        "📈 Trends", 
        "🔍 Detailed Breakdown"
    ])
    
    with tab1:
        col_chart, col_table = st.columns([3, 2])
        
        with col_chart:
            st.markdown(f"#### Top 15 Products by {ranking_metric}")
            
            # Create enhanced bar chart
            display_df = top_products.head(15).reset_index()
            display_df['Rank'] = range(1, len(display_df) + 1)
            
            # Determine color based on ranking metric
            if ranking_metric == "Revenue":
                color_col = 'Total_Amount'
                hover_data = ['Qty', 'Orders', 'Avg_Order_Value']
            elif ranking_metric == "Quantity":
                color_col = 'Qty'
                hover_data = ['Total_Amount', 'Orders', 'Avg_Order_Value']
            else:
                color_col = 'Orders'
                hover_data = ['Total_Amount', 'Qty', 'Avg_Order_Value']
            
            fig = px.bar(
                display_df,
                y='Product',
                x=sort_col,
                orientation='h',
                color=color_col,
                color_continuous_scale=chart_color_scale,
                title=f"Best Sellers - {selected_state}{year_label}",
                labels={sort_col: ranking_metric, 'Product': ''},
                hover_data=hover_data,
                text=sort_col
            )
            
            fig.update_traces(
                texttemplate=f'{currency_prefix}' + '%{text:,.0f}',
                textposition='outside',
                textfont=dict(size=10)
            )
            
            fig.update_layout(
                height=600,
                yaxis=dict(autorange="reversed", categoryorder='total ascending'),
                xaxis_title=ranking_metric,
                template='plotly_white',
                coloraxis_colorbar=dict(title=ranking_metric)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col_table:
            st.markdown("#### 📋 Detailed Rankings")
            
            # Prepare display table
            display_table = top_products.head(15).copy()
            display_table['Rank'] = range(1, len(display_table) + 1)
            
            # Format columns
            display_table['Revenue'] = display_table['Total_Amount'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
            display_table['Quantity'] = display_table['Qty'].apply(lambda x: f"{x:,.0f}")
            display_table['Orders'] = display_table['Orders'].apply(lambda x: f"{x:,}")
            display_table['Avg_Order'] = display_table['Avg_Order_Value'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
            display_table['Market_Share'] = display_table['Market_Share'].apply(lambda x: f"{x:.1f}%")
            
            # Reorder columns
            display_table = display_table[['Rank', 'Revenue', 'Quantity', 'Orders', 'Avg_Order', 'Market_Share']]
            
            # Apply styling
            def highlight_top3(row):
                if row['Rank'] == 1:
                    return ['background: linear-gradient(90deg, #FFD700, #FFA500)'] * len(row)
                elif row['Rank'] == 2:
                    return ['background: linear-gradient(90deg, #C0C0C0, #A0A0A0)'] * len(row)
                elif row['Rank'] == 3:
                    return ['background: linear-gradient(90deg, #CD7F32, #B87333)'] * len(row)
                return [''] * len(row)
            
            st.dataframe(
                display_table.style.apply(highlight_top3, axis=1),
                use_container_width=True,
                height=600,
                hide_index=False
            )
    
    with tab2:
        col_treemap, col_pie = st.columns(2)
        
        with col_treemap:
            st.markdown("#### 🗺️ Revenue Distribution (Treemap)")
            
            fig_treemap = px.treemap(
                top_products.head(10).reset_index(),
                path=[px.Constant(selected_state), 'Product'],
                values='Total_Amount',
                color='Total_Amount',
                color_continuous_scale='RdYlBu',
                title=f"Top 10 Products Revenue Share"
            )
            fig_treemap.update_layout(height=500, template='plotly_white')
            fig_treemap.update_traces(
                textinfo="label+value+percent parent",
                texttemplate='<b>%{label}</b><br>%{value:,.0f}<br>(%{percentParent:.1%})'
            )
            st.plotly_chart(fig_treemap, use_container_width=True)
        
        with col_pie:
            st.markdown("#### 🥧 Market Share (Top 10)")
            
            pie_data = top_products.head(10).reset_index()
            others_revenue = product_stats['Total_Amount'].sum() - pie_data['Total_Amount'].sum()
            
            if others_revenue > 0:
                pie_data = pd.concat([
                    pie_data,
                    pd.DataFrame([{'Product': 'Others', 'Total_Amount': others_revenue}])
                ], ignore_index=True)
            
            fig_pie = px.pie(
                pie_data,
                values='Total_Amount',
                names='Product',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig_pie.update_traces(
                textposition='outside',
                textinfo='percent+label',
                pull=[0.02 if i < 3 else 0 for i in range(len(pie_data))],
                marker=dict(line=dict(color='#ffffff', width=2))
            )
            
            fig_pie.update_layout(
                height=500,
                template='plotly_white',
                showlegend=False,
                annotations=[dict(text=f'Top 10<br>+Others', x=0.5, y=0.5, font_size=14, showarrow=False)]
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Pareto Chart
        st.markdown("#### 📊 Pareto Analysis (80/20 Rule)")
        
        pareto_data = top_products.copy()
        pareto_data['Cumulative_Revenue'] = pareto_data['Total_Amount'].cumsum()
        pareto_data['Cumulative_Percentage'] = (pareto_data['Cumulative_Revenue'] / 
                                                pareto_data['Total_Amount'].sum() * 100)
        
        fig_pareto = go.Figure()
        
        # Bar chart
        fig_pareto.add_trace(go.Bar(
            x=list(range(len(pareto_data.head(15)))),
            y=pareto_data.head(15)['Total_Amount'],
            name='Revenue',
            marker_color='royalblue',
            text=pareto_data.head(15)['Total_Amount'].apply(lambda x: f'{CURRENCY}{x/1000:.0f}K'),
            textposition='auto'
        ))
        
        # Line chart for cumulative percentage
        fig_pareto.add_trace(go.Scatter(
            x=list(range(len(pareto_data.head(15)))),
            y=pareto_data.head(15)['Cumulative_Percentage'],
            name='Cumulative %',
            yaxis='y2',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))
        
        # 80% line
        fig_pareto.add_hline(y=80, line_dash="dash", line_color="green", 
                            annotation_text="80% Threshold", yref='y2')
        
        fig_pareto.update_layout(
            title="Pareto Chart: Product Contribution Analysis",
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(len(pareto_data.head(15)))),
                ticktext=[p[:15] + "..." if len(p) > 15 else p for p in pareto_data.head(15).index],
                tickangle=-45
            ),
            yaxis=dict(title='Revenue', side='left'),
            yaxis2=dict(
                title='Cumulative %',
                side='right',
                overlaying='y',
                range=[0, 100],
                ticksuffix='%'
            ),
            height=500,
            template='plotly_white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        
        st.plotly_chart(fig_pareto, use_container_width=True)
        
        # Find products contributing to 80%
        products_80 = pareto_data[pareto_data['Cumulative_Percentage'] <= 80]
        if not products_80.empty:
            st.success(f"🎯 **Insight:** Top {len(products_80)} products ({len(products_80)/len(pareto_data)*100:.1f}%) "
                      f"contribute to 80% of total revenue in {selected_state}")
    
    with tab3:
        st.markdown(f"#### 📈 Monthly Trends for Top 5 Products")
        
        # Get top 5 products
        top_5_products = top_products.head(5).index.tolist()
        
        # Prepare monthly data
        monthly_trends = state_df[state_df['Product'].isin(top_5_products)].copy()
        monthly_trends['Month'] = monthly_trends['Date'].dt.to_period('M')
        
        monthly_agg = monthly_trends.groupby(['Month', 'Product'])['Total_Amount'].sum().reset_index()
        monthly_agg['Month'] = monthly_agg['Month'].dt.to_timestamp()
        
        fig_trends = px.line(
            monthly_agg,
            x='Month',
            y='Total_Amount',
            color='Product',
            markers=True,
            title=f"Monthly Revenue Trends - Top 5 Products",
            template='plotly_white'
        )
        
        fig_trends.update_layout(
            height=450,
            xaxis_title="Month",
            yaxis_title=f"Revenue ({CURRENCY})",
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=-0.3)
        )
        
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Seasonality analysis
        st.markdown("#### 🗓️ Seasonality Pattern")
        
        seasonal_data = monthly_trends.copy()
        seasonal_data['Month_Name'] = seasonal_data['Date'].dt.strftime('%B')
        seasonal_data['Month_Num'] = seasonal_data['Date'].dt.month
        
        seasonal_agg = seasonal_data.groupby(['Month_Num', 'Month_Name'])['Total_Amount'].sum().reset_index()
        seasonal_agg = seasonal_agg.sort_values('Month_Num')
        
        fig_seasonal = px.bar(
            seasonal_agg,
            x='Month_Name',
            y='Total_Amount',
            color='Total_Amount',
            color_continuous_scale='Viridis',
            title="Seasonal Revenue Distribution (All Products)",
            template='plotly_white'
        )
        
        fig_seasonal.update_layout(height=400, xaxis_title="Month", yaxis_title=f"Revenue ({CURRENCY})")
        st.plotly_chart(fig_seasonal, use_container_width=True)
    
    with tab4:
        st.markdown("#### 🔍 Product Performance Matrix")
        
        # Scatter plot: Quantity vs Revenue
        scatter_data = top_products.head(20).reset_index()
        
        fig_scatter = px.scatter(
            scatter_data,
            x='Qty',
            y='Total_Amount',
            size='Orders',
            color='Avg_Order_Value',
            hover_name='Product',
            text='Product',
            title="Product Performance Matrix (Top 20)",
            labels={
                'Qty': 'Total Quantity Sold',
                'Total_Amount': f'Total Revenue ({CURRENCY})',
                'Orders': 'Number of Orders',
                'Avg_Order_Value': f'Avg Order Value ({CURRENCY})'
            },
            template='plotly_white',
            color_continuous_scale='Plasma'
        )
        
        fig_scatter.update_traces(
            textposition='top center',
            textfont=dict(size=9),
            marker=dict(line=dict(width=1, color='DarkSlateGrey'))
        )
        
        fig_scatter.update_layout(height=550)
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Product comparison table with all metrics
        st.markdown("#### 📊 Complete Product Metrics")
        
        complete_metrics = top_products.copy()
        
        # Only calculate if columns exist
        if 'Qty' in complete_metrics.columns and complete_metrics['Qty'].sum() > 0:
            complete_metrics['Revenue_per_Unit'] = complete_metrics['Total_Amount'] / complete_metrics['Qty']
        else:
            complete_metrics['Revenue_per_Unit'] = 0
            
        complete_metrics['Revenue_per_Order'] = complete_metrics['Total_Amount'] / complete_metrics['Orders']
        
        # Format for display
        display_complete = complete_metrics.copy()
        display_complete['Total_Amount'] = display_complete['Total_Amount'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        display_complete['Qty'] = display_complete['Qty'].apply(lambda x: f"{x:,.0f}")
        display_complete['Orders'] = display_complete['Orders'].apply(lambda x: f"{x:,}")
        display_complete['Avg_Order_Value'] = display_complete['Avg_Order_Value'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        display_complete['Market_Share'] = display_complete['Market_Share'].apply(lambda x: f"{x:.2f}%")
        display_complete['Revenue_per_Unit'] = display_complete['Revenue_per_Unit'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        display_complete['Revenue_per_Order'] = display_complete['Revenue_per_Order'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        
        st.dataframe(
            display_complete[['Total_Amount', 'Qty', 'Orders', 'Avg_Order_Value', 
                             'Market_Share', 'Revenue_per_Unit', 'Revenue_per_Order']],
            use_container_width=True,
            height=500
        )
        
        # Export option
        st.download_button(
            label="📥 Download Product Analysis (CSV)",
            data=top_products.to_csv().encode('utf-8'),
            file_name=f'best_sellers_{selected_state}_{selected_year_option.replace(" ", "_")}.csv',
            mime='text/csv'
        )
# ==========================================
# REPORT 13: COMPANY ANALYSIS (ENHANCED & FIXED)
# ==========================================
elif report == "🏢 Company Analysis":
    st.markdown("## 🏢 Customer/Company Deep Dive")
    st.markdown("---")
    
    # Ensure Date column is datetime and extract Year
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    
    # Get available years
    available_years = sorted(df['Year'].unique())
    
    # Header filters
    col_year, col_segment, col_metric = st.columns([1, 1, 1])
    
    with col_year:
        year_option = st.selectbox(
            "📅 Select Period:",
            ["All Years"] + [str(y) for y in available_years],
            help="Analyze companies across specific time period"
        )
    
    # Filter data based on year
    if year_option != "All Years":
        selected_year = int(year_option)
        analysis_df = df[df['Year'] == selected_year].copy()
        period_label = f" ({selected_year})"
    else:
        analysis_df = df.copy()
        period_label = " (All Time)"
    
    with col_segment:
        segmentation = st.selectbox(
            "🎯 Segment By:",
            ["Revenue", "Order Frequency", "Order Value", "Growth Potential"],
            help="Choose segmentation strategy for customer analysis"
        )
    
    with col_metric:
        view_type = st.selectbox(
            "👁️ View:",
            ["Top Performers", "At-Risk Customers", "New Opportunities", "Complete List"],
            help="Filter companies by performance category"
        )
    
    st.markdown("---")
    
    # Calculate comprehensive company metrics
    company_metrics = analysis_df.groupby('Company').agg({
        'Total_Amount': ['sum', 'count', 'mean', 'std'],
        'Qty': ['sum', 'mean'],
        'Inquiry_No': 'nunique',
        'Date': ['min', 'max'],
        'Product': 'nunique',
        'State': lambda x: x.mode().iloc[0] if not x.empty else 'Unknown'
    }).round(2)
    
    # Flatten column names
    company_metrics.columns = [
        'Total_Revenue', 'Total_Orders', 'Avg_Order_Value', 'Order_StdDev',
        'Total_Qty', 'Avg_Qty_Per_Order', 'Unique_Orders', 
        'First_Order', 'Last_Order', 'Unique_Products', 'Primary_State'
    ]
    
    # Calculate additional metrics
    company_metrics['Days_Since_Last_Order'] = (
        pd.Timestamp.now() - pd.to_datetime(company_metrics['Last_Order'])
    ).dt.days
    
    company_metrics['Customer_Lifespan_Days'] = (
        pd.to_datetime(company_metrics['Last_Order']) - 
        pd.to_datetime(company_metrics['First_Order'])
    ).dt.days + 1
    
    company_metrics['Order_Frequency'] = (
        company_metrics['Total_Orders'] / company_metrics['Customer_Lifespan_Days'] * 30
    ).fillna(0)
    
    company_metrics['Revenue_Per_Day'] = (
        company_metrics['Total_Revenue'] / company_metrics['Customer_Lifespan_Days']
    ).fillna(0)
    
    # Customer Segmentation (RFM-style analysis)
    company_metrics['Recency_Score'] = pd.qcut(
        company_metrics['Days_Since_Last_Order'], 
        q=5, 
        labels=[5,4,3,2,1],
        duplicates='drop'
    ).astype(int)
    
    company_metrics['Frequency_Score'] = pd.qcut(
        company_metrics['Total_Orders'].rank(method='first'), 
        q=5, 
        labels=[1,2,3,4,5],
        duplicates='drop'
    ).astype(int)
    
    company_metrics['Monetary_Score'] = pd.qcut(
        company_metrics['Total_Revenue'].rank(method='first'), 
        q=5, 
        labels=[1,2,3,4,5],
        duplicates='drop'
    ).astype(int)
    
    company_metrics['RFM_Score'] = (
        company_metrics['Recency_Score'].astype(str) + 
        company_metrics['Frequency_Score'].astype(str) + 
        company_metrics['Monetary_Score'].astype(str)
    )
    
    # Customer Tier Classification
    def classify_customer(row):
        if row['Monetary_Score'] >= 4 and row['Frequency_Score'] >= 4:
            return '💎 Champion'
        elif row['Monetary_Score'] >= 4:
            return '🥇 Loyal Customer'
        elif row['Frequency_Score'] >= 4:
            return '📈 Potential Loyalist'
        elif row['Recency_Score'] >= 4:
            return '🆕 New Customer'
        elif row['Recency_Score'] <= 2 and row['Monetary_Score'] >= 3:
            return '⚠️ At Risk'
        elif row['Recency_Score'] <= 2:
            return '😴 Hibernating'
        else:
            return '📊 Needs Attention'
    
    company_metrics['Customer_Segment'] = company_metrics.apply(classify_customer, axis=1)
    
    # Filter based on view type
    if view_type == "Top Performers":
        filtered_metrics = company_metrics[company_metrics['Monetary_Score'] >= 4].copy()
    elif view_type == "At-Risk Customers":
        filtered_metrics = company_metrics[
            (company_metrics['Customer_Segment'].str.contains('At Risk|Hibernating')) |
            (company_metrics['Days_Since_Last_Order'] > 90)
        ].copy()
    elif view_type == "New Opportunities":
        filtered_metrics = company_metrics[
            (company_metrics['Customer_Segment'].str.contains('New|Potential')) |
            (company_metrics['Total_Orders'] <= 3) & (company_metrics['Total_Revenue'] > company_metrics['Total_Revenue'].median())
        ].copy()
    else:
        filtered_metrics = company_metrics.copy()
    
    # Additional filters
    st.markdown("### 🔍 Filter Controls")
    
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    
    with col_f1:
        # FIXED: Removed currency symbol from format
        min_revenue = st.number_input(
            "Min Revenue:",
            min_value=0.0,
            value=0.0,
            step=1000.0,
            format="%.0f",
            help=f"Minimum revenue threshold (in {CURRENCY})"
        )
        # Show currency indicator below
        st.caption(f"Currency: {CURRENCY}")
    
    with col_f2:
        min_orders = st.number_input(
            "Min Orders:",
            min_value=1,
            value=1,
            step=1
        )
    
    with col_f3:
        max_days_inactive = st.slider(
            "Max Days Inactive:",
            min_value=0,
            max_value=int(company_metrics['Days_Since_Last_Order'].max()),
            value=int(company_metrics['Days_Since_Last_Order'].max())
        )
    
    with col_f4:
        selected_segments = st.multiselect(
            "Customer Segments:",
            options=sorted(company_metrics['Customer_Segment'].unique()),
            default=sorted(company_metrics['Customer_Segment'].unique())
        )
    
    # Apply filters
    display_df = filtered_metrics[
        (filtered_metrics['Total_Revenue'] >= min_revenue) &
        (filtered_metrics['Total_Orders'] >= min_orders) &
        (filtered_metrics['Days_Since_Last_Order'] <= max_days_inactive) &
        (filtered_metrics['Customer_Segment'].isin(selected_segments))
    ].copy()
    
    # Sort based on segmentation selection
    if segmentation == "Revenue":
        display_df = display_df.sort_values('Total_Revenue', ascending=False)
    elif segmentation == "Order Frequency":
        display_df = display_df.sort_values('Order_Frequency', ascending=False)
    elif segmentation == "Order Value":
        display_df = display_df.sort_values('Avg_Order_Value', ascending=False)
    else:
        display_df['Growth_Score'] = (
            display_df['Frequency_Score'] + 
            display_df['Monetary_Score'] - 
            (5 - display_df['Recency_Score'])
        )
        display_df = display_df.sort_values('Growth_Score', ascending=False)
    
    # KPI Cards
    st.markdown("---")
    st.markdown(f"### 📊 Overview{period_label}")
    
    col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)
    
    with col_kpi1:
        st.metric("Total Companies", f"{len(display_df):,}")
    
    with col_kpi2:
        total_revenue = display_df['Total_Revenue'].sum()
        st.metric("Total Revenue", f"{CURRENCY}{total_revenue:,.0f}")
    
    with col_kpi3:
        total_orders = display_df['Total_Orders'].sum()
        st.metric("Total Orders", f"{total_orders:,}")
    
    with col_kpi4:
        avg_order_value = display_df['Avg_Order_Value'].mean()
        st.metric("Avg Order Value", f"{CURRENCY}{avg_order_value:,.0f}")
    
    with col_kpi5:
        avg_recency = display_df['Days_Since_Last_Order'].mean()
        st.metric("Avg Days Inactive", f"{avg_recency:.0f}")
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏆 Company Rankings", 
        "📈 Visual Analytics", 
        "🎯 Segment Analysis", 
        "📋 Detailed Profiles"
    ])
    
    with tab1:
        st.markdown(f"#### Top Companies by {segmentation}")
        
        top_50 = display_df.head(50).copy()
        
        display_table = top_50[[
            'Customer_Segment', 'Total_Revenue', 'Total_Orders', 
            'Avg_Order_Value', 'Total_Qty', 'Days_Since_Last_Order',
            'Order_Frequency', 'Unique_Products', 'Primary_State'
        ]].copy()
        
        display_table['Total_Revenue'] = display_table['Total_Revenue'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        display_table['Avg_Order_Value'] = display_table['Avg_Order_Value'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        display_table['Order_Frequency'] = display_table['Order_Frequency'].apply(lambda x: f"{x:.1f}/month")
        display_table['Days_Since_Last_Order'] = display_table['Days_Since_Last_Order'].apply(
            lambda x: f"{x} days" if x <= 30 else f"⚠️ {x} days" if x <= 90 else f"🔴 {x} days"
        )
        
        def highlight_segment(val):
            if 'Champion' in val:
                return 'background-color: gold; color: black; font-weight: bold'
            elif 'Loyal' in val:
                return 'background-color: silver; color: black'
            elif 'At Risk' in val:
                return 'background-color: #ff6b6b; color: white'
            elif 'Hibernating' in val:
                return 'background-color: #4ecdc4; color: white'
            return ''
        
        st.dataframe(
            display_table.style.applymap(highlight_segment, subset=['Customer_Segment']),
            use_container_width=True,
            height=600
        )
        
        col_exp1, col_exp2 = st.columns([4, 1])
        with col_exp2:
            csv = top_50.to_csv().encode('utf-8')
            st.download_button(
                "📥 Export",
                csv,
                f"company_analysis_{year_option.replace(' ', '_')}.csv",
                "text/csv"
            )
    
    with tab2:
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            st.markdown("#### 💰 Revenue vs Orders Scatter")
            
            fig_scatter = px.scatter(
                display_df.reset_index().head(100),
                x='Total_Orders',
                y='Total_Revenue',
                size='Total_Qty',
                color='Customer_Segment',
                hover_name='Company',
                hover_data=['Avg_Order_Value', 'Days_Since_Last_Order'],
                title="Customer Segmentation Map",
                template='plotly_white',
                height=500
            )
            
            fig_scatter.update_traces(
                marker=dict(line=dict(width=1, color='DarkSlateGrey')),
                selector=dict(mode='markers')
            )
            
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with col_viz2:
            st.markdown("#### 📊 Customer Segment Distribution")
            
            segment_counts = display_df['Customer_Segment'].value_counts().reset_index()
            segment_counts.columns = ['Segment', 'Count']
            
            fig_pie = px.pie(
                segment_counts,
                values='Count',
                names='Segment',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Set3,
                title="Segment Breakdown"
            )
            
            fig_pie.update_traces(
                textposition='outside',
                textinfo='percent+label',
                pull=[0.05 if 'Champion' in seg or 'At Risk' in seg else 0 for seg in segment_counts['Segment']]
            )
            
            fig_pie.update_layout(height=500, template='plotly_white', showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("#### 📈 Pareto Analysis (80/20 Rule)")
        
        pareto_df = display_df.sort_values('Total_Revenue', ascending=False).copy()
        pareto_df['Cumulative_Revenue'] = pareto_df['Total_Revenue'].cumsum()
        pareto_df['Cumulative_Percentage'] = (
            pareto_df['Cumulative_Revenue'] / pareto_df['Total_Revenue'].sum() * 100
        )
        
        fig_pareto = go.Figure()
        
        fig_pareto.add_trace(go.Bar(
            x=list(range(min(20, len(pareto_df)))),
            y=pareto_df.head(20)['Total_Revenue'],
            name='Revenue',
            marker_color='royalblue',
            text=pareto_df.head(20)['Total_Revenue'].apply(lambda x: f'{CURRENCY}{x/1000:.0f}K'),
            textposition='auto'
        ))
        
        fig_pareto.add_trace(go.Scatter(
            x=list(range(min(20, len(pareto_df)))),
            y=pareto_df.head(20)['Cumulative_Percentage'],
            name='Cumulative %',
            yaxis='y2',
            line=dict(color='red', width=3),
            marker=dict(size=8)
        ))
        
        fig_pareto.add_hline(y=80, line_dash="dash", line_color="green", 
                            annotation_text="80% Line", yref='y2')
        
        fig_pareto.update_layout(
            title="Top 20 Companies - Pareto Analysis",
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(min(20, len(pareto_df)))),
                ticktext=[c[:10] + "..." if len(c) > 10 else c for c in pareto_df.head(20).index],
                tickangle=-45
            ),
            yaxis=dict(title='Revenue', side='left'),
            yaxis2=dict(
                title='Cumulative %',
                side='right',
                overlaying='y',
                range=[0, 100],
                ticksuffix='%'
            ),
            height=450,
            template='plotly_white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02)
        )
        
        st.plotly_chart(fig_pareto, use_container_width=True)
        
        top_80 = pareto_df[pareto_df['Cumulative_Percentage'] <= 80]
        if not top_80.empty:
            st.success(f"🎯 **80/20 Insight:** Top {len(top_80)} companies ({len(top_80)/len(pareto_df)*100:.1f}%) "
                      f"generate 80% of total revenue ({CURRENCY}{pareto_df['Total_Revenue'].sum()*0.8:,.0f})")
    
    with tab3:
        st.markdown("#### 🎯 Segment Deep Dive")
        
        segment_analysis = display_df.groupby('Customer_Segment').agg({
            'Total_Revenue': ['sum', 'mean', 'count'],
            'Total_Orders': ['sum', 'mean'],
            'Avg_Order_Value': 'mean',
            'Days_Since_Last_Order': 'mean',
            'Order_Frequency': 'mean'
        }).round(2)
        
        segment_analysis.columns = [
            'Total_Revenue', 'Avg_Revenue', 'Company_Count',
            'Total_Orders', 'Avg_Orders_Per_Company',
            'Avg_Order_Value', 'Avg_Days_Inactive', 'Avg_Frequency_Per_Month'
        ]
        
        segment_analysis['Revenue_Share'] = (
            segment_analysis['Total_Revenue'] / segment_analysis['Total_Revenue'].sum() * 100
        ).round(1)
        
        segment_analysis = segment_analysis.sort_values('Total_Revenue', ascending=False)
        
        display_segment = segment_analysis.copy()
        display_segment['Total_Revenue'] = display_segment['Total_Revenue'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        display_segment['Avg_Revenue'] = display_segment['Avg_Revenue'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        display_segment['Avg_Order_Value'] = display_segment['Avg_Order_Value'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
        display_segment['Revenue_Share'] = display_segment['Revenue_Share'].apply(lambda x: f"{x}%")
        display_segment['Avg_Frequency_Per_Month'] = display_segment['Avg_Frequency_Per_Month'].apply(lambda x: f"{x:.1f}")
        
        st.dataframe(display_segment, use_container_width=True)
        
        st.markdown("#### 💡 Strategic Recommendations")
        
        recommendations = {
            '💎 Champion': "Reward them. Early adopter of new products. Will promote brand.",
            '🥇 Loyal Customer': "Upsell higher value products. Ask for reviews/referrals.",
            '📈 Potential Loyalist': "Offer membership/loyalty program. Keep engaged.",
            '🆕 New Customer': "Provide onboarding support. Early stage of relationship.",
            '⚠️ At Risk': "Send personalized reactivation campaigns. Special offers.",
            '😴 Hibernating': "Offer win-back deals. Survey to understand needs.",
            '📊 Needs Attention': "Don't lose them. Monitor for at-risk signals."
        }
        
        for segment, rec in recommendations.items():
            if segment in display_df['Customer_Segment'].values:
                with st.container():
                    col_seg, col_rec = st.columns([1, 3])
                    with col_seg:
                        st.markdown(f"**{segment}**")
                    with col_rec:
                        st.info(rec)
    
    with tab4:
        st.markdown("#### 📋 Individual Company Profile")
        
        selected_company = st.selectbox(
            "Select Company to View Profile:",
            options=display_df.index.tolist(),
            index=0 if len(display_df) > 0 else None
        )
        
        if selected_company:
            company_data = display_df.loc[selected_company]
            company_transactions = analysis_df[analysis_df['Company'] == selected_company].copy()
            
            col_prof1, col_prof2, col_prof3 = st.columns([2, 2, 1])
            
            with col_prof1:
                st.markdown(f"### 🏢 {selected_company}")
                st.caption(f"Primary State: {company_data['Primary_State']}")
                st.caption(f"Customer Since: {pd.to_datetime(company_data['First_Order']).strftime('%b %Y')}")
            
            with col_prof2:
                segment = company_data['Customer_Segment']
                st.markdown(f"**Segment:** {segment}")
                
                rfm_score = int(company_data['Recency_Score']) + int(company_data['Frequency_Score']) + int(company_data['Monetary_Score'])
                st.progress(rfm_score / 15, text=f"RFM Score: {rfm_score}/15")
            
            with col_prof3:
                st.metric("Total Revenue", f"{CURRENCY}{company_data['Total_Revenue']:,.0f}")
                st.metric("Total Orders", f"{int(company_data['Total_Orders'])}")
            
            st.markdown("#### 📜 Transaction History")
            
            trans_display = company_transactions[[
                'Date', 'Inquiry_No', 'Product', 'Qty', 'Total_Amount', 'State'
            ]].sort_values('Date', ascending=False)
            
            trans_display['Date'] = pd.to_datetime(trans_display['Date']).dt.strftime('%Y-%m-%d')
            trans_display['Total_Amount'] = trans_display['Total_Amount'].apply(lambda x: f"{CURRENCY}{x:,.0f}")
            
            st.dataframe(trans_display, use_container_width=True, height=300)
            
            st.markdown("#### 🏷️ Product Preferences")
            
            product_pref = company_transactions.groupby('Product').agg({
                'Total_Amount': 'sum',
                'Qty': 'sum',
                'Inquiry_No': 'count'
            }).rename(columns={'Inquiry_No': 'Orders'}).sort_values('Total_Amount', ascending=False).head(10)
            
            fig_pref = px.bar(
                product_pref.reset_index(),
                x='Total_Amount',
                y='Product',
                orientation='h',
                color='Orders',
                color_continuous_scale='Blues',
                title=f"Top Products for {selected_company}",
                labels={'Total_Amount': f'Revenue ({CURRENCY})'}
            )
            fig_pref.update_layout(height=350, template='plotly_white', yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig_pref, use_container_width=True)
            
            if len(company_transactions) > 1:
                st.markdown("#### 📈 Purchase Trend")
                
                monthly_company = company_transactions.groupby(
                    company_transactions['Date'].dt.to_period('M')
                )['Total_Amount'].sum().reset_index()
                monthly_company['Date'] = monthly_company['Date'].dt.to_timestamp()
                
                fig_trend = px.line(
                    monthly_company,
                    x='Date',
                    y='Total_Amount',
                    markers=True,
                    title="Monthly Purchase History",
                    template='plotly_white'
                )
                fig_trend.update_layout(height=300)
                st.plotly_chart(fig_trend, use_container_width=True)

# ==========================================
# REPORT 14: CUSTOMER SEGMENTATION (ENHANCED WITH LISTS)
# ==========================================
elif report == "🏢 Customer Segmentation":
    st.markdown("## 🏢 Customer Segmentation (ABC Analysis)")
    
    # ABC Analysis
    company_revenue = df.groupby('Company')['Total_Amount'].sum().sort_values(ascending=False)
    total_revenue = company_revenue.sum()
    
    company_revenue_pct = company_revenue / total_revenue * 100
    cumulative_pct = company_revenue_pct.cumsum()
    
    # Classify
    def classify_abc(x):
        if x <= 80:
            return 'A (Top 80%)'
        elif x <= 95:
            return 'B (Next 15%)'
        else:
            return 'C (Bottom 5%)'
    
    abc_classification = cumulative_pct.apply(classify_abc)
    
    abc_summary = pd.DataFrame({
        'Revenue': company_revenue,
        'Cumulative_%': cumulative_pct,
        'Segment': abc_classification
    })
    
    # Select Segment to View (NEW FILTER)
    segment_filter = st.selectbox("📊 Select Segment to View:", ["All Segments", "A (Top 80%)", "B (Next 15%)", "C (Bottom 5%)"])
    
    # Filter and display companies
    if segment_filter != "All Segments":
        filtered_segment = abc_summary[abc_summary['Segment'] == segment_filter]
        st.markdown(f"### 📋 Companies in {segment_filter}")
        st.dataframe(filtered_segment.style.format({
            'Revenue': lambda x: f"{CURRENCY}{x:,.0f}",
            'Cumulative_%': lambda x: f"{x:.2f}%"
        }), use_container_width=True, height=400)
        st.info(f"Total {len(filtered_segment)} companies in {segment_filter}")
    else:
        # Show all segments summary
        col1, col2, col3 = st.columns(3)
        segments = ['A (Top 80%)', 'B (Next 15%)', 'C (Bottom 5%)']
        colors = ['#2ecc71', '#f39c12', '#e74c3c']
        
        for col, segment, color in zip([col1, col2, col3], segments, colors):
            with col:
                count = (abc_classification == segment).sum()
                revenue = company_revenue[abc_classification == segment].sum()
                st.markdown(f"<div style='background-color:{color}; padding:20px; border-radius:10px; color:white; text-align:center;'>"
                           f"<h3>{segment}</h3>"
                           f"<h2>{count}</h2><p>Companies</p>"
                           f"<h4>{CURRENCY}{revenue:,.0f}</h4></div>", 
                           unsafe_allow_html=True)
        
        # Show lists for each segment
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 🟢 A Segment Companies (Top)")
            a_companies = abc_summary[abc_summary['Segment'] == 'A (Top 80%)'].head(10)
            for idx, (company, row) in enumerate(a_companies.iterrows(), 1):
                st.write(f"{idx}. **{company}** - {CURRENCY}{row['Revenue']:,.0f}")
        
        with col2:
            st.markdown("### 🟡 B Segment Companies")
            b_companies = abc_summary[abc_summary['Segment'] == 'B (Next 15%)'].head(10)
            for idx, (company, row) in enumerate(b_companies.iterrows(), 1):
                st.write(f"{idx}. **{company}** - {CURRENCY}{row['Revenue']:,.0f}")
        
        with col3:
            st.markdown("### 🔴 C Segment Companies")
            c_companies = abc_summary[abc_summary['Segment'] == 'C (Bottom 5%)'].head(10)
            for idx, (company, row) in enumerate(c_companies.iterrows(), 1):
                st.write(f"{idx}. **{company}** - {CURRENCY}{row['Revenue']:,.0f}")

# ==========================================
# REPORT 15: LEAD TIME ANALYSIS (NO CHARTS - NUMBERS ONLY)
# ==========================================
elif report == "⚡ Lead Time Analysis":
    st.markdown("## ⚡ Production & Delivery Lead Time Analysis")
    
    # Calculate lead time stats
    df['Lead_Time_Days'] = (df['EDD'] - df['Date']).dt.days
    
    # Filter valid lead times
    valid_lead = df[(df['Lead_Time_Days'] > 0) & (df['Lead_Time_Days'] < 365)]
    
    if not valid_lead.empty:
        # Overall Statistics (NO CHARTS)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("⏱️ Average Lead Time", f"{valid_lead['Lead_Time_Days'].mean():.1f} days")
        with col2:
            st.metric("⚡ Fastest Delivery", f"{valid_lead['Lead_Time_Days'].min()} days")
        with col3:
            st.metric("🐌 Slowest Delivery", f"{valid_lead['Lead_Time_Days'].max()} days")
        with col4:
            st.metric("📊 Median Lead Time", f"{valid_lead['Lead_Time_Days'].median():.1f} days")
        
        st.markdown("---")
        
        # Lead Time by Product (TABLE ONLY - NO GRAPHS)
        st.markdown("### ⏱️ Lead Time by Product (Numbers Only)")
        lead_by_product = valid_lead.groupby('Product')['Lead_Time_Days'].agg(['mean', 'min', 'max', 'count']).round(1)
        lead_by_product.columns = ['Avg_Days', 'Min_Days', 'Max_Days', 'Order_Count']
        lead_by_product = lead_by_product.sort_values('Avg_Days', ascending=False)
        
        # Add interpretation
        lead_by_product['Interpretation'] = lead_by_product['Avg_Days'].apply(
            lambda x: '🔴 Long Time' if x > 30 else ('🟡 Medium' if x > 15 else '🟢 Fast')
        )
        
        st.dataframe(lead_by_product, use_container_width=True)
        
        # Products that take MORE TIME (Text Analysis)
        st.markdown("---")
        st.markdown("### 🐌 Products with Longest Lead Time")
        slow_products = lead_by_product.head(5)
        for idx, (product, row) in enumerate(slow_products.iterrows(), 1):
            st.write(f"{idx}. **{product}** - Avg: **{row['Avg_Days']:.1f} days** "
                    f"(Range: {row['Min_Days']:.0f} to {row['Max_Days']:.0f} days)")
        
        st.markdown("### ⚡ Products with Fastest Delivery")
        fast_products = lead_by_product.tail(5)
        for idx, (product, row) in enumerate(fast_products.iterrows(), 1):
            st.write(f"{idx}. **{product}** - Avg: **{row['Avg_Days']:.1f} days**")
    else:
        st.warning("No valid lead time data available (check EDD dates format in your sheet)")

# ==========================================
# REPORT: RAW DATA EXPLORER (ENHANCED)
# ==========================================
elif report == "📋 Raw Data Explorer":
    st.markdown("## 📋 Interactive Data Explorer")
    st.markdown("---")
    
    # Data integrity check section
    with st.expander("🔍 Data Integrity Status", expanded=False):
        col_check1, col_check2, col_check3 = st.columns(3)
        
        with col_check1:
            total_records_source = len(df)
            st.metric("Total Records in DataFrame", f"{total_records_source:,}")
        
        with col_check2:
            # Check for duplicates
            duplicate_count = df.duplicated().sum()
            st.metric("Duplicate Rows", f"{duplicate_count:,}", 
                     delta=None if duplicate_count == 0 else "Check data")
        
        with col_check3:
            # Check for null values in key columns
            null_counts = df[['Inquiry_No', 'Date', 'State', 'Product']].isnull().sum().sum()
            st.metric("Missing Values (Key Columns)", f"{null_counts:,}",
                     delta=None if null_counts == 0 else "Data Quality Issue")
        
        # Show data range info
        st.caption(f"📅 Date Range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")
        st.caption(f"🗺️ Unique States: {df['State'].nunique()} | 🏷️ Unique Products: {df['Product'].nunique()}")
        
        # Show last few records to verify data loading
        with st.container():
            st.markdown("**📝 Last 5 Records (Verification):**")
            st.dataframe(df.tail(5), use_container_width=True, height=200)
    
    # Advanced filters
    with st.expander("🔍 Advanced Filters", expanded=True):
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        
        with col1:
            # Add "Select All" option for states
            all_states = sorted(df['State'].unique())
            select_all_states = st.checkbox("Select All States", value=True, key="select_all_states")
            if select_all_states:
                f_states = st.multiselect("States:", all_states, default=all_states, key="states_multiselect")
            else:
                f_states = st.multiselect("States:", all_states, default=[], key="states_multiselect")
        
        with col2:
            # Add "Select All" option for products
            all_products = sorted(df['Product'].unique())
            select_all_products = st.checkbox("Select All Products", value=True, key="select_all_products")
            if select_all_products:
                f_products = st.multiselect("Products:", all_products, default=all_products[:50], key="products_multiselect")  # Limit default to prevent lag
            else:
                f_products = st.multiselect("Products:", all_products, default=[], key="products_multiselect")
        
        with col3:
            # Better date range handling
            min_date = df['Date'].min().date()
            max_date = df['Date'].max().date()
            date_range = st.date_input(
                "Date Range:", 
                [min_date, max_date],
                min_value=min_date,
                max_value=max_date
            )
        
        with col4:
            st.markdown("<br>", unsafe_allow_html=True)
            reset_filters = st.button("🔄 Reset", use_container_width=True)
            if reset_filters:
                st.rerun()
    
    # Apply filters with validation
    filtered = df.copy()
    filter_log = []
    
    if f_states:
        filtered = filtered[filtered['State'].isin(f_states)]
        filter_log.append(f"States: {len(f_states)} selected")
    
    if f_products:
        filtered = filtered[filtered['Product'].isin(f_products)]
        filter_log.append(f"Products: {len(f_products)} selected")
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        # Ensure we capture the full end date (up to 23:59:59)
        start_timestamp = pd.Timestamp(start_date)
        end_timestamp = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
        
        filtered = filtered[(filtered['Date'] >= start_timestamp) & 
                           (filtered['Date'] <= end_timestamp)]
        filter_log.append(f"Date: {start_date} to {end_date}")
    
    # Display filter summary
    st.markdown("---")
    col_summary1, col_summary2, col_summary3 = st.columns([2, 2, 1])
    
    with col_summary1:
        st.markdown(f"**📊 Showing {len(filtered):,} of {len(df):,} records**")
        if filter_log:
            st.caption(" | ".join(filter_log))
    
    with col_summary2:
        # Pagination info
        if len(filtered) > 0:
            st.caption(f"💾 Memory Usage: ~{filtered.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    with col_summary3:
        # Export button
        if len(filtered) > 0:
            csv = filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export CSV",
                data=csv,
                file_name=f'raw_data_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv',
                use_container_width=True
            )
    
    # Data display with guaranteed full dataset visibility
    if len(filtered) == 0:
        st.warning("⚠️ No records match the selected filters. Please adjust your criteria.")
    else:
        # Show data with pagination options
        st.markdown("### 📋 Data Table")
        
        # Option to show all or paginated
        show_option = st.radio(
            "Display Mode:",
            ["Show All (Up to 1000 rows)", "Paginated View"],
            horizontal=True,
            key="display_mode"
        )
        
        if show_option == "Show All (Up to 1000 rows)" and len(filtered) <= 1000:
            display_df = filtered
            height_setting = min(800, 40 + (len(display_df) * 35))  # Dynamic height
        else:
            # Paginated view
            rows_per_page = st.selectbox("Rows per page:", [10, 25, 50, 100, 200], index=2)
            total_pages = max(1, (len(filtered) + rows_per_page - 1) // rows_per_page)
            
            col_page1, col_page2, col_page3 = st.columns([1, 2, 1])
            with col_page2:
                current_page = st.number_input(
                    f"Page (of {total_pages}):", 
                    min_value=1, 
                    max_value=total_pages, 
                    value=1
                )
            
            start_idx = (current_page - 1) * rows_per_page
            end_idx = min(start_idx + rows_per_page, len(filtered))
            display_df = filtered.iloc[start_idx:end_idx]
            
            st.caption(f"Showing rows {start_idx + 1} to {end_idx} of {len(filtered)}")
            height_setting = min(600, 40 + (len(display_df) * 35))
        
        # Display the dataframe with full configuration
        st.dataframe(
            display_df,
            use_container_width=True,
            height=int(height_setting),
            column_config={
                "Date": st.column_config.DateColumn(
                    "Date",
                    format="YYYY-MM-DD",
                    help="Order date"
                ),
                "Total_Amount": st.column_config.NumberColumn(
                    f"Amount ({CURRENCY})",
                    format=f"{CURRENCY}%.2f",
                    help="Total order amount"
                ),
                "Qty": st.column_config.NumberColumn(
                    "Quantity",
                    format="%d",
                    help="Quantity ordered"
                ),
                "Inquiry_No": st.column_config.TextColumn(
                    "Inquiry #",
                    help="Unique inquiry number"
                ),
                "State": st.column_config.TextColumn(
                    "State",
                    help="Customer state"
                ),
                "Product": st.column_config.TextColumn(
                    "Product",
                    help="Product name",
                    width="large"
                )
            },
            hide_index=False  # Show index to verify row count
        )
        
        # Row index verification
        st.caption(f"🔢 Row Indices: {display_df.index.min()} to {display_df.index.max()} "
                  f"(Total: {len(display_df)} rows)")
        
        # Show last row details to verify data completeness
        with st.expander("🔍 Verify Last Record"):
            if len(filtered) > 0:
                last_record = filtered.iloc[-1]
                st.json(last_record.to_dict())
                st.caption(f"Index position: {filtered.index[-1]}")
    
    # Data statistics
    with st.expander("📊 Quick Statistics"):
        if len(filtered) > 0:
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                st.metric("Total Revenue", f"{CURRENCY}{filtered['Total_Amount'].sum():,.2f}")
                st.metric("Avg Order Value", f"{CURRENCY}{filtered['Total_Amount'].mean():,.2f}")
            
            with col_stat2:
                st.metric("Total Quantity", f"{filtered['Qty'].sum():,}")
                st.metric("Avg Quantity", f"{filtered['Qty'].mean():.2f}")
            
            with col_stat3:
                st.metric("Unique Orders", f"{filtered['Inquiry_No'].nunique():,}")
                st.metric("Date Range", f"{(filtered['Date'].max() - filtered['Date'].min()).days} days")

# Global Footer - FIXED to show accurate count
st.sidebar.markdown("---")
st.sidebar.caption(f"🔄 Auto-refresh: 5 min | 📊 Total Records: {len(df):,}")

# Additional verification in sidebar
with st.sidebar.expander("🔍 Data Verification"):
    st.write(f"DataFrame Shape: {df.shape}")
    st.write(f"Index Range: {df.index.min()} to {df.index.max()}")
    st.write(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    if st.button("🔄 Force Reload Data"):
        st.cache_data.clear()
        st.rerun()
