import os
import json
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# PAGE CONFIGURATION & APPLE DESIGN SYSTEM TOKENS
# ==============================================================================
st.set_page_config(
    page_title="Ekurhuleni Women-Safety Analytics",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

APPLE_FONT = "SF Pro Text, SF Pro Display, system-ui, -apple-system, BlinkMacSystemFont, 'Inter', sans-serif"
APPLE_DISPLAY_FONT = "SF Pro Display, system-ui, -apple-system, BlinkMacSystemFont, 'Inter', sans-serif"

COLORS = {
    "primary": "#0066cc",
    "primary_focus": "#0071e3",
    "primary_on_dark": "#2997ff",
    "ink": "#1d1d1f",
    "body": "#1d1d1f",
    "body_on_dark": "#ffffff",
    "body_muted": "#cccccc",
    "ink_muted_80": "#333333",
    "ink_muted_48": "#7a7a7a",
    "divider_soft": "#f0f0f0",
    "hairline": "#e0e0e0",
    "canvas": "#ffffff",
    "canvas_parchment": "#f5f5f7",
    "surface_pearl": "#fafafc",
    "surface_tile_1": "#272729",
    "surface_tile_2": "#2a2a2c",
    "surface_tile_3": "#252527",
    "surface_black": "#000000",
    "surface_chip_translucent": "#d2d2d7"
}

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    :root {
        --color-primary: #0066cc;
        --color-primary-focus: #0071e3;
        --color-primary-on-dark: #2997ff;
        --color-ink: #1d1d1f;
        --color-body: #1d1d1f;
        --color-body-on-dark: #ffffff;
        --color-body-muted: #cccccc;
        --color-ink-muted-80: #333333;
        --color-ink-muted-48: #7a7a7a;
        --color-divider-soft: #f0f0f0;
        --color-hairline: #e0e0e0;
        --color-canvas: #ffffff;
        --color-canvas-parchment: #f5f5f7;
        --color-surface-pearl: #fafafc;
        --color-surface-tile-1: #272729;
        --color-surface-tile-2: #2a2a2c;
        --color-surface-tile-3: #252527;
        --color-surface-black: #000000;
        --font-display: 'SF Pro Display', system-ui, -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
        --font-text: 'SF Pro Text', system-ui, -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
    }

    /* Global typography & canvas reset */
    html, body, [class*="css"], .stApp {
        font-family: var(--font-text);
        color: var(--color-body);
        background-color: var(--color-canvas);
        font-size: 17px;
        font-weight: 400;
        line-height: 1.47;
        letter-spacing: -0.374px;
        -webkit-font-smoothing: antialiased;
    }

    /* Hide default Streamlit chrome header to let Apple global-nav + sub-nav-frosted lead */
    header[data-testid="stHeader"] {
        background: transparent;
        height: 0px;
    }
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        max-width: 1440px;
    }

    /* Headlines: SF Pro Display weight 600, tight negative tracking, no weight 500 */
    h1, h2, h3, h4 {
        font-family: var(--font-display) !important;
        color: var(--color-ink) !important;
        font-weight: 600 !important;
    }
    h1 {
        font-size: 56px !important;
        line-height: 1.07 !important;
        letter-spacing: -0.28px !important;
    }
    h2 {
        font-size: 40px !important;
        line-height: 1.10 !important;
        letter-spacing: 0px !important;
    }
    h3 {
        font-size: 28px !important;
        line-height: 1.14 !important;
        letter-spacing: 0.196px !important;
    }

    /* Links: single Action Blue (#0066cc) */
    a {
        color: var(--color-primary) !important;
        text-decoration: none;
    }

    /* Component: global-nav (44px true black bar) */
    .apple-global-nav {
        background-color: var(--color-surface-black);
        color: var(--color-body-on-dark);
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 32px;
        margin-left: -3rem;
        margin-right: -3rem;
        font-family: var(--font-text);
        font-size: 12px;
        font-weight: 400;
        line-height: 1.0;
        letter-spacing: -0.12px;
    }
    .apple-global-nav-links {
        display: flex;
        gap: 28px;
        color: var(--color-body-muted);
    }
    .apple-global-nav-links span {
        color: var(--color-body-on-dark);
    }

    /* Component: sub-nav-frosted (52px parchment with backdrop blur) */
    .apple-sub-nav {
        background-color: rgba(245, 245, 247, 0.82);
        backdrop-filter: saturate(180%) blur(20px);
        -webkit-backdrop-filter: saturate(180%) blur(20px);
        border-bottom: 1px solid rgba(0, 0, 0, 0.08);
        height: 52px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 32px;
        margin-left: -3rem;
        margin-right: -3rem;
        margin-bottom: 32px;
    }
    .apple-sub-nav-title {
        font-family: var(--font-display);
        font-size: 21px;
        font-weight: 600;
        line-height: 1.19;
        letter-spacing: 0.231px;
        color: var(--color-ink);
    }
    .apple-sub-nav-actions {
        display: flex;
        align-items: center;
        gap: 16px;
        font-size: 14px;
        letter-spacing: -0.224px;
        color: var(--color-ink-muted-80);
    }
    .apple-pill-cta {
        background-color: var(--color-primary);
        color: #ffffff !important;
        font-family: var(--font-text);
        font-size: 14px;
        font-weight: 400;
        line-height: 1.29;
        letter-spacing: -0.224px;
        border-radius: 9999px;
        padding: 6px 16px;
        display: inline-block;
        transition: transform 0.12s ease;
    }
    .apple-pill-cta:active {
        transform: scale(0.95);
    }
    .apple-pill-secondary {
        background-color: transparent;
        color: var(--color-primary) !important;
        border: 1px solid var(--color-primary);
        font-family: var(--font-text);
        font-size: 14px;
        font-weight: 400;
        line-height: 1.29;
        letter-spacing: -0.224px;
        border-radius: 9999px;
        padding: 5px 15px;
        display: inline-block;
    }

    /* Component: product-tile-light / parchment / dark */
    .apple-hero-tile {
        background-color: var(--color-canvas);
        color: var(--color-ink);
        text-align: center;
        padding: 56px 24px 40px 24px;
        border-radius: 0px;
    }
    .apple-eyebrow {
        font-family: var(--font-text);
        font-size: 14px;
        font-weight: 600;
        line-height: 1.29;
        letter-spacing: -0.224px;
        color: var(--color-primary);
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .apple-hero-headline {
        font-family: var(--font-display);
        font-size: 56px;
        font-weight: 600;
        line-height: 1.07;
        letter-spacing: -0.28px;
        color: var(--color-ink);
        margin: 0 auto 12px auto;
        max-width: 920px;
    }
    .apple-hero-lead {
        font-family: var(--font-display);
        font-size: 28px;
        font-weight: 400;
        line-height: 1.14;
        letter-spacing: 0.196px;
        color: var(--color-ink-muted-80);
        margin: 0 auto 24px auto;
        max-width: 780px;
    }
    .apple-dark-tile {
        background-color: var(--color-surface-tile-1);
        color: var(--color-body-on-dark);
        padding: 48px 36px;
        border-radius: 0px;
        margin: 32px 0;
    }
    .apple-dark-tile h3 {
        color: var(--color-body-on-dark) !important;
        font-size: 34px !important;
        line-height: 1.2 !important;
        letter-spacing: -0.374px !important;
        margin-bottom: 12px;
    }
    .apple-dark-tile p, .apple-dark-tile li {
        color: var(--color-body-muted);
        font-size: 17px;
        line-height: 1.47;
        letter-spacing: -0.374px;
    }
    .apple-dark-tile a, .apple-dark-tile .sky-accent {
        color: var(--color-primary-on-dark) !important;
        font-weight: 600;
    }

    .apple-parchment-tile {
        background-color: var(--color-canvas-parchment);
        color: var(--color-ink);
        padding: 48px 36px;
        border-radius: 0px;
        margin: 32px 0;
    }

    /* Component: store-utility-card (18px radius, 1px #e0e0e0 hairline, 24px padding, zero shadow) */
    .apple-utility-card {
        background-color: var(--color-canvas);
        border: 1px solid var(--color-hairline);
        border-radius: 18px;
        padding: 24px;
        box-shadow: none !important;
        height: 100%;
    }
    .apple-card-caption {
        font-family: var(--font-text);
        font-size: 14px;
        font-weight: 600;
        line-height: 1.29;
        letter-spacing: -0.224px;
        color: var(--color-ink-muted-48);
        margin-bottom: 6px;
    }
    .apple-card-metric {
        font-family: var(--font-display);
        font-size: 40px;
        font-weight: 600;
        line-height: 1.1;
        letter-spacing: 0px;
        color: var(--color-ink);
        margin-bottom: 8px;
    }
    .apple-card-sub {
        font-family: var(--font-text);
        font-size: 14px;
        font-weight: 400;
        line-height: 1.43;
        letter-spacing: -0.224px;
        color: var(--color-primary);
    }

    /* Streamlit native metric override to match store-utility-card */
    div[data-testid="stMetric"] {
        background-color: var(--color-canvas) !important;
        border: 1px solid var(--color-hairline) !important;
        border-radius: 18px !important;
        padding: 24px !important;
        box-shadow: none !important;
    }
    div[data-testid="stMetricLabel"] {
        font-family: var(--font-text) !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: -0.224px !important;
        color: var(--color-ink-muted-48) !important;
    }
    div[data-testid="stMetricValue"] {
        font-family: var(--font-display) !important;
        font-size: 34px !important;
        font-weight: 600 !important;
        letter-spacing: -0.374px !important;
        color: var(--color-ink) !important;
    }
    div[data-testid="stMetricDelta"] {
        color: var(--color-primary) !important;
        font-size: 14px !important;
    }

    /* Sidebar: canvas-parchment (#f5f5f7) with 1px hairline */
    section[data-testid="stSidebar"] {
        background-color: var(--color-canvas-parchment) !important;
        border-right: 1px solid var(--color-hairline) !important;
    }

    /* Tabs styled as Apple pill / clean sub-navigation */
    button[data-baseweb="tab"] {
        font-family: var(--font-text) !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        letter-spacing: -0.224px !important;
        color: var(--color-ink-muted-48) !important;
        padding: 12px 20px !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--color-primary) !important;
    }

    /* Buttons: signature Apple pill (#0066cc, 9999px radius, scale(0.95) active) */
    .stButton > button {
        background-color: var(--color-primary) !important;
        color: #ffffff !important;
        font-family: var(--font-text) !important;
        font-size: 17px !important;
        font-weight: 400 !important;
        border-radius: 9999px !important;
        border: none !important;
        padding: 11px 22px !important;
        box-shadow: none !important;
        transition: transform 0.12s ease !important;
    }
    .stButton > button:active {
        transform: scale(0.95) !important;
    }
    .stButton > button:focus {
        outline: 2px solid var(--color-primary-focus) !important;
    }

    /* Component: footer (Parchment #f5f5f7, fine-print 12px) */
    .apple-footer {
        background-color: var(--color-canvas-parchment);
        color: var(--color-ink-muted-48);
        font-family: var(--font-text);
        font-size: 12px;
        font-weight: 400;
        line-height: 1.43;
        letter-spacing: -0.12px;
        padding: 48px 32px;
        margin-top: 64px;
        margin-left: -3rem;
        margin-right: -3rem;
        border-top: 1px solid var(--color-hairline);
    }
    .apple-footer strong {
        color: var(--color-ink-muted-80);
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


def style_apple_plotly(fig, height=440, dark_tile=False):
    """Apply Apple Design System typography and surface tokens to Plotly figures."""
    bg = COLORS["surface_tile_1"] if dark_tile else COLORS["canvas"]
    txt = COLORS["body_on_dark"] if dark_tile else COLORS["ink"]
    grid = "#3a3a3c" if dark_tile else COLORS["divider_soft"]
    fig.update_layout(
        font=dict(family=APPLE_FONT, size=14, color=txt),
        title_font=dict(family=APPLE_DISPLAY_FONT, size=21, color=txt),
        paper_bgcolor=bg,
        plot_bgcolor=bg,
        height=height,
        margin=dict(l=16, r=16, t=48, b=16),
        xaxis=dict(gridcolor=grid, zerolinecolor=grid, title_font=dict(size=14)),
        yaxis=dict(gridcolor=grid, zerolinecolor=grid, title_font=dict(size=14)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=13))
    )
    return fig


