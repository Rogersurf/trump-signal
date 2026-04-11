"""
Trump Truth Social → Market Impact Analyzer
============================================
All market data is already in the SQLite DB — no yfinance needed.

Table: truth_social
Key market columns per ticker (18 tickers):
  {ticker}_open, {ticker}_close, {ticker}_1hr_before,
  {ticker}_5min_before, {ticker}_at_post, {ticker}_5min_after, {ticker}_1hr_after

Impact is measured as price move AROUND the post:
  - during_market_hours=True  → 5min_before → 5min_after  (immediate reaction)
                               + at_post    → 1hr_after    (sustained move)
  - during_market_hours=False → prior close → next open    = _open vs _close
                                (already captured by open/close columns)

pip install pandas numpy scikit-learn xgboost plotly dash dash-bootstrap-components
"""

import os
import sqlite3
import warnings

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Input, Output, dash_table, dcc, html
from sklearn.metrics import (
    average_precision_score,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from backend_database.data_api import *
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
TABLE_NAME = "truth_social"

# Impact threshold per ticker type (abs % move)
THRESHOLDS = {
    "default": 0.005,   # 0.5% for broad indices (sp500, qqq, dia)
    "djt":     0.020,   # 2.0% for Trump Media (very volatile)
    "ibit":    0.015,   # 1.5% for Bitcoin ETF
    "uso":     0.010,   # 1.0% for oil
    "gld":     0.008,   # 0.8% for gold
}

# Primary ticker used for the main impact label + dashboard
PRIMARY_TICKER = "sp500"

# All 18 tickers in the dataset
TICKERS = [
    "sp500", "dia", "qqq", "djt", "lmt", "war", "xli", "xlv",
    "xph", "cnrg", "gld", "uso", "fxi", "eww", "vgk", "ibit", "tlt", "uup",
]

# Ticker display names for charts
TICKER_NAMES = {
    "sp500": "S&P 500", "dia": "Dow Jones", "qqq": "Nasdaq-100",
    "djt": "Trump Media", "lmt": "Lockheed Martin", "war": "Military ETF",
    "xli": "Industrials", "xlv": "Healthcare", "xph": "Pharma",
    "cnrg": "Clean Energy", "gld": "Gold", "uso": "Oil",
    "fxi": "China ETF", "eww": "Mexico ETF", "vgk": "Europe ETF",
    "ibit": "Bitcoin ETF", "tlt": "Treasury Bonds", "uup": "USD Index",
}

CAT_COLS = [
    "cat_attacking_individual", "cat_attacking_opposition",
    "cat_threatening_intl", "cat_enacting_aggressive",
    "cat_enacting_nonaggressive", "cat_deescalating",
    "cat_praising_endorsing", "cat_self_promotion", "cat_other",
]

GDELT_COLS = [
    "gdelt_military", "gdelt_sanctions", "gdelt_threat", "gdelt_protest",
    "gdelt_force_posture", "gdelt_diplomatic", "gdelt_material_conflict",
    "gdelt_verbal_conflict", "gdelt_material_cooperation",
    "gdelt_verbal_cooperation", "gdelt_goldstein_avg", "gdelt_avg_tone",
    "gdelt_total_events",
]

KEYWORD_GROUPS = {
    "tariff":   r"\b(tariff|tariffs|trade war|import tax|customs)\b",
    "china":    r"\b(china|chinese|beijing|xi jinping|ccp)\b",
    "fed":      r"\b(fed|federal reserve|powell|interest rate|rate hike|rate cut)\b",
    "energy":   r"\b(oil|gas|energy|opec|pipeline|lng|crude)\b",
    "crypto":   r"\b(bitcoin|crypto|btc|ethereum|digital currency)\b",
    "military": r"\b(military|troops|war|nato|weapon|defense)\b",
    "economy":  r"\b(economy|gdp|recession|inflation|jobs|unemployment)\b",
    "company":  r"\b(apple|tesla|amazon|google|microsoft|stock|shares)\b",
    "threat":   r"\b(sanction|ban|block|fine|investigate|sue|lawsuit)\b",
}


# ─────────────────────────────────────────────
# 1.  LOAD POSTS
# ─────────────────────────────────────────────
def load_posts(db_path: str, table: str) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    cur  = conn.execute(f"PRAGMA table_info({table})")
    all_cols = [r[1] for r in cur.fetchall()]

    # Discover which ticker/gdelt/cat cols actually exist in this DB
    ticker_cols = [c for c in all_cols
                   if any(c.startswith(f"{t}_") for t in TICKERS)]
    cat_cols    = [c for c in all_cols if c in CAT_COLS]
    gdelt_cols  = [c for c in all_cols if c in GDELT_COLS]

    base_cols = [
        "date", "time", "time_eastern", "day_of_week", "datetime",
        "text", "url", "post_id", "is_president", "is_president_elect",
        "during_market_hours", "market_period",
        "replies_count", "reblogs_count", "favourites_count",
        "has_media",
    ]
    base_cols = [c for c in base_cols if c in all_cols]

    select = base_cols + ticker_cols + cat_cols + gdelt_cols
    df = pd.read_sql(f"SELECT {', '.join(select)} FROM {table}", conn)
    conn.close()

    # ── datetime ──────────────────────────────────────────
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce", utc=True)
    df["date"]     = pd.to_datetime(df["date"], errors="coerce")

    # ── booleans ─────────────────────────────────────────
    for bc in ["during_market_hours", "is_president", "is_president_elect", "has_media"]:
        if bc in df.columns:
            df[bc] = df[bc].astype(str).str.lower().isin(["1", "true", "yes"])

    # ── numerics ─────────────────────────────────────────
    num_cols = ticker_cols + cat_cols + gdelt_cols + [
        "replies_count", "reblogs_count", "favourites_count"
    ]
    num_cols = [c for c in num_cols if c != "sp500_resolution"]

    for c in num_cols:
        if c in df.columns:
            print(df[c])
            df[c] = pd.to_numeric(df[c], errors="coerce")

    df["content"] = df["text"].fillna("").astype(str)
    df = df.dropna(subset=["datetime"]).reset_index(drop=True)

    return df, ticker_cols, cat_cols, gdelt_cols


# ─────────────────────────────────────────────
# 2.  COMPUTE RETURNS FROM EXISTING PRICE COLS
# ─────────────────────────────────────────────
def compute_returns(df: pd.DataFrame, ticker_cols: list) -> pd.DataFrame:
    """
    For each ticker compute:
      immediate_ret  : 5min_before → 5min_after  (market hours posts)
      sustained_ret  : at_post     → 1hr_after   (market hours posts)
      overnight_ret  : open        → close        (off-hours posts)
      daily_ret      : open        → close        (all posts, context)
    Then build primary label from PRIMARY_TICKER.
    """
    for t in TICKERS:
        cols_needed = [f"{t}_{s}" for s in
                       ["open", "close", "1hr_before", "5min_before",
                        "at_post", "5min_after", "1hr_after"]]
        # Only compute if at least some cols exist
        existing = [c for c in cols_needed if c in df.columns]
        if not existing:
            continue

        # Daily return (open → close) — available for ALL posts
        if f"{t}_open" in df.columns and f"{t}_close" in df.columns:
            df[f"{t}_daily_ret"] = (
                (df[f"{t}_close"] - df[f"{t}_open"]) / df[f"{t}_open"]
            )

        # Immediate reaction (during market hours)
        if f"{t}_5min_before" in df.columns and f"{t}_5min_after" in df.columns:
            df[f"{t}_immediate_ret"] = (
                (df[f"{t}_5min_after"] - df[f"{t}_5min_before"])
                / df[f"{t}_5min_before"]
            )

        # Sustained move (during market hours)
        if f"{t}_at_post" in df.columns and f"{t}_1hr_after" in df.columns:
            df[f"{t}_sustained_ret"] = (
                (df[f"{t}_1hr_after"] - df[f"{t}_at_post"])
                / df[f"{t}_at_post"]
            )

    # ── Primary impact label ───────────────────────────────
    t = PRIMARY_TICKER
    thresh = THRESHOLDS.get(t, THRESHOLDS["default"])

    # During market hours → use immediate reaction
    # Off hours           → use daily open→close
    if f"{t}_immediate_ret" in df.columns and f"{t}_daily_ret" in df.columns:
        df["primary_ret"] = np.where(
            df["during_market_hours"],
            df[f"{t}_immediate_ret"],
            df[f"{t}_daily_ret"],
        )
    elif f"{t}_daily_ret" in df.columns:
        df["primary_ret"] = df[f"{t}_daily_ret"]
    else:
        df["primary_ret"] = np.nan

    df["high_impact"] = (df["primary_ret"].abs() >= thresh).astype(float)
    df.loc[df["primary_ret"].isna(), "high_impact"] = np.nan

    return df


# ─────────────────────────────────────────────
# 3.  FEATURE ENGINEERING
# ─────────────────────────────────────────────
def engineer_features(df: pd.DataFrame,
                       cat_cols: list,
                       gdelt_cols: list) -> tuple[pd.DataFrame, list]:
    text = df["content"].str.lower().fillna("")

    # Keyword flags
    for name, pat in KEYWORD_GROUPS.items():
        df[f"kw_{name}"] = text.str.contains(pat, regex=True).astype(int)

    pos_pat = r"\b(great|huge|winning|beautiful|best|tremendous|deal|agreement)\b"
    neg_pat = r"\b(fake|disaster|corrupt|failing|witch hunt|hoax|rigged|bad|horrible)\b"
    df["pos_words"]  = text.str.contains(pos_pat, regex=True).astype(int)
    df["neg_words"]  = text.str.contains(neg_pat, regex=True).astype(int)
    df["text_len"]   = df["content"].str.len().fillna(0)
    df["caps_ratio"] = (df["content"].str.findall(r"[A-Z]").apply(len)
                        / (df["text_len"] + 1))
    df["exclaim"]    = df["content"].str.count("!")
    df["question"]   = df["content"].str.count(r"\?")
    df["has_url"]    = df["content"].str.contains(r"https?://", regex=True).astype(int)
    df["word_count"] = df["content"].str.split().apply(len)

    # Engagement (log-scaled)
    for col, alias in [("favourites_count", "likes"),
                       ("reblogs_count",    "reposts"),
                       ("replies_count",    "replies")]:
        src = col if col in df.columns else None
        df[f"log_{alias}"] = np.log1p(df[src]) if src else 0.0
    df["engagement_score"] = (
        df["log_likes"] * 1.0 +
        df["log_reposts"] * 2.0 +
        df["log_replies"] * 0.5
    )

    # Temporal (cyclical)
    df["hour"]     = df["datetime"].dt.hour
    df["dow"]      = df["datetime"].dt.dayofweek
    df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
    df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)
    df["dow_sin"]  = np.sin(2 * np.pi * df["dow"] / 7)
    df["dow_cos"]  = np.cos(2 * np.pi * df["dow"] / 7)

    # Binary context flags
    df["is_market_hours"]      = df["during_market_hours"].astype(int)
    df["is_president_flag"]    = df["is_president"].astype(int) if "is_president" in df.columns else 0
    df["is_pres_elect_flag"]   = df["is_president_elect"].astype(int) if "is_president_elect" in df.columns else 0
    df["has_media_flag"]       = df["has_media"].astype(int) if "has_media" in df.columns else 0

    # Market period one-hot
    mp_dummies = pd.get_dummies(
        df["market_period"].fillna("unknown"), prefix="mp"
    ).astype(int)
    df = pd.concat([df, mp_dummies], axis=1)

    feature_cols = (
        [f"kw_{k}" for k in KEYWORD_GROUPS]
        + ["pos_words", "neg_words", "text_len", "caps_ratio",
           "exclaim", "question", "has_url", "word_count",
           "log_likes", "log_reposts", "log_replies", "engagement_score",
           "hour_sin", "hour_cos", "dow_sin", "dow_cos",
           "is_market_hours", "is_president_flag",
           "is_pres_elect_flag", "has_media_flag"]
        + list(mp_dummies.columns)
        + [c for c in cat_cols    if c in df.columns]   # LLM categories
        + [c for c in gdelt_cols  if c in df.columns]   # GDELT geopolitical
    )
    return df, feature_cols


