"""
backend/model_dashboard.py
==========================
Trump Truth Social → Market Impact 可视化 Dashboard。
依赖 model_training.run_pipeline() 的输出结果。

用法：
    python -m backend.model_dashboard         # 训练 + 启动 dashboard
    from backend.model_dashboard import build_dashboard
"""

import warnings

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, dash_table, dcc, html

from backend.model_training import (
    PRIMARY_TICKER,
    TICKER_NAMES,
    TICKERS,
    run_pipeline,
)

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# THEME
# ─────────────────────────────────────────────
BG      = "#1e1e2e"
CARD_BG = "#2a2a3e"
HIGH_C  = "#ff4b4b"
LOW_C   = "#4b9eff"
GOLD    = "#ffd700"
GREEN   = "#7fff7f"
PURPLE  = "#c084fc"


def kpi(label, value, color="#ffffff"):
    return dbc.Card(dbc.CardBody([
        html.H2(value, style={"color": color, "marginBottom": 0}),
        html.P(label,  style={"color": "#aaa", "marginTop": "4px"}),
    ]), style={"backgroundColor": CARD_BG, "borderRadius": "10px",
               "textAlign": "center"})


# ─────────────────────────────────────────────
# BUILD DASHBOARD
# ─────────────────────────────────────────────
def build_dashboard(posts: pd.DataFrame,
                    importance: pd.DataFrame,
                    metrics: dict,
                    cat_cols: list,
                    gdelt_cols: list) -> dash.Dash:
    
    # FIX: ensure market_period exists (daily data does not have it)
    if "market_period" not in posts.columns:
        posts["market_period"] = "unknown"

    app       = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    has_proba = "impact_proba" in posts.columns and posts["impact_proba"].notna().any()

    # ── Static figures ───────────────────────────────────

    # Feature importance top-20
    fig_imp = px.bar(
        importance.head(20)[::-1],
        x="importance", y="feature", orientation="h",
        title="Top-20 XGBoost Feature Importance",
        color="importance", color_continuous_scale="Plasma",
        template="plotly_dark",
    ).update_layout(paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
                    showlegend=False, coloraxis_showscale=False)

    # ROC curve
    fig_roc = go.Figure([
        go.Scatter(x=metrics["fpr"], y=metrics["tpr"], mode="lines",
                   name=f"Test AUC = {metrics['roc_auc']:.3f}",
                   line=dict(color=HIGH_C, width=2)),
        go.Scatter(x=[0, 1], y=[0, 1], mode="lines",
                   line=dict(dash="dash", color="gray"), name="Random"),
    ]).update_layout(
        title=f"ROC Curve (holdout: {metrics['test_start']} → {metrics['test_end']})",
        xaxis_title="FPR", yaxis_title="TPR",
        template="plotly_dark", paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
    )

    # Precision-Recall curve
    fig_pr = go.Figure([
        go.Scatter(x=metrics["rec"], y=metrics["prec"], mode="lines",
                   name=f"AP = {metrics['avg_precision']:.3f}",
                   line=dict(color=LOW_C, width=2)),
    ]).update_layout(
        title="Precision-Recall Curve (test set)",
        xaxis_title="Recall", yaxis_title="Precision",
        template="plotly_dark", paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
    )

    # LLM category: avg score high vs low impact
    lbl_mask     = posts["high_impact"].notna()
    existing_cat = [c for c in cat_cols if c in posts.columns]
    if existing_cat and lbl_mask.any():
        cat_df = (posts[lbl_mask]
                  .groupby("high_impact")[existing_cat]
                  .mean().T.reset_index())
        cat_df.columns = (
            ["category"] + [f"impact_{int(c)}" for c in cat_df.columns[1:]]
        )
        cat_df["category"] = cat_df["category"].str.replace("cat_", "", regex=False)
        fig_cat = go.Figure()
        if "impact_0" in cat_df.columns:
            fig_cat.add_trace(go.Bar(name="Low Impact",  x=cat_df["category"],
                                     y=cat_df["impact_0"], marker_color=LOW_C))
        if "impact_1" in cat_df.columns:
            fig_cat.add_trace(go.Bar(name="High Impact", x=cat_df["category"],
                                     y=cat_df["impact_1"], marker_color=HIGH_C))
        fig_cat.update_layout(
            title="LLM Category Scores: High vs Low Market Impact",
            barmode="group", template="plotly_dark",
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            xaxis_tickangle=-35, legend=dict(orientation="h"),
        )
    else:
        fig_cat = go.Figure().update_layout(
            title="LLM Categories (no data)", template="plotly_dark",
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        )

    # Multi-ticker heatmap
    ret_map = {t: f"{t}_daily_ret" for t in TICKERS if f"{t}_daily_ret" in posts.columns}
    if ret_map and lbl_mask.any():
        hmap_rows = []
        for t, col in ret_map.items():
            sub = posts[lbl_mask & posts[col].notna()]
            if sub.empty:
                continue
            hmap_rows.append({
                "ticker":       TICKER_NAMES.get(t, t),
                "High Impact":  sub[sub["high_impact"] == 1][col].abs().mean(),
                "Low Impact":   sub[sub["high_impact"] == 0][col].abs().mean(),
            })
        hmap_df = pd.DataFrame(hmap_rows).set_index("ticker")
        fig_hmap = go.Figure(go.Heatmap(
            z=[hmap_df["High Impact"].values, hmap_df["Low Impact"].values],
            x=hmap_df.index.tolist(),
            y=["High Impact Posts", "Low Impact Posts"],
            colorscale="RdYlGn_r",
            text=[[f"{v:.3%}" if not np.isnan(v) else "—" for v in row]
                  for row in [hmap_df["High Impact"].values,
                               hmap_df["Low Impact"].values]],
            texttemplate="%{text}",
        )).update_layout(
            title="Mean Absolute Daily Return by Ticker — High vs Low Impact Posts",
            template="plotly_dark", paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        )
    else:
        fig_hmap = go.Figure().update_layout(
            title="Ticker Heatmap (no data)", template="plotly_dark",
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        )

    # ── Layout ───────────────────────────────────────────
    if "market_period" in posts.columns:
        market_periods = sorted(posts["market_period"].dropna().unique().tolist())
    else:
        market_periods = ["unknown"]
    ticker_options = [
        {"label": f"{TICKER_NAMES.get(t, t)} ({t.upper()})", "value": t}
        for t in TICKERS if f"{t}_daily_ret" in posts.columns
    ]

    app.layout = dbc.Container(fluid=True, style={
        "backgroundColor": BG, "minHeight": "100vh", "padding": "24px",
    }, children=[

        html.H1("🇺🇸 Trump Truth Social → Market Impact",
                style={"color": "#fff", "textAlign": "center", "marginBottom": "8px"}),
        html.P(
            f"Primary: {PRIMARY_TICKER.upper()}  ·  "
            f"Train: {metrics['n_train']:,} posts  ·  "
            f"Test holdout: {metrics['n_test']:,} posts  "
            f"({metrics['test_start']} → {metrics['test_end']})",
            style={"color": "#888", "textAlign": "center", "marginBottom": "24px"},
        ),

        # KPIs
        dbc.Row([
            dbc.Col(kpi("Total Posts",       f"{len(posts):,}"),                  md=2),
            dbc.Col(kpi("High-Impact Posts", f"{metrics['n_high']:,}", HIGH_C),   md=2),
            dbc.Col(kpi("Test ROC-AUC",      f"{metrics['roc_auc']:.3f}", GOLD),  md=2),
            dbc.Col(kpi("Train ROC-AUC",     f"{metrics['roc_auc_train']:.3f}", PURPLE), md=2),
            dbc.Col(kpi("CV AUC (TS 5-fold)",
                        f"{metrics['cv_auc_mean']:.3f} ± {metrics['cv_auc_std']:.3f}",
                        GREEN), md=2),
            dbc.Col(kpi("Avg Precision",     f"{metrics['avg_precision']:.3f}", LOW_C), md=2),
        ], className="mb-4"),

        # Filters
        dbc.Row([
            dbc.Col([
                html.Label("Market Period", style={"color": "#ccc"}),
                dcc.Dropdown(
                    id="dd-period",
                    options=[{"label": "All periods", "value": "all"}] +
                            [{"label": p, "value": p} for p in market_periods],
                    value="all", clearable=False,
                    style={"backgroundColor": "#333", "color": "#000"},
                ),
            ], md=3),
            dbc.Col([
                html.Label("Impact Label", style={"color": "#ccc"}),
                dcc.Dropdown(
                    id="dd-impact",
                    options=[
                        {"label": "All",         "value": "all"},
                        {"label": "High Impact", "value": "1"},
                        {"label": "Low Impact",  "value": "0"},
                    ],
                    value="all", clearable=False,
                    style={"backgroundColor": "#333", "color": "#000"},
                ),
            ], md=3),
            dbc.Col([
                html.Label("Ticker (return plots)", style={"color": "#ccc"}),
                dcc.Dropdown(
                    id="dd-ticker",
                    options=ticker_options,
                    value=PRIMARY_TICKER, clearable=False,
                    style={"backgroundColor": "#333", "color": "#000"},
                ),
            ], md=3),
            dbc.Col([
                html.Label("Min Predicted Probability", style={"color": "#ccc"}),
                dcc.Slider(id="sl-proba", min=0, max=1, step=0.05, value=0,
                           marks={i / 10: str(round(i / 10, 1)) for i in range(0, 11)}),
            ], md=3),
        ], className="mb-4"),

        # Charts
        dbc.Row([dbc.Col(dcc.Graph(id="g-timeline"), md=12)], className="mb-4"),
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_hmap), md=12)], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_cat),  md=6),
            dbc.Col(dcc.Graph(id="g-returns"),  md=6),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(id="g-period-dist"), md=6),
            dbc.Col(dcc.Graph(id="g-intraday"),    md=6),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_imp), md=4),
            dbc.Col(dcc.Graph(figure=fig_roc), md=4),
            dbc.Col(dcc.Graph(figure=fig_pr),  md=4),
        ], className="mb-4"),
        dbc.Row([
            dbc.Col([
                html.H4("Top Posts by Predicted Impact Probability",
                        style={"color": "#ccc", "marginBottom": "12px"}),
                html.Div(id="tbl-posts"),
            ], md=12),
        ]),
    ])

    # ── Callback ─────────────────────────────────────────
    @app.callback(
        Output("g-timeline",     "figure"),
        Output("g-returns",      "figure"),
        Output("g-period-dist",  "figure"),
        Output("g-intraday",     "figure"),
        Output("tbl-posts",      "children"),
        Input("dd-period",  "value"),
        Input("dd-impact",  "value"),
        Input("dd-ticker",  "value"),
        Input("sl-proba",   "value"),
    )
    def update(sel_period, sel_impact, sel_ticker, sel_proba):
        dff = posts.copy()
        if sel_period != "all":
            dff = dff[dff["market_period"] == sel_period]
        if sel_impact != "all":
            dff = dff[dff["high_impact"] == float(sel_impact)]
        if has_proba and sel_proba and sel_proba > 0:
            dff = dff[dff["impact_proba"].fillna(0) >= sel_proba]

        dff["snippet"] = dff["content"].str[:100] + "…"
        daily_col = (f"{sel_ticker}_daily_ret"
                     if sel_ticker and f"{sel_ticker}_daily_ret" in dff.columns
                     else f"{PRIMARY_TICKER}_daily_ret")

        # Timeline
        fig_tl = go.Figure()
        for h, grp in dff.groupby("high_impact", dropna=False):
            fig_tl.add_trace(go.Scatter(
                x=grp["datetime"],
                y=grp["primary_ret"].fillna(0) * 100,
                mode="markers",
                marker=dict(color=HIGH_C if h == 1 else LOW_C,
                            symbol="star" if h == 1 else "circle",
                            size=9 if h == 1 else 5, opacity=0.75),
                name="High Impact" if h == 1 else "Low Impact",
                text=grp["snippet"],
                hovertemplate="<b>%{text}</b><br>%{x|%Y-%m-%d %H:%M UTC}"
                              "<br>Δ %{y:.2f}%<extra></extra>",
            ))
        fig_tl.update_layout(
            title=f"Post Timeline — {PRIMARY_TICKER.upper()} Price Move",
            xaxis_title="Date (UTC)", yaxis_title="% Change",
            template="plotly_dark", paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            legend=dict(orientation="h", y=1.05),
        )

        # Return box
        dff_box = dff[dff[daily_col].notna()].copy() if daily_col in dff.columns else dff.copy()
        dff_box["Impact"] = dff_box["high_impact"].map(
            {1.0: "High", 0.0: "Low"}).fillna("Unlabelled")
        fig_ret = px.box(
            dff_box, x="market_period",
            y=(dff_box[daily_col] * 100) if daily_col in dff_box.columns else None,
            color="Impact",
            color_discrete_map={"High": HIGH_C, "Low": LOW_C, "Unlabelled": "#888"},
            title=f"{TICKER_NAMES.get(sel_ticker, sel_ticker)} Daily Return by Period",
            labels={"y": "Daily Return %", "market_period": "Period"},
            template="plotly_dark",
        ).update_layout(paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)

        # Period distribution
        pc = dff["market_period"].value_counts().reset_index()
        pc.columns = ["period", "count"]
        fig_pd = px.bar(
            pc, x="period", y="count", color="period",
            title="Posts by Market Period", template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        ).update_layout(paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG, showlegend=False)

        # Intraday scatter
        imm_col = f"{sel_ticker}_immediate_ret"
        sus_col = f"{sel_ticker}_sustained_ret"
        fig_id  = go.Figure()
        if imm_col in dff.columns and sus_col in dff.columns:
            mh = dff[dff["during_market_hours"]].copy()
            mh["Impact"] = mh["high_impact"].map(
                {1.0: "High", 0.0: "Low"}).fillna("Unlabelled")
            for lbl, col in [("High", HIGH_C), ("Low", LOW_C)]:
                sub = mh[mh["Impact"] == lbl]
                fig_id.add_trace(go.Scatter(
                    x=sub[imm_col] * 100, y=sub[sus_col] * 100,
                    mode="markers",
                    marker=dict(color=col, size=6, opacity=0.7),
                    name=lbl, text=sub["snippet"],
                    hovertemplate="<b>%{text}</b><br>"
                                  "Immediate ±5min: %{x:.2f}%<br>"
                                  "Sustained 1hr:  %{y:.2f}%<extra></extra>",
                ))
            fig_id.update_layout(
                title=(f"{TICKER_NAMES.get(sel_ticker, sel_ticker)}: "
                       f"Immediate (±5min) vs Sustained (1hr) — market hours only"),
                xaxis_title="Immediate Reaction %", yaxis_title="Sustained Move %",
                template="plotly_dark", paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            )
        else:
            fig_id.update_layout(
                title="Intraday chart (5-min/1-hr cols not available for this ticker)",
                template="plotly_dark", paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            )

        # Top posts table
        tbl_base = ["datetime", "content", "market_period", "primary_ret", "high_impact"]
        if has_proba:
            tbl_base.append("impact_proba")
        for suffix in ["_at_post", "_5min_after", "_1hr_after", "_daily_ret"]:
            c = f"{sel_ticker}{suffix}"
            if c in dff.columns:
                tbl_base.append(c)
        tbl_cols = [c for c in tbl_base if c in dff.columns]
        tbl = (dff[tbl_cols]
               .sort_values("impact_proba" if has_proba else "primary_ret",
                            ascending=False, na_position="last")
               .head(50).copy())
        tbl["datetime"]    = tbl["datetime"].astype(str).str[:19]
        tbl["content"]     = tbl["content"].str[:130]
        tbl["primary_ret"] = tbl["primary_ret"].apply(
            lambda x: f"{x * 100:.2f}%" if pd.notna(x) else "—")
        if has_proba:
            tbl["impact_proba"] = tbl["impact_proba"].apply(
                lambda x: f"{x:.3f}" if pd.notna(x) else "—")
        for suffix in ["_at_post", "_5min_after", "_1hr_after", "_daily_ret"]:
            c = f"{sel_ticker}{suffix}"
            if c in tbl.columns:
                tbl[c] = tbl[c].apply(lambda x: f"{x:.2f}" if pd.notna(x) else "—")

        table = dash_table.DataTable(
            data=tbl.to_dict("records"),
            columns=[{"name": c, "id": c} for c in tbl.columns],
            style_header={"backgroundColor": "#333355",
                          "color": "#fff", "fontWeight": "bold"},
            style_cell={"backgroundColor": CARD_BG, "color": "#ccc",
                        "textAlign": "left", "fontSize": "12px",
                        "whiteSpace": "normal", "height": "auto",
                        "maxWidth": "420px"},
            style_data_conditional=[{
                "if": {"filter_query": "{high_impact} = 1.0"},
                "backgroundColor": "#3d1a1a", "color": HIGH_C,
            }],
            sort_action="native", filter_action="native", page_size=20,
        )
        return fig_tl, fig_ret, fig_pd, fig_id, table

    return app


# ─────────────────────────────────────────────
if __name__ == "__main__":
    # 1. Run pipeline to train model and get metrics
    daily, importance, metrics, cat_cols, gdelt_cols = run_pipeline()

    # 2. Load RAW posts (NOT aggregated daily data)
    from backend.model_training import load_posts
    raw_posts, _, _ = load_posts()

    # 3. Merge predictions (daily → raw posts)
    # This allows each post to inherit the day's prediction
    if "date" in raw_posts.columns and "date" in daily.columns:
        raw_posts = raw_posts.merge(
        daily[["date", "impact_proba", "high_impact"]],
        on="date",
        how="left"
    )

    # 4. Build dashboard using RAW data (correct input)
    raw_posts["primary_ret"] = raw_posts.get("sp500_close", 0)
    raw_posts["market_period"] = raw_posts.get("market_period", "unknown")
    app = build_dashboard(raw_posts, importance, metrics, cat_cols, gdelt_cols)

    print("\n🚀 Starting dashboard on http://0.0.0.0:8050 …")
    app.run(debug=False, host="0.0.0.0", port=8050)