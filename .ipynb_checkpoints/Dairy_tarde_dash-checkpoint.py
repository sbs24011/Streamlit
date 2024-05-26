import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import calendar

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

def plot_data(data, title, year, colour, max_results):
    st.subheader(title)
    summary = data[data['year'] == year].groupby('Partner')['Quantityintonnes'].sum().reset_index()
    summary = summary.sort_values(by='Quantityintonnes', ascending=False)
    if max_results != 'No Limit':
        summary = summary.head(int(max_results))
        
    chart = px.bar(summary, x='Quantityintonnes', y='Partner', orientation='h', title=title, color_discrete_sequence=[colour])
    st.plotly_chart(chart)

# Data URLs
imports_url = "https://raw.githubusercontent.com/sbs24011/Streamlit/main/ireland_imports.csv"
exports_url = "https://raw.githubusercontent.com/sbs24011/Streamlit/main/ireland_exports.csv"

# UI Elements
selected_year = st.selectbox("Select Year", list(range(2023, 2010, -1)))

# Load Data
imports_data = load_data(imports_url)
exports_data = load_data(exports_url)

st.header("Ireland's Dairy Trade Analysis")

if imports_data is not None and exports_data is not None:
    selected_dataset = st.selectbox("Select the Dataset for Plotting", ['Both', 'Imports', 'Exports'])
    selected_product_group = st.selectbox("Select Product Group", imports_data['ProductGroup'].unique())
    selected_max_results = st.selectbox("Select Maximum Results per Plot", ['No Limit', '5', '10', '20'])

    filtered_imports = imports_data[imports_data['ProductGroup'] == selected_product_group]
    filtered_exports = exports_data[exports_data['ProductGroup'] == selected_product_group]

    if selected_dataset in ['Both', 'Imports']: 
        plot_data(filtered_imports, f"Imports of {selected_product_group} in {selected_year}", selected_year, '#1f77b4', selected_max_results)
    if selected_dataset in ['Both', 'Exports']: 
        plot_data(filtered_exports, f"Exports of {selected_product_group} in {selected_year}", selected_year, '#ff7f0e', selected_max_results)
else:
    st.write("Please upload both imports and exports CSV files.")

# Second visualization: Ireland's Export Quantity and Value Over the Years
st.header("Ireland's Export Quantity and Value Over the Years")

ireland_totals_by_product_group = pd.read_csv("https://raw.githubusercontent.com/sbs24011/Streamlit/main/ireland_totals_by_product_group.csv")  # Replace with actual URL
fig2 = go.Figure()

initial_year = ireland_totals_by_product_group['year'].min()
df_initial = ireland_totals_by_product_group[ireland_totals_by_product_group['year'] == initial_year]

fig2.add_trace(go.Bar(
    x=df_initial['ProductGroup'],
    y=df_initial['Quantityintonnes'],
    name='Quantity (tonnes)',
    marker=dict(color='rgba(0, 128, 128, 0.6)'),
    yaxis='y1'
))

fig2.add_trace(go.Bar(
    x=df_initial['ProductGroup'],
    y=df_initial['Value_per_tonne'],
    name='Value per tonne (euro)',
    marker=dict(color='rgba(255, 165, 0, 0.6)'),
    yaxis='y2'
))

frames = []
for year in ireland_totals_by_product_group['year'].unique():
    df_year = ireland_totals_by_product_group[ireland_totals_by_product_group['year'] == year]
    frames.append(go.Frame(
        data=[
            go.Bar(
                x=df_year['ProductGroup'],
                y=df_year['Quantityintonnes'],
                marker=dict(color='rgba(54, 162, 235, 0.6)'),
                yaxis='y1',
                name='Quantity (tonnes)'
            ),
            go.Bar(
                x=df_year['ProductGroup'],
                y=df_year['Value_per_tonne'],
                marker=dict(color='rgba(255, 99, 71, 0.6)'),
                yaxis='y2',
                name='Value per tonne (euro)'
            )
        ],
        name=str(year)
    ))

fig2.update(frames=frames)

fig2.update_layout(
    title_text="Ireland's Export Quantity and Value Over the Years",
    xaxis=dict(
        title="Product Group",
        title_standoff=20,
        tickangle=-35
    ),
    yaxis=dict(
        title="Quantity (tonnes)",
        range=[0, 300000],
        side='left'
    ),
    yaxis2=dict(
        title="Value per tonne (euro)",
        range=[0, 20],
        overlaying='y',
        side='right'
    ),
    updatemenus=[{
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 500, 'redraw': True}, 'fromcurrent': True}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }],
    sliders=[{
        'steps': [
            {
                'args': [
                    [str(year)],
                    {
                        'frame': {'duration': 500, 'redraw': True},
                        'mode': 'immediate',
                        'transition': {'duration': 0}
                    }
                ],
                'label': str(year),
                'method': 'animate'
            } for year in ireland_totals_by_product_group['year'].unique()
        ],
        'x': 0.1,
        'len': 0.9,
        'xanchor': 'left',
        'y': -0.3
    }]
)

