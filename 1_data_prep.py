import streamlit as st
import pandas as pd
import networkx as nx
from pathlib import Path
from collections import defaultdict
from sklearn.metrics import normalized_mutual_info_score
import community.community_louvain as community_louvain
import plotly.graph_objects as go



def build_overview_network_figure(g):
    """
    Build a lightweight network figure for the Overview tab.
    Uses the largest weakly connected component so the graph is easier to read.
    """

    largest_wcc_nodes = max(nx.weakly_connected_components(g), key=len)
    sub_g = g.subgraph(largest_wcc_nodes).copy()

    pos = nx.spring_layout(sub_g, seed=42)

    edge_x = []
    edge_y = []

    for source, target in sub_g.edges():
        x0, y0 = pos[source]
        x1, y1 = pos[target]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        hoverinfo="none",
        line=dict(width=0.4, color="lightgray")
    )

    node_x = []
    node_y = []
    node_color = []
    node_text = []

    for node in sub_g.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        dept = sub_g.nodes[node].get("department", -1)
        node_color.append(dept)
        node_text.append(f"Node: {node}<br>Department: {dept}")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers",
        hoverinfo="text",
        text=node_text,
        marker=dict(
            size=6,
            color=node_color,
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Department"),
            line=dict(width=0.3, color="black")
        )
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Email Network Preview (Largest Weakly Connected Component)",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        margin=dict(l=10, r=10, t=50, b=10),
        height=600
    )

    return fig

@st.cache_data
def load_network_data():
    """
    Load the email communication dataset and compute dashboard-ready results.
    """

    base_path = Path(__file__).resolve().parent

    edge_path = base_path / "email-Eu-core.txt"
    dept_path = base_path / "email-Eu-core-department-labels.txt"

    edges_df = pd.read_csv(
        edge_path,
        sep=r"\s+",
        header=None,
        names=["source", "target"]
    )

    department_df = pd.read_csv(
        dept_path,
        sep=r"\s+",
        header=None,
        names=["node", "department"]
    )

    g = nx.from_pandas_edgelist(
        edges_df,
        source="source",
        target="target",
        create_using=nx.DiGraph()
    )

    department_dict = dict(zip(department_df["node"], department_df["department"]))
    nx.set_node_attributes(g, department_dict, "department")

    # Remove self-loops
    g.remove_edges_from(nx.selfloop_edges(g))

    # -------------------------
    # Summary stats
    # -------------------------
    density = nx.density(g)
    reciprocity = nx.reciprocity(g)
    weak_components = nx.number_weakly_connected_components(g)
    strong_components = nx.number_strongly_connected_components(g)

    in_degrees = dict(g.in_degree())
    out_degrees = dict(g.out_degree())

    avg_in_degree = sum(in_degrees.values()) / len(in_degrees)
    avg_out_degree = sum(out_degrees.values()) / len(out_degrees)
    max_in_degree = max(in_degrees.values())
    max_out_degree = max(out_degrees.values())

    top_in_degree = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:10]
    top_out_degree = sorted(out_degrees.items(), key=lambda x: x[1], reverse=True)[:10]

    betweenness = nx.betweenness_centrality(g)
    top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:10]

    top_in_df = pd.DataFrame(top_in_degree, columns=["node", "in_degree"])
    top_out_df = pd.DataFrame(top_out_degree, columns=["node", "out_degree"])
    top_bet_df = pd.DataFrame(top_betweenness, columns=["node", "betweenness"])

    summary_stats = {
        "nodes": g.number_of_nodes(),
        "edges": g.number_of_edges(),
        "density": density,
        "reciprocity": reciprocity,
        "weak_components": weak_components,
        "strong_components": strong_components,
        "avg_in_degree": avg_in_degree,
        "avg_out_degree": avg_out_degree,
        "max_in_degree": max_in_degree,
        "max_out_degree": max_out_degree,
    }

    # -------------------------
    # Communities / department comparison
    # -------------------------
    partition = community_louvain.best_partition(g.to_undirected())

    community_labels = []
    department_labels = []

    for node in g.nodes():
        community_labels.append(partition[node])
        department_labels.append(g.nodes[node]["department"])

    nmi = normalized_mutual_info_score(department_labels, community_labels)
    assortativity = nx.attribute_assortativity_coefficient(g, "department")

    # Internal vs external edges
    internal_edges = 0
    external_edges = 0

    for u, v in g.edges():
        if g.nodes[u]["department"] == g.nodes[v]["department"]:
            internal_edges += 1
        else:
            external_edges += 1

    total_edges = internal_edges + external_edges

    internal_pct = internal_edges / total_edges
    external_pct = external_edges / total_edges

    # Department-level internal/external
    dept_internal = defaultdict(int)
    dept_external = defaultdict(int)

    for u, v in g.edges():
        dept_u = g.nodes[u]["department"]
        dept_v = g.nodes[v]["department"]

        if dept_u == dept_v:
            dept_internal[dept_u] += 1
        else:
            dept_external[dept_u] += 1
            dept_external[dept_v] += 1

    dept_stats = {}
    departments = sorted(set(nx.get_node_attributes(g, "department").values()))

    for dept in departments:
        internal = dept_internal[dept]
        external = dept_external[dept]
        total = internal + external

        if total > 0:
            dept_stats[dept] = {
                "internal": internal,
                "external": external,
                "internal_pct": internal / total,
                "external_pct": external / total
            }

    dept_df = pd.DataFrame([
        {
            "department": dept,
            "internal": stats["internal"],
            "external": stats["external"],
            "internal_pct": stats["internal_pct"],
            "external_pct": stats["external_pct"]
        }
        for dept, stats in dept_stats.items()
    ])

    dept_df = dept_df.sort_values("internal_pct", ascending=False)

    # Department-to-department communication matrix
    dept_list = sorted(set(department_df["department"]))
    dept_index = {dept: i for i, dept in enumerate(dept_list)}

    matrix = [[0 for _ in dept_list] for _ in dept_list]
    sender_totals = defaultdict(int)

    for u, v in g.edges():
        dept_u = g.nodes[u]["department"]
        dept_v = g.nodes[v]["department"]

        i = dept_index[dept_u]
        j = dept_index[dept_v]

        matrix[i][j] += 1
        sender_totals[dept_u] += 1

    normalized_matrix = []
    for dept_u in dept_list:
        row = []
        total = sender_totals[dept_u]
        i = dept_index[dept_u]

        for j in range(len(dept_list)):
            if total > 0:
                row.append(matrix[i][j] / total)
            else:
                row.append(0)
        normalized_matrix.append(row)

    heatmap_df = pd.DataFrame(normalized_matrix, index=dept_list, columns=dept_list)

    communities_stats = {
        "nmi": nmi,
        "assortativity": assortativity,
        "internal_edges": internal_edges,
        "external_edges": external_edges,
        "internal_pct": internal_pct,
        "external_pct": external_pct,
    }

    overview_fig = build_overview_network_figure(g)

    return (
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
    )