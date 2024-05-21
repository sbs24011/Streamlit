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
selected_year = st.selectbox("Select Year", [2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010])

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
    
    # Dropdowns for selecting specific ProductGroup for imports and exports
    product_groups_import = imports_data['ProductGroup'].unique()
    product_groups_export = exports_data['ProductGroup'].unique()
    
    selected_product_group_import = st.selectbox("Select ProductGroup for Imports", product_groups_import)
    selected_product_group_export = st.selectbox("Select ProductGroup for Exports", product_groups_export)
    
    # Plot specific ProductGroup data for imports
    st.subheader(f"Specific ProductGroup Imports ({selected_product_group_import}) in {selected_year}")
    specific_imports = imports_data[(imports_data['year'] == selected_year) & 
                                    (imports_data['ProductGroup'] == selected_product_group_import)]
    st.write(specific_imports)
    specific_imports_chart = px.bar(specific_imports, x='Quantityintonnes', y='Partner', orientation='h',
                                    title=f"Dairy Imports for {selected_product_group_import} by Partner ({selected_year})",
                                    color='Quantityintonnes', color_continuous_scale='Blues')
    st.plotly_chart(specific_imports_chart)
    
    # Plot specific ProductGroup data for exports
    st.subheader(f"Specific ProductGroup Exports ({selected_product_group_export}) in {selected_year}")
    specific_exports = exports_data[(exports_data['year'] == selected_year) & 
                                    (exports_data['ProductGroup'] == selected_product_group_export)]
    st.write(specific_exports)
    specific_exports_chart = px.bar(specific_exports, x='Quantityintonnes', y='Partner', orientation='h',
                                    title=f"Dairy Exports for {selected_product_group_export} by Partner ({selected_year})",
                                    color='Quantityintonnes', color_continuous_scale='Blues')
    st.plotly_chart(specific_exports_chart)
    
    # Additional interactive elements
    st.sidebar.header("Filters")
    
    # Filter by Partner
    partners_import = st.sidebar.multiselect("Select Partners for Imports", imports_data['Partner'].unique())
    partners_export = st.sidebar.multiselect("Select Partners for Exports", exports_data['Partner'].unique())
    
    if partners_import:
        filtered_imports = imports_data[(imports_data['year'] == selected_year) & 
                                        (imports_data['ProductGroup'] == selected_product_group_import) &
                                        (imports_data['Partner'].isin(partners_import))]
        st.subheader(f"Filtered Imports for {selected_product_group_import} in {selected_year}")
        st.write(filtered_imports)
        filtered_imports_chart = px.bar(filtered_imports, x='Quantityintonnes', y='Partner', orientation='h',
                                        title=f"Filtered Dairy Imports for {selected_product_group_import} by Partner ({selected_year})",
                                        color='Quantityintonnes', color_continuous_scale='Blues')
        st.plotly_chart(filtered_imports_chart)
    
    if partners_export:
        filtered_exports = exports_data[(exports_data['year'] == selected_year) & 
                                        (exports_data['ProductGroup'] == selected_product_group_export) &
                                        (exports_data['Partner'].isin(partners_export))]
        st.subheader(f"Filtered Exports for {selected_product_group_export} in {selected_year}")
        st.write(filtered_exports)
        filtered_exports_chart = px.bar(filtered_exports, x='Quantityintonnes', y='Partner', orientation='h',
                                        title=f"Filtered Dairy Exports for {selected_product_group_export} by Partner ({selected_year})",
                                        color='Quantityintonnes', color_continuous_scale='Blues')
        st.plotly_chart(filtered_exports_chart)
