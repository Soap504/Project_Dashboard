import streamlit as st
import plotly.express as px


def render_centrality(top_in_df, top_out_df, top_bet_df):
    st.header("Who is Central?")

    st.markdown("""
    This section examines **structural prominence**.
    The key idea is that **importance depends on how we define it**.
    """)

    metric = st.selectbox(
        "Choose a centrality measure",
        ["in_degree", "out_degree", "betweenness"]
    )

    metric_explanations = {
        "in_degree": "In-degree highlights nodes that receive communication from many others.",
        "out_degree": "Out-degree highlights nodes that send communication broadly across the network.",
        "betweenness": "Betweenness centrality highlights nodes that may act as bridges between groups."
    }
    st.caption(metric_explanations[metric])

    top_k = st.slider(
        "How many top nodes should be shown?",
        min_value=5,
        max_value=10,
        value=10,
        key="centrality_slider"
    )

    if metric == "in_degree":
        top_nodes = top_in_df.sort_values("in_degree", ascending=False).head(top_k)
        y_col = "in_degree"
        y_title = "In-Degree"
    elif metric == "out_degree":
        top_nodes = top_out_df.sort_values("out_degree", ascending=False).head(top_k)
        y_col = "out_degree"
        y_title = "Out-Degree"
    else:
        top_nodes = top_bet_df.sort_values("betweenness", ascending=False).head(top_k)
        y_col = "betweenness"
        y_title = "Betweenness Centrality"

    left, right = st.columns([1, 1.2])

    with left:
        st.subheader("Top-ranked nodes")
        st.dataframe(top_nodes, use_container_width=True)

    with right:
        fig_bar = px.bar(
            top_nodes,
            x="node",
            y=y_col,
            title=f"Top {top_k} Nodes by {y_title}"
        )
        fig_bar.update_layout(xaxis_title="Node", yaxis_title=y_title)
        st.plotly_chart(fig_bar, use_container_width=True)

    st.write("### What should the user conclude here?")
    st.write(
        "This view supports comparison across different definitions of centrality. "
        "Some nodes stand out across multiple measures, while others appear important in only one way."
    )

    st.success(
        f"Interpretation: Under **{y_title}**, certain nodes stand out as structurally prominent. "
        "Node 160 appears especially important because it ranks highly across multiple measures."
    )