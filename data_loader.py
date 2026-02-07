import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import numpy as np
import streamlit as st
from config import SHEET_ID, SHEET_NAME, BRUSH_SHEET_NAME


class OrderDataLoader:
    def __init__(self):
        self.df = None

        # ---- Load Google Service Account secrets from secrets.toml ----
        try:
            service_account_info = st.secrets["google_service_account"]

            # Required Google Scopes
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]

            # Create credentials
            credentials = Credentials.from_service_account_info(
                service_account_info,
                scopes=scopes
            )

            # Authorize Google client
            self.client = gspread.authorize(credentials)

        except Exception as e:
            st.error(f"Authentication Error: {e}")
            self.client = None

    def connect(self):
        """Return authorized client"""
        return self.client

    @st.cache_data(ttl=300)
    def fetch_data(_self):
        """Fetch main sheet data"""
        try:
            client = _self.connect()
            if not client:
                return None

            sheet = client.open_by_key(SHEET_ID)
            worksheet = sheet.worksheet(SHEET_NAME)

            all_values = worksheet.get_all_values()
            rows = all_values[1:]  # Skip header

            processed_data = []
            for row in rows:
                if len(row) >= 19:
                    try:
                        processed_data.append({
                            'Date': row[0],           # A
                            'Inquiry_No': row[1],     # B
                            'Company': row[3],        # D
                            'Client_Name': row[5],    # F
                            'Product': row[6],        # G
                            'Qty': row[7],            # H
                            'City': row[8],           # I
                            'State': row[9],          # J
                            'Total_Amount': row[14],  # O
                            'EDD': row[18]            # S
                        })
                    except:
                        continue

            df = pd.DataFrame(processed_data)
            df = _self.clean_data(df)
            return df

        except Exception as e:
            st.error(f"Data Fetch Error: {e}")
            return None

    def clean_data(self, df):
        """Clean and format data"""
        if df.empty:
            return df

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', dayfirst=True)

        df['Total_Amount'] = (
            df['Total_Amount']
            .astype(str)
            .str.replace(r'[₹,]', '', regex=True)
        )
        df['Total_Amount'] = pd.to_numeric(df['Total_Amount'], errors='coerce')

        df['Qty'] = pd.to_numeric(df['Qty'], errors='coerce').fillna(1)

        df['State'] = (
            df['State']
            .astype(str)
            .str.strip()
            .str.title()
            .replace({'N/A': 'Not Specified', 'Na': 'Not Specified', '': 'Not Specified'})
        )

        df['Product'] = df['Product'].astype(str).str.strip()
        df['Company'] = df['Company'].astype(str).str.strip().str.title()
        df['Client_Name'] = df['Client_Name'].astype(str).str.strip().str.title()

        df['EDD'] = pd.to_datetime(df['EDD'], errors='coerce', dayfirst=True)
        df['Lead_Time_Days'] = (df['EDD'] - df['Date']).dt.days

        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Month_Name'] = df['Date'].dt.month_name()

        df = df.dropna(subset=['Date', 'Total_Amount'])

        return df

    def get_stats(self, df):
        """Summary statistics"""
        if df is None or df.empty:
            return {}

        return {
            'total_orders': len(df),
            'total_revenue': df['Total_Amount'].sum(),
            'total_qty': df['Qty'].sum(),
            'avg_order': df['Total_Amount'].mean(),
            'top_state': df.groupby('State')['Total_Amount'].sum().idxmax()
                           if not df.empty else "N/A",
            'date_range': {
                'start': df['Date'].min(),
                'end': df['Date'].max()
            }
        }

    # ---------------------- BRUSH / SWEEPER / BROOMER LOGIC ----------------------

    def identify_brush_products(self, df):
        """Identify products with keywords"""
        if df is None or df.empty:
            return pd.DataFrame()

        keywords = ['broomer', 'sweeper', 'brush']
        pattern = '|'.join(keywords)

        mask = df['Product'].str.contains(pattern, case=False, na=False)
        return df[mask].copy()

    def calculate_followup_dates(self, brush_df):
        """Add follow-up dates"""
        if brush_df.empty:
            return brush_df

        df = brush_df.copy()
        df['Follow_Up_Date'] = df['Date'] + pd.DateOffset(days=90)
        df['Days_Until_Followup'] = (df['Follow_Up_Date'] - pd.Timestamp.now()).dt.days

        def urgency(days):
            if days < 0:
                return '🔴 Overdue'
            elif days <= 7:
                return '🟠 Due This Week'
            elif days <= 30:
                return '🟡 Due This Month'
            else:
                return '🟢 Future'

        df['Urgency'] = df['Days_Until_Followup'].apply(urgency)
        return df

    def get_brush_summary_stats(self, brush_df):
        """Brush product stats"""
        if brush_df.empty:
            return {}

        upcoming = brush_df[brush_df['Days_Until_Followup'] <= 30]

        return {
            'total_units': len(brush_df),
            'total_revenue': brush_df['Total_Amount'].sum(),
            'unique_companies': brush_df['Company'].nunique(),
            'unique_states': brush_df['State'].nunique(),
            'urgency_counts': brush_df['Urgency'].value_counts().to_dict(),
            'top_products': brush_df['Product'].value_counts().head(5).to_dict(),
            'upcoming_count': len(upcoming),
            'overdue_count': len(brush_df[brush_df['Days_Until_Followup'] < 0])
        }

    def store_to_brush_sheet(self, brush_df):
        """Store brush product results to sheet"""
        try:
            client = self.connect()
            if not client:
                return False, "Connection failed"

            sheet = client.open_by_key(SHEET_ID)

            try:
                worksheet = sheet.worksheet(BRUSH_SHEET_NAME)
                worksheet.clear()
            except gspread.WorksheetNotFound:
                worksheet = sheet.add_worksheet(title=BRUSH_SHEET_NAME, rows=1000, cols=20)

            storage_df = brush_df[[
                'Date', 'Inquiry_No', 'Company', 'Client_Name', 'Product',
                'Qty', 'State', 'City', 'Total_Amount', 'Follow_Up_Date', 'Urgency'
            ]].copy()

            storage_df['Date'] = storage_df['Date'].dt.strftime('%d-%m-%Y')
            storage_df['Follow_Up_Date'] = storage_df['Follow_Up_Date'].dt.strftime('%d-%m-%Y')

            storage_df['Last_Updated'] = pd.Timestamp.now().strftime('%d-%m-%Y %H:%M')
            storage_df['Data_Source'] = 'Order Confirmation Automation'

            headers = [
                'Purchase Date', 'Inquiry No', 'Company Name', 'Client Name', 'Product',
                'Quantity', 'State', 'City', 'Total Amount (₹)', 'Follow Up Date',
                'Urgency Status', 'Last Updated', 'Data Source'
            ]

            values = [headers] + storage_df.values.tolist()
            worksheet.update(values, value_input_option='RAW')

            worksheet.format('A1:M1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.2, 'green': 0.4, 'blue': 0.6}
            })

            return True, f"Stored {len(storage_df)} records to '{BRUSH_SHEET_NAME}'"

        except Exception as e:
            return False, f"Error: {str(e)}"

    def fetch_existing_brush_data(self):
        try:
            client = self.connect()
            if not client:
                return None

            sheet = client.open_by_key(SHEET_ID)
            worksheet = sheet.worksheet(BRUSH_SHEET_NAME)
            data = worksheet.get_all_records()

            return pd.DataFrame(data) if data else pd.DataFrame()

        except gspread.WorksheetNotFound:
            return pd.DataFrame()

        except Exception as e:
            st.error(f"Error fetching brush data: {e}")
            return None
