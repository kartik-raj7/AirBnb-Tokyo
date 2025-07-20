from sqlalchemy import create_engine, text
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium
import streamlit as st
from folium import CircleMarker
import geopandas as gpd
from branca.colormap import LinearColormap

st.set_page_config(page_title="Tokyo Airbnb EDA", layout="wide")

st.title("🏠 Tokyo Airbnb Exploratory Data Analysis")

st.subheader("🏠 Tokyo Airbnb - Dataset Overview")

@st.cache_data
def load_data():
    df = pd.read_csv("listings.csv")  
    return df

df = load_data()

st.subheader("🔍 Basic Info")
st.write(f"**Number of rows:** {df.shape[0]}")
st.write(f"**Number of columns:** {df.shape[1]}")

st.subheader("📄 Preview of Listings")
st.dataframe(df.head(20), use_container_width=True)

df_counts = pd.read_csv("neighbourhood_counts.csv")
df_map = pd.read_csv("neighbourhood_listings.csv")

col1, col2 = st.columns([3, 4])

with col1:
    view_option = st.selectbox(
        "🧭 View:",
        [
            "📊 Bar Chart (Listings per Neighbourhood)",
            "🗺️ Map View (Listing Clusters)"
        ]
    )

if view_option == "📊 Bar Chart (Listings per Neighbourhood)":
    st.subheader("🏘️ Distribution of Listings by Neighbourhood")
    fig = px.bar(
        df_counts.sort_values("listing_count", ascending=True),
        x="listing_count",
        y="neighbourhood",
        orientation='h',
        color="listing_count",
        color_continuous_scale="Reds",
        labels={"listing_count": "Number of Listings", "neighbourhood": "Neighbourhood"},
        title="Listings by Normalized Neighbourhood"
    )
    fig.update_layout(height=500,width=800)
    st.plotly_chart(fig, use_container_width=True)

elif view_option == "🗺️ Map View (Listing Clusters)":
    st.subheader("📍 Listings Clustered on Tokyo Map")
    locations = df_map[['latitude', 'longitude']].dropna().values.tolist()
    m = folium.Map(location=[35.6895, 139.6917], zoom_start=11.5, tiles='CartoDB positron')
    FastMarkerCluster(data=locations).add_to(m)
    st_data = st_folium(m, width=800, height=500)

import pandas as pd
import streamlit as st
import plotly.express as px

df_flagged = pd.read_csv("non_compliant_listings.csv")

st.header("🚨 Licensing & Compliance Check")

total = len(df)
flagged = len(df_flagged)
compliant = total - flagged

compliance_data = pd.DataFrame({
    'Status': ['Compliant', 'Potentially Non-Compliant'],
    'Count': [compliant, flagged]
})

st.subheader("📊 Compliance Distribution")
fig = px.pie(
    compliance_data,
    values='Count',
    names='Status',
    color_discrete_sequence=["light blue", "red"] 
)
fig.update_traces(textinfo='percent+label')
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
These listings have a **Minpaku license** (starting with 'M') and are available for more than **180 days per year** —  yet they are **missing a smoke alarm** in their listed amenities.  

            Such listings may be Non-compliant with safety or regulatory requirements.
""")

gdf = gpd.read_file("avg_price_neighbourhood.geojson")
gdf = gdf[~gdf['geometry'].isnull()]
gdf.crs = "EPSG:4326"

color_scale = LinearColormap(['yellow', 'red'],
                             vmin=gdf['price'].min(),
                             vmax=gdf['price'].max())

def get_color(feature):
    value = feature['properties'].get('price')
    return 'gray' if value is None else color_scale(value)

st.subheader("🗺️ Choropleth Map of Average Price per Neighbourhood")
m = folium.Map(location=[35.6895, 139.6917], zoom_start=11, tiles='CartoDB positron')

folium.GeoJson(
    data=gdf.__geo_interface__,
    name='Neighborhoods',
    tooltip=folium.GeoJsonTooltip(
        fields=['neighbourhood', 'price', 'avg_review_score'],
        aliases=['Neighbourhood', 'Average Price', 'Avg Rating']
    ),
    style_function=lambda feature: {
        'fillColor': get_color(feature),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    },
    highlight_function=lambda feature: {
        'weight': 2,
        'fillColor': get_color(feature),
        'fillOpacity': 0.8
    }
).add_to(m)

st_folium(m, width=800, height=600)

st.header("📈 Review Trends Over Years")
st.markdown("""
This chart shows the number of listings that received reviews each year.  
It highlights the **impact of COVID-19 in 2020–2021**, followed by a **recovery in 2022 and beyond**.
""")

yearly_reviews = pd.read_csv('yearly_reviews.csv')
fig = px.line(
    yearly_reviews,
    x='review_year',
    y='review_count',
    markers=True,
    title='Review Trends Over the Years',
    labels={'review_year': 'Year', 'review_count': 'Number of Reviews'},
)

fig.update_traces(line=dict(color='royalblue', width=3))
fig.update_layout(
    xaxis=dict(dtick=1),
    yaxis_title='Number of Reviews',
    xaxis_title='Year',
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)

st.header("Top 10 Hosts by Total Reviews")
df_hosts = pd.read_csv('top_hosts.csv')
fig = px.bar(
    df_hosts, 
    x='host_name', 
    y='total_reviews', 
    color='avg_rating',
    hover_data=['total_listings', 'avg_rating', 'host_is_superhost'],
    labels={
        'total_reviews': 'Number of Reviews', 
        'host_name': 'Host',
        'avg_rating': 'Avg Rating',
        'host_is_superhost': 'Superhost'
    }
)

fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

st.header("💎 Best Value Listings in Tokyo")
top_listings = pd.read_csv("top_listings.csv")
lats = top_listings['latitude'].tolist()
lons = top_listings['longitude'].tolist()
locations = list(zip(lats, lons))

map1 = folium.Map(location=[35.6895, 139.6917], zoom_start=11.5,tiles='CartoDB positron')
FastMarkerCluster(data=locations).add_to(map1)
st_folium(map1, width=800, height=500)