# ─────────────────────────────────────────────
# 4.  TRAIN XGBOOST
# ─────────────────────────────────────────────
def train_model(df: pd.DataFrame, feature_cols: list):
    labelled = df[df["high_impact"].notna()].copy()
    for c in feature_cols:
        if c not in labelled.columns:
            labelled[c] = 0.0

    X = labelled[feature_cols].fillna(0).astype(float).values
    y = labelled["high_impact"].astype(int).values

    if y.sum() < 5:
        print("[WARN] Very few high-impact labels – results may be unreliable.")

    scaler = StandardScaler()
    X_sc   = scaler.fit_transform(X)

    scale_pos = max(1, int((y == 0).sum() / max(y.sum(), 1)))
    clf = XGBClassifier(
        n_estimators=400, max_depth=4, learning_rate=0.04,
        subsample=0.8, colsample_bytree=0.8,
        scale_pos_weight=scale_pos,
        eval_metric="logloss", random_state=42, n_jobs=-1,
    )

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(clf, X_sc, y, cv=cv, scoring="roc_auc")

    clf.fit(X_sc, y)
    proba = clf.predict_proba(X_sc)[:, 1]

    fpr, tpr, _   = roc_curve(y, proba)
    prec, rec, _  = precision_recall_curve(y, proba)

    importance = pd.DataFrame({
        "feature": feature_cols,
        "importance": clf.feature_importances_,
    }).sort_values("importance", ascending=False)

    labelled["impact_proba"] = proba
    metrics = dict(
        roc_auc          = roc_auc_score(y, proba),
        avg_precision    = average_precision_score(y, proba),
        cv_auc_mean      = cv_scores.mean(),
        cv_auc_std       = cv_scores.std(),
        n_total          = len(labelled),
        n_high           = int(y.sum()),
        fpr=fpr, tpr=tpr, prec=prec, rec=rec,
    )
    return clf, scaler, labelled[["datetime", "impact_proba"]], importance, metrics