# ==============================================================================
# DATA LOADING
# ==============================================================================
@st.cache_data
def load_dashboard_data():
    station_df = pd.read_csv("ekurhuleni_station_summary.csv")
    quarterly_df = pd.read_csv("ekurhuleni_quarterly_long.csv")
    with open("ekurhuleni_precincts.geojson", "r", encoding="utf-8") as f:
        geojson_data = json.load(f)
    with open("model_evaluation.json", "r", encoding="utf-8") as f:
        model_eval = json.load(f)
    return station_df, quarterly_df, geojson_data, model_eval


station_df, quarterly_df, geojson_data, model_eval = load_dashboard_data()

CATEGORY_LABELS = {
    "Murder": "Murder (Headline Proxy)",
    "Sexual_Offences": "Sexual Offences (Headline Proxy)",
    "Assault_GBH": "Assault GBH (Headline Proxy)",
    "Common_Assault": "Common Assault (Headline Proxy)",
    "Rape": "Rape (Sub-category of Sexual Offences)",
    "Sexual_Assault": "Sexual Assault (Sub-category of Sexual Offences)",
    "Attempted_Murder": "Attempted Murder (Contextual Violent Crime)",
    "Kidnapping": "Kidnapping (Contextual Vulnerability Crime)",
    "Abduction": "Abduction (Contextual Vulnerability Crime)"
}
PRIMARY_PROXY_KEYS = ["Murder", "Sexual_Offences", "Assault_GBH", "Common_Assault"]