st.plotly_chart(fig2)

# Third visualization: Ireland Export Partners Over Time
st.header("Ireland Export Partners Over Time")

ireland_totals_by_partner = pd.read_csv("https://raw.githubusercontent.com/sbs24011/Streamlit/main/ireland_totals_by_partner.csv")  # Replace with actual URL

fig_quantity = px.choropleth(ireland_totals_by_partner,
                             locations="Alpha-3code_Partner",
                             color="Quantityintonnes",
                             hover_name="Partner",
                             color_continuous_scale=px.colors.sequential.Plasma,
                             animation_frame="year",
                             animation_group="Partner",
                             labels={"Quantityintonnes": "Quantity (Tonnes)", "Partner": "Export Partner"}
                             )
fig_quantity.update_layout(geo=dict(showframe=False, showcoastlines=False))

fig_value = px.choropleth(ireland_totals_by_partner,
                          locations="Alpha-3code_Partner",
                          color="Valueinthousandeuro",
                          hover_name="Partner",
                          color_continuous_scale=px.colors.sequential.Plasma,
                          animation_frame="year",
                          animation_group="Partner",
                          labels={"Valueinthousandeuro": "Value (EUR)", "Partner": "Export Partner"}
                          )
fig_value.update_layout(geo=dict(showframe=False, showcoastlines=False))

fig3 = go.Figure()

for data in fig_quantity.data:
    fig3.add_trace(data)

for data in fig_value.data:
    fig3.add_trace(data)

frames = []
for year in ireland_totals_by_partner['year'].unique():
    frame_data = []
    for data in fig_quantity.frames:
        if data.name == str(year):
            frame_data.extend(data.data)
    for data in fig_value.frames:
        if data.name == str(year):
            frame_data.extend(data.data)
    frames.append(go.Frame(data=frame_data, name=str(year)))

fig3.frames = frames

dropdown_buttons = [
    {'label': 'Quantity (Tonnes)',
     'method': 'update',
     'args': [{'visible': [True if i < len(fig_quantity.data) else False for i in range(len(fig3.data))]},
              {'title': 'Ireland Export Partners by Quantity (Tonnes) Over Time'}]},
    {'label': 'Value (EUR)',
     'method': 'update',
     'args': [{'visible': [False if i < len(fig_quantity.data) else True for i in range(len(fig3.data))]},
              {'title': 'Ireland Export Partners by Value (EUR) Over Time'}]}
]

fig3.update_layout(
    updatemenus=[{
        'buttons': dropdown_buttons,
        'direction': 'down',
        'showactive': True
    }],
    title='Ireland Export Partners Over Time',
    geo=dict(showframe=False, showcoastlines=False),
    sliders=[{
        'steps': [{'args': [[f.name], {'frame': {'duration': 500, 'redraw': True},
                                      'mode': 'immediate',
                                      'transition': {'duration': 300}}],
                   'label': f.name,
                   'method': 'animate'} for f in fig3.frames],
        'transition': {'duration': 300},
        'x': 0.1,
        'xanchor': 'left',
        'y': 0,
        'yanchor': 'top'}
    ]
)

st.plotly_chart(fig3)

# Fourth visualization: 2023 Dairy Trade Partners Comparison
st.header("2023 Dairy Trade Partners Comparison")

ireland_export_partners_2023 = pd.read_csv("https://raw.githubusercontent.com/sbs24011/Streamlit/main/ireland_export_partners_2023.csv")  # Replace with actual URL
nl_totals_by_partners2023 = pd.read_csv("https://raw.githubusercontent.com/sbs24011/Streamlit/main/nl_totals_by_partners2023.csv")  # Replace with actual URL

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

# Machine learning visualization: Interactive Word Cloud for All Clusters
st.header("Interactive Word Cloud for All Clusters")

def generate_word_vectors(words):
    return np.random.rand(len(words), 2)  # Placeholder for actual word vector generation

def get_tsne_coordinates(word_vectors, perplexity):
    tsne = TSNE(n_components=2, perplexity=perplexity, random_state=42)
    return tsne.fit_transform(word_vectors)

def add_jitter(coordinates, jitter):
    return coordinates + np.random.normal(0, jitter, coordinates.shape)

top_keywords_kmeans = {
    "Cluster 1": ["milk", "dairy", "cheese"],
    "Cluster 2": ["butter", "cream", "yogurt"],
    "Cluster 3": ["whey", "casein", "lactose"],
    "Cluster 4": ["ice", "cream", "milkshake"],
    "Cluster 5": ["kefir", "buttermilk", "curd"]
}

