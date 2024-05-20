import streamlit as st
from src import layout
from src import utils


if __name__ == "__main__":
    #Streamlit config
    utils.config_streamlit()
    
    #Carregando os dados
    df = utils.load_data()
    df_espumante = utils.load_data_espumante()
    
    #Header
    layout.header()
