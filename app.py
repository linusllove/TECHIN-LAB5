import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DATABASE_URL = "postgresql://TianyiMu:Zly83685855@techin510lab4tianyimu.postgres.database.azure.com/postgres"

@st.cache_data
def load_data():
    conn = psycopg2.connect(DATABASE_URL)
    sql_query = "SELECT * FROM events;"
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df

def process_date(date_str):
    if 'through' in date_str:
        date_str = date_str.split('through')[-1]
    try:
        return pd.to_datetime(date_str.strip(), errors='coerce', utc=True)
    except:
        return pd.NaT

data = load_data()

data['parsed_date'] = data['date'].apply(process_date)
data['month'] = data['parsed_date'].dt.month
data['dayofweek'] = data['parsed_date'].dt.dayofweek

st.title('Seattle Events Dashboard')

# Event Categories
st.subheader('1. Event Categories')
category_counts = data['type'].value_counts()
st.bar_chart(category_counts)

# Events by Month
st.subheader('2. Events by Month')
monthly_counts = data['month'].value_counts().sort_index()
st.line_chart(monthly_counts)

# Events by Day of the Week
st.subheader('3. Events by Day of the Week')
day_of_week_counts = data['dayofweek'].value_counts().sort_index()
st.bar_chart(day_of_week_counts)

# Event Locations
st.subheader('4. Event Locations')
st.map(data.dropna(subset=['latitude', 'longitude']))

# Filter by Category
st.subheader('Filter by Category')
selected_category = st.selectbox('Select a category', data['type'].unique())
filtered_data_by_category = data[data['type'] == selected_category]
st.write(filtered_data_by_category)

# Filter by Date Range
st.subheader('Filter by Date Range')
start_date, end_date = st.date_input("Select a date range", [])
if start_date and end_date:
    filtered_data_by_date = data[(data['parsed_date'] >= start_date) & (data['parsed_date'] <= end_date)]
    st.write(filtered_data_by_date)

# Filter by Location
st.subheader('Filter by Location')
selected_location = st.selectbox('Select a location', data['location'].unique())
filtered_data_by_location = data[data['location'] == selected_location]
st.write(filtered_data_by_location)
