import streamlit as st

from src import functions as f


if __name__ == "__main__":
    f.config_streamlit()

    tabs = st.tabs(["🌎", "📋", "📊"])

    with tabs[0]:
        st.markdown(
            """Aba 1"""
        )

    with tabs[1]:
        st.markdown(
            """Aba 2"""
        )


    with tabs[2]:
        st.markdown(
            """Aba 3"""
        )
