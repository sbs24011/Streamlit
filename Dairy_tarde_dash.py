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

# Year selection
selected_year_imports = st.selectbox("Select Year for Imports", imports_data['year'].unique())
selected_year_exports = st.selectbox("Select Year for Exports", exports_data['year'].unique())

# Main header
st.header("Dairy Imports and Exports Analysis")

# Subheader for Imports Analysis
st.subheader("Imports Analysis")
st.write(f"Data for Imports in {selected_year_imports}:")
summary_imports = imports_data[imports_data['year'] == selected_year_imports].groupby('Partner')['Quantityintonnes'].sum().reset_index()
st.write(summary_imports)
chart_imports = px.bar(summary_imports, x='Quantityintonnes', y='Partner', orientation='h', title=f"Dairy Imports by Partner ({selected_year_imports})",
                   color_discrete_sequence=['#1f77b4'])  # Specify a single color for all bars
st.plotly_chart(chart_imports)

# Subheader for Exports Analysis
st.subheader("Exports Analysis")
st.write(f"Data for Exports in {selected_year_exports}:")
summary_exports = exports_data[exports_data['year'] == selected_year_exports].groupby('Partner')['Quantityintonnes'].sum().reset_index()
st.write(summary_exports)
chart_exports = px.bar(summary_exports, x='Quantityintonnes', y='Partner', orientation='h', title=f"Dairy Exports by Partner ({selected_year_exports})",
                   color_discrete_sequence=['#ff7f0e'])  # Specify a single color for all bars
st.plotly_chart(chart_exports)
