import streamlit as st
import gspread
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import pandas as pd
from datetime import datetime

class OrderDataLoader:
    def __init__(self):
        # Get Sheet ID from secrets
        try:
            self.sheet_id = st.secrets["SHEET_ID"]
        except:
            self.sheet_id = "your-default-sheet-id-here"
    
    def get_credentials(self):
        """Get credentials from Streamlit Secrets with proper scopes"""
        try:
            # Define required scopes for Google Sheets
            SCOPES = [
                'https://www.googleapis.com/auth/spreadsheets.readonly',
                'https://www.googleapis.com/auth/drive.readonly'
            ]
            
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
            
            # Create credentials with scopes
            creds = service_account.Credentials.from_service_account_info(
                credentials_dict,
                scopes=SCOPES
            )
            
            # Refresh token
            creds.refresh(Request())
            
            return creds
            
        except Exception as e:
            st.error(f"❌ Credentials error: {str(e)}")
            return None
    
    def fetch_data(self):
        """Fetch data from Google Sheets"""
        creds = self.get_credentials()
        if creds is None:
            return pd.DataFrame()
        
        try:
            # Authorize gspread with credentials
            client = gspread.authorize(creds)
            
            # Open sheet by key
            spreadsheet = client.open_by_key(self.sheet_id)
            worksheet = spreadsheet.sheet1  # First worksheet
            
            # Get all records
            data = worksheet.get_all_records()
            
            if not data:
                st.warning("⚠️ Sheet is empty")
                return pd.DataFrame()
            
            df = pd.DataFrame(data)
            
            # Process data (adjust column names as per your sheet)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
                df['Year'] = df['Date'].dt.year
                df['Month'] = df['Date'].dt.month
                df['Month_Name'] = df['Date'].dt.strftime('%B')
            
            # Ensure numeric columns
            numeric_cols = ['Qty', 'Total_Amount', 'Unit_Price', 'Quantity']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            # EDD column for lead time
            if 'EDD' in df.columns:
                df['EDD'] = pd.to_datetime(df['EDD'], dayfirst=True, errors='coerce')
            
            # State and Product columns
            if 'State' in df.columns:
                df['State'] = df['State'].astype(str).str.strip()
            if 'Product' in df.columns:
                df['Product'] = df['Product'].astype(str).str.strip()
            if 'Company' in df.columns:
                df['Company'] = df['Company'].astype(str).str.strip()
            
            return df
            
        except gspread.exceptions.SpreadsheetNotFound:
            st.error("❌ Spreadsheet not found! Check SHEET_ID in secrets.")
            return pd.DataFrame()
        except gspread.exceptions.WorksheetNotFound:
            st.error("❌ Worksheet not found! Check if sheet has data.")
            return pd.DataFrame()
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