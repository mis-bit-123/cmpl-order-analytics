# import gspread
# from google.oauth2.service_account import Credentials
# import pandas as pd
# import numpy as np
# import streamlit as st
# from config import SHEET_ID, SHEET_NAME, CREDENTIALS_FILE

# class OrderDataLoader:
#     def __init__(self):
#         self.df = None
        
#     def connect(self):
#         """Connect to Google Sheets"""
#         try:
#             scope = [
#                 'https://spreadsheets.google.com/feeds',
#                 'https://www.googleapis.com/auth/drive'
#             ]
#             creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=scope)
#             client = gspread.authorize(creds)
#             return client
#         except Exception as e:
#             st.error(f"Connection Error: {e}")
#             return None
    
#     @st.cache_data(ttl=300)
#     def fetch_data(_self):
#         """Fetch data from Google Sheet"""
#         try:
#             client = _self.connect()
#             if not client:
#                 return None
                
#             sheet = client.open_by_key(SHEET_ID)
#             worksheet = sheet.worksheet(SHEET_NAME)
            
#             # Get all values
#             all_values = worksheet.get_all_values()
#             data_rows = all_values[1:]  # Skip header
            
#             # Extract columns: A=0, B=1, D=3, G=6, H=7, I=8, O=14, S=18
#             processed_data = []
#             for row in data_rows:
#                 if len(row) >= 19:
#                     try:
#                         processed_data.append({
#                             'Date': row[0],           # A: Timestamp
#                             'Inquiry_No': row[1],     # B: Inquiry No
#                             'Company': row[3],        # D: Company Name
#                             'Product': row[6],        # G: Product Description
#                             'Qty': row[7],            # H: Quantity
#                             'State': row[9],          # I: State
#                             'Total_Amount': row[14],  # O: Total Amount
#                             'EDD': row[18]            # S: Delivery Date
#                         })
#                     except:
#                         continue
            
#             df = pd.DataFrame(processed_data)
#             df = _self.clean_data(df)
#             return df
            
#         except Exception as e:
#             st.error(f"Data Fetch Error: {e}")
#             return None
    
#     def clean_data(self, df):
#         """Clean and format data"""
#         if df.empty:
#             return df
            
#         # Clean Date
#         df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)
        
#         # Clean Amount (remove ₹ and commas)
#         df['Total_Amount'] = df['Total_Amount'].astype(str).str.replace(r'[₹,]', '', regex=True)
#         df['Total_Amount'] = pd.to_numeric(df['Total_Amount'], errors='coerce')
        
#         # Clean Quantity
#         df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(1)
        
#         # Clean State
#         df['State'] = df['State'].str.strip().str.title()
#         df['State'] = df['State'].replace({'N/A': 'Not Specified', 'Na': 'Not Specified'})
        
#         # Clean Product & Company
#         df['Product'] = df['Product'].str.strip()
#         df['Company'] = df['Company'].str.strip().str.title()
        
#         # Process EDD
#         df['EDD'] = pd.to_datetime(df['EDD'], errors='coerce', dayfirst=True)
#         df['Lead_Time_Days'] = (df['EDD'] - df['Date']).dt.days
        
#         # Add derived columns
#         df['Year'] = df['Date'].dt.year
#         df['Month'] = df['Date'].dt.month
#         df['Month_Name'] = df['Date'].dt.month_name()
        
#         # Remove invalid rows
#         df = df.dropna(subset=['Date', 'Total_Amount'])
        
#         return df
    
#     def get_stats(self, df):
#         """Calculate summary statistics"""
#         if df is None or df.empty:
#             return {}
            
#         return {
#             'total_orders': len(df),
#             'total_revenue': df['Total_Amount'].sum(),
#             'total_qty': df['Qty'].sum(),
#             'avg_order': df['Total_Amount'].mean(),
#             'top_state': df.groupby('State')['Total_Amount'].sum().idxmax() if not df.empty else "N/A",
#             'date_range': {
#                 'start': df['Date'].min(),
#                 'end': df['Date'].max()
#             }
# 
# 
# 
# 
# 
#         }



import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from config import SHEET_NAME, SHEET_ID

class OrderDataLoader:
    def __init__(self):
        # 1. Define the REQUIRED scopes for Google Sheets and Drive
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        try:
            # 2. Check for Streamlit Cloud Secrets
            if "gcp_service_account" in st.secrets:
                creds_info = st.secrets["gcp_service_account"]
                self.creds = Credentials.from_service_account_info(
                    creds_info, 
                    scopes=self.scope
                )
                self.sheet_id = st.secrets.get("SHEET_ID", SHEET_ID)
            
            # 3. Fallback to Local JSON
            else:
                self.creds = Credentials.from_service_account_file(
                    "credentials/service_account.json", 
                    scopes=self.scope
                )
                self.sheet_id = SHEET_ID
            
            self.client = gspread.authorize(self.creds)
            
        except Exception as e:
            st.error(f"❌ Connection Setup Failed: {e}")
            self.client = None

    @st.cache_data(ttl=300)
    def fetch_data(_self):
        if not _self.client:
            return None
        try:
            sheet = _self.client.open_by_key(_self.sheet_id).worksheet(SHEET_NAME)
            
            # Use get_all_values to avoid the "duplicate header" crash
            all_values = sheet.get_all_values()
            if not all_values:
                return pd.DataFrame()

            # Clean headers (handles empty or duplicate names)
            raw_headers = all_values[0]
            clean_headers = []
            for i, h in enumerate(raw_headers):
                h_str = str(h).strip()
                if h_str == "" or h_str in clean_headers:
                    clean_headers.append(f"Column_{i}")
                else:
                    clean_headers.append(h_str)

            # Create DataFrame from the remaining rows
            df = pd.DataFrame(all_values[1:], columns=clean_headers)
            
            # Convert types (since get_all_values imports everything as text)
            if not df.empty:
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                    df['Year'] = df['Date'].dt.year.fillna(0).astype(int)
                    df['Month_Name'] = df['Date'].dt.strftime('%B').fillna('Unknown')
                
                # Convert Numeric Columns
                for col in ['Qty', 'Total_Amount', 'Rate']:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
            return df
            
        except Exception as e:
            st.error(f"❌ Fetch Error: {e}")
            return None

    def get_stats(self, df):
        """Calculates basic KPIs for the sidebar and dashboard."""
        if df is None or df.empty:
            return {"total_rev": 0, "total_qty": 0, "avg_order": 0}
        
        return {
            "total_rev": df['Total_Amount'].sum(),
            "total_qty": df['Qty'].sum(),
            "avg_order": df['Total_Amount'].mean()
        }