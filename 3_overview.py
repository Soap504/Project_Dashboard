import streamlit as st
import pandas as pd


def render_overview(summary_stats, overview_fig):
    st.header("Overview")

    st.markdown("""
    ### About the Dataset 
    This dataset includes email communications that are anonymized within a large European research institution. It contains directed edges(u,v) which is intended to represent a person u, sent at least one email to person v. The dataset only has communication between the institution’s members without outside contact. The dataset also contains department labels for each individual, with every person belonging to one of 42 departments.
    
    The dataset includes:
    - email-Eu-core.txt.gz 
        - This file shows the email communications between members within the large European research institution
    - email-Eu-core-department-labels.txt.gz
        - This file shows the department labels of each member within the large European research institution
    """)

    st.markdown("""
    ### Guiding Questions
    In this network:
    1. **Do communication communities align with department structure?**
    2. **Who appears structurally central?**
    3. **Which individuals may act as bridges across groups?**
    """)

    st.markdown("""
    ### What this network represents
    - **Nodes** are members of a large European research institution.
    - **Edges** represent directed email communication.
    - The network is analyzed as a **directed, unweighted graph**.
    """)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Nodes", summary_stats["nodes"])
    c2.metric("Edges", summary_stats["edges"])
    c3.metric("Density", round(summary_stats["density"], 4))
    c4.metric("Reciprocity", round(summary_stats["reciprocity"], 4))

    c5, c6 = st.columns(2)
    c5.metric("Weakly Connected Components", summary_stats["weak_components"])
    c6.metric("Strongly Connected Components", summary_stats["strong_components"])

    st.subheader("Network Preview")
    st.plotly_chart(overview_fig, use_container_width=True)
    st.caption(
        "This network preview shows the largest weakly connected component of the email network, with nodes colored by department. The visualization suggests a highly interconnected structure rather than isolated departmental clusters."
    )

    st.subheader("Why start here?")
    st.write(
        "A good dashboard begins with context before detailed visualizations. "
        "This tab helps users understand what the network represents and what questions the analysis is trying to answer."
    )

    with st.expander("Show summary values used in the analysis"):
        summary_df = pd.DataFrame({
            "metric": [
                "Average in-degree",
                "Average out-degree",
                "Maximum in-degree",
                "Maximum out-degree"
            ],
            "value": [
                summary_stats["avg_in_degree"],
                summary_stats["avg_out_degree"],
                summary_stats["max_in_degree"],
                summary_stats["max_out_degree"]
            ]
        })
        st.dataframe(summary_df, use_container_width=True)

    st.success(
        "Interpretation: Communication appears sparse overall, but reciprocity is fairly high, "
        "which suggests many ties are mutual rather than one-sided."
    )