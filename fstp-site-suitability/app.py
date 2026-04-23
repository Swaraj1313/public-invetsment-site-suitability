# =========================
# SECTION 1 — IMPORTS
# =========================
import streamlit as st
import plotly.express as px


# =========================
# SECTION 2 — SIDEBAR CONTROLS (USER INPUTS)
# =========================

# Move controls to sidebar (clean UI)
st.sidebar.header("Controls")

# --- Flow Selector ---
flow_option = st.sidebar.selectbox(
    "Select Flow",
    ["Exports", "Imports"],
    key="flow_selector"
)

flow_map = {
    "Exports": "EXP",
    "Imports": "IMP"
}
selected_flow = flow_map[flow_option]


# --- Year Selector ---
year = st.sidebar.selectbox(
    "Select Year",
    [2005, 2010, 2015, 2020, 2023],
    key="year_selector"
)


# --- Reporting Country Selector ---
country_map = {
    "India": "IND",
    "United States": "USA",
    "United Kingdom": "GBR",
    "China": "CHN",
    "Germany": "DEU",
    "Singapore": "SGP",
    "United Arab Emirates": "ARE"
}

country_name = st.sidebar.selectbox(
    "Select Reporting Country",
    list(country_map.keys()),
    key="country_selector"
)

selected_country = country_map[country_name]

# --- Region Selector ---
region_option = st.sidebar.selectbox(
    "Select Region",
    ["Africa", "LAC", "Asia", "Europe", "World"],
    key="region_selector"
)
# --- Sector Selector ---
sector_map = {
    "Total Services": "S",
    "Manufacturing Services": "SA",
    "Maintenance & Repair": "SB",
    "Transport": "SC",
    "Travel": "SD",
    "Construction": "SE",
    "Insurance & Pension": "SF",
    "Financial Services": "SG",
    "Intellectual Property": "SH",
    "ICT Services": "SI",
    "Business Services": "SJ",
    "Cultural & Recreational": "SK"
}

sector_name = st.sidebar.selectbox(
    "Select Sector",
    list(sector_map.keys()),
    key="sector_selector"
)

selected_sector = sector_map[sector_name]

# =========================
# SECTION 3 — TITLE & CONTEXT
# =========================
st.title("My Services Trade Data Explorer")

st.subheader(f"{flow_option} | {country_name} | {sector_name} | {year}")
st.caption("Values in USD Millions (OECD Balanced Trade in Services-BaTIS Data)")

# =========================
# SECTION 4 — DATABASE CONNECTION
# =========================

# (Handled via cached connection in Section 6)

# =========================
# SECTION 5 — REGION FILTER (CURRENTLY 3 Regions HARDCODED)
# =========================
# Region definitions
africa = (
    'DZA','AGO','BEN','BWA','BFA','BDI','CMR','CPV','CAF','TCD','COM','CIV','COD','DJI','EGY','GNQ','ERI','SWZ',
    'ETH','GAB','GMB','GHA','GIN','GNB','KEN','LSO','LBR','LBY','MDG','MWI','MLI','MUS','MAR','MOZ','NAM','NER',
    'NGA','COG','RWA','STP','SEN','SYC','SLE','SOM','ZAF','SSD','SDN','TZA','TGO','TUN','UGA','ZMB','ZWE','MRT'
)

lac = (
    'ATG','ARG','BHS','BRB','BLZ','BOL','BRA','CHL','COL','CRI','CUB','DMA','DOM','ECU','SLV','GRD','GTM',
    'GUY','HTI','HND','JAM','NIC','PAN','PRY','PER','KNA','LCA','VCT','SUR','TTO','URY','VEN',
    'ABW','AIA','BMU','CUW','FLK','GRL','MSR','SXM'
)

asia = (
    'AFG','ARM','AUS','AZE','BGD','BTN','BRN','KHM','CHN','FJI','GEO','HKG','IND','IDN','JPN','KAZ','KIR',
    'KOR','KGZ','LAO','MYS','MDV','MHL','FSM','MNG','MMR','NRU','NPL','NZL','PAK','PLW','PNG','PHL','WSM',
    'SGP','SLB','LKA','TWN','TJK','THA','TLS','TON','TKM','TUV','UZB','VUT','VNM'
)

