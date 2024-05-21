import streamlit as st
import pandas as pd
import plotly.express as px
import gdown

@st.cache_data(hash_funcs={pd.DataFrame: lambda _: None})
def load_data(file):
    if file is not None:
        return pd.read_csv(file)
    return None

def plot_data(data, title, year, colour, max_results):
    st.subheader(title)
    summary = data[data['year'] == year].groupby('Partner')['Quantityintonnes'].sum().reset_index()
    summary = summary.sort_values(by='Quantityintonnes', ascending=False)
    # st.write(summary)
    if max_results != 'No Limit':
        summary = summary.head(int(max_results))
        
    chart = px.bar(summary, x='Quantityintonnes', y='Partner', orientation='h', title=title, color_discrete_sequence=[colour], category_orders={"Partner": summary['Partner'].values.tolist()})
    st.plotly_chart(chart)

#uploaded_imports = st.file_uploader("Upload Ireland Imports CSV", type="csv")
#uploaded_exports = st.file_uploader("Upload Ireland Exports CSV", type="csv")

current_dir = os.path.dirname(os.path.abspath(__file__))
imports_file = os.path.join(current_dir, "imports.csv")
exports_file = os.path.join(current_dir, "exports.csv")

selected_year = st.selectbox("Select Year", [2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013,2012,2011,2010])

imports_data = load_data(uploaded_imports)
exports_data = load_data(uploaded_exports)

st.header("Ireland's Dairy Trade Analysis")

if imports_data is not None and exports_data is not None:
    selected_product_group = st.selectbox("Select Product Group", imports_data['ProductGroup'].unique())

    selected_max_results = st.selectbox("Select Maximum Results per Graph", ['No Limit', '5', '10', '20'])

    filtered_imports = imports_data[imports_data['ProductGroup'] == selected_product_group]
    filtered_exports = exports_data[exports_data['ProductGroup'] == selected_product_group]

    plot_data(filtered_imports, f"Imports of {selected_product_group} on {selected_year}", selected_year, '#1f77b4', selected_max_results)
    plot_data(filtered_exports, f"Exports of {selected_product_group} on {selected_year}", selected_year, '#ff7f0e', selected_max_results)
else:
    st.write("Please upload both imports and exports CSV files.")
