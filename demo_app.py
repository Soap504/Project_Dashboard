import streamlit as st
from importlib import import_module

data_module = import_module("1_data_prep")
tabs_module = import_module("2_tabs")
overview_module = import_module("3_overview")
communities_summary_module = import_module("5_communities_summary")
q2_centrality_module = import_module("6_q2_centrality")
q3_bridge_nodes_module = import_module("7_q3_bridge_nodes")
interpretation_module = import_module("8_interpretation")

st.set_page_config(
    page_title="Who Connects the Organization?",
    layout="wide"
)

(
    g,
    edges_df,
    department_df,
    summary_stats,
    top_in_df,
    top_out_df,
    top_bet_df,
    communities_stats,
    dept_df,
    heatmap_df,
    overview_fig
) = data_module.load_network_data()

st.title("Who Connects the Organization?")
st.write("**A Network Analysis of Email Communication**")
st.write("**Team Members:** Sophia Arce and Tony Le")

st.write(
    "This dashboard explores email communication within a large European research institution. "
    "It is designed to help users understand how communication structure compares to formal departments, "
    "who appears most central in the network, and which nodes may act as bridges across groups."
)

tab1, tab2, tab3, tab4, tab5 = tabs_module.create_tabs()

with tab1:
    overview_module.render_overview(summary_stats, overview_fig)

with tab2:
    communities_summary_module.render_communities_summary(
        communities_stats,
        dept_df,
        heatmap_df
    )

with tab3:
    q2_centrality_module.render_q2_centrality(g)

with tab4:
    q3_bridge_nodes_module.render_q3_bridge_nodes(g)

with tab5:
    interpretation_module.render_interpretation()