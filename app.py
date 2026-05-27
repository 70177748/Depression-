from __future__ import annotations
from pathlib import Path
import os
import zipfile
import pandas as pd
import numpy as np
import streamlit as st
from filters import detect_columns, apply_filters, add_features
import charts

st.set_page_config(
    page_title="Reddit Depression in Indian Society Dashboard",
    page_icon="🧠",
    layout="wide"
)

CSS = """
<style>
.block-container{padding-top:1.2rem;}
.hero{padding:28px;border-radius:26px;background:linear-gradient(135deg,#1e293b,#0f172a);color:white;}
.hero h1{font-size:2.3rem;margin-bottom:.25rem;}
.hero p{font-size:1rem;opacity:.95;}
.kpi{padding:18px;border-radius:20px;background:#111827;color:white;}
.small-note{opacity:.75;font-size:.86rem;}
[data-testid="stMetricValue"]{font-size:1.8rem;}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_data(uploaded_file=None):

    if uploaded_file is not None:
        name = uploaded_file.name.lower()

        if name.endswith(".csv"):
            return pd.read_csv(uploaded_file)

        if name.endswith((".xlsx", ".xls")):
            return pd.read_excel(uploaded_file)

        if name.endswith(".json"):
            return pd.read_json(uploaded_file)

    if os.path.exists("society depression.zip"):
        with zipfile.ZipFile("society depression.zip") as z:
            csv_name = [f for f in z.namelist() if f.endswith(".csv")][0]
            return pd.read_csv(z.open(csv_name))

    data_dir = Path(__file__).parent / "data"

    files = [
        p for p in data_dir.glob("*")
        if p.suffix.lower() in [".csv", ".xlsx", ".xls", ".json"]
    ]

    if not files:
        return None

    p = files[0]

    if p.suffix.lower() == ".csv":
        return pd.read_csv(p)

    if p.suffix.lower() in [".xlsx", ".xls"]:
        return pd.read_excel(p)

    return pd.read_json(p)

st.markdown("""
<div class='hero'>
<h1>🧠 Reddit Depression in Indian Society Dashboard</h1>
<p>Interactive mental health discourse analysis dashboard</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:

    st.header("Dataset")

    uploaded = st.file_uploader(
        "Upload dataset",
        type=["csv", "xlsx", "xls", "json"]
    )

df = load_data(uploaded)

if df is None:
    st.error("No dataset found.")
    st.stop()

df = add_features(df)

filtered = apply_filters(df)

numeric_cols, categorical_cols, date_cols = detect_columns(filtered)

main_num = numeric_cols[0] if numeric_cols else None
main_cat = categorical_cols[0] if categorical_cols else None

tabs = st.tabs([
    "Overview",
    "Charts",
    "Mental Health Signals",
    "Dataset"
])

with tabs[0]:

    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Total Records", len(filtered))

    if numeric_cols:
        k2.metric(
            "Average Score",
            round(filtered[numeric_cols[0]].mean(), 2)
        )

    if "_risk_score" in filtered.columns:
        k3.metric(
            "Average Risk",
            round(filtered["_risk_score"].mean(), 2)
        )

    if "_word_count" in filtered.columns:
        k4.metric(
            "Avg Words",
            round(filtered["_word_count"].mean(), 0)
        )

    left, right = st.columns([1.2, 1])

    with left:
        st.pyplot(
            charts.line_chart(filtered),
            use_container_width=True
        )

        st.pyplot(
            charts.area_chart(filtered),
            use_container_width=True
        )

    with right:
        st.pyplot(
            charts.count_plot(filtered),
            use_container_width=True
        )

        st.pyplot(
            charts.word_cloud(filtered),
            use_container_width=True
        )

with tabs[1]:

    st.subheader("All 10 Required Chart Types")

    a, b = st.columns(2)

    with a:

        st.pyplot(
            charts.pie_chart(filtered, main_cat),
            use_container_width=True
        )

        st.pyplot(
            charts.histogram(filtered, main_num),
            use_container_width=True
        )

        st.pyplot(
            charts.bar_chart(filtered, main_cat),
            use_container_width=True
        )

        st.pyplot(
            charts.box_plot(filtered, main_cat, main_num),
            use_container_width=True
        )

        st.pyplot(
            charts.heatmap(filtered),
            use_container_width=True
        )

    with b:

        st.pyplot(
            charts.line_chart(filtered),
            use_container_width=True
        )

        st.pyplot(
            charts.scatter_plot(
                filtered,
                main_num,
                "_risk_score"
            ),
            use_container_width=True
        )

        st.pyplot(
            charts.area_chart(filtered),
            use_container_width=True
        )

        st.pyplot(
            charts.count_plot(filtered),
            use_container_width=True
        )

        st.pyplot(
            charts.violin_plot(
                filtered,
                main_cat,
                "_risk_score"
            ),
            use_container_width=True
        )

with tabs[2]:

    st.subheader("Mental Health Text Signals")

    cols = [
        "_clean_text",
        "_word_count",
        "_negative_terms",
        "_positive_terms",
        "_risk_score",
        "_risk_band"
    ]

    st.dataframe(
        filtered[cols]
        .sort_values("_risk_score", ascending=False)
        .head(100),
        use_container_width=True,
        hide_index=True
    )

with tabs[3]:

    st.subheader("Filtered Dataset Preview")

    st.dataframe(
        filtered.head(500),
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download filtered CSV",
        filtered.to_csv(index=False).encode("utf-8"),
        "filtered_reddit_depression_dashboard.csv",
        "text/csv"
    )

st.caption(
    "Educational EDA only — this dashboard does not diagnose mental-health conditions."
)

        
