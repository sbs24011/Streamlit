import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data(hash_funcs={pd.DataFrame: lambda _: None})
def load_data(file):
    if file is not None:
        return pd.read_csv(file)
    return None

def plot_data_by_partner(data, title, year):
    st.subheader(title)
    summary = data[data['year'] == year].groupby('Partner')['Quantityintonnes'].sum().reset_index()
    st.write(summary)
    chart = px.bar(summary, x='Quantityintonnes', y='Partner', orientation='h', title=title,
                   color='Quantityintonnes', color_continuous_scale='Viridis')
    st.plotly_chart(chart)

def plot_data_by_product_group(data, title, year):
    st.subheader(title)
    summary = data[data['year'] == year].groupby('ProductGroup')['Quantityintonnes'].sum().reset_index()
    st.write(summary)
    chart = px.bar(summary, x='Quantityintonnes', y='ProductGroup', orientation='h', title=title,
                   color='Quantityintonnes', color_continuous_scale='Cividis')
    st.plotly_chart(chart)

uploaded_imports = st.file_uploader("Upload Ireland Imports CSV", type="csv")
uploaded_exports = st.file_uploader("Upload Ireland Exports CSV", type="csv")

selected_year = st.selectbox("Select Year", [2023, 2022, 2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010])

imports_data = load_data(uploaded_imports)
exports_data = load_data(uploaded_exports)

if imports_data is not None and exports_data is not None:
    st.header("Dairy Imports and Exports Analysis")
    st.subheader("Imports and Exports by Partner")
    
    plot_data_by_partner(imports_data, f"Dairy Imports by Partner ({selected_year})", selected_year)
    plot_data_by_partner(exports_data, f"Dairy Exports by Partner ({selected_year})", selected_year)
    st.subheader("ProductGroups Imported and Exported by Year")
    plot_data_by_product_group(imports_data, f"Dairy Imports by ProductGroup ({selected_year})", selected_year)
    plot_data_by_product_group(exports_data, f"Dairy Exports by ProductGroup ({selected_year})", selected_year)

    product_groups_import = imports_data['ProductGroup'].unique()
    product_groups_export = exports_data['ProductGroup'].unique()
    
    selected_product_group_import = st.selectbox("Select ProductGroup for Imports", product_groups_import)
    selected_product_group_export = st.selectbox("Select ProductGroup for Exports", product_groups_export)
    
    st.subheader(f"Specific ProductGroup Imports ({selected_product_group_import}) in {selected_year}")
    specific_imports = imports_data[(imports_data['year'] == selected_year) & 
                                    (imports_data['ProductGroup'] == selected_product_group_import)]
    st.write(specific_imports)
    specific_imports_chart = px.bar(specific_imports, x='Quantityintonnes', y='Partner', orientation='h',
                                    title=f"Dairy Imports for {selected_product_group_import} by Partner ({selected_year})",
                                    color='Quantityintonnes', color_continuous_scale='Blues')
    st.plotly_chart(specific_imports_chart)
    
    st.subheader(f"Specific ProductGroup Exports ({selected_product_group_export}) in {selected_year}")
    specific_exports = exports_data[(exports_data['year'] == selected_year) & 
                                    (exports_data['ProductGroup'] == selected_product_group_export)]
    st.write(specific_exports)
    specific_exports_chart = px.bar(specific_exports, x='Quantityintonnes', y='Partner', orientation='h',
                                    title=f"Dairy Exports for {selected_product_group_export} by Partner ({selected_year})",
                                    color='Quantityintonnes', color_continuous_scale='Reds')
    st.plotly_chart(specific_exports_chart)
