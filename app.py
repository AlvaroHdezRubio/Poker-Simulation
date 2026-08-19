# Importamos Streamlit.
import streamlit as st


# Configuramos el título de la pestaña del navegador.
st.set_page_config(
    page_title="Calculadora de póker",
    page_icon="♠️",
    layout="centered"
)


# Título principal de la aplicación.
st.title("♠️ Calculadora de póker")


# Texto provisional.
st.write(
    "Primera prueba de la aplicación en Streamlit."
)


# Botón de prueba.
if st.button("Probar aplicación"):

    st.success(
        "Streamlit está funcionando correctamente."
    )
