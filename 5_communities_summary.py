import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def render_communities_summary(communities_stats, dept_df, heatmap_df):
    st.header("Question 1: Do communication communities align with department structure?")

    st.markdown("""
    This section compares detected communication structure with the institution’s department structure.
    It focuses on whether communication stays mostly within departments or moves across them.
    """)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("NMI", f"{communities_stats['nmi']:.3f}")
    c2.metric("Assortativity", f"{communities_stats['assortativity']:.3f}")
    c3.metric("Internal Edges", communities_stats["internal_edges"])
    c4.metric("External Edges", communities_stats["external_edges"])

    chart_df = pd.DataFrame({
        "type": ["Internal", "External"],
        "proportion": [
            communities_stats["internal_pct"],
            communities_stats["external_pct"]
        ]
    })

    fig_main = px.bar(
        chart_df,
        x="type",
        y="proportion",
        title="Internal vs External Communication",
        text="proportion"
    )
    fig_main.update_traces(texttemplate="%{text:.3f}", textposition="outside")
    fig_main.update_layout(
        yaxis_title="Proportion",
        xaxis_title="Communication Type"
    )

    st.plotly_chart(fig_main, use_container_width=True)
    st.caption(
        "Figure 1. Most communication in the network occurs across departments rather than within them, suggesting that the institution operates as an interconnected communication system."
    )

    st.subheader("Internal Communication % by Department")

    fig_bar = px.bar(
        dept_df,
        x="internal_pct",
        y="department",
        orientation="h",
        title="Internal Communication % by Department"
    )
    fig_bar.update_layout(
        xaxis_title="Internal Communication Proportion",
        yaxis_title="Department #"
    )

    st.plotly_chart(fig_bar, use_container_width=True)
    st.caption(
        "Figure 2. Internal communication varies by department, but most departments show relatively low internal proportions, suggesting that much of the network’s communication crosses department boundaries."
    )

    st.subheader("Top Departments: Internal vs External Communication")

    top_n = st.slider(
        "Choose how many top departments to display",
        min_value=5,
        max_value=min(15, len(dept_df)),
        value=10,
        key="dept_top_n_slider"
    )

    top_dept_df = dept_df.head(top_n).copy()

    fig_stacked = go.Figure()

    fig_stacked.add_trace(go.Bar(
        y=top_dept_df["department"].astype(str),
        x=top_dept_df["internal_pct"],
        name="Internal",
        orientation="h",
        marker_color="steelblue"
    ))

    fig_stacked.add_trace(go.Bar(
        y=top_dept_df["department"].astype(str),
        x=top_dept_df["external_pct"],
        name="External",
        orientation="h",
        marker_color="darkorange"
    ))

    fig_stacked.update_layout(
        barmode="stack",
        title=f"Internal vs External Communication by Department (Top {top_n})",
        xaxis_title="Proportion of Communication",
        yaxis_title="Department",
        legend_title="",
        height=500
    )

    st.plotly_chart(fig_stacked, use_container_width=True)
    st.caption(
        "Figure 3. This view compares the top departments by internal communication share and shows that even among the more internally focused departments, external communication still makes up a large portion of total communication."
    )

    st.subheader("Normalized Department-to-Department Communication")

    fig_heatmap = px.imshow(
        heatmap_df,
        labels=dict(x="Receiver Department", y="Sender Department", color="Proportion"),
        aspect="auto",
        title="Normalized Department-to-Department Communication"
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.caption(
        "Figure 4. The heatmap shows both within-department and cross-department communication, with substantial off-diagonal activity indicating that communication across departments is common and structured."
    )

    st.write("### Overall takeaway")
    st.write(
        "The results show that people do still communicate within their own departments, so the department structure is clearly present in the network. At the same time, there appears to be even more communication happening across different departments than within the same one. This makes the network look less like a set of separate groups and more like an organization where departments regularly work and communicate with each other. Some departments seem more internally focused than others, so the pattern is not exactly the same everywhere. Overall, department membership still matters, but communication across departments appears to be more noticeable."
    )