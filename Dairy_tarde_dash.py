import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

@st.cache_data(hash_funcs={pd.DataFrame: lambda _: None})
def load_data(file):
    if file is not None:
        return pd.read_csv(file)
    return None

uploaded_imports = st.file_uploader("Upload Ireland Imports CSV", type="csv")
uploaded_exports = st.file_uploader("Upload Ireland Exports CSV", type="csv")

imports_data = load_data(uploaded_imports)
exports_data = load_data(uploaded_exports)

st.header("Ireland's Dairy Trade Analysis")

if imports_data is not None and exports_data is not None:
    selected_product_group = st.selectbox("Select Product Group", imports_data['ProductGroup'].unique())

    filtered_imports = imports_data[imports_data['ProductGroup'] == selected_product_group]
    filtered_exports = exports_data[exports_data['ProductGroup'] == selected_product_group]

    summary_imports = filtered_imports.groupby('year')['Quantity'].sum().reset_index()
    chart_imports = px.bar(summary_imports, x='year', y='Quantity', title=f"Imports of {selected_product_group} Over Years",
                           color_discrete_sequence=['#1f77b4'])
    st.plotly_chart(chart_imports)

    summary_exports = filtered_exports.groupby('year')['Quantity'].sum().reset_index()
    chart_exports = px.bar(summary_exports, x='year', y='Quantity', title=f"Exports of {selected_product_group} Over Years",
                           color_discrete_sequence=['#ff7f0e'])
    st.plotly_chart(chart_exports)
else:
    st.write("Please upload both imports and exports CSV files.")

