import streamlit as st
import pandas as pd

st.title("Dados de produção")

producao_df = pd.read_csv("data/producao.csv", sep=";")

st.subheader("Vinho de mesa")
st.dataframe(producao_df)