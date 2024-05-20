import streamlit as st


@st.cache_data
def config_streamlit() -> None:
    st.set_page_config(
        page_title="Tech Challenge: Exportação de Vinho",
        page_icon="🍷",
        layout="wide",
    )

    return None