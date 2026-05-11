# Who Connects the Organization?
## A Network Analysis of Email Communication

**Team Members:** Sophia Arce and Tony Le

## Project Overview
This dashboard is a prototype for our network analysis project based on the **email-Eu-core** dataset from the Stanford Network Analysis Project (SNAP).
The project explores email communication within a large European research institution in order to understand how communication structure compares to formal department structure, who appears most central in the network, and which nodes may act as bridges across groups.

## Current Prototype
This version of the dashboard is a **Stage 3 prototype**. It is meant to show the planned structure of the final dashboard while also including the progress we have already made.

At this stage, the dashboard includes:
- an **Overview** tab with project context, summary statistics, and a network preview
- a **Q1: Departments & Communities** tab with community/department findings and visualizations
- in-progress sections for the remaining research questions
- an **Interpretation & Limitations** section describing current progress and next steps

Some sections are more complete than others because this is not yet the final dashboard.

## Research Questions
The dashboard is organized around these main research questions:
1. **Do communication communities align with department structure?**
2. **Who appears structurally central?**
3. **Which individuals may act as bridges across groups?**

## Files
- `demo_app.py` — main Streamlit app
- `1_data_prep.py` — loads the dataset and computes dashboard-ready results
- `2_tabs.py` — defines the dashboard tabs
- `3_overview.py` — overview tab
- `5_communities_summary.py` — Question 1 tab
- `6_q2_centrality.py` — Question 2 tab
- `7_q3_bridge_nodes.py` — Question 3 tab
- `8_interpretation.py` — interpretation and limitations tab
- `email-Eu-core.txt` — edge list
- `email-Eu-core-department-labels.txt` — department labels

## Dataset
This project uses the **email-Eu-core** dataset from SNAP.
It includes:
- a directed email network between members of a large European research institution
- department labels for each node
- anonymized node identities

## Requirements
Set up the project environment and install the required dependencies before running the dashboard:

```bash
pip install streamlit pandas plotly networkx scikit-learn python-louvain