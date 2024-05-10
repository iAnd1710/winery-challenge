import streamlit as st


if "y" == 'y':
    from src.components import sidebar
    sidebar.show_sidebar()

st.title('winery_challenge')
st.write('Pos Tech ')