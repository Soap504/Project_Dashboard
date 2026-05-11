import streamlit as st


def create_tabs():
    return st.tabs([
        "Overview",
        "Q1: Departments & Communities",
        "Q2: Centrality",
        "Q3: Bridge Nodes",
        "Interpretation & Limitations"
    ])