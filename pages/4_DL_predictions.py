import streamlit as st
import tensorflow as tf
import numpy as np


@st.cache()
def load_model():
    model = tf.keras.models.load_model('models/basic_iris_model.h5')
    return model    


model = load_model()

# Definir la función de predicción
def predict(input_data):
    input_data = np.array(input_data).reshape(1, -1)
    predictions = model.predict(input_data)
    predicted_class = tf.argmax(predictions, axis=1).numpy()[0]
    return predicted_class

# Interfaz de usuario de Streamlit
st.title("Predicción del Modelo Iris")

# Crear campos de entrada para las características
sepal_length = st.slider("Longitud del sépalo", min_value=0.0, max_value=10.0, step=0.1)
sepal_width = st.slider("Ancho del sépalo", min_value=0.0, max_value=10.0, step=0.1)
petal_length = st.slider("Longitud del pétalo", min_value=0.0, max_value=10.0, step=0.1)
petal_width = st.slider("Ancho del pétalo", min_value=0.0, max_value=10.0, step=0.1)

# Botón para hacer la predicción


input_data = [sepal_length, sepal_width, petal_length, petal_width]
prediction = predict(input_data)
st.write(f"La clase predicha es: {prediction}")

