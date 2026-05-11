import streamlit as st
import pandas as pd


def render_node_explorer(top_in_df, top_out_df, top_bet_df):
    st.header("Node Explorer")

    st.markdown("""
    This section is planned to support **drill-down exploration**.
    After viewing the big picture, users will be able to inspect one node in more detail.
    """)

    st.info(
        "This is still a prototype preview. For now, it shows available node rankings from the current analysis."
    )

    all_nodes = sorted(
        set(top_in_df["node"]).union(set(top_out_df["node"])).union(set(top_bet_df["node"]))
    )

    selected_node = st.selectbox("Preview a node selector", all_nodes)

    in_val = top_in_df.loc[top_in_df["node"] == selected_node, "in_degree"]
    out_val = top_out_df.loc[top_out_df["node"] == selected_node, "out_degree"]
    bet_val = top_bet_df.loc[top_bet_df["node"] == selected_node, "betweenness"]

    preview_df = pd.DataFrame({
        "metric": ["In-Degree", "Out-Degree", "Betweenness"],
        "value": [
            int(in_val.iloc[0]) if not in_val.empty else "Not in top 10",
            int(out_val.iloc[0]) if not out_val.empty else "Not in top 10",
            round(float(bet_val.iloc[0]), 6) if not bet_val.empty else "Not in top 10"
        ]
    })

    st.subheader(f"Preview for Node {selected_node}")
    st.dataframe(preview_df, use_container_width=True)

    st.caption(
        "This prototype preview shows whether the selected node appears among the current top-ranked nodes for in-degree, out-degree, and betweenness."
    )

    st.info(
        "What comes next: In the final version, this section will be updated to show a selected node’s full metrics, department label, neighborhood connections, and a small local network view so users can explore how that node fits into the larger communication structure."
    )