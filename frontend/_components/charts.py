"""
components/charts.py
====================
กราฟที่ใช้ซ้ำได้ทุก page
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from frontend.config import CATEGORY_COLORS

def pie_chart(df: pd.DataFrame) -> go.Figure:
    """Donut pie chart สำหรับ topic breakdown"""
    fig = px.pie(
        df, names="category", values="count",
        color="category", color_discrete_map=CATEGORY_COLORS,
        hole=0.42,
    )
    fig.update_traces(textinfo="label+percent", pull=[0.03] * len(df))
    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35),
        showlegend=True,
    )
    return fig


def stock_line_chart(df: pd.DataFrame, label: str) -> go.Figure:
    """Line chart ราคาหุ้น พร้อม star markers วันที่มีโพสต์ใหญ่"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["date"], y=df["price"],
        mode="lines", name=label,
        line=dict(color="#378ADD", width=2),
        hovertemplate="%{x}<br>" + label + ": %{y:,.2f}<extra></extra>",
    ))
    big = df[df["has_big_post"]]
    if not big.empty:
        fig.add_trace(go.Scatter(
            x=big["date"], y=big["price"],
            mode="markers", name="Major Trump post",
            marker=dict(color="#E24B4A", size=11, symbol="star"),
            hovertemplate="%{x}<br>Major post<extra></extra>",
        ))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=f"{label} Price",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
        margin=dict(t=20, b=60, l=60, r=20),
        hovermode="x unified",
    )
    return fig


def category_impact_bar(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart ผลกระทบต่อตลาดแยกตาม category"""
    df = df.sort_values("avg_impact")
    df["color"] = df["avg_impact"].apply(lambda x: "#E24B4A" if x < 0 else "#1D9E75")
    fig = px.bar(
        df, x="avg_impact", y="category", orientation="h",
        color="avg_impact",
        color_continuous_scale=["#E24B4A", "#F1EFE8", "#1D9E75"],
        color_continuous_midpoint=0,
        labels={"avg_impact": "Avg % change (5 min)", "category": ""},
    )
    fig.add_vline(x=0, line_width=1, line_color="gray", line_dash="dot")
    fig.update_layout(
        margin=dict(t=10, b=20, l=180, r=20),
        coloraxis_showscale=False,
    )
    return fig


def gdelt_tone_bar(df: pd.DataFrame) -> go.Figure:
    """Bar chart global tone ต่อสัปดาห์"""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["week"], y=df["avg_tone"],
        marker_color=["#E24B4A" if v < -1.5 else "#378ADD" for v in df["avg_tone"]],
        hovertemplate="%{x}<br>Tone: %{y:.2f}<extra></extra>",
    ))
    fig.add_hline(y=0, line_width=1, line_color="gray", line_dash="dot")
    fig.update_layout(
        xaxis_title="Week", yaxis_title="Avg tone (negative = conflict)",
        margin=dict(t=10, b=40, l=60, r=20),
    )
    return fig


def gdelt_breakdown_bar(gdelt: dict) -> go.Figure:
    """Bar chart GDELT signals สัปดาห์นี้"""
    df = pd.DataFrame({
        "signal":  ["Military", "Verbal conflict", "Verbal cooperation", "Material conflict", "Diplomatic"],
        "count":   [gdelt["military_events"], gdelt["verbal_conflict"],
                    gdelt["verbal_cooperation"], gdelt["material_conflict"], gdelt["diplomatic"]],
        "type":    ["negative", "negative", "positive", "negative", "positive"],
    })
    fig = px.bar(
        df, x="signal", y="count", color="type",
        color_discrete_map={"negative": "#E24B4A", "positive": "#1D9E75"},
        labels={"count": "Events this week", "signal": ""},
    )
    fig.update_layout(margin=dict(t=10, b=20), showlegend=False)
    return fig