fig_ml = go.Figure()
colors = ['blue', 'green', 'red', 'orange', 'purple']
shapes = ['circle', 'square', 'diamond', 'cross', 'x']

for i, ((cluster, words), color, shape) in enumerate(zip(top_keywords_kmeans.items(), colors, shapes), start=1):
    word_vectors = generate_word_vectors(words)
    scaler = StandardScaler()
    word_vectors = scaler.fit_transform(word_vectors)
    perplexity = min(50, len(words) - 1)
    coordinates = get_tsne_coordinates(word_vectors, perplexity)
    coordinates = add_jitter(coordinates, 0.2)
    
    fig_ml.add_trace(go.Scatter(
        x=coordinates[:, 0],
        y=coordinates[:, 1],
        mode='markers+text',
        marker=dict(size=12, opacity=0.7, color=color, symbol=shape),
        text=words,
        textposition="top center",
        textfont=dict(size=10),
        hoverinfo='text',
        hovertext=[f'Word: {word}<br>Cluster: {cluster}' for word in words],
        showlegend=True,
        name=f'Cluster {cluster}'
    ))

fig_ml.update_layout(
    title='Interactive Word Cloud for All Clusters',
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    legend=dict(title='Clusters')
)

st.plotly_chart(fig_ml)

# Additional Machine Learning visualization: PCA of Clusters with Top Words
st.header("PCA of Clusters with Top Words")

principal_components = np.random.rand(100, 2)  # Placeholder for actual PCA data
kmeans_labels = np.random.randint(0, 5, 100)  # Placeholder for actual KMeans labels
challenge_other = pd.Series(np.random.choice(['milk', 'butter', 'cheese', 'cream'], 100))  # Placeholder for actual data

df_pca = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
df_pca['Cluster'] = kmeans_labels
df_pca['Text'] = challenge_other.values
df_pca['Top_Words'] = df_pca['Cluster'].map(lambda x: ', '.join(top_keywords_kmeans[f'Cluster {x+1}']))

df_pca['customdata'] = df_pca.apply(lambda row: [row['Top_Words'], row['Text']], axis=1)

fig_pca = px.scatter(df_pca, x='PC1', y='PC2', color='Cluster', 
                     custom_data=['Top_Words', 'Text'], 
                     title='PCA of Clusters with Top Words',
                     labels={'PC1': 'Principal Component 1', 'PC2': 'Principal Component 2'})

fig_pca.update_traces(marker=dict(size=10), 
                      hovertemplate="<b>Principal Component 1</b>: %{x}<br>"
                                    "<b>Principal Component 2</b>: %{y}<br>"
                                    "<b>Cluster</b>: %{marker.color}<br>"
                                    "Top Words: %{customdata[0]}<br>"
                                    "Text: %{customdata[1]}<extra></extra>")

st.plotly_chart(fig_pca)

# Dash app equivalent in Streamlit: Forecasted Quantity using Random Forest Regressor
st.header("Forecasted Quantity using Random Forest Regressor")

best_prediction_df = pd.read_csv("https://raw.githubusercontent.com/sbs24011/Streamlit/main/best_prediction_df.csv")  # Replace with actual URL

unique_months = best_prediction_df['month'].unique()
unique_years = best_prediction_df['year'].unique()
month_names = {month: calendar.month_name[month] for month in unique_months}

country = st.selectbox("Select Country", best_prediction_df['Partner'].unique())
limit = st.selectbox("Select Limit", [5, 10, 20, -1], format_func=lambda x: "No limit" if x == -1 else f"Top {x} products")
month = st.slider("Select Month", 0, len(unique_months) - 1, 0, format_func=lambda x: month_names[unique_months[x]])

filtered_df = best_prediction_df[
    (best_prediction_df['month'] == unique_months[month]) &
    (best_prediction_df['year'] == unique_years[0]) &
    (best_prediction_df['Partner'] == country)
]

if limit != -1:
    filtered_df = filtered_df.nlargest(limit, 'RF_ForecastedQuantity')

filtered_df = filtered_df.sort_values(by='RF_ForecastedQuantity', ascending=False)

fig_dash = go.Figure()
for product_group in filtered_df['ProductGroup'].unique():
    product_group_df = filtered_df[filtered_df['ProductGroup'] == product_group]
    rounded_quantity = round(product_group_df["RF_ForecastedQuantity"].values[0], 2)
    fig_dash.add_trace(go.Bar(
        x=[product_group],
        y=product_group_df['RF_ForecastedQuantity'],
        name=product_group,
        hovertemplate=f'{product_group}: {rounded_quantity}<extra></extra>'
    ))

fig_dash.update_layout(
    title=f'Forecasted Export Quantity for {month_names[unique_months[month]]} {unique_years[0]}',
    xaxis_title='Products',
    yaxis_title='Forecasted Quantity',
    barmode='group',
    xaxis=dict(tickangle=-90)
)

st.plotly_chart(fig_dash)
