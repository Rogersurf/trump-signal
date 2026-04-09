import sqlite3
import pandas as pd
from datasets import load_dataset
import os

DB_PATH = "trump_data.db"
HF_REPO = "chrissoria/trump-truth-social"


def initialize():
    if os.path.exists(DB_PATH):
        print(f"警告: {DB_PATH} 已存在。若需重新初始化，请手动删除该文件。")
        return

    print("--- 正在进行首次初始化 ---")
    print(f"正在从 HuggingFace 下载全量数据: {HF_REPO}...")

    # 1. 下载全量数据
    dataset = load_dataset(HF_REPO)
    df = dataset['train'].to_pandas()

    # 2. 预处理日期格式 (存入 SQLite 建议使用字符串或标准 ISO 格式)
    df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d %H:%M:%S')

    # 3. 存入 SQLite
    print(f"正在写入本地数据库，总计 {len(df)} 条记录...")
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql("truth_social", conn, if_exists="replace", index=False)

        # 4. 创建关键列索引，确保后续查询 2026 年数据是毫秒级的
        conn.execute("CREATE INDEX idx_date ON truth_social (date)")
        print("数据库索引创建完毕。")

    print("--- 初始化成功！---")


if __name__ == "__main__":
    initialize()