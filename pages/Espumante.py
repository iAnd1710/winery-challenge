import streamlit as st
from src import layout
from src import utils

utils.config_streamlit()
df = utils.load_data_espumante()

tabs = st.tabs(["Introdução", "Tabela", "Gráficos"])

with tabs[0]:
    layout.tab_intro(df)

with tabs[1]:
    layout.tab_tabela(df)

with tabs[2]:
    layout.tab_graph(df)
