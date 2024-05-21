import streamlit as st
import pandas as pd
import plotly.express as px

# Cache data loading function
@st.cache_data(hash_funcs={pd.DataFrame: lambda _: None})
def load_data_from_github(url):
    return pd.read_csv(url)

# Function to plot data by Partner
def plot_data_by_partner(data, title, year):
    st.subheader(title)
    summary = data[data['year'] == year].groupby('Partner')['Quantityintonnes'].sum().reset_index()
    st.write(summary)
    chart = px.bar(summary, x='Quantityintonnes', y='Partner', orientation='h', title=title,
                   color='Quantityintonnes', color_continuous_scale='Blues')
    st.plotly_chart(chart)

# Function to plot data by ProductGroup
def plot_data_by_product_group(data, title, year):
    st.subheader(title)
    summary = data[data['year'] == year].groupby('ProductGroup')['Quantityintonnes'].sum().reset_index()
    st.write(summary)
    chart = px.bar(summary, x='Quantityintonnes', y='ProductGroup', orientation='h', title=title,
                   color='Quantityintonnes', color_continuous_scale='Blues')
    st.plotly_chart(chart)

# GitHub URLs for datasets
imports_url = "https://raw.githubusercontent.com/sbs24011/Streamlit/main/ireland_imports.csv"
exports_url = "https://raw.githubusercontent.com/sbs24011/Streamlit/main/ireland_exports.csv"

# Load data
imports_data = load_data_from_github(imports_url)
exports_data = load_data_from_github(exports_url)

# Year selection
selected_year = st.selectbox("Select Year", imports_data['year'].unique())

# Main header
if imports_data is not None and exports_data is not None:
    st.header("Dairy Imports and Exports Analysis")
    
    # Subheader for Partner Analysis
    st.subheader("Imports and Exports by Partner")
    
    # Plot imports and exports data by Partner
    plot_data_by_partner(imports_data, f"Dairy Imports by Partner ({selected_year})", selected_year)
    plot_data_by_partner(exports_data, f"Dairy Exports by Partner ({selected_year})", selected_year)
    
    # Subheader for ProductGroups Analysis
    st.subheader("ProductGroups Imported and Exported by Year")
    
    # Plot imports and exports data by ProductGroup
    plot_data_by_product_group(imports_data, f"Dairy Imports by ProductGroup ({selected_year})", selected_year)
    plot_data_by_product_group(exports_data, f"Dairy Exports by ProductGroup ({selected_year})", selected_year)
