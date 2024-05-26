import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import calendar

# Corrected caching decorator
@st.cache
def load_data(url):
    return pd.read_csv(url)

# Plot data
def plot_data(data, title, color):
    st.subheader(title)
    filtered_data = data[(data['ProductGroup'] == selected_product_group) & (data['year'] == selected_year)]
    summary = filtered_data.groupby('Partner')['Quantityintonnes'].sum().reset_index()
    summary = summary.sort_values(by='Quantityintonnes', ascending=False)
    if selected_max_results != 'No Limit':
        summary = summary.head(int(selected_max_results))
    chart = px.bar(summary, x='Quantityintonnes', y='Partner', orientation='h', title=title, color_discrete_sequence=[color])
    st.plotly_chart(chart)

# UI Elements
year_options = list(range(2023, 2010, -1))
selected_year = st.selectbox("Select Year", year_options)

# Load Data
imports_data = load_data("https://raw.githubusercontent.com/sbs24011/Streamlit/main/ireland_imports.csv")
exports_data = load_data("https://raw.githubusercontent.com/sbs24011/Streamlit/main/ireland_exports.csv")
ireland_totals_by_partner = load_data("https://raw.githubusercontent.com/sbs24011/Streamlit/main/ireland_totals_by_partner_steamlit.csv")
ireland_export_partners_2023 = load_data("https://raw.githubusercontent.com/sbs24011/Streamlit/main/ireland_export_partners_2023_steamlit.csv")
nl_totals_by_partners2023 = load_data("https://raw.githubusercontent.com/sbs24011/Streamlit/main/nl_totals_by_partners2023_steamlit.csv")
best_prediction_df = load_data("https://raw.githubusercontent.com/sbs24011/Streamlit/main/best_prediction_df_steamlit.csv")

# Ensure data is loaded
if imports_data is not None and exports_data is not None:
    st.header("Ireland's Dairy Trade Analysis")

    product_groups = imports_data['ProductGroup'].unique()
    selected_product_group = st.selectbox("Select Product Group", product_groups)
    selected_max_results = st.selectbox("Select Maximum Results per Plot", ['No Limit', '5', '10', '20'])  
    import_export_selected = st.multiselect("Select Dataset to Display", ['Imports', 'Exports'], default=['Imports'])
    
    # Filtering and plotting data
    if 'Imports' in import_export_selected:
        plot_data(imports_data, f"Imports of {selected_product_group} in {selected_year}", '#1f77b4')
    if 'Exports' in import_export_selected:
        plot_data(exports_data, f"Exports of {selected_product_group} in {selected_year}", '#ff7f0e')
else:
    st.error("Failed to load data. Please check the data URLs and format.")

if ireland_totals_by_partner is not None:
    st.header("Dynamic map of Irelands export")
    
    unique_years = ireland_totals_by_partner['year'].unique()
    selected_year = st.select_slider("Select Year", options=unique_years)
    
    filtered_totals_df = ireland_totals_by_partner[
        (ireland_totals_by_partner['year'] == unique_years[0])
    ]
    
    dynamic_map = px.choropleth(filtered_totals_df,
                         locations="Alpha-3code_Partner",
                         title="Ireland Export Partners by Value in thousand euro in 2023",
                         color="Valueinthousandeuro",
                         hover_name="Partner",
                         color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(dynamic_map)
    
    
# Example of a simple choropleth map for 2023 export partners
if ireland_export_partners_2023 is not None and nl_totals_by_partners2023 is not None:
    st.header("2023 Dairy Trade Partners Comparison (Ireland and Netherlands)")
    fig4 = px.choropleth(ireland_export_partners_2023,
                         locations="Alpha-3code_Partner",
                         title="Ireland Export Partners by Value in thousand euro in 2023",
                         color="Valueinthousandeuro",
                         hover_name="Partner",
                         color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig4)
    
    fig5 = px.choropleth(nl_totals_by_partners2023,
                         locations="Alpha-3code_Partner",
                         title="Netherlands Export Partners by Value in thousand euro in 2023",
                         color="Valueinthousandeuro",
                         hover_name="Partner",
                         color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(fig5)

# Handling forecast visualization with data checks
if best_prediction_df is not None:
    st.header("Forecasted Quantity using Random Forest Regressor")
    unique_years = best_prediction_df['year'].unique()
    unique_months = range(1, 13)
    month_names = {month: calendar.month_name[month] for month in unique_months}

    selected_country = st.selectbox("Select Country", best_prediction_df['Partner'].unique())
    selected_limit = st.selectbox("Select Limit", [5, 10, 20, -1], format_func=lambda x: "No limit" if x == -1 else f"Top {x} products")
    selected_month = st.select_slider("Select Month", options=list(month_names.keys()), format_func=lambda x: month_names[x])

    filtered_df = best_prediction_df[
        (best_prediction_df['month'] == selected_month) &
        (best_prediction_df['year'] == unique_years[0]) &
        (best_prediction_df['Partner'] == selected_country)
    ]

    if selected_limit != -1:
        filtered_df = filtered_df.nlargest(selected_limit, 'RF_ForecastedQuantity')

    fig_forecast = px.bar(filtered_df, x='ProductGroup', y='RF_ForecastedQuantity', color='ProductGroup',
                          title=f'Forecasted Export Quantity for {month_names[selected_month]} {unique_years[0]}')
    st.plotly_chart(fig_forecast)
    