# ─────────────────────────────────────────────
# 5.  PIPELINE
# ─────────────────────────────────────────────
def run_pipeline():
    print("[1/4] Loading posts from SQLite …")
    posts, ticker_cols, cat_cols, gdelt_cols = load_posts(DB_PATH, TABLE_NAME)
    print(f"      {len(posts):,} posts  |  "
          f"{len(ticker_cols)} ticker cols  |  "
          f"{len(cat_cols)} cat cols  |  "
          f"{len(gdelt_cols)} gdelt cols")

    print("[2/4] Computing returns & impact labels from existing price data …")
    posts = compute_returns(posts, ticker_cols)
    n_high = int(posts["high_impact"].fillna(0).sum())
    print(f"      Primary ticker: {PRIMARY_TICKER.upper()}  |  "
          f"High-impact posts: {n_high:,}")

    print("[3/4] Engineering features …")
    posts, feature_cols = engineer_features(posts, cat_cols, gdelt_cols)

    print("[4/4] Training XGBoost …")
    clf, scaler, proba_df, importance, metrics = train_model(posts, feature_cols)

    # Merge probabilities back
    posts = posts.merge(proba_df, on="datetime", how="left")

    print(f"\n✅  Done  |  ROC-AUC: {metrics['roc_auc']:.3f}"
          f"  |  CV AUC: {metrics['cv_auc_mean']:.3f} ± {metrics['cv_auc_std']:.3f}"
          f"  |  High-impact: {metrics['n_high']:,} / {metrics['n_total']:,}")

    return posts, importance, metrics, cat_cols, gdelt_cols


