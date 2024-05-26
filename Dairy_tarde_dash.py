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
milk_prices_df = load_data("https://raw.githubusercontent.com/sbs24011/Streamlit/main/milk_prices_df_steamlit.csv")
ireland_totals_by_product_group = load_data("https://raw.githubusercontent.com/sbs24011/Streamlit/main/ireland_totals_by_product_group_steamlit.csv")

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
    
    ireland_totals_unique_years = ireland_totals_by_partner['year'].unique()
    ireland_totals_selected_year = st.select_slider("Select Year", options=ireland_totals_unique_years)
    
    filtered_totals_df = ireland_totals_by_partner[
        (ireland_totals_by_partner['year'] == ireland_totals_selected_year)
    ]
    
    dynamic_ireland_totals_map = px.choropleth(filtered_totals_df,
                         locations="Alpha-3code_Partner",
                         title=f"Ireland Export Partners by Value in thousand euro ({ireland_totals_selected_year})",
                         color="Valueinthousandeuro",
                         hover_name="Partner",
                         color_continuous_scale=px.colors.sequential.Plasma)
    st.plotly_chart(dynamic_ireland_totals_map)
    

if ireland_totals_by_product_group is not None:
    st.header("Ireland's Export Quantity and Value Over the Years")
    ireland_totals_by_product_group_years = ireland_totals_by_product_group['year'].unique()
    ireland_totals_by_product_group_selected_year = st.slider('Select Year', min_value=int(ireland_totals_by_product_group_years.min()), max_value=int(ireland_totals_by_product_group_years.max()), value=int(ireland_totals_by_product_group_years.min()))
    
    ireland_totals_by_product_group_filtered_data = ireland_totals_by_product_group[ireland_totals_by_product_group['year'] == ireland_totals_by_product_group_selected_year]
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Bar(
            x=ireland_totals_by_product_group_filtered_data['ProductGroup'],
            y=ireland_totals_by_product_group_filtered_data['Quantityintonnes'],
            name='Quantity in tonnes',
            yaxis='y1'
        )
    )

    # Value per tonne on the right y-axis
    fig.add_trace(
        go.Scatter(
            x=ireland_totals_by_product_group_filtered_data['ProductGroup'],
            y=ireland_totals_by_product_group_filtered_data['Value_per_tonne'],
            name='Value per tonne',
            yaxis='y2',
            mode='lines+markers'
        )
    )

    # Update the layout for dual y-axes
    fig.update_layout(
        title=f'Product Group Data for {ireland_totals_by_product_group_selected_year}',
        xaxis_title='Product Group',
        yaxis=dict(
            title='Quantity in tonnes',
            titlefont=dict(color='#1f77b4'),
            tickfont=dict(color='#1f77b4')
        ),
        yaxis2=dict(
            title='Value per tonne',
            titlefont=dict(color='#ff7f0e'),
            tickfont=dict(color='#ff7f0e'),
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.1, y=1.1, orientation='h')
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)

    
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
    
if milk_prices_df is not None:
    st.header("Organic and Raw Milk prices over the years")
    
    milk_prices_unique_years = milk_prices_df['year'].unique()
    milk_prices_selected_year = st.select_slider("Select Year", options=milk_prices_unique_years)
    selected_milk_type = st.selectbox("Select Milk Type", ['Raw', 'Organic raw'])
    
    filtered_milk_prices_df = milk_prices_df[
        (milk_prices_df['year'] == milk_prices_selected_year)
    ]
    
    if (selected_milk_type == "Raw"):
        color_column = "Raw milk price"
    else:
        color_column = "Organic raw milk price"
        
    dynamic_milk_prices_map = px.choropleth(filtered_milk_prices_df,
                         locations="Country",
                         locationmode="country names",
                         title=f"{selected_milk_type} milk price (Euros per 100Kg) - {milk_prices_selected_year}",
                         color=color_column,
                         color_continuous_scale=px.colors.sequential.Plasma,
                         scope="europe")
    st.plotly_chart(dynamic_milk_prices_map)

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
    

