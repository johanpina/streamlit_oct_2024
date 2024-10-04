import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import folium
from streamlit_folium import st_folium

# Título
st.title("Clustering Geográfico de Crímenes en San Francisco por Categoría de Crimen")

# Descripción
st.write("""
Este ejemplo utiliza el algoritmo KMeans para realizar un clustering geográfico de incidentes de crímenes en San Francisco.
Puedes seleccionar una categoría de crimen y se te asignará el cluster más cercano basado en las ubicaciones de esos crímenes.
""")

# Cargar el dataset de incidentes de crímenes en San Francisco
@st.cache_data
def load_crime_data():
    # Dataset de crímenes en San Francisco
    url = "https://data.sfgov.org/resource/wg3w-h783.csv?$limit=10000"
    data = pd.read_csv(url)
    data = data[['incident_id', 'latitude', 'longitude', 'incident_category', 'incident_subcategory', 'police_district']]
    data = data.dropna()  # Eliminar datos faltantes
    return data

data = load_crime_data()

# Mostrar una vista previa de los datos
st.write("Datos de incidentes de crímenes cargados:")
st.dataframe(data.head())

# Entrenamiento del modelo KMeans
st.write("Entrenando el modelo de clustering con KMeans...")

# Definir el número de clusters
num_clusters = st.slider("Número de clusters (agrupación de incidentes de crímenes)", 2, 20, 10)

# Entrenar el modelo con las coordenadas geográficas de los incidentes
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(data[['latitude', 'longitude']])

# Añadir las etiquetas de los clusters a los datos
data['cluster'] = kmeans.labels_

# Crear una lista de categorías de crimen disponibles
categorias = data['incident_category'].unique()

# Selección del usuario basada en la categoría de crimen
st.write("Selecciona una categoría de crimen para asignarla al cluster más cercano:")

categoria_seleccionada = st.selectbox("Categoría de crimen", categorias)

# Filtrar los incidentes por la categoría seleccionada
incidentes_filtrados = data[data['incident_category'] == categoria_seleccionada]

# Calcular el centroide de las coordenadas de los incidentes filtrados
centroide_lat = incidentes_filtrados['latitude'].mean()
centroide_lng = incidentes_filtrados['longitude'].mean()

st.write(f"Ubicación promedio para la categoría '{categoria_seleccionada}' es: ({centroide_lat}, {centroide_lng})")

# Predecir el cluster más cercano basado en el centroide
predicted_cluster = kmeans.predict([[centroide_lat, centroide_lng]])[0]

# Mostrar el resultado de la predicción
st.write(f"La categoría de crimen seleccionada pertenece al grupo número {predicted_cluster}, correspondiente a la ubicación más cercana.")

# Crear un mapa con Folium para visualizar los clusters
st.write("Mapa interactivo con los clusters de crímenes y la ubicación calculada:")

# Crear el mapa centrado en San Francisco
mapa = folium.Map(location=[37.7749, -122.4194], zoom_start=12)

# Colorear los incidentes de crímenes por su cluster
for i, row in data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=3,
        color='blue' if row['cluster'] == predicted_cluster else 'gray',
        fill=True,
        fill_color='blue' if row['cluster'] == predicted_cluster else 'gray',
        fill_opacity=0.7,
        popup=f"Categoría: {row['incident_category']}, Subcategoría: {row['incident_subcategory']}, Distrito: {row['police_district']}"
    ).add_to(mapa)

# Añadir la ubicación calculada por el usuario
folium.Marker(
    location=[centroide_lat, centroide_lng],
    popup=f"Ubicación calculada para {categoria_seleccionada}",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(mapa)

# Mostrar el mapa en Streamlit
st_folium(mapa, width=700, height=500)