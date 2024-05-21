#!/usr/bin/env python
# coding: utf-8
import streamlit as st
import pandas as pd

try:
    import plotly.express as px
except ImportError as e:
    st.error(f"Error importing plotly: {e}")
    st.stop()

@st.cache
def load_data(uploaded_file):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data

uploaded_imports = st.file_uploader("Upload Ireland Imports CSV", type="csv")
uploaded_exports = st.file_uploader("Upload Ireland Exports CSV", type="csv")

years = [2021, 2022, 2023]
selected_year = st.selectbox("Select Year", years)

imports_data = load_data(uploaded_imports)
exports_data = load_data(uploaded_exports)

if imports_data is not None and exports_data is not None:
    st.header("Dairy Imports")
    st.subheader(f"Sum by Partners - {selected_year}")
    imports_sum_by_partners = imports_data[imports_data['year'] == selected_year].groupby('Partner')['Quantityintonnes'].sum().reset_index()
    st.write(imports_sum_by_partners)

    st.header("Dairy Exports")
    st.subheader(f"Sum by Partners - {selected_year}")
    exports_sum_by_partners = exports_data[exports_data['year'] == selected_year].groupby('Partner')['Quantityintonnes'].sum().reset_index()
    st.write(exports_sum_by_partners)

    # Visualization using Plotly Express
    st.subheader("Bar Chart Visualization")
    imports_chart = px.bar(imports_sum_by_partners, x='Quantityintonnes', y='Partner', orientation='h', title=f"Dairy Imports by Partner - {selected_year}")
    st.plotly_chart(imports_chart)

    exports_chart = px.bar(exports_sum_by_partners, x='Quantityintonnes', y='Partner', orientation='h', title=f"Dairy Exports by Partner - {selected_year}")
    st.plotly_chart(exports_chart)