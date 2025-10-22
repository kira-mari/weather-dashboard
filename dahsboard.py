import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Station Météo Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design moderne
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    .stMetric > div {
        background: transparent !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: bold !important;
    }
    h1 {
        color: white;
        text-align: center;
        font-size: 3em;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    </style>
""", unsafe_allow_html=True)

# Titre principal
st.markdown("# 🌤️ Station Météo Dashboard")
st.markdown("---")

# Sidebar pour l'upload du fichier
with st.sidebar:
    st.markdown("## 📂 Chargement des données")
    uploaded_file = st.file_uploader("Importer votre fichier LOG", type=['log', 'txt'])
    
    st.markdown("---")
    st.markdown("### 📊 Informations")
    st.info("Format attendu: Date, Heure, Température, Humidité, Pression, Lumière, Latitude, Longitude, Altitude")

# Fonction pour charger et traiter les données
@st.cache_data
def load_data(file):
    df = pd.read_csv(file, header=None, names=[
        'date', 'heure', 'temperature', 'humidite', 'pression', 
        'lumiere', 'latitude', 'longitude', 'altitude'
    ], sep=',')
    
    # Conversion de la date et heure
    df['datetime'] = pd.to_datetime(df['date'].astype(str) + ' ' + df['heure'].astype(str), 
                                     format='%d%m%y %H:%M:%S', errors='coerce')
    
    return df

if uploaded_file is not None:
    df = load_data(uploaded_file)
    
    # Dernières valeurs
    last_row = df.iloc[-1]
    
    # Métriques principales
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        temp_delta = df['temperature'].iloc[-1] - df['temperature'].iloc[-10] if len(df) > 10 else 0
        st.metric(
            label="🌡️ Température",
            value=f"{last_row['temperature']:.1f}°C",
            delta=f"{temp_delta:.1f}°C"
        )
    
    with col2:
        hum_delta = df['humidite'].iloc[-1] - df['humidite'].iloc[-10] if len(df) > 10 else 0
        st.metric(
            label="💧 Humidité",
            value=f"{last_row['humidite']:.1f}%",
            delta=f"{hum_delta:.1f}%"
        )
    
    with col3:
        press_delta = df['pression'].iloc[-1] - df['pression'].iloc[-10] if len(df) > 10 else 0
        st.metric(
            label="🌀 Pression",
            value=f"{last_row['pression']:.1f} hPa",
            delta=f"{press_delta:.1f} hPa"
        )
    
    with col4:
        st.metric(
            label="☀️ Luminosité",
            value=f"{last_row['lumiere']:.0f} lux"
        )
    
    st.markdown("---")
    
    # Graphiques avancés
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Graphique température avec dégradé
        fig_temp = go.Figure()
        
        fig_temp.add_trace(go.Scatter(
            x=df['datetime'],
            y=df['temperature'],
            mode='lines',
            name='Température',
            line=dict(color='#FF6B6B', width=3),
            fill='tozeroy',
            fillcolor='rgba(255, 107, 107, 0.2)'
        ))
        
        fig_temp.update_layout(
            title="📈 Évolution de la Température",
            title_font=dict(size=20, color='white'),
            xaxis_title="Temps",
            yaxis_title="Température (°C)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_temp, use_container_width=True)
        
        # Graphique pression atmosphérique
        fig_press = go.Figure()
        
        fig_press.add_trace(go.Scatter(
            x=df['datetime'],
            y=df['pression'],
            mode='lines+markers',
            name='Pression',
            line=dict(color='#4ECDC4', width=3),
            marker=dict(size=6, color='#4ECDC4'),
            fill='tozeroy',
            fillcolor='rgba(78, 205, 196, 0.2)'
        ))
        
        fig_press.update_layout(
            title="🌀 Pression Atmosphérique",
            title_font=dict(size=20, color='white'),
            xaxis_title="Temps",
            yaxis_title="Pression (hPa)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_press, use_container_width=True)
    
    with col_right:
        # Graphique humidité avec jauge
        fig_hum = go.Figure()
        
        fig_hum.add_trace(go.Scatter(
            x=df['datetime'],
            y=df['humidite'],
            mode='lines',
            name='Humidité',
            line=dict(color='#95E1D3', width=3),
            fill='tozeroy',
            fillcolor='rgba(149, 225, 211, 0.3)'
        ))
        
        fig_hum.update_layout(
            title="💧 Humidité Relative",
            title_font=dict(size=20, color='white'),
            xaxis_title="Temps",
            yaxis_title="Humidité (%)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_hum, use_container_width=True)
        
        # Graphique luminosité
        fig_lux = go.Figure()
        
        colors = ['#FFD93D' if x > 800 else '#FFA500' if x > 600 else '#FF8C42' 
                  for x in df['lumiere']]
        
        fig_lux.add_trace(go.Bar(
            x=df['datetime'],
            y=df['lumiere'],
            name='Luminosité',
            marker=dict(
                color=df['lumiere'],
                colorscale='YlOrRd',
                showscale=True,
                colorbar=dict(title="Lux")
            )
        ))
        
        fig_lux.update_layout(
            title="☀️ Intensité Lumineuse",
            title_font=dict(size=20, color='white'),
            xaxis_title="Temps",
            yaxis_title="Luminosité (lux)",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_lux, use_container_width=True)
    
    # Graphique combiné
    st.markdown("---")
    st.markdown("## 📊 Vue d'ensemble multi-paramètres")
    
    fig_combined = go.Figure()
    
    # Normalisation des données pour les mettre sur la même échelle
    df_norm = df.copy()
    for col in ['temperature', 'humidite', 'pression', 'lumiere']:
        df_norm[f'{col}_norm'] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    
    fig_combined.add_trace(go.Scatter(
        x=df['datetime'], y=df_norm['temperature_norm'],
        name='Température', line=dict(color='#FF6B6B', width=2)
    ))
    
    fig_combined.add_trace(go.Scatter(
        x=df['datetime'], y=df_norm['humidite_norm'],
        name='Humidité', line=dict(color='#95E1D3', width=2)
    ))
    
    fig_combined.add_trace(go.Scatter(
        x=df['datetime'], y=df_norm['pression_norm'],
        name='Pression', line=dict(color='#4ECDC4', width=2)
    ))
    
    fig_combined.add_trace(go.Scatter(
        x=df['datetime'], y=df_norm['lumiere_norm'],
        name='Luminosité', line=dict(color='#FFD93D', width=2)
    ))
    
    fig_combined.update_layout(
        title="Comparaison normalisée des paramètres",
        title_font=dict(size=20, color='white'),
        xaxis_title="Temps",
        yaxis_title="Valeur normalisée (0-1)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig_combined, use_container_width=True)
    
    # Statistiques
    st.markdown("---")
    st.markdown("## 📈 Statistiques")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🌡️ Température")
        st.write(f"**Min:** {df['temperature'].min():.1f}°C")
        st.write(f"**Max:** {df['temperature'].max():.1f}°C")
        st.write(f"**Moyenne:** {df['temperature'].mean():.1f}°C")
    
    with col2:
        st.markdown("### 💧 Humidité")
        st.write(f"**Min:** {df['humidite'].min():.1f}%")
        st.write(f"**Max:** {df['humidite'].max():.1f}%")
        st.write(f"**Moyenne:** {df['humidite'].mean():.1f}%")
    
    with col3:
        st.markdown("### 🌀 Pression")
        st.write(f"**Min:** {df['pression'].min():.1f} hPa")
        st.write(f"**Max:** {df['pression'].max():.1f} hPa")
        st.write(f"**Moyenne:** {df['pression'].mean():.1f} hPa")
    
    # Carte GPS
    st.markdown("---")
    st.markdown("## 🗺️ Localisation GPS et Trajet")
    
    # Créer la carte avec les points GPS
    fig_map = go.Figure()
   
    # Ajouter la trace du trajet
    fig_map.add_trace(go.Scattermapbox(
    lat=df['latitude'],
    lon=df['longitude'],
    mode='lines+markers',
    marker=dict(
        size=8,
        color=df.index,
        colorscale='Viridis',
        showscale=True,
        colorbar=dict(
            title=dict(
                text="Séquence",
                side="right"
            ),
            tickmode="linear"
        )
    ),
    line=dict(
        width=2,
        color='rgba(255, 107, 107, 0.6)'
    ),
    text=df['heure'],
    hovertemplate='<b>Heure:</b> %{text}<br>' +
                  '<b>Latitude:</b> %{lat:.6f}<br>' +
                  '<b>Longitude:</b> %{lon:.6f}<br>' +
                  '<b>Température:</b> ' + df['temperature'].astype(str) + '°C<br>' +
                  '<b>Humidité:</b> ' + df['humidite'].astype(str) + '%<br>' +
                  '<extra></extra>',
    name='Trajet'
))

    # Configuration de la carte
    center_lat = df['latitude'].mean()
    center_lon = df['longitude'].mean()
    
    fig_map.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=center_lat, lon=center_lon),
            zoom=14
        ),
        height=600,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Informations GPS
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📍 Position actuelle", f"{last_row['latitude']:.6f}, {last_row['longitude']:.6f}")
    with col2:
        st.metric("🏔️ Altitude", f"{last_row['altitude']:.0f} m")
    with col3:
        # Calculer la distance parcourue approximative
        if len(df) > 1:
            # Formule simplifiée de Haversine pour distance approximative
            lat_diff = df['latitude'].diff()
            lon_diff = df['longitude'].diff()
            distances = np.sqrt(lat_diff**2 + lon_diff**2) * 111  # km approximatif
            total_distance = distances.sum()
            st.metric("🚶 Distance parcourue", f"{total_distance:.2f} km")
        else:
            st.metric("🚶 Distance parcourue", "0 km")

else:
    st.info("👆 Veuillez charger un fichier CSV depuis la barre latérale pour commencer")
    st.markdown("""
    ### Format attendu du fichier LOG:
    ```
    date,heure,temperature,humidite,pression,lumiere,latitude,longitude,altitude
    251021,10:41:09,23.5,55.4,992.0,801,50.604988,3.150694,50.0
    ```
    """)