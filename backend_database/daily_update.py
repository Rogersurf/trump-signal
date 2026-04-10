import sqlite3
import pandas as pd
import time
from datetime import datetime
from datasets import load_dataset
from apscheduler.schedulers.blocking import BlockingScheduler
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "trump_data.db")
HF_REPO = "chrissoria/trump-truth-social"


def sync_task():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] 触发每日同步...")

    try:
        # 获取最新数据
        dataset = load_dataset(HF_REPO)
        df_new = dataset['train'].to_pandas()
        df_new['date'] = pd.to_datetime(df_new['date']).dt.strftime('%Y-%m-%d %H:%M:%S')

        with sqlite3.connect(DB_PATH) as conn:
            # 策略：直接覆盖本地表。
            # 如果数据量极庞大，可改用 SQL 'INSERT OR IGNORE' 实现真正的增量。
            df_new.to_sql("truth_social", conn, if_exists="replace", index=False)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_date ON truth_social (date)")

        print(f"[{now}] 同步成功，当前记录数: {len(df_new)}")
    except Exception as e:
        print(f"[{now}] 同步异常: {e}")


if __name__ == "__main__":
    # 检查数据库是否已由 init_db.py 生成
    if not os.path.exists(DB_PATH):
        print("错误: 未找到数据库文件。请先运行 python init_db.py")
        exit(1)

    scheduler = BlockingScheduler()

    # 设定每天凌晨 02:00 同步一次
    scheduler.add_job(sync_task, 'cron', hour=2, minute=0)

    print(f"更新调度器已启动 [目标: {DB_PATH}]")
    print("程序将保持后台运行...")

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("调度服务已关闭。")