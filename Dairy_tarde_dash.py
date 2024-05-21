import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data(hash_funcs={pd.DataFrame: lambda _: None})
def load_data(file):
    if file is not None:
        return pd.read_csv(file)
    return None

def plot_data(data, title, year):
    st.subheader(title)
    summary = data[data['year'] == year].groupby('Partner')['Quantityintonnes'].sum().reset_index()
    st.write(summary)
    chart = px.bar(summary, x='Quantityintonnes', y='Partner', orientation='h', title=title)
    st.plotly_chart(chart)


uploaded_imports = st.file_uploader("Upload Ireland Imports CSV", type="csv")
uploaded_exports = st.file_uploader("Upload Ireland Exports CSV", type="csv")

selected_year = st.selectbox("Select Year", [2018,2019,2020,2021, 2022, 2023])


imports_data = load_data(uploaded_imports)
exports_data = load_data(uploaded_exports)


if imports_data is not None and exports_data is not None:
    st.header("Dairy Imports and Exports Analysis")
    
    # Subheader for ProductGroups
    st.subheader("ProductGroups Imported and Exported by Year")
    
    # Plot imports and exports data
    plot_data(imports_data, f"Dairy Imports by Partner ({selected_year})", selected_year)
    plot_data(exports_data, f"Dairy Exports by Partner ({selected_year})", selected_year)
