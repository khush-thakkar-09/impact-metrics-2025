import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="India Air Quality – Impact Metrics Dashboard",
    layout="wide",
)

components.html(
    """
    <script>
      const root = parent.document.documentElement;

      function move(e){
        root.style.setProperty('--mx', e.clientX + 'px');
        root.style.setProperty('--my', e.clientY + 'px');
      }

      window.addEventListener('mousemove', move, {passive:true});
    </script>
    """,
    height=0,
)

st.markdown(
    """
    <style>
    html { scroll-behavior: smooth; }

    :root{
        --mx: 50vw;
        --my: 50vh;
    }

    /* GLOBAL BACKGROUND (default for task pages) */
    [data-testid="stAppViewContainer"]{
      position: relative;
      background:
        radial-gradient(900px 600px at 10% 10%, rgba(99,102,241,0.18), transparent 60%),
        radial-gradient(800px 520px at 90% 30%, rgba(56,189,248,0.14), transparent 55%),
        radial-gradient(900px 700px at 50% 95%, rgba(34,197,94,0.10), transparent 60%),
        linear-gradient(180deg, #020617 0%, #020617 55%, #01030a 100%);
      overflow: hidden;
    }

    /* interactive glow follows cursor */
    [data-testid="stAppViewContainer"]::before{
      content:"";
      position:absolute; inset:-2px;
      background:
        radial-gradient(650px 650px at var(--mx) var(--my),
          rgba(99,102,241,0.22),
          rgba(56,189,248,0.12) 35%,
          transparent 70%);
      pointer-events:none;
      mix-blend-mode: screen;
      transition: background 0.05s linear;
    }

    /* noise overlay */
    [data-testid="stAppViewContainer"]::after{
      content:"";
      position:absolute; inset:0;
      background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)' opacity='.18'/%3E%3C/svg%3E");
      opacity: 0.08;
      mix-blend-mode: overlay;
      pointer-events:none;
    }

    /* ensure your content stays above the background layers */
    .block-container{
        position: relative;
        z-index: 1;
        max-width: 1200px;
        margin: 0 auto;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617 0%, #020617 40%, #0b1120 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.4);
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #e5e7eb !important;
    }

    /* Typography */
    h1, h2, h3, h4, h5 {
        color: #f9fafb !important;
        letter-spacing: 0.03em;
    }

    p, li {
        color: #e5e7eb;
        font-size: 0.97rem;
    }

    label[data-baseweb="radio"] > div {
        color: #e5e7eb !important;
        font-size: 0.95rem !important;
    }

    /* YOUR GRAPH BOXES (THIS IS WHAT WENT MISSING) */
    .element-container:has(.js-plotly-plot),
    .element-container:has(canvas),
    .element-container:has(.stPlotlyChart),
    .element-container:has(.stpyplot) {
        padding: 1.1rem 1.2rem;
        border-radius: 1rem;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(148, 163, 184, 0.35);
        box-shadow: 0 18px 35px rgba(15, 23, 42, 0.75);
        margin-bottom: 1.4rem;
    }

    /* ---------------------------
       INTRO LANDING PAGE OVERRIDES
    --------------------------- */

    body.page-intro [data-testid="stAppViewContainer"]{
      background:
        radial-gradient(1100px 700px at 50% 20%, rgba(99,102,241,0.28), transparent 60%),
        radial-gradient(900px 600px at 80% 35%, rgba(56,189,248,0.18), transparent 55%),
        radial-gradient(900px 700px at 20% 80%, rgba(34,197,94,0.14), transparent 60%),
        linear-gradient(180deg, #020617 0%, #020617 45%, #01030a 100%);
    }

    body.page-intro [data-testid="stAppViewContainer"]::before{
      background:
        radial-gradient(780px 780px at var(--mx) var(--my),
          rgba(99,102,241,0.30),
          rgba(56,189,248,0.16) 35%,
          transparent 72%);
      opacity: 0.85;
    }

    body.page-intro .block-container{
      max-width: 980px;
      padding-top: 3.2rem;
    }

    .hero-kicker{
      font-size: 1.05rem;
      color: #cbd5e1;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 0.8rem;
    }
    .hero-title{
      font-size: 3.2rem;
      line-height: 1.05;
      margin: 0;
    }
    .hero-subtitle{
      font-size: 1.15rem;
      color: #cbd5e1;
      margin-top: 0.9rem;
      max-width: 62ch;
    }

    .hero-cards{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 0.9rem;
      margin-top: 1.6rem;
    }
    .hero-card{
      padding: 1rem 1.05rem;
      border-radius: 1rem;
      background: rgba(15, 23, 42, 0.72);
      border: 1px solid rgba(148, 163, 184, 0.28);
      box-shadow: 0 18px 35px rgba(15, 23, 42, 0.55);
    }
    .hero-card .k{
      font-size: 0.82rem;
      color: #94a3b8;
      margin-bottom: 0.25rem;
    }
    .hero-card .v{
      font-size: 1.55rem;
      font-weight: 700;
      color: #f8fafc;
    }

    @media (max-width: 1100px){
      .hero-cards{ grid-template-columns: repeat(2, minmax(0, 1fr)); }
      .hero-title{ font-size: 2.6rem; }
    }
    @media (max-width: 640px){
      .hero-cards{ grid-template-columns: 1fr; }
      .hero-title{ font-size: 2.2rem; }
    }

    </style>
    """,
    unsafe_allow_html=True
)


