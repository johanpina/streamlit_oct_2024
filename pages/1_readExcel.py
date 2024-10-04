import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt

st.title("EDA🔝")


file = st.file_uploader("Sube un archivo .xlsx", type=["xlsx"])


if file is not None:

    df = pd.read_excel(file)
    st.write("Datos del archivo:")
    st.dataframe(df)

    columna = st.selectbox("Selecciona una columna", df.columns)

    if columna:
        fig, ax = plt.subplots()
        df[columna].value_counts().plot(kind="pie",ax=ax,autopct='%1.1f%%')

        st.pyplot(fig)



