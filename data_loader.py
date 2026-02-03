import streamlit as st
import gspread
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime
import json

class OrderDataLoader:
    def __init__(self):
        # Get Sheet ID from secrets or config
        try:
            self.sheet_id = st.secrets["SHEET_ID"]
        except:
            # Fallback to hardcoded or config
            self.sheet_id = "your-default-sheet-id-here"  # Replace with your actual sheet ID
    
    def get_credentials(self):
        """Get credentials from Streamlit Secrets"""
        try:
            # Load from Streamlit Cloud Secrets
            credentials_dict = {
                "type": st.secrets["gcp_service_account"]["type"],
                "project_id": st.secrets["gcp_service_account"]["project_id"],
                "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
                "private_key": st.secrets["gcp_service_account"]["private_key"],
                "client_email": st.secrets["gcp_service_account"]["client_email"],
                "client_id": st.secrets["gcp_service_account"]["client_id"],
                "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
                "token_uri": st.secrets["gcp_service_account"]["token_uri"],
                "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
                "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"],
                "universe_domain": st.secrets["gcp_service_account"]["universe_domain"]
            }
            creds = service_account.Credentials.from_service_account_info(credentials_dict)
            return creds
        except Exception as e:
            st.error(f"❌ Failed to load credentials from secrets: {str(e)}")
            st.info("💡 Make sure you've added secrets in Streamlit Cloud settings!")
            return None
    
    def fetch_data(self):
        """Fetch data from Google Sheets"""
        creds = self.get_credentials()
        if creds is None:
            return pd.DataFrame()
        
        try:
            client = gspread.authorize(creds)
            sheet = client.open_by_key(self.sheet_id)
            worksheet = sheet.get_worksheet(0)
            data = worksheet.get_all_records()
            
            df = pd.DataFrame(data)
            
            # Process your data (adjust column names as per your sheet)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                df['Year'] = df['Date'].dt.year
                df['Month'] = df['Date'].dt.month
                df['Month_Name'] = df['Date'].dt.strftime('%B')
            
            # Ensure numeric columns
            numeric_cols = ['Qty', 'Total_Amount', 'Unit_Price']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # Ensure EDD column exists for lead time analysis
            if 'EDD' in df.columns:
                df['EDD'] = pd.to_datetime(df['EDD'], errors='coerce')
            
            return df
            
        except Exception as e:
            st.error(f"❌ Error fetching data: {str(e)}")
            return pd.DataFrame()
    
    def get_stats(self, df):
        """Calculate statistics"""
        if df.empty:
            return {
                'total_orders': 0,
                'total_revenue': 0,
                'total_qty': 0,
                'avg_order_value': 0
            }
        
        return {
            'total_orders': len(df),
            'total_revenue': df['Total_Amount'].sum() if 'Total_Amount' in df.columns else 0,
            'total_qty': df['Qty'].sum() if 'Qty' in df.columns else 0,
            'avg_order_value': df['Total_Amount'].mean() if 'Total_Amount' in df.columns else 0
        }