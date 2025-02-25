import streamlit as st
from datetime import datetime
import requests
import pandas as pd

API_URL = 'http://127.0.0.1:8000'

def analytics_tab():
    col1, col2 = st.columns(2)
    with  col1:
        start_date = st.date_input('Start date', datetime(2024,8,1))
    with col2:
        end_date = st.date_input('End daate', datetime(2024, 8, 5))
    if st.button('Get analytics'):
        payload = {
             "startdate": start_date.strftime("%Y-%m-%d"),
            "enddate": end_date.strftime("%Y-%m-%d")
        }
        summary = requests.post(f'{API_URL}/analytics/', json=payload)
        summary = summary.json()
        data = {
            'Category': list(summary.keys()),
            'Total': [summary[category]['total'] for category in summary],
            'Percentage': [summary[category]['percentage'] for category in summary]
        }

        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by = 'Percentage', ascending=False)
        st.title('Expense by Category')
        st.bar_chart(data=df_sorted.set_index('Category')['Percentage'], width=0, height=0, use_container_width=5)
        st.table(df_sorted)