# ==============================================================================
# SIDEBAR CONFIGURATOR (PARCHMENT SURFACE)
# ==============================================================================
with st.sidebar:
    st.markdown(
        "<div style='font-size:12px; font-weight:600; color:#0066cc; letter-spacing:-0.12px; text-transform:uppercase;'>TLPR200 / TPRO200</div>"
        "<div style='font-size:21px; font-weight:600; color:#1d1d1f; letter-spacing:0.231px; margin-bottom:4px;'>S. Nombika · 22312280</div>"
        "<div style='font-size:14px; color:#7a7a7a; letter-spacing:-0.224px; margin-bottom:16px;'>City of Ekurhuleni Analytics</div>",
        unsafe_allow_html=True
    )

    all_stations = sorted(station_df["Station"].unique().tolist())
    cluster_filter = st.selectbox(
        "Vulnerability Profile",
        options=["All Ekurhuleni Precincts (39)"] + sorted(station_df["cluster_profile_name"].unique().tolist()),
        index=0
    )
    if cluster_filter == "All Ekurhuleni Precincts (39)":
        default_stations = all_stations
    else:
        default_stations = sorted(
            station_df[station_df["cluster_profile_name"] == cluster_filter]["Station"].unique().tolist()
        )

    selected_stations = st.multiselect(
        "Police Precincts",
        options=all_stations,
        default=default_stations
    )
    if not selected_stations:
        selected_stations = all_stations

    category_mode = st.radio(
        "Crime Category Scope",
        options=["4 Primary Women-Safety Proxy Offences", "Custom Offence Selection"],
        index=0
    )
    if category_mode == "4 Primary Women-Safety Proxy Offences":
        selected_categories = PRIMARY_PROXY_KEYS
    else:
        selected_categories = st.multiselect(
            "Select Offence Categories",
            options=list(CATEGORY_LABELS.keys()),
            default=PRIMARY_PROXY_KEYS,
            format_func=lambda k: CATEGORY_LABELS.get(k, k)
        )
        if not selected_categories:
            selected_categories = PRIMARY_PROXY_KEYS

    ordered_quarters = (
        quarterly_df[["Sort_Key", "Quarter_Short"]]
        .drop_duplicates()
        .sort_values("Sort_Key")["Quarter_Short"]
        .tolist()
    )
    q_start, q_end = st.select_slider(
        "Quarterly Time Span",
        options=ordered_quarters,
        value=(ordered_quarters[0], ordered_quarters[-1])
    )
    start_idx = ordered_quarters.index(q_start)
    end_idx = ordered_quarters.index(q_end)
    selected_quarters = ordered_quarters[start_idx : end_idx + 1]

    st.markdown(
        "<div style='margin-top:24px; padding-top:16px; border-top:1px solid #e0e0e0; font-size:12px; color:#7a7a7a; line-height:1.8;'>"
        "<strong style='color:#1d1d1f;'>Verified Open Sources</strong><br>"
        "<a href='https://www.saps.gov.za/services/crimestats.php' target='_blank'>SAPS Crime Statistics ↗</a><br>"
        "<a href='https://www.saps.gov.za/services/boundary.php' target='_blank'>SAPS Station Boundaries ↗</a><br>"
        "<a href='https://www.openstreetmap.org' target='_blank'>OpenStreetMap (OSMnx) ↗</a>"
        "</div>",
        unsafe_allow_html=True
    )

