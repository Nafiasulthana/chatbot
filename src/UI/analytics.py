import pandas as pd
import plotly.express as px
import streamlit as st

def candidate_distribution():

    data = pd.DataFrame({
        "Category":[
            "Strong Match",
            "Moderate Match",
            "Weak Match"
        ],
        "Count":[45,30,15]
    })

    fig = px.bar(
        data,
        x="Category",
        y="Count",
        title="Candidate Distribution"
    )

    st.plotly_chart(fig,use_container_width=True)

def skill_distribution():

    skills = pd.DataFrame({
        "Skill":[
            "Python",
            "SQL",
            "AWS",
            "React",
            "Docker"
        ],
        "Count":[55,40,25,20,15]
    })

    fig = px.bar(
        skills,
        x="Skill",
        y="Count",
        title="Top Skills"
    )

    st.plotly_chart(fig,use_container_width=True)