def set_page_class(page_name: str):
    components.html(
        f"""
        <script>
          const body = parent.document.body;
          body.classList.remove("page-intro", "page-task");
          body.classList.add("{page_name}");
        </script>
        """,
        height=0,
    )

def style_plotly(fig, title=None):
    fig.update_layout(
        title=dict(text=title, font=dict(size=24)),
        font=dict(size=14),
        legend=dict(font=dict(size=12)),
        margin=dict(l=40, r=40, t=80, b=40)
    )
    return fig

@st.cache_data
def load_data():
    stations_df = pd.read_csv("https://huggingface.co/datasets/khush-thakkar-09/station_hour/resolve/main/stations.csv",low_memory=False)
    
    station_day_df = pd.read_csv("https://huggingface.co/datasets/khush-thakkar-09/station_hour/resolve/main/station_day.csv",low_memory=False)
    
    city_day_df = pd.read_csv("https://huggingface.co/datasets/khush-thakkar-09/station_hour/resolve/main/city_day.csv",low_memory=False)
    
    city_hour_df = pd.read_csv("https://huggingface.co/datasets/khush-thakkar-09/station_hour/resolve/main/city_hour.csv.gz",compression="gzip",low_memory=False)

    return stations_df, station_day_df, city_day_df, city_hour_df
    
@st.cache_data(show_spinner="Loading station_hour dataset (this may take a bit)...")
def load_station_hour():
    station_hour_df = pd.read_csv(
    "https://huggingface.co/datasets/khush-thakkar-09/station_hour/resolve/main/station_hour.csv.gz",
    compression="gzip",
    low_memory=False)
    return station_hour_df

stations_df, station_day_df, city_day_df, city_hour_df = load_data()

