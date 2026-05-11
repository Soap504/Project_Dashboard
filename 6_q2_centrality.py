import streamlit as st
import networkx as nx
import pandas as pd
import plotly.express as px


def render_q2_centrality(g):
    st.header("Question 2: Who appears structurally central?")

    st.markdown("""
    This analysis identifies **structurally central individuals** in the network using:
    - **Betweenness centrality** (control over information flow)
    - **In-degree** (how many connections they receive)
    - **Out-degree** (how many connections they initiate)

    These metrics together highlight individuals who are highly connected and influential within the network.
    """)

    # --- Degree ---
    in_degree = dict(g.in_degree())
    out_degree = dict(g.out_degree())

    # --- Betweenness ---
    betweenness = nx.betweenness_centrality(g)

    # --- Central score ---
    central_score = {
        n: betweenness[n] + in_degree[n] + out_degree[n]
        for n in g.nodes()
    }

    # --- Slider ---
    max_nodes = min(300, len(g.nodes()))  # cap for readability
    top_n = st.slider(
        "Select number of top nodes to display",
        min_value=10,
        max_value=max_nodes,
        value=10,
        step=10
    )

    # --- View selector ---
    view = st.radio("Select view", ["Bar Chart", "Distribution Curve"])

    # --- Sort all nodes ---
    sorted_nodes = sorted(
        central_score.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_central = sorted_nodes[:top_n]

    df_top = pd.DataFrame(top_central, columns=["Node", "Central Score"])
    df_top.insert(0, "Rank", range(1, len(df_top) + 1))

    # --- BAR CHART ---
    if view == "Bar Chart":
        fig = px.bar(
            df_top,
            x="Node",
            y="Central Score",
            color="Central Score",
            color_continuous_scale="Blues",
            title=f"Top {top_n} Most Central Individuals",
            text="Central Score"
        )

        fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
        fig.update_layout(xaxis={'categoryorder': 'total descending'})
        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.2)')

    # --- DISTRIBUTION CURVE ---
    else:
        df_all = pd.DataFrame(sorted_nodes, columns=["Node", "Central Score"])
        df_all["Rank"] = range(1, len(df_all) + 1)

        fig = px.line(
            df_all.head(top_n),
            x="Rank",
            y="Central Score",
            title="Centrality Score Distribution"
        )

        fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.2)')

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
    "Figure 1: This visualization shows the distribution of centrality scores for the top-ranked nodes, "
    "calculated as (betweenness centrality + in-degree + out-degree). The bar chart highlights the most "
    "central individuals directly, while the distribution curve shows how centrality declines as rank increases. "
    "Together, these views illustrate that a small number of nodes have significantly higher centrality scores, "
    "indicating that influence and connectivity are concentrated among a few key individuals."
    )

    # --- Table ---
    df_display = df_top.copy()
    df_display["Central Score"] = df_display["Central Score"].map("{:.4f}".format)

    st.write("### Top Central Nodes")
    st.dataframe(df_display, use_container_width=True)

    st.caption(
        "Figure 2: Central score is defined as: (betweenness centrality + in-degree + out-degree). "
        "This metric captures both a node’s role in information flow and its overall level "
        "of connectivity within the network."
    )

    st.markdown("""
    ### Overall takeaway

    The results indicate that centrality in the network is concentrated among a relatively small number of nodes. 
    These individuals have high combined scores due to their high in-degrees and out-degrees
    and their high betweenness centrality. This suggests that influence and communication activity are not evenly distributed, but instead centered around 
    key individuals who are both highly connected and frequently lie on important communication paths. 
    While many nodes participate in the network, these central nodes play a dominant role in maintaining overall 
    connectivity and facilitating the flow of information.
    """)