"""pages/dev.py — Developer dashboard"""
import streamlit as st
import plotly.express as px
from frontend._data.api_client import get_pipeline_status, get_artifact_log, get_posts

def render(T: dict):
    st.title("🛠️ Developer dashboard")
    st.caption("Pipeline status · artifact log · raw data")

    status = get_pipeline_status()

    if status["status"] == "healthy":
        st.success(f"✅ {T['all_healthy']}")
    else:
        st.error(f"❌ {T['error_detected']}")
        if status.get("errors"):
            for e in status["errors"]:
                st.code(e)

    # ── Metrics ───────────────────────────────────────────────────────────────
    total = status.get('total_posts', 0)
    posts_today = status.get('posts_today', 0)
    pct_mh = status.get('pct_market_hours', 0)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(T["total_posts"],  f"{total:,}" if total else "N/A")
    c2.metric(T["posts_today"],  posts_today if posts_today else "N/A")
    c3.metric("Market-hours posts", f"{pct_mh}%")
    c4.metric("GDELT updated",   "Weekly")

    st.divider()

    # ── Pipeline run times ────────────────────────────────────────────────────
    st.subheader(T["pipeline_status"])
    stages = {
        "ingest":     status["last_ingest"],
        "preprocess": status["last_preprocess"],
        "sentiment":  status["last_sentiment_run"],
        "embeddings": status["last_embedding_build"],
    }
    for stage, ts in stages.items():
        st.markdown(f"- **{stage}** → `{ts}`")

    st.divider()

    # ── Models ────────────────────────────────────────────────────────────────
    st.subheader("Models in use")
    mc1, mc2 = st.columns(2)
    with mc1:
        st.info(
            f"**Sentiment**\n\n`{status['model_name']}`\n\n"
            "Source: pre-labeled in dataset · RoBERTa fine-tuned on Twitter"
        )
    with mc2:
        st.info(
            f"**Semantic Search**\n\n`{status['embedding_model']}`\n\n"
            "Dim: 384 · ChromaDB cosine similarity · built on ingest"
        )

    st.divider()

    # ── Artifact log ──────────────────────────────────────────────────────────
    st.subheader(T["artifact_log"])
    st.caption(f"Source: `{status['artifact_path']}`")

    log_df = get_artifact_log()
    log_df["status_icon"] = log_df["status"].map(
        {"ok": "✅", "error": "❌", "warning": "⚠️"}
    )
    st.dataframe(
        log_df[["timestamp","stage","rows","duration_s","status_icon"]].rename(
            columns={"timestamp":"Time","stage":"Stage",
                     "rows":"Rows","duration_s":"Duration (s)","status_icon":"Status"}
        ),
        use_container_width=True, hide_index=True,
    )

    today_log = log_df[log_df["timestamp"].str.startswith("2026-04-06")]
    if not today_log.empty:
        fig = px.bar(today_log, x="stage", y="duration_s",
                     color="status",
                     color_discrete_map={"ok": "#1D9E75", "error": "#E24B4A"},
                     labels={"duration_s": "Duration (s)", "stage": "Stage"},
                     title="Today's run durations")
        fig.update_layout(margin=dict(t=40, b=20), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Raw data ──────────────────────────────────────────────────────────────
    st.subheader(T["raw_data"])
    st.caption(
        # REPLACE: pd.read_parquet(status['artifact_path'])
        "Mock data — replace with real parquet load"
    )
    raw = get_posts()
    show_cols = ["date","time","text","sentiment","sentiment_score",
                 "dominant_category","engagement_score",
                 "sp500_5min_before","sp500_5min_after","market_impact_pct"]
    st.dataframe(raw[show_cols], use_container_width=True, hide_index=True)
    st.download_button(
        f"⬇️ {T['download_csv']}", raw.to_csv(index=False),
        "trumpsignal_processed.csv", "text/csv",
    )

    st.divider()

    # ── Config reference ──────────────────────────────────────────────────────
    st.subheader("config.yaml reference")
    st.code("""
# REPLACE: สร้างไฟล์นี้ที่ root ของ repo
dataset:
  source: chrissoria/trump-truth-social
  version: main
  update_schedule: "0 8 * * *"   # daily 8am UTC

models:
  sentiment: cardiffnlp/twitter-roberta-base-sentiment
  embedding: all-MiniLM-L6-v2

artifacts:
  raw_dir:       artifacts/raw/
  processed_dir: artifacts/processed/
  embeddings_dir: artifacts/embeddings/
  run_log_dir:   artifacts/runs/

gdelt:
  update_schedule: "0 0 * * 1"   # weekly Monday

api:
  host: 0.0.0.0
  port: 8000
""", language="yaml")