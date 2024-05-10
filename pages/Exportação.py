import streamlit as st
import pandas as pd

st.title("Dados de exportação")

exp_vinho_df = pd.read_csv("data/exportacao_vinho.csv", sep=";")
exp_expumante_df = pd.read_csv("data/exportacao_espumante.csv", sep=";")

st.subheader("Vinho de mesa")
st.dataframe(exp_vinho_df)

st.subheader("Espumantes")
st.dataframe(exp_expumante_df)