# ==============================================================================
# APPLY FILTERS
# ==============================================================================
filtered_q_df = quarterly_df[
    (quarterly_df["Station"].isin(selected_stations)) &
    (quarterly_df["Category_Key"].isin(selected_categories)) &
    (quarterly_df["Quarter_Short"].isin(selected_quarters))
].copy()

dyn_station_totals = (
    filtered_q_df.groupby("Station")["Incidents"]
    .sum()
    .reset_index()
    .rename(columns={"Incidents": "filtered_incidents"})
)

filtered_station_df = station_df[station_df["Station"].isin(selected_stations)].merge(
    dyn_station_totals, on="Station", how="left"
)
filtered_station_df["filtered_incidents"] = filtered_station_df["filtered_incidents"].fillna(0)
filtered_station_df["filtered_density"] = (
    filtered_station_df["filtered_incidents"] / filtered_station_df["area_sq_km"]
)

# ==============================================================================
# APPLE GLOBAL-NAV + SUB-NAV-FROSTED + HERO TILE
# ==============================================================================
st.markdown(f"""
<div class="apple-global-nav">
    <div style="font-weight:600; color:#ffffff; letter-spacing:0px;"> Ekurhuleni Public Safety</div>
    <div class="apple-global-nav-links">
        <span>Spatial Hotspots</span>
        <span>Temporal Patterns</span>
        <span>Random Forest ML</span>
        <span>Cluster Profiles</span>
        <span>Prevention</span>
    </div>
    <div style="color:#cccccc;">S. Nombika · 22312280</div>
</div>

<div class="apple-sub-nav">
    <div class="apple-sub-nav-title">Women-Safety Analytics</div>
    <div class="apple-sub-nav-actions">
        <span>{len(selected_stations)} of 39 Precincts</span>
        <span>·</span>
        <span>{q_start} – {q_end}</span>
        <a class="apple-pill-cta" href="https://www.saps.gov.za/services/crimestats.php" target="_blank">SAPS Data</a>
    </div>
</div>

<div class="apple-hero-tile">
    <div class="apple-eyebrow">City of Ekurhuleni · April 2021 – June 2026</div>
    <div class="apple-hero-headline">Spatial concentration. Clear prevention.</div>
    <div class="apple-hero-lead">
        Mapping 21 quarters of violent contact offences, precinct boundaries, and transit corridors across 39 police stations.
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================================================================
# STORE-UTILITY-CARD KPI GRID (18px radius, 1px hairline, zero shadow)
# ==============================================================================
total_inc = int(filtered_station_df["filtered_incidents"].sum())
hotspot_cnt = int(filtered_station_df["Hotspot"].sum())
top_dens_row = filtered_station_df.sort_values("filtered_density", ascending=False).iloc[0]
thresh_val = model_eval["station_model"]["threshold_75_density"]
cv_auc = model_eval["station_model"]["cv_roc_auc"]
sq_auc = model_eval["station_quarter_model"]["test_roc_auc"]

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Recorded Incidents", f"{total_inc:,d}", f"{len(selected_quarters)} Quarters selected")
kpi2.metric("Hotspot Precincts", f"{hotspot_cnt} / {len(filtered_station_df)}", f"≥75th Pct ({thresh_val:.1f}/km²)")
kpi3.metric("Peak Density Station", top_dens_row["Station"], f"{top_dens_row['filtered_density']:.1f} incidents/km²")
kpi4.metric("Station RF ROC-AUC", f"{cv_auc:.4f}", f"5-Fold CV ({model_eval['station_model']['cv_accuracy']:.1%} Acc)")
kpi5.metric("Quarterly RF ROC-AUC", f"{sq_auc:.4f}", f"819 Units ({model_eval['station_quarter_model']['test_accuracy']:.1%} Acc)")

st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

# ==============================================================================
# NAVIGATION TABS
# ==============================================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Spatial Hotspot Map",
    "EDA & Temporal Patterns",
    "Hotspot Classification & Confusion Matrix",
    "Three-Area Comparison & Clustering",
    "Prevention Insights & Limitations"
])

# ------------------------------------------------------------------------------
# TAB 1: SPATIAL HOTSPOT MAP & OVERVIEW
# ------------------------------------------------------------------------------
with tab1:
    col_map, col_rank = st.columns([1.45, 1.0], gap="large")

    with col_map:
        st.markdown("<h3>Precinct Choropleth Map</h3>", unsafe_allow_html=True)
        map_metric = st.selectbox(
            "Spatial Layer",
            options=[
                ("filtered_density", "Filtered Crime Density (Incidents / km²)"),
                ("filtered_incidents", "Filtered Raw Incident Count"),
                ("proxy_crime_density", "21-Quarter Women-Safety Proxy Density (Incidents / km²)"),
                ("transport_density_index", "OSM Transport Infrastructure Density (Transit Stops / km²)"),
                ("RF_Hotspot_Prob", "Random Forest Predicted Hotspot Probability (0.0 – 1.0)"),
                ("Hotspot", "Binary Hotspot Designation (1 = Top 25% Density, 0 = Normal)")
            ],
            format_func=lambda x: x[1]
        )
        metric_col, _ = map_metric
        apple_blue_scale = [[0.0, "#f5f5f7"], [0.35, "#99c2ff"], [0.7, "#0066cc"], [1.0, "#1d1d1f"]]

        map_kwargs = dict(
            data_frame=filtered_station_df,
            geojson=geojson_data,
            locations="match_name",
            featureidkey="properties.match_name",
            color=metric_col,
            hover_name="Station",
            hover_data={
                "match_name": False,
                "cluster_profile_name": True,
                "Hotspot": True,
                "area_sq_km": ":.2f",
                "filtered_incidents": ":,.0f",
                "filtered_density": ":.2f",
                "transport_density_index": ":.2f",
                "poi_count": ":,.0f",
                "RF_Hotspot_Prob": ":.3f"
            },
            color_continuous_scale=apple_blue_scale,
            zoom=9.1,
            center={"lat": -26.21, "lon": 28.28},
            opacity=0.84,
            height=520
        )
        if hasattr(px, "choropleth_map"):
            fig_map = px.choropleth_map(map_style="carto-positron", **map_kwargs)
        else:
            fig_map = px.choropleth_mapbox(mapbox_style="carto-positron", **map_kwargs)

        fig_map.update_layout(
            font=dict(family=APPLE_FONT, size=13, color=COLORS["ink"]),
            paper_bgcolor=COLORS["canvas"],
            margin={"r": 0, "t": 8, "l": 0, "b": 0}
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_rank:
        st.markdown("<h3>Precinct Density Ranking</h3>", unsafe_allow_html=True)
        rank_sort = st.radio(
            "Rank Precincts By",
            options=["Crime Density (Incidents / km²)", "Raw Incident Volume"],
            horizontal=True
        )
        sort_col = "filtered_density" if "Density" in rank_sort else "filtered_incidents"
        top_n_df = filtered_station_df.sort_values(sort_col, ascending=True).tail(15).copy()
        top_n_df["Tier"] = np.where(top_n_df["Hotspot"] == 1, "Hotspot (≥75th Pct)", "Standard Precinct")

        fig_bar = px.bar(
            top_n_df,
            x=sort_col,
            y="Station",
            color="Tier",
            orientation="h",
            color_discrete_map={"Hotspot (≥75th Pct)": COLORS["primary"], "Standard Precinct": "#d2d2d7"},
            labels={
                "filtered_density": "Incidents per km²",
                "filtered_incidents": "Recorded Incidents",
                "Tier": "Designation"
            },
            text_auto=".1f" if sort_col == "filtered_density" else ",.0f",
            height=490
        )
        style_apple_plotly(fig_bar, height=490)
        st.plotly_chart(fig_bar, use_container_width=True)

    with st.expander("View Full Ekurhuleni Precinct Table (39 Stations)", expanded=False):
        display_cols = [
            "Station", "cluster_profile_name", "Hotspot", "RF_Hotspot_Prob",
            "area_sq_km", "poi_count", "transport_poi_count", "transport_density_index",
            "filtered_incidents", "filtered_density", "women_safety_proxy_total", "proxy_crime_density"
        ]
        st.dataframe(
            filtered_station_df[display_cols].sort_values("filtered_density", ascending=False),
            use_container_width=True,
            hide_index=True
        )

# ------------------------------------------------------------------------------
# TAB 2: EXPLORATORY DATA ANALYSIS & TEMPORAL PATTERNS
# ------------------------------------------------------------------------------
with tab2:
    st.markdown("<h3>Temporal Trajectory & Seasonal Rhythm (April 2021 – June 2026)</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.4, 1.0], gap="large")

    with c1:
        q_ts = (
            filtered_q_df.groupby(["Sort_Key", "Quarter_Short", "Category_Key"])["Incidents"]
            .sum()
            .reset_index()
            .sort_values("Sort_Key")
        )
        fig_ts = px.line(
            q_ts,
            x="Quarter_Short",
            y="Incidents",
            color="Category_Key",
            markers=True,
            color_discrete_sequence=[COLORS["primary"], COLORS["ink"], "#2997ff", "#7a7a7a", "#333333"],
            title="Quarterly Recorded Incidents by Offence Category",
            labels={"Quarter_Short": "Quarter", "Incidents": "Recorded Incidents", "Category_Key": "Offence"},
            height=430
        )
        fig_ts.update_xaxes(tickangle=45)
        style_apple_plotly(fig_ts, height=430)
        st.plotly_chart(fig_ts, use_container_width=True)

    with c2:
        season_df = (
            filtered_q_df.groupby(["Quarter_Short", "Season"])["Incidents"]
            .sum()
            .reset_index()
            .groupby("Season")["Incidents"]
            .mean()
            .reindex([
                "Autumn/Winter (Apr-Jun)",
                "Winter/Spring (Jul-Sep)",
                "Summer/Festive (Oct-Dec)",
                "Late Summer (Jan-Mar)"
            ])
            .reset_index()
        )
        fig_season = px.bar(
            season_df,
            x="Season",
            y="Incidents",
            color="Season",
            color_discrete_map={
                "Autumn/Winter (Apr-Jun)": "#d2d2d7",
                "Winter/Spring (Jul-Sep)": "#7a7a7a",
                "Summer/Festive (Oct-Dec)": COLORS["primary"],
                "Late Summer (Jan-Mar)": COLORS["ink"]
            },
            text_auto=",.0f",
            title="Mean Quarterly Incidents by Season",
            labels={"Incidents": "Mean Quarterly Incidents"},
            height=430
        )
        fig_season.update_layout(showlegend=False)
        style_apple_plotly(fig_season, height=430)
        st.plotly_chart(fig_season, use_container_width=True)

    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    c3, c4 = st.columns(2, gap="large")

    with c3:
        fig_scat = px.scatter(
            filtered_station_df,
            x="transport_density_index",
            y="filtered_density",
            size="poi_count",
            color="cluster_profile_name",
            hover_name="Station",
            trendline="ols",
            color_discrete_sequence=[COLORS["primary"], COLORS["ink"], "#7a7a7a"],
            title="Transport Stop Density vs. Crime Density",
            labels={
                "transport_density_index": "Transport Density Index (Stops / km²)",
                "filtered_density": "Crime Density (Incidents / km²)",
                "cluster_profile_name": "Profile"
            },
            height=430
        )
        style_apple_plotly(fig_scat, height=430)
        st.plotly_chart(fig_scat, use_container_width=True)

    with c4:
        corr_vars = [
            "proxy_crime_density", "women_safety_proxy_total", "transport_density_index",
            "poi_density_index", "area_sq_km", "shape_compactness", "adjacent_precincts", "dist_to_metro_center_km"
        ]
        corr_mat = filtered_station_df[corr_vars].corr().round(2)
        fig_corr = px.imshow(
            corr_mat,
            text_auto=True,
            color_continuous_scale=[[0.0, "#1d1d1f"], [0.5, "#f5f5f7"], [1.0, "#0066cc"]],
            zmin=-1,
            zmax=1,
            title="Spatial & Crime Feature Correlation Matrix",
            height=430
        )
        style_apple_plotly(fig_corr, height=430)
        st.plotly_chart(fig_corr, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 3: ML HOTSPOT CLASSIFICATION & CONFUSION MATRIX
# ------------------------------------------------------------------------------
with tab3:
    st.markdown("<h3>Random Forest Hotspot Classification</h3>", unsafe_allow_html=True)

    model_choice = st.radio(
        "Evaluation Scope",
        options=[
            "Model A: Precinct-Level Classifier (N = 39 Stations, 5-Fold Cross-Validation)",
            "Model B: Spatio-Temporal Station-Quarter Classifier (N = 819 Station-Quarter Units)"
        ],
        horizontal=True
    )

    if "Model A" in model_choice:
        m_data = model_eval["station_model"]
        acc_val, auc_val = m_data["cv_accuracy"], m_data["cv_roc_auc"]
        prec_val, rec_val, f1_val = m_data["cv_precision"], m_data["cv_recall"], m_data["cv_f1"]
        cm_arr = np.array(m_data["confusion_matrix"])
        subtitle_cm = f"5-Fold CV Confusion Matrix (N = 39)"
    else:
        m_data = model_eval["station_quarter_model"]
        acc_val, auc_val = m_data["test_accuracy"], m_data["test_roc_auc"]
        prec_val, rec_val, f1_val = m_data["test_precision"], m_data["test_recall"], m_data["test_f1"]
        cm_arr = np.array(m_data["confusion_matrix"])
        subtitle_cm = f"Test Confusion Matrix (N = {m_data['n_test']})"

    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Accuracy", f"{acc_val:.2%}")
    m2.metric("ROC-AUC Score", f"{auc_val:.4f}")
    m3.metric("Precision", f"{prec_val:.2%}")
    m4.metric("Recall (Sensitivity)", f"{rec_val:.2%}")
    m5.metric("F1-Score", f"{f1_val:.4f}")

    col_cm, col_roc, col_imp = st.columns(3, gap="large")

    with col_cm:
        fig_cm = px.imshow(
            cm_arr,
            text_auto=True,
            color_continuous_scale=[[0.0, "#f5f5f7"], [1.0, "#0066cc"]],
            x=["Pred: Normal (0)", "Pred: Hotspot (1)"],
            y=["Actual: Normal (0)", "Actual: Hotspot (1)"],
            title=subtitle_cm,
            height=400
        )
        fig_cm.update_traces(textfont_size=18)
        fig_cm.update_coloraxes(showscale=False)
        style_apple_plotly(fig_cm, height=400)
        st.plotly_chart(fig_cm, use_container_width=True)

    with col_roc:
        fig_roc = go.Figure()
        fig_roc.add_trace(go.Scatter(
            x=model_eval["station_model"]["roc_curve"]["fpr"],
            y=model_eval["station_model"]["roc_curve"]["tpr"],
            mode="lines",
            name=f"Model A: 39 Stations (AUC = {model_eval['station_model']['cv_roc_auc']:.3f})",
            line=dict(color=COLORS["primary"], width=3)
        ))
        fig_roc.add_trace(go.Scatter(
            x=model_eval["station_quarter_model"]["roc_curve"]["fpr"],
            y=model_eval["station_quarter_model"]["roc_curve"]["tpr"],
            mode="lines",
            name=f"Model B: 819 Units (AUC = {model_eval['station_quarter_model']['test_roc_auc']:.3f})",
            line=dict(color=COLORS["ink"], width=3)
        ))
        fig_roc.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1], mode="lines", name="Baseline (0.500)",
            line=dict(color="#7a7a7a", dash="dash")
        ))
        fig_roc.update_layout(
            title="ROC Curve Comparison",
            xaxis_title="False Positive Rate",
            yaxis_title="True Positive Rate (Recall)",
            legend=dict(x=0.28, y=0.12)
        )
        style_apple_plotly(fig_roc, height=400)
        st.plotly_chart(fig_roc, use_container_width=True)

    with col_imp:
        imp_dict = m_data["feature_importances"]
        imp_df = pd.DataFrame({
            "Feature": list(imp_dict.keys()),
            "Importance": list(imp_dict.values())
        }).sort_values("Importance", ascending=True)
        fig_imp = px.bar(
            imp_df,
            x="Importance",
            y="Feature",
            orientation="h",
            text_auto=".3f",
            title="Feature Importance (Non-Leaking)",
            color_discrete_sequence=[COLORS["primary"]],
            height=400
        )
        style_apple_plotly(fig_imp, height=400)
        st.plotly_chart(fig_imp, use_container_width=True)

    st.markdown("""
    <div class="apple-parchment-tile">
        <h3>Threshold Justification & Leakage Prevention</h3>
        <p>
            Precinct land sizes across Ekurhuleni range from <strong>8.49 km² (Tokoza)</strong> and <strong>8.95 km² (Tembisa South)</strong> to <strong>385.37 km² (Springs)</strong>. Dividing incident totals by land area (crimes/km²) and flagging the <strong>75th percentile (≥ 220.78 incidents/km²)</strong> isolates the 10 most densely affected precincts. All crime count and crime rate columns are excluded from the feature matrix <em>X</em> so the Random Forest predicts hotspot status strictly from physical geometry and public transport infrastructure.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# TAB 4: 3-HOTSPOT DEEP COMPARISON & CLUSTERING
# ------------------------------------------------------------------------------
with tab4:
    st.markdown("<h3>PCA + K-Means Vulnerability Profiles & Three-Area Comparison</h3>", unsafe_allow_html=True)

    default_focus = ["Tembisa", "Katlehong", "Kempton Park"]
    comp_stations = st.multiselect(
        "Focus Precincts for Side-by-Side Comparison",
        options=all_stations,
        default=default_focus,
        max_selections=4
    )
    if not comp_stations:
        comp_stations = default_focus

    comp_df = station_df[station_df["Station"].isin(comp_stations)].copy()
    st.dataframe(
        comp_df[[
            "Station", "cluster_profile_name", "Hotspot", "RF_Hotspot_Prob",
            "area_sq_km", "poi_count", "transport_poi_count", "transport_density_index",
            "Murder", "Sexual_Offences", "Assault_GBH", "Common_Assault",
            "women_safety_proxy_total", "proxy_crime_density"
        ]],
        use_container_width=True,
        hide_index=True
    )

    col_pca, col_comp_bar = st.columns(2, gap="large")

    with col_pca:
        fig_pca = px.scatter(
            station_df,
            x="PCA1",
            y="PCA2",
            color="cluster_profile_name",
            symbol="Hotspot",
            size="women_safety_proxy_total",
            hover_name="Station",
            text="Station",
            color_discrete_sequence=[COLORS["primary"], COLORS["ink"], "#7a7a7a"],
            title=f"PCA + K-Means Clusters (Silhouette = {model_eval['clustering']['silhouette_score']:.3f})",
            height=450
        )
        fig_pca.update_traces(textposition="top center", textfont_size=10)
        style_apple_plotly(fig_pca, height=450)
        st.plotly_chart(fig_pca, use_container_width=True)

    with col_comp_bar:
        comp_melt = comp_df.melt(
            id_vars=["Station"],
            value_vars=PRIMARY_PROXY_KEYS,
            var_name="Offence_Category",
            value_name="Incidents"
        )
        fig_comp = px.bar(
            comp_melt,
            x="Station",
            y="Incidents",
            color="Offence_Category",
            barmode="group",
            color_discrete_sequence=[COLORS["ink"], COLORS["primary"], "#2997ff", "#d2d2d7"],
            text_auto=",.0f",
            title="21-Quarter Offence Breakdown (Tembisa, Katlehong, Kempton Park)",
            height=450
        )
        style_apple_plotly(fig_comp, height=450)
        st.plotly_chart(fig_comp, use_container_width=True)

    comp_q_ts = (
        quarterly_df[
            (quarterly_df["Station"].isin(comp_stations)) &
            (quarterly_df["Category_Key"].isin(PRIMARY_PROXY_KEYS))
        ]
        .groupby(["Sort_Key", "Quarter_Short", "Station"])["Incidents"]
        .sum()
        .reset_index()
        .sort_values("Sort_Key")
    )
    fig_comp_ts = px.line(
        comp_q_ts,
        x="Quarter_Short",
        y="Incidents",
        color="Station",
        markers=True,
        color_discrete_sequence=[COLORS["primary"], COLORS["ink"], "#7a7a7a", "#2997ff"],
        title="Quarterly Trajectory Across Selected Focus Precincts (2021–2026)",
        height=390
    )
    fig_comp_ts.update_xaxes(tickangle=45)
    style_apple_plotly(fig_comp_ts, height=390)
    st.plotly_chart(fig_comp_ts, use_container_width=True)

# ------------------------------------------------------------------------------
# TAB 5: PREVENTION INSIGHTS, LIMITATIONS & ETHICS (ALTERNATING LIGHT/DARK TILES)
# ------------------------------------------------------------------------------
with tab5:
    st.markdown("""
    <div class="apple-dark-tile">
        <div style="font-size:14px; font-weight:600; color:#2997ff; letter-spacing:-0.224px; text-transform:uppercase; margin-bottom:8px;">
            Targeted Prevention Planning
        </div>
        <h3>Three structural profiles. Three tailored interventions.</h3>
        <p>
            <strong>1. Compact High-Density Township Hotspots (Tembisa, Katlehong, Daveyton, Vosloorus, Tokoza):</strong><br>
            Compact land footprints (8.5–28 km²) experiencing intense concentrations of Assault GBH, Common Assault, and Sexual Offences (&gt;220 incidents/km²) that surge every October–March. Prioritise <span class="sky-accent">high-mast solar street lighting</span> along informal walkways, weekend evening visible policing during Q3/Q4, and mobile Victim Friendly Rooms (VFRs).
        </p>
        <p>
            <strong>2. Commercial &amp; Transit Commuter Hubs (Kempton Park, Germiston, Boksburg, Benoni):</strong><br>
            Large commercial footprints (40–98 km²) with the highest concentration of rail platforms, bus stops, taxi ranks, and shops (676 POIs in Kempton Park), where Common Assault accounts for 58.3% of proxy offences. Focus on <span class="sky-accent">Crime Prevention Through Environmental Design (CPTED)</span> around rail/taxi interchanges, securing derelict CBD buildings, CCTV, and dawn/dusk commuter safety marshals.
        </p>
        <p>
            <strong>3. Sprawling Peri-Urban &amp; Outer Precincts (Springs, Brakpan, Nigel, Devon):</strong><br>
            Geographically vast precincts (160–385 km²) with low overall spatial density (12.6/km² in Springs) where incidents cluster in isolated pockets. Deploy <span class="sky-accent">sector-based mobile patrol routing</span> and satellite reporting kiosks to cut emergency response times.
        </p>
    </div>

    <div class="apple-parchment-tile">
        <div style="font-size:14px; font-weight:600; color:#0066cc; letter-spacing:-0.224px; text-transform:uppercase; margin-bottom:8px;">
            Critical Interpretation &amp; Data Integrity
        </div>
        <h3 style="font-size:34px; margin-bottom:12px;">Association is not causation.</h3>
        <p style="font-size:17px; color:#333333; line-height:1.47;">
            My analysis shows a positive association between <code>transport_density_index</code> and <code>proxy_crime_density</code> (r = +0.58) and a negative association with <code>area_sq_km</code> (r = -0.50). <strong>Public transport stops and compact residential neighbourhoods do not cause violence.</strong> Rather, transit interchanges and dense settlements are places where thousands of daily pedestrian commutes converge with environmental risk factors such as unlit pathways and long walks at dawn or dusk.
        </p>
        <p style="font-size:17px; color:#333333; line-height:1.47; margin-top:16px;">
            <strong>Key Limitations:</strong> (1) Official SAPS station spreadsheets do not disaggregate victims by sex, so the four-offence proxy index includes male victims in aggregate counts; (2) gender-based violence and domestic assault remain systematically under-reported; (3) static boundary maps do not separate night-time residential populations from daytime commuter inflows in hubs like Kempton Park.
        </p>
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# APPLE PARCHMENT FOOTER
# ==============================================================================
st.markdown("""
<div class="apple-footer">
    <strong>TLPR200 / TPRO200 Supplementary Examination 2026</strong> · Student: S. Nombika (22312280) · City of Ekurhuleni Women-Safety Hotspot &amp; Pattern Analytics.<br>
    Data sourced from official South African Police Service (SAPS) Quarterly Crime Statistics (2021–2026), SAPS Police Station Boundary GIS Shapefiles (v1.4.2), and OpenStreetMap (OSMnx). All hotspot designations are analytical models intended strictly for preventative resource allocation.
</div>
""", unsafe_allow_html=True)