def task1(city_day_df, station_day_df, stations_df, city_hour_df):
    st.header("Task 1 – Trend Visualisations")
    st.caption("Bad-air days, worst cities, seasonal and festival patterns, and hourly impacts.")
    st.markdown("---")
    
    st.subheader("1. Bad-Air Percentage for Top Polluted Cities")

    city_day = city_day_df.dropna(subset=["AQI_Bucket"])
    city_day_df['AQI_Bucket'].value_counts()

    # %%
    city_day = city_day_df.dropna(subset=["AQI_Bucket"])

    # %%
    city_day["Date"] = pd.to_datetime(city_day["Date"])
    city_day["Year"] = city_day["Date"].dt.year

    # %%
    bad = ["Poor", "Very Poor", "Severe"]
    bad_air = city_day[city_day["AQI_Bucket"].isin(bad)]
    bad_air_yearly = (
        bad_air.groupby(["City", "Year"])["AQI_Bucket"]
        .count()
        .reset_index(name="Bad_Air_Days")
    )

    # %%
    total_days_yearly = (
        city_day.groupby(["City", "Year"])["AQI_Bucket"]
        .count()
        .reset_index(name="Total_Valid_Days")
    )
    merged = bad_air_yearly.merge(total_days_yearly, on=["City", "Year"])
    merged["Bad_Air_Percentage"] = (
        merged["Bad_Air_Days"] / merged["Total_Valid_Days"]
    )

    # %%
    city_rank = merged.groupby("City")["Bad_Air_Percentage"].mean().sort_values(ascending=False)
    top_cities = city_rank.head(5).index

    # %%
    top_cities = ['Ahmedabad', 'Delhi', 'Patna', 'Gurugram', 'Lucknow']
    df_top = merged[merged['City'].isin(top_cities)].copy()

    # %%
    import plotly.graph_objects as go
    fig = go.Figure()
    for city in top_cities:
        df_city = df_top[df_top['City'] == city]
        fig.add_trace(go.Scatter(
            x=df_city["Year"],
            y=df_city["Bad_Air_Percentage"],
            mode="lines+markers",
            name=city,
            visible=True
        ))
    buttons = []
    for i, city in enumerate(top_cities):
        visibility = [False] * len(top_cities)
        visibility[i] = True
        
        buttons.append(dict(
            label=city,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"Bad-Air Percentage Trend: {city}"}]
        ))
    buttons.insert(0, dict(
        label="Show All",
        method="update",
        args=[{"visible": [True] * len(top_cities)},
              {"title": "Yearly Bad-Air Percentage for All Top Cities"}]
    ))
    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=1.2
        )],
        title="Yearly Bad-Air Percentage for Top Polluted Cities",
        xaxis_title="Year",
        yaxis_title="Bad-Air Percentage",
        legend=dict(
        orientation="h",
        y=-0.2
    )
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("2. Bad-Air Percentage of Worst Stations")

    station_day = station_day_df.dropna(subset=["AQI_Bucket"])

    station_day["Date"] = pd.to_datetime(station_day["Date"])
    station_day["Year"] = station_day["Date"].dt.year
    valid_station = station_day.dropna(subset=["AQI", "AQI_Bucket"])

    bad = ["Poor", "Very Poor", "Severe"]
    bad_air_station = valid_station[valid_station["AQI_Bucket"].isin(bad)]
    bad_air_yearly = (
        bad_air_station.groupby(["StationId", "Year"])["AQI_Bucket"]
        .count()
        .reset_index(name="Bad_Air_Days")
    )

    total_days_yearly = (
        valid_station.groupby(["StationId", "Year"])["AQI_Bucket"]
        .count()
        .reset_index(name="Total_Valid_Days")
    )

    station_merged = bad_air_yearly.merge(total_days_yearly, on=["StationId", "Year"])
    station_merged["Bad_Air_Percentage"] = (
        station_merged["Bad_Air_Days"] / station_merged["Total_Valid_Days"]
    )

    worst_stations = (
        station_merged.groupby("StationId")["Bad_Air_Percentage"]
        .mean()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    top_station_ids = ['DL028','GJ001','DL002','DL007']
    station_top = station_merged[station_merged["StationId"].isin(top_station_ids)]

    import plotly.graph_objects as go
    top_stations = top_station_ids
    fig = go.Figure()
    for station in top_stations:
        df_s = station_top[station_top["StationId"] == station]
        fig.add_trace(go.Scatter(
            x=df_s["Year"],
            y=df_s["Bad_Air_Percentage"],
            mode="lines+markers",
            name=station,
            visible=True
        ))
    buttons = []
    buttons.append(dict(
        label="Show All",
        method="update",
        args=[{"visible": [True] * len(top_stations)},
              {"title": "Bad-Air Percentage Trends for Worst Stations"}]
    ))
    for i, station in enumerate(top_stations):
        visible = [False] * len(top_stations)
        visible[i] = True
        
        buttons.append(dict(
            label=station,
            method="update",
            args=[{"visible": visible},
                  {"title": f"Bad-Air Percentage Trend: {station}"}]
        ))
    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=1.15,
            y=1.0
        )],
        title="Bad-Air Percentage Trends for Worst Stations",
        xaxis_title="Year",
        yaxis_title="Bad-Air Percentage",
        legend=dict(
        orientation="h",
        y=-0.2
    )
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("3. Top 2 Worst Stations per City")

    station_day = station_day_df.dropna(subset=['AQI_Bucket'])
    bad_categories = ['Poor', 'Very Poor', 'Severe']
    station_day['Bad_Air'] = station_day['AQI_Bucket'].isin(bad_categories).astype(int)
    station_day['Date'] = pd.to_datetime(station_day['Date'])
    station_day['Year'] = station_day['Date'].dt.year
    station_day_full = station_day.merge(
        stations_df[['StationId', 'City']],
        on='StationId',
        how='left'
    )

    station_overall = (
        station_day_full.groupby(['City', 'StationId'])
        .agg(
            Bad_Air_Days=('Bad_Air', 'sum'),
            Total_Days=('Bad_Air', 'count')
        )
        .reset_index()
    )
    station_overall['Bad_Air_Percentage'] = (
        station_overall['Bad_Air_Days'] / station_overall['Total_Days']
    )

    top_cities = ['Ahmedabad', 'Delhi', 'Patna', 'Gurugram', 'Lucknow']
    station_overall = station_overall[station_overall['City'].isin(top_cities)]

    top2_per_city = (
        station_overall.sort_values(['City', 'Bad_Air_Percentage'], ascending=[True, False])
        .groupby('City')
        .head(2)
    )

    import plotly.express as px
    fig = px.bar(
        top2_per_city,
        x='Bad_Air_Percentage',
        y='StationId',
        color='City',
        orientation='h',
        title='Top 2 Most Polluted Stations per City',
        labels={
            "Bad_Air_Percentage": "Bad-Air Percentage",
            "StationId": "Station ID"
        }
    )
    fig.update_layout(
        yaxis=dict(categoryorder='total ascending'),
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("4. Monthly AQI Heatmap")

    city_day_df['Date'] = pd.to_datetime(city_day_df['Date'])
    city_day_df['Year'] = city_day_df['Date'].dt.year
    city_day_df['Month'] = city_day_df['Date'].dt.month
    city_day_df['MonthName'] = city_day_df['Date'].dt.month_name()
    city_day = city_day_df.dropna(subset=['AQI_Bucket'])

    monthly_aqi = (
        city_day.groupby(['Year','Month'])['AQI']
        .mean()
        .reset_index()
    )

    heatmap_df = monthly_aqi.pivot(index='Year', columns='Month', values='AQI')

    import plotly.express as px
    fig = px.imshow(
        heatmap_df,
        labels=dict(x="Month", y="Year", color="Avg AQI"),
        x=[ 'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec' ],
        title="Monthly Average AQI Heatmap (All Cities Combined)",
        color_continuous_scale='RdYlGn_r'
    )

    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("5. Yearly AQI Area Chart")

    fig = go.Figure()
    years = sorted(monthly_aqi['Year'].unique())
    for yr in years:
        data = monthly_aqi[monthly_aqi['Year'] == yr]
        fig.add_trace(go.Scatter(
            x=data['Month'],
            y=data['AQI'],
            fill='tozeroy',
            mode='lines+markers',
            name=str(yr),
            visible=True if yr == years[0] else False   # show first year initially
        ))
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label=str(yr),
                        method='update',
                        args=[
                            {"visible": [yr == y for y in years]},
                            {"title": f"Monthly AQI Area Chart for {yr}"}
                        ]
                    ) for yr in years
                ],
                direction="down",
                showactive=True,
                x=1.15,
                y=1
            )
        ],
        title=f"Monthly AQI Area Chart for {years[0]}",
        xaxis=dict(
            tickmode='array',
            tickvals=list(range(1,13)),
            ticktext=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        ),
        yaxis_title="Average AQI",
        xaxis_title="Month",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("6. Festival Impact on AQI")

    festival_dates = {
        "Diwali": {
            2015: "2015-11-11",
            2016: "2016-10-30",
            2017: "2017-10-19",
            2018: "2018-11-07",
            2019: "2019-10-27",
            2020: "2020-11-14"
        },
        "Dussehra": {
            2015: "2015-10-22",
            2016: "2016-10-11",
            2017: "2017-09-30",
            2018: "2018-10-19",
            2019: "2019-10-08",
            2020: "2020-10-25"
        },
        "Holi": {
            2015: "2015-03-06",
            2016: "2016-03-24",
            2017: "2017-03-13",
            2018: "2018-03-02",
            2019: "2019-03-21",
            2020: "2020-03-10"
        }
    }

    def assign_festival_label(row):
        year = row['Year']
        date = row['Date']
        for fest, fest_years in festival_dates.items():
            fest_date = pd.to_datetime(fest_years.get(year, None))
            if pd.isna(fest_date):
                continue
            before_window = (fest_date - pd.Timedelta(days=7))
            after_window  = (fest_date + pd.Timedelta(days=7))
            if date == fest_date:
                return fest + "_Day"
            elif before_window <= date < fest_date:
                return fest + "_Before"
            elif fest_date < date <= after_window:
                return fest + "_After"
        return "None"

    city_day['Festival'] = city_day.apply(assign_festival_label, axis=1)
    diwali_df = city_day[city_day['Festival'].str.contains("Diwali")]
    holi_df = city_day[city_day['Festival'].str.contains("Holi")]
    dussehra_df = city_day[city_day['Festival'].str.contains("Dussehra")]

    diwali_summary = (
        diwali_df.groupby('Festival')['AQI']
        .mean()
        .reset_index()
    )

    holi_summary = (
        holi_df.groupby('Festival')['AQI']
        .mean()
        .reset_index()
    )

    dussehra_summary = (
        dussehra_df.groupby('Festival')['AQI']
        .mean()
        .reset_index()
    )

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=diwali_summary['Festival'],
        y=diwali_summary['AQI'],
        name='Diwali',
        marker_color='blue',
        visible=True
    ))
    fig.add_trace(go.Bar(
        x=holi_summary['Festival'],
        y=holi_summary['AQI'],
        name='Holi',
        marker_color='green',
        visible=False
    ))

    fig.add_trace(go.Bar(
        x=dussehra_summary['Festival'],
        y=dussehra_summary['AQI'],
        name='Dussehra',
        marker_color='red',
        visible=False
    ))
    fig.update_layout(
        updatemenus=[
            dict(
                type="dropdown",
                x=1.15, y=1,
                showactive=True,
                buttons=[
                    dict(
                        label="Diwali",
                        method="update",
                        args=[{"visible": [True, False, False]},
                              {"title": "AQI Impact Around Diwali (±7 Days)"}]
                    ),
                    dict(
                        label="Holi",
                        method="update",
                        args=[{"visible": [False, True, False]},
                              {"title": "AQI Impact Around Holi (±7 Days)"}]
                    ),
                    dict(
                        label="Dussehra",
                        method="update",
                        args=[{"visible": [False, False, True]},
                              {"title": "AQI Impact Around Dussehra (±7 Days)"}]
                    )
                ]
            )
        ],
        title="Festival-wise AQI Impact (Select a Festival)",
        xaxis_title="Festival Window",
        yaxis_title="Average AQI",
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("7. Hourly AQI – Diwali vs Normal Day")

    city_hour = city_hour_df.dropna(subset=['AQI_Bucket'])
    city_hour.info()

    df = city_hour[city_hour['City'].isin(['Delhi', 'Mumbai'])].copy()
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['Date'] = df['Datetime'].dt.date
    df['Hour'] = df['Datetime'].dt.hour
    df['Year'] = df['Datetime'].dt.year

    diwali_dates = {
        2015: '2015-11-11',
        2016: '2016-10-30',
        2017: '2017-10-19',
        2018: '2018-11-07',
        2019: '2019-10-27',
        2020: '2020-11-14'
    }

    fig = go.Figure()

    cities = ['Delhi', 'Mumbai']
    years = [2018, 2019]

    initial_city = 'Delhi'
    initial_year = 2019
    diwali_day = pd.to_datetime(diwali_dates[initial_year]).date()
    normal_day = (pd.to_datetime(diwali_dates[initial_year]) - pd.Timedelta(days=7)).date()

    df_city_year = df[(df['City'] == initial_city) & (df['Year'] == initial_year)]

    dd = df_city_year[df_city_year['Date'] == diwali_day]
    nd = df_city_year[df_city_year['Date'] == normal_day]

    fig.add_trace(go.Scatter(
        x=dd['Hour'], y=dd['AQI'], mode='lines+markers',
        name='Diwali Day', line=dict(color='red')
    ))
    fig.add_trace(go.Scatter(
        x=nd['Hour'], y=nd['AQI'], mode='lines+markers',
        name='Normal Day', line=dict(color='blue')
    ))
    buttons = []
    for city in cities:
        for year in years:

            diwali = pd.to_datetime(diwali_dates[year]).date()
            normal = (pd.to_datetime(diwali_dates[year]) - pd.Timedelta(days=7)).date()

            temp = df[(df['City'] == city) & (df['Year'] == year)]

            dd2 = temp[temp['Date'] == diwali]
            nd2 = temp[temp['Date'] == normal]

            buttons.append(dict(
                label=f"{city} - {year}",
                method="update",
                args=[
                    {
                        "x": [dd2['Hour'], nd2['Hour']],
                        "y": [dd2['AQI'], nd2['AQI']]
                    },
                    {
                        "title": f"Hourly AQI on Diwali vs Normal Day — {city} ({year})"
                    }
                ]
            ))

    fig.update_layout(
        updatemenus=[{
            "buttons": buttons,
            "direction": "down",
            "showactive": True,
            "x": 1.15,
            "y": 1
        }],
        title=f"Hourly AQI on Diwali vs Normal Day — {initial_city} ({initial_year})",
        xaxis_title="Hour of Day",
        yaxis_title="AQI",
        height=550,
        legend=dict(
        orientation="h",
        y=-0.2
    ))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("8. Average Hourly AQI (Diurnal Cycle)")

    diurnal = df.groupby(['City', 'Hour'])['AQI'].mean().reset_index()
    initial_city = 'Delhi'
    sub = diurnal[diurnal['City'] == initial_city]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=sub['Hour'], y=sub['AQI'],
        mode='lines+markers',
        name=initial_city,
        line=dict(width=3)
    ))
    buttons = []
    for city in cities:
        tmp = diurnal[diurnal['City'] == city]
        
        buttons.append(dict(
            label=city,
            method="update",
            args=[
                {"x": [tmp['Hour']],
                 "y": [tmp['AQI']]},
                {"title": f"Average Hourly AQI (Diurnal Cycle) — {city}"}
            ]
        ))
    fig.update_layout(
        updatemenus=[{
            "buttons": buttons,
            "direction": "down",
            "x": 1.15,
            "y": 1,
            "showactive": True
        }],
        title=f"Average Hourly AQI (Diurnal Cycle) — {initial_city}",
        xaxis_title="Hour of Day",
        yaxis_title="Average AQI",
        height=550
    )
    st.plotly_chart(fig, use_container_width=True)


