import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data(hash_funcs={pd.DataFrame: lambda _: None})
def load_data(uploaded_file):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data

# File uploader for imports and exports data
uploaded_imports = st.file_uploader("Upload Ireland Imports CSV", type="csv")
uploaded_exports = st.file_uploader("Upload Ireland Exports CSV", type="csv")

# Select year
years = [2021, 2022, 2023]
selected_year = st.selectbox("Select Year", years)

# Load data
imports_data = load_data(uploaded_imports)
exports_data = load_data(uploaded_exports)

if imports_data is not None and exports_data is not None:
    st.header("Dairy Imports and Exports Analysis")

    # Dairy Imports
    st.subheader(f"Dairy Imports - Sum by Partners ({selected_year})")
    imports_sum_by_partners = imports_data[imports_data['year'] == selected_year].groupby('Partner')['Quantityintonnes'].sum().reset_index()
    st.write(imports_sum_by_partners)

    # Dairy Exports
    st.subheader(f"Dairy Exports - Sum by Partners ({selected_year})")
    exports_sum_by_partners = exports_data[exports_data['year'] == selected_year].groupby('Partner')['Quantityintonnes'].sum().reset_index()
    st.write(exports_sum_by_partners)

    # Bar Chart Visualization for Imports
    st.subheader(f"Dairy Imports by Partner ({selected_year})")
    imports_chart = px.bar(imports_sum_by_partners, x='Quantityintonnes', y='Partner', orientation='h', title=f"Dairy Imports by Partner - {selected_year}")
    st.plotly_chart(imports_chart)

    # Bar Chart Visualization for Exports
    st.subheader(f"Dairy Exports by Partner ({selected_year})")
    exports_chart = px.bar(exports_sum_by_partners, x='Quantityintonnes', y='Partner', orientation='h', title=f"Dairy Exports by Partner - {selected_year}")
    st.plotly_chart(exports_chart)
