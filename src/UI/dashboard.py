import streamlit as st
from cards import metric_card
from analytics import candidate_distribution
from analytics import skill_distribution

def render_dashboard():

    st.title("🟡 TalentAI Dashboard")

    c1,c2,c3,c4 = st.columns(4)

    with c1:
        metric_card(
            "Resumes Uploaded",
            "248"
        )

    with c2:
        metric_card(
            "Strong Matches",
            "72"
        )

    with c3:
        metric_card(
            "Avg Fit Score",
            "84%"
        )

    with c4:
        metric_card(
            "Candidates Ranked",
            "196"
        )

    st.divider()

    st.subheader("Candidate Ranking")

    ranking = [
        {
            "Rank":1,
            "Candidate":"John Doe",
            "Score":"94%",
            "Skills":"Python, AWS"
        },
        {
            "Rank":2,
            "Candidate":"Sarah",
            "Score":"89%",
            "Skills":"React, Node"
        },
        {
            "Rank":3,
            "Candidate":"Mike",
            "Score":"84%",
            "Skills":"SQL, Docker"
        }
    ]

    st.dataframe(
        ranking,
        use_container_width=True
    )

    st.divider()

    candidate_distribution()

    skill_distribution()