def task2(city_day_df, station_day_df, city_hour_df, stations_df):
    import plotly.express as px
    import plotly.graph_objects as go
    import numpy as np
    
    st.header("Task 2 – Pollution Heatmaps & Trends")
    st.caption("Monthly/seasonal pollutant behaviour, correlations and city groupings.")
    st.markdown("---")

    st.subheader("1. Monthly Pollutant Concentrations")
    
    df = city_day_df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.month

    pollutants = ['PM2.5', 'PM10', 'NO2', 'NOx', 'SO2', 'CO', 'O3']

    monthly_pollutants = df.groupby('Month')[pollutants].mean().reset_index()

    fig = go.Figure()
    for pollutant in pollutants:
        fig.add_trace(go.Scatter(
            x=monthly_pollutants['Month'],
            y=monthly_pollutants[pollutant],
            mode='lines+markers',
            name=pollutant
        ))
    fig.update_layout(
        title="Monthly Average Concentration of Pollutants (All India)",
        xaxis_title="Month",
        yaxis_title="Average Pollutant Concentration",
        xaxis=dict(tickmode='array', tickvals=list(range(1,13))),
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("2. Seasonal Pollutant Comparison")
    
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Summer'
        elif month in [6, 7, 8]:
            return 'Monsoon'
        else:
            return 'Post-Monsoon'

    df['Season'] = df['Month'].apply(get_season)
    pollutants = ['PM2.5', 'PM10', 'NO2', 'NOx', 'SO2', 'CO', 'O3']
    seasonal = df.groupby('Season')[pollutants].mean().reset_index()
    season_order = ['Winter', 'Summer', 'Monsoon', 'Post-Monsoon']
    seasonal = seasonal.set_index('Season').loc[season_order].reset_index()

    fig = go.Figure()
    for pollutant in pollutants:
        fig.add_trace(go.Bar(
            x=seasonal['Season'],
            y=seasonal[pollutant],
            name=pollutant
        ))

    fig.update_layout(
        title="Seasonal Comparison of Pollutants (All India)",
        xaxis_title="Season",
        yaxis_title="Average Concentration",
        barmode='group',
        height=600
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("3. Correlation Heatmap")
    
    cols = ['AQI', 'PM2.5', 'PM10', 'NO2', 'NOx', 'SO2', 'CO', 'O3']
    corr_df = df[cols].corr().round(2)

    mask = np.tril(np.ones_like(corr_df, dtype=bool))
    corr_lower = corr_df.where(mask)
    fig = px.imshow(
        corr_lower,
        text_auto=True,
        color_continuous_scale='RdBu_r',
        width=700,
        height=700,
        title="Correlation Matrix:- "
    )
    fig.update_layout(
        font=dict(size=14),
        title_font=dict(size=20)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("4. City Clustering")
    
    df = city_day_df.copy()
    df = df.dropna(subset=['City'])
    pollutants = ['PM2.5','PM10','NO2','NOx','SO2','CO','O3']
    city_pollution = df.groupby('City')[pollutants].mean()
    city_pollution = city_pollution.dropna()

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    scaled = scaler.fit_transform(city_pollution)
    scaled_df = pd.DataFrame(scaled, index=city_pollution.index, columns=pollutants)

    import matplotlib.pyplot as plt
    from scipy.cluster.hierarchy import dendrogram, linkage
    plt.figure(figsize=(16, 8))
    Z = linkage(scaled_df, method='ward')
    dendrogram(Z,
               labels=scaled_df.index,
               leaf_rotation=90,
               leaf_font_size=12,
               color_threshold=8)

    plt.title("Hierarchical Clustering of Indian Cities Based on Pollution Profile")
    plt.xlabel("Cities")
    plt.ylabel("Distance")
    st.pyplot(plt.gcf())
    
    st.subheader("5. Top Industrial Pollution Hotspot Stations")
    
    station_day = station_day_df.copy()
    stations_info = stations_df[['StationId', 'City', 'State']]
    station_day = station_day.merge(stations_info, on='StationId', how='left')

    station_day['Vehicular_Score'] = (
        station_day['NO2'] * 0.45 +
        station_day['NOx'] * 0.35 +
        station_day['CO'] * 0.20
    )
    station_day['Industrial_Score'] = (
        station_day['SO2'] * 0.50 +
        station_day['PM10'] * 0.30 +
        station_day['PM2.5'] * 0.20
    )

    station_scores = station_day.groupby(['StationId','City','State'])[
        ['Vehicular_Score','Industrial_Score']
    ].mean().reset_index()

    top_vehicular = station_scores.nlargest(5, 'Vehicular_Score')
    top_industrial = station_scores.nlargest(5, 'Industrial_Score')

    fig = px.pie(
        top_industrial,
        names="StationId",
        values="Industrial_Score",
        color="City",
        hole=0.45,
        title="Top Industrial Pollution Hotspot Stations"
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=18,
        pull=[0.05]*len(top_industrial)
    )

    fig.update_layout(
        width=900,
        height=700,
        title_font_size=26,
        legend_title="City",
        legend_font_size=16
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    
    st.subheader("6. Top Vehicular Pollution Hotspot Stations")
    
    fig = px.pie(
        top_vehicular,
        names="StationId",
        values="Vehicular_Score",
        color="City",
        hole=0.45,
        title="Top Vehicular Pollution Hotspot Stations"
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        textfont_size=18,
        pull=[0.05]*len(top_vehicular)
    )

    fig.update_layout(
        width=900,
        height=700,
        title_font_size=26,
        legend_title="City",
        legend_font_size=16
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")


def task3(station_hour_df,city_day_df, station_day_df, stations_df, city_hour_df):

    st.header("Task 3 – Station Performance & Reliability")
    st.caption("Data completeness, pollutant coverage and station reliability rankings.")
    st.markdown("---")

    st.subheader("1. Pollutant Coverage Heatmap")
    
    df = station_hour_df.copy()
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    pollutants = [
        'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3',
        'CO', 'SO2', 'O3', 'Benzene', 'Toluene', 'Xylene', 'AQI'
    ]

    base = (
        df.groupby('StationId')['Datetime']
          .agg(start_dt='min', end_dt='max', actual_hours='count')
    )

    time_diff_hours = (base['end_dt'] - base['start_dt']).dt.total_seconds() / 3600
    base['expected_hours'] = time_diff_hours.astype(int) + 1
    base['coverage_pct'] = base['actual_hours'] / base['expected_hours']
    base['missing_pct'] = 1 - base['coverage_pct']
    base = base[base['expected_hours'] > 0]

    pollutant_counts = (
        df.groupby('StationId')[pollutants]
          .count()
    )
    pollutant_cov = pollutant_counts.div(base['expected_hours'], axis=0)
    pollutant_cov = pollutant_cov.clip(upper=1.0)
    pollutant_cov = pollutant_cov.add_suffix('_cov')
    station_quality = base.join(pollutant_cov)
    station_quality = station_quality.sort_values('coverage_pct', ascending=False)

    subset = station_quality.sort_values('coverage_pct', ascending=True).head(200)
    poll_cov_cols = [c for c in station_quality.columns if c.endswith('_cov')]
    heat_df = subset[poll_cov_cols].copy()
    heat_df.index.name = 'StationId'
    heat_df = heat_df * 100
    fig = px.imshow(
        heat_df,
        color_continuous_scale="magma",
        labels=dict(x="Pollutant", y="Station", color="Coverage (%)"),
        aspect='auto',
        text_auto='.1f',
        title="Pollutant-wise Coverage per Station"
    )
    fig.update_layout(height=2500)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("2. Top 10 Most Reliable Stations")
    
    poll_cov_cols = [c for c in station_quality.columns if c.endswith('_cov')]
    station_quality['pollutant_coverage_mean'] = station_quality[poll_cov_cols].mean(axis=1)
    station_quality['reliability_score'] = (
        (1 - station_quality['missing_pct']) * 0.4 +
        station_quality['pollutant_coverage_mean'] * 0.6
    )

    def reliability_category(score):
        if score >= 0.85:
            return "High"
        elif score >= 0.70:
            return "Moderate"
        else:
            return "Low"

    station_quality['reliability_category'] = station_quality['reliability_score'].apply(reliability_category)
    top_reliable = station_quality.sort_values('reliability_score', ascending=False).head(10)
    bottom_reliable = station_quality.sort_values('reliability_score', ascending=True).head(10)
    top_reliable = top_reliable[['reliability_score', 'reliability_category', 'coverage_pct', 'pollutant_coverage_mean']]
    bottom_reliable = bottom_reliable[['reliability_score', 'reliability_category', 'coverage_pct', 'pollutant_coverage_mean']]

    fig = px.bar(
        top_reliable.reset_index(),
        x='StationId',
        y='reliability_score',
        title="Top 10 Most Reliable Stations",
        labels={'reliability_score': 'Reliability Score'}
    )
    fig.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("3. Bottom 10 Least Reliable Stations")
    
    fig = px.bar(
        bottom_reliable.reset_index(),
        x='StationId',
        y='reliability_score',
        title="Bottom 10 Least Reliable Stations",
        labels={'reliability_score': 'Reliability Score'}
    )
    fig.update_layout(xaxis_tickangle=-45)

    st.plotly_chart(fig, use_container_width=True)


def task4(city_day_df, station_day_df, city_hour_df, stations_df):
    city_day = city_day_df.dropna(subset=["AQI_Bucket"])
    st.header("Task 4 – Risk Index & Policy Insights")
    st.caption("City-level risk scoring, spatial risk map and long-term AQI change.")
    st.markdown("---")

    st.subheader("1. Pollution Risk Map of Indian Cities")
    
    df = city_day.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    pollutants = ["PM2.5", "PM10", "NO2", "NOx", "SO2", "CO"]
    city_pollutants = df.groupby("City")[pollutants].mean().reset_index()

    city_pollutants = city_pollutants.fillna(city_pollutants.median(numeric_only=True))

    exposure = (
        df.assign(unhealthy = df["AQI"] > 100)
          .groupby("City")["unhealthy"]
          .mean()
          .reset_index()
          .rename(columns={"unhealthy": "ExposureFactor"})
    )

    norm_df = city_pollutants.copy()
    for col in pollutants:
        min_val = norm_df[col].min()
        max_val = norm_df[col].max()
        norm_df[col] = (norm_df[col] - min_val) / (max_val - min_val + 1e-8)

    weights = {
        "PM2.5": 0.40,
        "PM10": 0.20,
        "NO2": 0.15,
        "NOx": 0.10,
        "SO2": 0.10,
        "CO": 0.05
    }
    norm_df["WeightedRisk"] = sum(norm_df[col] * w for col, w in weights.items())
    risk_df = norm_df.merge(exposure, on="City", how="left")
    risk_df["FinalRiskScore"] = risk_df["WeightedRisk"] * (1 + risk_df["ExposureFactor"])
    risk_df = risk_df.sort_values("FinalRiskScore", ascending=False)

    def categorize(score):
        if score > 1.4: return "Severe"
        if score > 1.0: return "High"
        if score > 0.6: return "Moderate"
        return "Low"

    risk_df["RiskCategory"] = risk_df["FinalRiskScore"].apply(categorize)

    city_coords = {
        "Delhi": (28.7041, 77.1025),
        "Patna": (25.5941, 85.1376),
        "Ahmedabad": (23.0225, 72.5714),
        "Gurugram": (28.4595, 77.0266),
        "Lucknow": (26.8467, 80.9462),
        "Talcher": (20.9497, 85.2335),
        "Jorapokhar": (23.7795, 86.2100),
        "Kolkata": (22.5726, 88.3639),
        "Jaipur": (26.9124, 75.7873),
        "Brajrajnagar": (21.8167, 83.9167),
        "Bhopal": (23.2599, 77.4126),
        "Guwahati": (26.1445, 91.7362),
        "Visakhapatnam": (17.6868, 83.2185),
        "Amritsar": (31.6340, 74.8723),
        "Hyderabad": (17.3850, 78.4867),
        "Mumbai": (19.0760, 72.8777),
        "Kochi": (9.9312, 76.2673),
        "Chennai": (13.0827, 80.2707),
        "Bengaluru": (12.9716, 77.5946),
        "Amaravati": (16.5417, 80.5150),
        "Chandigarh": (30.7333, 76.7794),
        "Coimbatore": (11.0168, 76.9558),
        "Ernakulam": (9.9816, 76.2999),
        "Thiruvananthapuram": (8.5241, 76.9366),
        "Shillong": (25.5788, 91.8933),
        "Aizawl": (23.7271, 92.7176)
    }

    risk_df["lat"] = risk_df["City"].map(lambda x: city_coords[x][0])
    risk_df["lon"] = risk_df["City"].map(lambda x: city_coords[x][1])

    fig = px.scatter_geo(
        risk_df,
        lat="lat",
        lon="lon",
        color="FinalRiskScore",
        size="FinalRiskScore",
        hover_name="City",
        hover_data=["RiskCategory", "FinalRiskScore"],
        color_continuous_scale="RdYlGn_r",
        size_max=35,
        title="India City Pollution Risk Map"
    )
    fig.update_geos(
        scope="asia",
        projection_type="natural earth",
        projection_scale=4,
        center=dict(lat=22.5, lon=79),
        showcountries=True,
        countrycolor="black",
    )
    fig.update_layout(height=700)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("2. Best vs Worst Year-on-Year AQI Change")
    
    df = city_day_df.copy()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df = df[['City','Year','AQI']]

    df = df[df['Year'] != 2020]

    df = (
        df.groupby(['City','Year'])['AQI']
          .mean()
          .reset_index()
          .rename(columns={'AQI': 'yearly_aqi_mean'})
    )

    df['yearly_diff'] = df.groupby('City')['yearly_aqi_mean'].diff()

    city_change = (
        df.groupby(['City'])['yearly_diff']
          .sum()
          .reset_index()
          .rename(columns={'yearly_diff': 'total_change'})
    )

    df = df.merge(city_change, on='City', how='left')

    df.drop(columns=['yearly_diff'],axis=1,inplace=True)

    top_deteriorate = city_change.sort_values('total_change', ascending=False).head(5)['City'].tolist()
    top_improve = city_change.sort_values('total_change').head(5)['City'].tolist()

    df_plot = df[df['City'].isin(top_deteriorate + top_improve)]

    fig = px.line(
        df[df['City'].isin(top_deteriorate)],
        x="Year",
        y="yearly_aqi_mean",
        color="City",
        markers=True,
        title="Top 5 Cities With Worst Year-on-Year Deterioration (2015–2019)"
    )
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Average AQI",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    fig = px.line(
        df[df['City'].isin(top_improve)],
        x="Year",
        y="yearly_aqi_mean",
        color="City",
        markers=True,
        title="Top 5 Cities With Best Year-on-Year Improvement (2015–2019)"
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Average AQI",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)


st.sidebar.title("Navigation")
selection = st.sidebar.radio(
    "Go to task:",
    ["Introduction", "Task 1", "Task 2", "Task 3", "Task 4"]
)

if selection == "Introduction":
    set_page_class("page-intro")

    st.markdown('<div class="hero-kicker">🇮🇳 Impact Metrics Project</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="hero-title">India Air Quality – Dashboard</div>
        <div class="hero-subtitle">
          Multi-year analysis of Indian air quality: hotspots, station reliability, pollutant patterns,
          and city-level risk — presented as an interactive dashboard.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="hero-cards">
          <div class="hero-card"><div class="k">Modules</div><div class="v">4 Tasks</div></div>
          <div class="hero-card"><div class="k">Views</div><div class="v">Trends + Heatmaps</div></div>
          <div class="hero-card"><div class="k">Focus</div><div class="v">Reliability</div></div>
          <div class="hero-card"><div class="k">Outcome</div><div class="v">Risk Insights</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.markdown("---")

    st.markdown(
        """
        **What you can explore inside:**
        - Trend visualisations (city / year / hour)  
        - Pollution heatmaps & pollutant behaviour  
        - Station performance & data quality audit  
        - Risk indices, vulnerable cities & improvement trends  

        Use the **sidebar** to navigate between tasks.
        """
    )


elif selection == "Task 1":
    set_page_class("page-task")
    task1(city_day_df, station_day_df,stations_df,city_hour_df)

elif selection == "Task 2":
    set_page_class("page-task")
    task2(city_day_df, station_day_df,city_hour_df,stations_df)

elif selection == "Task 3":
    set_page_class("page-task")
    station_hour_df = load_station_hour()
    task3(station_hour_df, city_day_df, station_day_df, stations_df,city_hour_df)

elif selection == "Task 4":
    set_page_class("page-task")
    task4(city_day_df, station_day_df, city_hour_df, stations_df)