# ─────────────────────────────────────────────
# 6.  DASHBOARD
# ─────────────────────────────────────────────
BG       = "#1e1e2e"
CARD_BG  = "#2a2a3e"
HIGH_C   = "#ff4b4b"
LOW_C    = "#4b9eff"
GOLD     = "#ffd700"
GREEN    = "#7fff7f"
PURPLE   = "#c084fc"


def kpi(label, value, color="#ffffff"):
    return dbc.Card(dbc.CardBody([
        html.H2(value, style={"color": color, "marginBottom": 0}),
        html.P(label,  style={"color": "#aaa", "marginTop": "4px"}),
    ]), style={"backgroundColor": CARD_BG, "borderRadius": "10px",
               "textAlign": "center"})


def build_dashboard(posts, importance, metrics, cat_cols, gdelt_cols):
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    has_proba = "impact_proba" in posts.columns and posts["impact_proba"].notna().any()

    # ── Static figures ─────────────────────────────────────

    # Feature importance
    top20 = importance.head(20)
    fig_imp = px.bar(
        top20[::-1], x="importance", y="feature", orientation="h",
        title="Top-20 XGBoost Feature Importance",
        color="importance", color_continuous_scale="Plasma",
        template="plotly_dark",
    ).update_layout(paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
                    showlegend=False, coloraxis_showscale=False)

    # ROC
    fig_roc = go.Figure([
        go.Scatter(x=metrics["fpr"], y=metrics["tpr"], mode="lines",
                   name=f"AUC = {metrics['roc_auc']:.3f}",
                   line=dict(color=HIGH_C, width=2)),
        go.Scatter(x=[0,1], y=[0,1], mode="lines",
                   line=dict(dash="dash", color="gray"), name="Random"),
    ]).update_layout(title="ROC Curve", xaxis_title="FPR", yaxis_title="TPR",
                     template="plotly_dark",
                     paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)

    # PR curve
    fig_pr = go.Figure([
        go.Scatter(x=metrics["rec"], y=metrics["prec"], mode="lines",
                   name=f"AP = {metrics['avg_precision']:.3f}",
                   line=dict(color=LOW_C, width=2)),
    ]).update_layout(title="Precision-Recall Curve",
                     xaxis_title="Recall", yaxis_title="Precision",
                     template="plotly_dark",
                     paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)

    # Cat columns: avg score high vs low impact
    labelled_mask = posts["high_impact"].notna()
    if cat_cols and labelled_mask.any():
        cat_df = posts[labelled_mask].groupby("high_impact")[
            [c for c in cat_cols if c in posts.columns]
        ].mean().T.reset_index()
        cat_df.columns = (["category"] +
                          [f"impact_{int(c)}" for c in cat_df.columns[1:]])
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
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)

    # Multi-ticker return heatmap: mean |return| per ticker
    ret_cols = {t: f"{t}_daily_ret" for t in TICKERS
                if f"{t}_daily_ret" in posts.columns}
    if ret_cols and labelled_mask.any():
        hmap_data = []
        for t, col in ret_cols.items():
            sub = posts[labelled_mask & posts[col].notna()]
            if sub.empty:
                continue
            hmap_data.append({
                "ticker": TICKER_NAMES.get(t, t),
                "high_impact_mean_ret": sub[sub["high_impact"] == 1][col].abs().mean(),
                "low_impact_mean_ret":  sub[sub["high_impact"] == 0][col].abs().mean(),
            })
        hmap_df = pd.DataFrame(hmap_data).set_index("ticker")
        fig_hmap = go.Figure(data=go.Heatmap(
            z=[hmap_df["high_impact_mean_ret"].values,
               hmap_df["low_impact_mean_ret"].values],
            x=hmap_df.index.tolist(),
            y=["High Impact Posts", "Low Impact Posts"],
            colorscale="RdYlGn_r",
            text=[[f"{v:.3%}" for v in row]
                  for row in [hmap_df["high_impact_mean_ret"].values,
                               hmap_df["low_impact_mean_ret"].values]],
            texttemplate="%{text}",
        )).update_layout(
            title="Mean Absolute Daily Return by Ticker (High vs Low Impact Posts)",
            template="plotly_dark",
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
        )
    else:
        fig_hmap = go.Figure().update_layout(
            title="Ticker Heatmap (no data)", template="plotly_dark",
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)

    # ── Layout ─────────────────────────────────────────────
    market_periods = sorted(posts["market_period"].dropna().unique().tolist())

    app.layout = dbc.Container(fluid=True, style={
        "backgroundColor": BG, "minHeight": "100vh", "padding": "24px"
    }, children=[

        html.H1("🇺🇸 Trump Truth Social → Market Impact Dashboard",
                style={"color": "#fff", "textAlign": "center",
                       "marginBottom": "8px"}),
        html.P(f"Primary ticker: {PRIMARY_TICKER.upper()} · "
               f"Impact threshold: {THRESHOLDS['default']*100:.1f}%",
               style={"color": "#888", "textAlign": "center",
                      "marginBottom": "24px"}),

        # ── KPIs ───────────────────────────────────────────
        dbc.Row([
            dbc.Col(kpi("Total Posts",        f"{len(posts):,}"),              md=3),
            dbc.Col(kpi("High-Impact Posts",  f"{metrics['n_high']:,}", HIGH_C), md=3),
            dbc.Col(kpi("ROC-AUC",            f"{metrics['roc_auc']:.3f}", GOLD), md=3),
            dbc.Col(kpi("CV AUC (5-fold)",
                        f"{metrics['cv_auc_mean']:.3f} ± {metrics['cv_auc_std']:.3f}",
                        GREEN), md=3),
        ], className="mb-4"),

        # ── Filters ────────────────────────────────────────
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
                html.Label("Ticker (for return plot)", style={"color": "#ccc"}),
                dcc.Dropdown(
                    id="dd-ticker",
                    options=[{"label": f"{TICKER_NAMES.get(t,t)} ({t.upper()})",
                              "value": t} for t in TICKERS
                             if f"{t}_daily_ret" in posts.columns],
                    value=PRIMARY_TICKER, clearable=False,
                    style={"backgroundColor": "#333", "color": "#000"},
                ),
            ], md=3),
            dbc.Col([
                html.Label("Min Predicted Probability", style={"color": "#ccc"}),
                dcc.Slider(id="sl-proba", min=0, max=1, step=0.05, value=0,
                           marks={i/10: str(round(i/10, 1)) for i in range(0, 11)}),
            ], md=3),
        ], className="mb-4"),

        # ── Timeline ───────────────────────────────────────
        dbc.Row([dbc.Col(dcc.Graph(id="g-timeline"), md=12)], className="mb-4"),

        # ── Multi-ticker heatmap (full width) ──────────────
        dbc.Row([dbc.Col(dcc.Graph(figure=fig_hmap), md=12)], className="mb-4"),

        # ── LLM category bar + returns box ─────────────────
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_cat),     md=6),
            dbc.Col(dcc.Graph(id="g-returns"),     md=6),
        ], className="mb-4"),

        # ── Market period dist + immediate vs sustained ────
        dbc.Row([
            dbc.Col(dcc.Graph(id="g-period-dist"), md=6),
            dbc.Col(dcc.Graph(id="g-intraday"),    md=6),
        ], className="mb-4"),

        # ── Model charts ───────────────────────────────────
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_imp), md=4),
            dbc.Col(dcc.Graph(figure=fig_roc), md=4),
            dbc.Col(dcc.Graph(figure=fig_pr),  md=4),
        ], className="mb-4"),

        # ── Top posts table ────────────────────────────────
        dbc.Row([
            dbc.Col([
                html.H4("Top Posts by Predicted Impact Probability",
                        style={"color": "#ccc", "marginBottom": "12px"}),
                html.Div(id="tbl-posts"),
            ], md=12),
        ]),
    ])

    # ── Callback ───────────────────────────────────────────
    @app.callback(
        Output("g-timeline",   "figure"),
        Output("g-returns",    "figure"),
        Output("g-period-dist","figure"),
        Output("g-intraday",   "figure"),
        Output("tbl-posts",    "children"),
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
        ret_col = f"{sel_ticker}_daily_ret" if sel_ticker else f"{PRIMARY_TICKER}_daily_ret"

        # ── Timeline ───────────────────────────────────────
        fig_tl = go.Figure()
        for h, grp in dff.groupby("high_impact", dropna=False):
            col = HIGH_C if h == 1 else LOW_C
            sym = "star" if h == 1 else "circle"
            lbl = "High Impact" if h == 1 else "Low Impact"
            fig_tl.add_trace(go.Scatter(
                x=grp["datetime"],
                y=grp["primary_ret"].fillna(0) * 100,
                mode="markers",
                marker=dict(color=col, symbol=sym,
                            size=9 if h == 1 else 5, opacity=0.75),
                name=lbl,
                text=grp["snippet"],
                hovertemplate=(
                    "<b>%{text}</b><br>%{x|%Y-%m-%d %H:%M UTC}"
                    "<br>S&P Δ: %{y:.2f}%<extra></extra>"
                ),
            ))
        fig_tl.update_layout(
            title=f"Post Timeline — {PRIMARY_TICKER.upper()} Price Move",
            xaxis_title="Date (UTC)", yaxis_title="% Change",
            template="plotly_dark",
            paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            legend=dict(orientation="h", y=1.05),
        )

        # ── Returns box by market_period ───────────────────
        dff_box = dff[dff[ret_col].notna()].copy() if ret_col in dff.columns else dff.copy()
        dff_box["Impact"] = dff_box["high_impact"].map(
            {1.0: "High", 0.0: "Low"}).fillna("Unlabelled")
        fig_ret = px.box(
            dff_box,
            x="market_period",
            y=(dff_box[ret_col] * 100) if ret_col in dff_box.columns else None,
            color="Impact",
            color_discrete_map={"High": HIGH_C, "Low": LOW_C, "Unlabelled": "#888"},
            title=f"{TICKER_NAMES.get(sel_ticker, sel_ticker)} Daily Return by Market Period",
            labels={"y": "Daily Return %", "market_period": "Period"},
            template="plotly_dark",
        ).update_layout(paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)

        # ── Market period distribution ──────────────────────
        pc = dff["market_period"].value_counts().reset_index()
        pc.columns = ["period", "count"]
        fig_pd = px.bar(
            pc, x="period", y="count", color="period",
            title="Posts by Market Period",
            template="plotly_dark",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        ).update_layout(paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
                        showlegend=False)

        # ── Intraday: immediate vs sustained (market hours) ─
        imm_col = f"{sel_ticker}_immediate_ret"
        sus_col = f"{sel_ticker}_sustained_ret"
        fig_id  = go.Figure()
        if imm_col in dff.columns and sus_col in dff.columns:
            mh = dff[dff["during_market_hours"] == True].copy()
            mh["Impact"] = mh["high_impact"].map(
                {1.0: "High", 0.0: "Low"}).fillna("Unlabelled")
            for lbl, col in [("High", HIGH_C), ("Low", LOW_C)]:
                sub = mh[mh["Impact"] == lbl]
                fig_id.add_trace(go.Scatter(
                    x=sub[imm_col] * 100,
                    y=sub[sus_col] * 100,
                    mode="markers",
                    marker=dict(color=col, size=6, opacity=0.7),
                    name=lbl,
                    text=sub["snippet"],
                    hovertemplate=(
                        "<b>%{text}</b><br>"
                        "Immediate (±5min): %{x:.2f}%<br>"
                        "Sustained (1hr):  %{y:.2f}%<extra></extra>"
                    ),
                ))
            fig_id.update_layout(
                title=f"{TICKER_NAMES.get(sel_ticker,sel_ticker)}: "
                      f"Immediate (±5min) vs Sustained (1hr) Move<br>"
                      f"<sup>Market-hours posts only</sup>",
                xaxis_title="Immediate Reaction %",
                yaxis_title="Sustained Move %",
                template="plotly_dark",
                paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG,
            )
        else:
            fig_id.update_layout(
                title="Intraday chart (5-min/1-hr cols not available for this ticker)",
                template="plotly_dark",
                paper_bgcolor=CARD_BG, plot_bgcolor=CARD_BG)

        # ── Top posts table ─────────────────────────────────
        tbl_base = ["datetime", "content", "market_period",
                    "primary_ret", "high_impact"]
        if has_proba:
            tbl_base.append("impact_proba")
        # Add selected ticker intraday cols if present
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
        tbl["content"]     = tbl["content"].str[:120]
        tbl["primary_ret"] = tbl["primary_ret"].apply(
            lambda x: f"{x*100:.2f}%" if pd.notna(x) else "—")
        if has_proba:
            tbl["impact_proba"] = tbl["impact_proba"].apply(
                lambda x: f"{x:.3f}" if pd.notna(x) else "—")
        for suffix in ["_at_post", "_5min_after", "_1hr_after", "_daily_ret"]:
            c = f"{sel_ticker}{suffix}"
            if c in tbl.columns:
                tbl[c] = tbl[c].apply(
                    lambda x: f"{x:.2f}" if pd.notna(x) else "—")

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
# ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    posts, importance, metrics, cat_cols, gdelt_cols = run_pipeline()
    app = build_dashboard(posts, importance, metrics, cat_cols, gdelt_cols)
    app.run(debug=False, host="0.0.0.0", port=8050)