import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
import folium
from streamlit_folium import folium_static

# Título
st.title("Clustering Geográfico con KMeans y Folium")

# Descripción
st.write("""
Este ejemplo utiliza el algoritmo KMeans para realizar un clustering geográfico. 
Puedes ingresar unas coordenadas (latitud y longitud) para que se te asigne el grupo más cercano basado en las ciudades del dataset.
""")

# Cargar el dataset de ciudades (puedes usar un dataset de ciudades del mundo)
@st.cache_data
def load_data():
    # Dataset de ciudades del mundo (puedes cambiarlo por cualquier otro dataset)
    url = "https://simplemaps.com/static/data/world-cities/basic/simplemaps_worldcities_basicv1.75/worldcities.csv"
    data = pd.read_csv(url)
    #data = data[['city', 'lat', 'lng', 'population']]
    data = data.dropna()  # Eliminar datos faltantes
    return data

data = load_data()

# Mostrar una vista previa de los datos
st.write("Datos de ciudades cargados:")
st.dataframe(data.head())


# Entrenamiento del modelo KMeans
st.write("Entrenando el modelo de clustering con KMeans...")

# Definir el número de clusters
num_clusters = st.slider("Número de clusters (ciudades cercanas)", 2, 20, 10)

# Entrenar el modelo con las coordenadas geográficas
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
kmeans.fit(data[['lat', 'lng']])

# Añadir las etiquetas de los clusters a los datos
data['cluster'] = kmeans.labels_

# Entrada del usuario para las coordenadas geográficas
st.write("Ingresa tus coordenadas para encontrar la ciudad más cercana:")

latitud = st.number_input("Latitud", min_value=-90.0, max_value=90.0, value=0.0, step=0.1)
longitud = st.number_input("Longitud", min_value=-180.0, max_value=180.0, value=0.0, step=0.1)

# Predecir el cluster más cercano basado en las coordenadas ingresadas
predicted_cluster = kmeans.predict([[latitud, longitud]])[0]

# Mostrar el resultado de la predicción
st.write(f"Te encuentras en el grupo número {predicted_cluster}, correspondiente a la ciudad más cercana.")

# Crear un mapa con Folium para visualizar los clusters
st.write("Mapa interactivo con los clusters y tu ubicación:")

# Crear el mapa centrado en el primer grupo
mapa = folium.Map(location=[data['lat'].mean(), data['lng'].mean()], zoom_start=2)


# Colorear las ciudades por su cluster
for i, row in data.iterrows():
    folium.CircleMarker(
        location=[row['lat'], row['lng']],
        radius=5,
        color='blue' if row['cluster'] == predicted_cluster else 'gray',
        fill=True,
        fill_color='blue' if row['cluster'] == predicted_cluster else 'gray',
        fill_opacity=0.7,
        popup=f"{row['city']} (Cluster {row['cluster']})"
    ).add_to(mapa)

# Añadir la ubicación ingresada por el usuario
folium.Marker(
    location=[latitud, longitud],
    popup="Tu ubicación",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(mapa)

# Mostrar el mapa en Streamlit
folium_static(mapa)