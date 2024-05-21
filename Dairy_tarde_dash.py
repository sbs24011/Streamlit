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
imports_url = "https://drive.google.com/file/d/1fkHA9OjW97qqhL2Eci6FYNah3hfqkw45"
exports_url = "https://drive.google.com/file/d/1I8gCIZ8ASIk_Qk_hJ5S_IN61D9bvCA2a"

# Load data
imports_data = load_data_from_google_drive(imports_url)
exports_data = load_data_from_google_drive(exports_url)

# Main header
st.header("Ireland's Dairy Trade Imports and Exports Analysis")

# Subheader for Imports Analysis
st.subheader("Imports Analysis")
summary_imports = imports_data.groupby(['year', 'ProductGroup'])['Quantityintonnes'].sum().reset_index()
fig_imports = px.bar(summary_imports, x='year', y='Quantityintonnes', color='ProductGroup', 
                     title="Dairy Imports by Product Group per Year", barmode='group')
st.plotly_chart(fig_imports)

# Subheader for Exports Analysis
st.subheader("Exports Analysis")
summary_exports = exports_data.groupby(['year', 'ProductGroup'])['Quantityintonnes'].sum().reset_index()
fig_exports = px.bar(summary_exports, x='year', y='Quantityintonnes', color='ProductGroup', 
                     title="Dairy Exports by Product Group per Year", barmode='group')
st.plotly_chart(fig_exports)
