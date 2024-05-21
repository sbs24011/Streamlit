import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

# Function to load data from Google Drive
@st.cache(allow_output_mutation=True)
def load_data_from_google_drive(url):
    output_file = "/tmp/ireland_data.csv"
    gdown.download(url, output_file, quiet=False)
    return pd.read_csv(output_file)

# Google Drive URLs for datasets
imports_url = "https://drive.google.com/uc?id=1fkHA9OjW97qqhL2Eci6FYNah3hfqkw45"
exports_url = "https://drive.google.com/uc?id=1I8gCIZ8ASIk_Qk_hJ5S_IN61D9bvCA2a"

# Load data
imports_data = load_data_from_google_drive(imports_url)
exports_data = load_data_from_google_drive(exports_url)

# Main header
st.header("Ireland's Dairy Trade Imports and Exports Analysis")

# Selection for Product Group Analysis
selected_product_group = st.selectbox("Select Product Group", imports_data['ProductGroup'].unique())

# Filter data by selected product group
filtered_imports = imports_data[imports_data['ProductGroup'] == selected_product_group]
filtered_exports = exports_data[exports_data['ProductGroup'] == selected_product_group]

# Create summary for imports by year
summary_imports = filtered_imports.groupby('year')['Quantity'].sum().reset_index()
chart_imports = px.bar(summary_imports, x='year', y='Quantity', title=f"Imports of {selected_product_group} Over Years",
                       color_discrete_sequence=['#1f77b4'])
st.plotly_chart(chart_imports)

# Create summary for exports by year
summary_exports = filtered_exports.groupby('year')['Quantity'].sum().reset_index()
chart_exports = px.bar(summary_exports, x='year', y='Quantity', title=f"Exports of {selected_product_group} Over Years",
                       color_discrete_sequence=['#ff7f0e'])
st.plotly_chart(chart_exports)
