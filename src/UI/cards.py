import streamlit as st

def metric_card(title,value):

    st.markdown(
        f"""
        <div class='metric-card'>
            <h3>{title}</h3>
            <h1>{value}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )