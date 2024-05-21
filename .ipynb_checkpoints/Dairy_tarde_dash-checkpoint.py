#!/usr/bin/env python
# coding: utf-8
#!pip install streamlit

import streamlit as st
import pydeck as pdk
import pandas as pd


@st.cache
def load_data(uploaded_file):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data

uploaded_imports = st.file_uploader("ireland_exports", type="csv")
uploaded_exports = st.file_uploader("ireland_imports", type="csv")

years = [2021,2022, 2023]
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

    # Visualization using Altair
    st.subheader("Bar Chart Visualization")
    imports_chart = alt.Chart(imports_sum_by_partners).mark_bar().encode(
        x='Quantityintonnes:Q',
        y=alt.Y('Partner:N', sort='-x')
    ).properties(
        title=f"Dairy Imports by Partner - {selected_year}",
        width=600,
        height=400
    )
    st.altair_chart(imports_chart)

    exports_chart = alt.Chart(exports_sum_by_partners).mark_bar().encode(
        x='Quantityintonnes:Q',
        y=alt.Y('Partner:N', sort='-x')
    ).properties(
        title=f"Dairy Exports by Partner - {selected_year}",
        width=600,
        height=400
    )
    st.altair_chart(exports_chart)