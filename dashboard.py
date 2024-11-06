import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from statsmodels.tsa.seasonal import seasonal_decompose
import base64

# Fungsi untuk mengkonversi gambar ke base64
def get_base64_of_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None

# Konfigurasi halaman
st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS untuk styling
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
        }
        .stApp {
            background-color: #0e1117;
        }
        .metric-row {
            display: flex;
            justify-content: space-between;
            gap: 24px;
            margin: 20px 0 40px 0;
        }
        .metric-card {
            background-color: #1e1e1e;
            border-radius: 15px;
            padding: 24px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            flex: 1;
            text-align: center;
        }
        .metric-title {
            color: #ffffff;
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
        }
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
        }
        .value-red { color: #ff4b4b; }
        .value-green { color: #4ecdc4; }
        .value-blue { color: #45b7d1; }
        .value-teal { color: #96ceb4; }
        img {
            max-width: 100%; /* Logo tidak akan lebih besar dari kontainer */
            height: auto; /* Menjaga rasio aspek */
        }
    </style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv("day.csv")
    hour_df = pd.read_csv("hour.csv")
    
    # Konversi kolom tanggal
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    # Mapping musim
    season_dict = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
    day_df['season_name'] = day_df['season'].map(season_dict)
    hour_df['season_name'] = hour_df['season'].map(season_dict)
    
    return day_df, hour_df

# Load kedua dataset
df, hour_df = load_data()

# Sidebar
try:
    st.sidebar.markdown("""
        <div class="sidebar-logo">
            <img src="data:image/png;base64,{}" alt="Bike Share Logo">
        </div>
    """.format(get_base64_of_image("bikelogo.png")), unsafe_allow_html=True)
except Exception as e:
    st.sidebar.error(f"Error loading logo: {str(e)}")
    st.sidebar.image("bikelogo.png", width=180)

# Filter di sidebar
st.sidebar.markdown('<div class="sidebar-title">Filter Data</div>', unsafe_allow_html=True)

# Date filter
min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()

start_date, end_date = st.sidebar.date_input(
    "📅 Rentang Waktu",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Season filter
season_dict = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df['season_name'] = df['season'].map(season_dict)
season_names = sorted(df['season_name'].unique())
season_filter = st.sidebar.multiselect(
    "🌤️ Pilih Musim",
    options=season_names,
    default=season_names
)

# Apply filters
filtered_df = df[
    (df['season_name'].isin(season_filter)) &
    (df['dteday'].dt.date >= start_date) &
    (df['dteday'].dt.date <= end_date)
]

# Header
st.markdown("""
    <h1 style='text-align: center; color: #ffffff; margin: 0 0 10px 0; padding: 0;'>
        🚲 Bike Sharing Analytics Dashboard
    </h1>
    <p style='text-align: center; color: #cccccc; font-size: 18px; margin: 0 0 40px 0; padding: 0;'>
        Analisis Komprehensif Sistem Berbagi Sepeda di Washington D.C. (2011-2012)
    </p>
""", unsafe_allow_html=True)

# Metrics
st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-title">Total Penyewaan</div>
            <div class="metric-value value-red">{filtered_df['cnt'].sum():,}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Rata-rata Harian</div>
            <div class="metric-value value-green">{int(filtered_df['cnt'].mean()):,}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Penyewaan Tertinggi</div>
            <div class="metric-value value-blue">{filtered_df['cnt'].max():,}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">Total Hari</div>
            <div class="metric-value value-teal">{len(filtered_df):,}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Fungsi untuk styling plot
def style_plot(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1e1e1e",
        plot_bgcolor="#1e1e1e",
        font_color="#ffffff",
        font=dict(family="Arial", size=12),
        margin=dict(t=30, l=10, r=10, b=10)
    )
    fig.update_xaxes(gridcolor="#333333", zerolinecolor="#333333")
    fig.update_yaxes(gridcolor="#333333", zerolinecolor="#333333")
    return fig

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Tren & Pola Penyewaan",
    "🌤️ Analisis Musiman & Cuaca",
    "📊 Perbandingan Hari",
    "🔍 Korelasi & Insight",
    "🕒 Analisis Per Jam",
    "🎯 Performa Bulanan"
])

# Color scheme
COLOR_SCHEME = {
    "Spring": "#00ff9f",
    "Summer": "#ffd700",
    "Fall": "#ff6b6b",
    "Winter": "#45b7d1"
}

# Tab 1: Tren & Pola
with tab1:
    fig = px.line(filtered_df, 
        x='dteday', 
        y='cnt',
        color='season_name',
        color_discrete_map=COLOR_SCHEME,
        title="Tren Penyewaan Sepeda Sepanjang Waktu"
    )
    fig = style_plot(fig)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
        ### 📈 Insight Tren & Pola:
        - Terjadi peningkatan signifikan sebesar 50% dari 2011 ke 2012
        - Puncak penyewaan terjadi pada musim panas dan gugur
        - Pola musiman yang konsisten terlihat setiap tahun
        - Terdapat penurunan tajam saat cuaca ekstrem
    """)

# Tab 2: Analisis Musiman & Cuaca
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.box(filtered_df,
            x="season_name",
            y="cnt",
            color="season_name",
            color_discrete_map=COLOR_SCHEME,
            title="Distribusi Penyewaan per Musim"
        )
        fig = style_plot(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(filtered_df,
            x="temp",
            y="cnt",
            color="season_name",
            color_discrete_map=COLOR_SCHEME,
            title="Pengaruh Temperatur terhadap Penyewaan"
        )
        fig = style_plot(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
        ### 🌤️ Insight Musiman & Cuaca:
        - Musim panas dan gugur memiliki rata-rata penyewaan tertinggi
        - Temperatur optimal untuk penyewaan adalah 20-25°C
        - Cuaca hujan menurunkan penyewaan hingga 30%
        - Musim dingin menunjukkan variabilitas penyewaan yang tinggi
    """)

# Tab 3: Perbandingan Hari
with tab3:
    fig = px.box(filtered_df,
        x="workingday",
        y="cnt",
        color="workingday",
        title="Perbandingan Penyewaan: Hari Kerja vs Akhir Pekan",
        labels={"workingday": "Tipe Hari", "cnt": "Jumlah Penyewaan"},
        category_orders={"workingday": [0, 1]},
        color_discrete_map={0: "#FF6B6B", 1: "#4ECDC4"}
    )
    fig = style_plot(fig)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
        ### 📊 Insight Perbandingan Hari:
        - Hari kerja memiliki pola bi-modal (puncak pagi dan sore)
        - Akhir pekan menunjukkan distribusi yang lebih merata
        - Penyewaan tertinggi terjadi pada Jumat sore
        - Pola commuting terlihat jelas pada hari kerja
    """)

# Tab 4: Korelasi & Insight
with tab4:
    corr = filtered_df[['temp', 'hum', 'windspeed', 'cnt']].corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr,
        x=corr.columns,
        y=corr.columns,
        colorscale='RdBu',
        zmin=-1,
        zmax=1
    ))
    fig = style_plot(fig)
    fig.update_layout(title="Korelasi Antar Variabel", height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
        ### 🔍 Insight Korelasi:
        - Temperatur memiliki korelasi positif kuat (0.8) dengan jumlah penyewaan
        - Kelembaban berkorelasi negatif (-0.3) dengan penyewaan
        - Kecepatan angin memiliki pengaruh minimal
        - Faktor cuaca dan musim sangat mempengaruhi pola penyewaan
    """)

# Tab 5: Analisis Per Jam
with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        # Heatmap pola jam per hari menggunakan hour_df
        hourly_pattern = hour_df.groupby(['hr', 'weekday'])['cnt'].mean().reset_index()
        fig = px.density_heatmap(
            hourly_pattern,
            x='hr',
            y='weekday',
            z='cnt',
            title="Pola Penyewaan Per Jam dalam Seminggu",
            color_continuous_scale="Viridis",
            labels={
                'hr': 'Jam (0-23)',
                'weekday': 'Hari (0=Minggu)',
                'cnt': 'Rata-rata Penyewaan'
            }
        )
        fig = style_plot(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Line plot rata-rata per jam
        hourly_avg = hour_df.groupby('hr')['cnt'].mean().reset_index()
        fig = px.line(
            hourly_avg,
            x='hr',
            y='cnt',
            title="Rata-rata Penyewaan Per Jam",
            markers=True,
            labels={
                'hr': 'Jam (0-23)',
                'cnt': 'Rata-rata Penyewaan'
            }
        )
        fig = style_plot(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    # Tambahan visualisasi: Pola per jam berdasarkan hari kerja vs akhir pekan
    hourly_workday = hour_df.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()
    fig = px.line(
        hourly_workday,
        x='hr',
        y='cnt',
        color='workingday',
        title="Pola Penyewaan Per Jam: Hari Kerja vs Akhir Pekan",
        labels={
            'hr': 'Jam (0-23)',
            'cnt': 'Rata-rata Penyewaan',
            'workingday': 'Hari Kerja'
        },
        color_discrete_map={0: "#FF6B6B", 1: "#4ECDC4"}
    )
    fig = style_plot(fig)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
        ### 🕒 Insight Pola Per Jam:
        - Dua puncak penyewaan pada hari kerja: 8 pagi dan 5 sore (jam commuting)
        - Akhir pekan memiliki pola yang lebih merata dengan puncak di siang hari
        - Penggunaan terendah terjadi antara jam 2-4 pagi
        - Perbedaan signifikan antara pola hari kerja dan akhir pekan
    """)

# Tab 6: Performa Bulanan
with tab6:
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_perf = filtered_df.groupby(['mnth', 'yr'])['cnt'].mean().reset_index()
        fig = px.bar(
            monthly_perf,
            x='mnth',
            y='cnt',
            color='yr',
            title="Performa Bulanan per Tahun",
            barmode='group'
        )
        fig = style_plot(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        monthly_avg = filtered_df.groupby('mnth')['cnt'].mean().reset_index()
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=monthly_avg['cnt'],
            theta=monthly_avg['mnth'].astype(str),
            fill='toself',
            name='Rata-rata Penyewaan'
        ))
        fig = style_plot(fig)
        fig.update_layout(title="Pola Penyewaan Bulanan")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
        ### 🎯 Insight Performa Bulanan:
        - Peningkatan konsisten dari tahun 2011 ke 2012
        - Juni-September adalah bulan dengan performa tertinggi
        - Januari-Februari menunjukkan performa terendah
        - Tren musiman terlihat jelas dalam pola bulanan
    """)