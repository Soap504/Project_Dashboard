import streamlit as st
import networkx as nx
import pandas as pd
import plotly.express as px


def render_q3_bridge_nodes(g):
    st.header("Question 3: Which individuals may act as bridges across groups?")

    st.markdown("""
    This analysis identifies **bridge nodes** that connect different parts of the network by combining:
    - **Betweenness centrality** (control over paths between nodes)
    - **Cross-department connections** (links to nodes in other departments)

    These individuals play a key role in linking otherwise separate groups.
    """)

    # --- Betweenness ---
    betweenness = nx.betweenness_centrality(g)

    # --- Cross-department connections ---
    cross_edges = {}

    for node in g.nodes():
        node_dept = g.nodes[node].get('department', None)

        neighbors = set(g.successors(node)).union(set(g.predecessors(node)))

        cross = sum(
            1 for n in neighbors
            if g.nodes[n].get('department', None) != node_dept
        )

        cross_edges[node] = cross

    # --- Data for scatter ---
    df = pd.DataFrame({
        "node": list(g.nodes()),
        "betweenness": [betweenness[n] for n in g.nodes()],
        "cross_dept": [cross_edges[n] for n in g.nodes()]
    })

    # --- Scatter plot ---
    fig = px.scatter(
        df,
        x="betweenness",
        y="cross_dept",
        hover_name="node",
        title="Bridge Nodes Identification"
    )

    fig.update_xaxes(showgrid=True, gridcolor='rgba(0,0,0,0.2)')
    fig.update_yaxes(showgrid=True, gridcolor='rgba(0,0,0,0.2)')

    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "Figure 1: Nodes in the upper-right region have both high betweenness centrality and many cross-department connections, "
        "indicating strong bridging roles."
    )

    # --- Bridge score ---
    bridge_score = {
        n: betweenness[n] * cross_edges[n]
        for n in g.nodes()
    }

    # --- Top 10 ---
    top_bridges = sorted(
        bridge_score.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]

    df_top = pd.DataFrame(top_bridges, columns=["Node", "Bridge Score"])
    df_top["Bridge Score"] = df_top["Bridge Score"].map("{:.4f}".format)

    st.write("### Top Bridge Nodes")
    st.dataframe(df_top, use_container_width=True)

    st.caption(
        "Figure 2: Bridge score is calculated as (betweenness centrality × cross-department connections), "
        "highlighting nodes that both lie on many shortest paths and connect different groups."
    )

    st.markdown("""
    ### Overall takeaway

    The results show that while cross-department communication is common throughout the network, it is not evenly distributed. 
    Instead, a smaller set of nodes play a disproportionately important role in connecting different groups.
    Nodes with high betweenness centrality and many cross-department connections act as key bridges, facilitating communication 
    across the organization. This suggests that even though many individuals communicate across departments, the overall structure 
    of the network still relies on a limited number of nodes to maintain connectivity between groups.
    These bridge nodes are therefore critical to the flow of information and the cohesion of the network as a whole.
    """)