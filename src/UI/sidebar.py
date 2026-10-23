import streamlit as st

def render_sidebar():

    with st.sidebar:

        st.markdown("# 🟡 TalentAI")

        st.divider()

        page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "Resume Screening",
                "Candidate Ranking",
                "Analytics",
                "Portfolio Generator"
            ]
        )

        st.divider()

        st.caption("TalentAI ATS v1.0")

    return page