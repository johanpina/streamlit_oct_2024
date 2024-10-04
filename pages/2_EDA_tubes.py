import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot_histogram(Column,title):
    plt.figure(figsize=(6,4))
    plt.hist(data[Column], bins=20, color='skyblue',edgecolor='black')
    plt.title(title)
    plt.title(Column)
    plt.xlabel(Column)
    plt.ylabel('Frequency')
    return plt 

def box_plot(Column,title):
    plt.figure(figsize=(6,4))
    plt.boxplot(data[Column])
    plt.title(title)
    plt.title(Column)
    plt.xlabel(Column)
    plt.ylabel('Frequency')
    return plt

st.title("EDA🔝")

data = pd.read_csv("models/data/12DB_6FP.csv")


name_clases = {0:"DB",1:"SS",2:"SW",3:"A",4:"I",5:"B"}
data['FlowPattern'] = data['FlowPattern'].replace(name_clases)

st.dataframe(data)

st.subheader("Descripción de los datos")

st.dataframe(data.describe())

st.markdown("---")

col1 , col2 = st.columns(2)

with col1:
    st.write("Histograma")
    selected_column = st.selectbox("Seleccione una columna",data.columns)
    st.pyplot(plot_histogram(selected_column,f"Histograma de {selected_column}"))
with col2:
    st.write("Boxplot")
    selected_column = st.selectbox("Seleccione otra columna",data.columns)
    st.pyplot(box_plot(selected_column,f"Histograma de {selected_column}"))


