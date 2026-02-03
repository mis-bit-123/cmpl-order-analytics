import streamlit as st
import gspread
from google.oauth2 import service_account
import pandas as pd

class OrderDataLoader:
    def __init__(self):
        # Safely get SHEET_ID with fallback
        try:
            self.sheet_id = st.secrets["SHEET_ID"]
        except Exception as e:
            st.error("❌ SHEET_ID not found in secrets!")
            st.info("💡 Local: Create .streamlit/secrets.toml | Cloud: Add in Settings")
            self.sheet_id = None
    
    def get_credentials(self):
        """Get credentials from Streamlit Secrets"""
        try:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]
            
            creds_dict = {
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
            
            return service_account.Credentials.from_service_account_info(creds_dict, scopes=scopes)
            
        except Exception as e:
            st.error(f"❌ Failed to load credentials: {e}")
            return None
    
    def fetch_data(self):
        if not self.sheet_id:
            return pd.DataFrame()
            
        creds = self.get_credentials()
        if not creds:
            return pd.DataFrame()
        
        try:
            client = gspread.authorize(creds)
            spreadsheet = client.open_by_key(self.sheet_id)
            worksheet = spreadsheet.sheet1
            data = worksheet.get_all_records()
            
            if not data:
                st.warning("⚠️ Sheet is empty")
                return pd.DataFrame()
            
            df = pd.DataFrame(data)
            
            # Process data
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce')
                df['Year'] = df['Date'].dt.year
                df['Month'] = df['Date'].dt.month
                df['Month_Name'] = df['Date'].dt.strftime('%B')
            
            return df
            
        except gspread.exceptions.SpreadsheetNotFound:
            st.error("❌ Spreadsheet not found!")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"❌ Error: {e}")
            return pd.DataFrame()