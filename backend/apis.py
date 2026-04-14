from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import io
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from backend_database.data_api import TrumpDataClient

app = FastAPI(title="Trump Geopolitical Rhetoric API (High Speed)", version="2.0")

# 初始化数据客户端
# 此时不再需要从网络下载数据集，启动速度极快
db_client = TrumpDataClient("trump_data.db")


@app.get("/")
def read_root():
    return {
        "status": "Online",
        "engine": "SQLite Local Storage",
        "message": "API is running using the Local Data API."
    }


@app.get("/stats")
def get_top_correlations():
    """通过 Data Client 获取最强指标关联"""
    # 直接调用方法库中的逻辑
    top_corrs = db_client.get_top_rhetoric_correlations(limit=5)

    # 转换格式以便 JSON 输出
    return {
        "top_impact_pairs": top_corrs.to_dict()
    }


@app.get("/chart/pie")
def get_pie_chart():
    """获取最新数据的饼图"""
    # 从 Client 获取基础清洗数据
    df = db_client.get_full_data()
    r_cols = [c for c in df.columns if c.startswith('cat_')]
    rhetoric_sums = df[r_cols].mean().sort_values(ascending=False)

    plt.figure(figsize=(8, 8))
    plt.pie(rhetoric_sums,
            labels=[c.replace('cat_', '').replace('_', ' ').title() for c in rhetoric_sums.index],
            autopct='%1.1f%%',
            colors=sns.color_palette("rocket"))
    plt.title("Trump Rhetoric Composition (From Local DB)")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")


@app.get("/data/daily")
def get_daily_json():
    """获取每日聚合趋势数据"""
    # 直接调用方法库的高效 SQL 聚合方法
    df_daily = db_client.get_daily_metrics()

    # 将 Timestamp 转换为字符串以便 JSON 序列化
    df_daily['day'] = df_daily['day'].dt.strftime('%Y-%m-%d')
    return df_daily.to_dict(orient="records")


@app.get("/data/latest")
def get_recent_posts(n: int = 5):
    """获取最近的 N 条原始帖子预览"""
    posts = db_client.get_latest_posts(limit=n)
    return posts.to_dict(orient="records")


if __name__ == "__main__":
    import uvicorn

    # 启动 API
    uvicorn.run(app, host="0.0.0.0", port=8000)