europe = (
    'ALB','AND','AUT','BEL','BIH','BGR','HRV','CYP','CZE','DNK','EST','FIN','FRA','DEU','GRC','HUN','ISL',
    'IRL','ITA','LVA','LIE','LTU','LUX','MLT','MDA','MCO','MNE','NLD','MKD','NOR','POL','PRT','ROU','SMR',
    'SRB','SVK','SVN','ESP','SWE','CHE','UKR'
)
# Select region dynamically
if region_option == "Africa":
    selected_region = africa
elif region_option == "LAC":
    selected_region = lac
elif region_option == "Asia":
    selected_region = asia
elif region_option == "Europe":
    selected_region = europe
else:
    selected_region = None
# =========================
#Ensure you have this above the query
# =========================

region_filter = ""
if selected_region is not None:
    region_filter = f"AND Partner IN {selected_region}"

# =========================
# SECTION 6 — DATA FILTERING (CACHED)
# =========================

@st.cache_resource
def get_connection():
    import duckdb
    con = duckdb.connect()
    return con

con = get_connection()

# --- S3 CONNECTION SETTINGS ---
con.execute("""
SET s3_region='ap-south-1';
SET s3_access_key_id='YOUR_ACCESS_KEY';
SET s3_secret_access_key='YOUR_SECRET_KEY';
""")

# --- MAIN QUERY ---
df_map = con.execute(f"""
SELECT 
    Partner,
    SUM(Final_value) AS exports
FROM read_parquet('s3://services-trade-demo1/services-data-parquets/batis_clean.parquet')
WHERE Reporter = '{selected_country}'
AND Flow = '{selected_flow}'
AND Item_code = '{selected_sector}'
AND Year = {year}
{region_filter}
GROUP BY Partner
""").fetchdf()

df_top5 = df_map.sort_values("exports", ascending=False).head(5)

# =========================
# SECTION 7 — CHOROPLETH MAP (BASE LAYER)
# =========================

fig = px.choropleth(
    df_map,
    locations="Partner",
    color="exports",
    hover_name="Partner",
    color_continuous_scale="Blues",
)

# =========================
# SECTION 7b — ADD TOP 5 BUBBLES (ANALYTICAL LAYER)
# =========================

# --- Safe scaling for bubble sizes ---
max_val = df_top5["exports"].max()

if max_val > 0:
    sizes = df_top5["exports"] / max_val * 40
else:
    sizes = [10] * len(df_top5)  # fallback size to avoid crash

# --- Add bubbles ---
fig.add_scattergeo(
    locations=df_top5["Partner"],
    locationmode="ISO-3",
    text=df_top5["Partner"],
    customdata=df_top5["exports"],
    marker=dict(
        size=sizes,
        color="red",
        line=dict(width=2, color="black"),
        opacity=0.85
    ),
    name="Top 5 Partners",
    hovertemplate="<b>%{text}</b><br>Exports: %{customdata:,.2f}<extra></extra>"
)

# =========================
# SECTION 7c — DYNAMIC MAP SCOPE
# =========================

if region_option == "Africa":
    fig.update_geos(scope='africa')

elif region_option == "Asia":
    fig.update_geos(scope='asia')

elif region_option == "Europe":
    fig.update_geos(scope='europe')

elif region_option == "LAC":
    fig.update_geos(
        scope='world',
        center=dict(lat=-15, lon=-60),
        projection_scale=2.5
    )

else:
    fig.update_geos(scope='world')

# =========================
# SECTION 7d — MAP STYLING
# =========================

fig.update_geos(
    showcountries=True,
    countrycolor="black",
    showcoastlines=True,
    coastlinecolor="black",
    resolution=50
)

fig.update_layout(
    height=750,
    margin={"r":0, "t":0, "l":0, "b":0}
)

# =========================
# DISPLAY
# =========================

st.plotly_chart(fig, use_container_width=True)

