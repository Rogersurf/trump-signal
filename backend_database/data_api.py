# ─────────────────────────────────────────────
# Data Client (extended from original)
# ─────────────────────────────────────────────
import sqlite3
import pandas as pd
import datetime
import os
from backend_database.init_db import DEFAULT_DB_PATH

class TrumpDataClient:
    def __init__(self, db_path=None):
        self.db_path = db_path or DEFAULT_DB_PATH

    def _get_conn(self):
        print(f"[DB DEBUG] Using DB_PATH: {self.db_path}")  # 🔥 IMPORTANTE
        return sqlite3.connect(self.db_path)

    # ── Raw / Full ────────────────────────────
    def get_full_data(self, date_from=None, date_to=None, market_hours_only=False):
        conds = ["gdelt_total_events > 0"]
        if date_from:
            conds.append(f"DATE(date) >= '{date_from}'")
        if date_to:
            conds.append(f"DATE(date) <= '{date_to}'")
        if market_hours_only:
            conds.append("during_market_hours = 1")
        where = " AND ".join(conds)
        query = f"SELECT * FROM truth_social WHERE {where}"
        with self._get_conn() as conn:
            return pd.read_sql(query, conn, parse_dates=["date"])

    # ── Section 1: Overview KPIs ──────────────
    def get_kpis(self, date_from=None, date_to=None):
        conds = ["1=1"]
        if date_from:
            conds.append(f"DATE(date) >= '{date_from}'")
        if date_to:
            conds.append(f"DATE(date) <= '{date_to}'")
        where = " AND ".join(conds)
        query = f"""
            SELECT
                COUNT(*)                                                        AS total_posts,
                AVG(replies_count)                                              AS avg_replies,
                AVG(reblogs_count)                                              AS avg_reblogs,
                AVG(favourites_count)                                           AS avg_favs,
                ROUND(100.0 * SUM(CASE WHEN during_market_hours = 1 THEN 1 ELSE 0 END)
                      / COUNT(*), 1)                                            AS pct_market_hours
            FROM truth_social
            WHERE {where}
        """
        with self._get_conn() as conn:
            return pd.read_sql(query, conn).iloc[0]

    # ── Section 2: Temporal Trends ────────────
    def get_daily_metrics(self, date_from=None, date_to=None):
        conds = ["1=1"]
        if date_from:
            conds.append(f"DATE(date) >= '{date_from}'")
        if date_to:
            conds.append(f"DATE(date) <= '{date_to}'")
        where = " AND ".join(conds)
        query = f"""
            SELECT
                strftime('%Y-%m-%d', date)  AS day,
                COUNT(*)                    AS posts,
                AVG(sp500_close)            AS sp500_close,
                AVG(djt_close)              AS djt_close,
                AVG(gdelt_avg_tone)         AS tone,
                SUM(gdelt_total_events)     AS gdelt_events
            FROM truth_social
            WHERE {where}
            GROUP BY day
            ORDER BY day
        """
        with self._get_conn() as conn:
            df = pd.read_sql(query, conn)
            df["day"] = pd.to_datetime(df["day"])
            return df


    def get_correlation_matrix(self, date_from=None, date_to=None):
        df = self.get_full_data(date_from, date_to)
        cat_cols  = [c for c in df.columns if c.startswith("cat_")]
        mkt_cols  = [c for c in df.columns if c in (
            "sp500_close","djt_close",
            "sp500_1hr_after","sp500_1hr_before",
        )]
        gdelt_cols = [c for c in df.columns if c.startswith("gdelt_")]
        target_cols = mkt_cols + gdelt_cols
        avail = [c for c in cat_cols + target_cols if c in df.columns]
        return df[avail].corr().loc[
            [c for c in cat_cols if c in avail],
            [c for c in target_cols if c in avail]
        ]

    # ── Section 4: Category Distribution ──────
    def get_category_distribution(self, date_from=None, date_to=None):
        conds = ["1=1"]
        if date_from:
            conds.append(f"DATE(date) >= '{date_from}'")
        if date_to:
            conds.append(f"DATE(date) <= '{date_to}'")
        where = " AND ".join(conds)
        query = f"""
            SELECT
                AVG(cat_self_promotion)      AS self_promotion,
                AVG(cat_praising_endorsing)  AS praising_endorsing,
                AVG(cat_attacking_opposition)AS attacking_opposition,
                AVG(cat_attacking_individual)AS attacking_individual,
                AVG(cat_other)               AS other
            FROM truth_social
            WHERE {where}
        """
        with self._get_conn() as conn:
            row = pd.read_sql(query, conn).iloc[0]
            return row.sort_values(ascending=False)

    # ── Section 5: Engagement by Category ─────
    def get_engagement_by_category(self, date_from=None, date_to=None):
        conds = ["1=1"]
        if date_from:
            conds.append(f"DATE(date) >= '{date_from}'")
        if date_to:
            conds.append(f"DATE(date) <= '{date_to}'")
        where = " AND ".join(conds)
        cats = {
            "self_promotion":       "cat_self_promotion",
            "praising_endorsing":   "cat_praising_endorsing",
            "attacking_opposition": "cat_attacking_opposition",
            "attacking_individual": "cat_attacking_individual",
            "other":                "cat_other",
        }
        rows = []
        with self._get_conn() as conn:
            for label, col in cats.items():
                q = f"""
                    SELECT
                        '{label}' AS category,
                        AVG(replies_count)    AS avg_replies,
                        AVG(reblogs_count)    AS avg_reblogs,
                        AVG(favourites_count) AS avg_favs
                    FROM truth_social
                    WHERE {where} AND {col} = (
                        SELECT MAX(v) FROM (
                            SELECT cat_self_promotion AS v FROM truth_social WHERE {where}
                            UNION ALL SELECT cat_praising_endorsing FROM truth_social WHERE {where}
                            UNION ALL SELECT cat_attacking_opposition FROM truth_social WHERE {where}
                            UNION ALL SELECT cat_attacking_individual FROM truth_social WHERE {where}
                            UNION ALL SELECT cat_other FROM truth_social WHERE {where}
                        )
                    ) OR {col} > 0.3
                """
                # Simpler: just weight engagement by category score
                q2 = f"""
                    SELECT
                        '{label}'                           AS category,
                        AVG(replies_count    * {col})       AS avg_replies,
                        AVG(reblogs_count    * {col})       AS avg_reblogs,
                        AVG(favourites_count * {col})       AS avg_favs
                    FROM truth_social
                    WHERE {where}
                """
                rows.append(pd.read_sql(q2, conn))
        return pd.concat(rows, ignore_index=True)

    # ── Section 6: Top Posts ───────────────────
    def get_top_posts(self, metric="favourites_count", limit=10,
                      date_from=None, date_to=None):
        conds = ["1=1"]
        if date_from:
            conds.append(f"DATE(date) >= '{date_from}'")
        if date_to:
            conds.append(f"DATE(date) <= '{date_to}'")
        where = " AND ".join(conds)
        query = f"""
            SELECT
                post_id, url,
                strftime('%Y-%m-%d %H:%M', date) AS date,
                SUBSTR(text, 1, 180)           AS snippet,
                favourites_count, replies_count, reblogs_count,
                during_market_hours
            FROM truth_social
            WHERE {where}
            ORDER BY {metric} DESC
            LIMIT {limit}
        """
        with self._get_conn() as conn:
            return pd.read_sql(query, conn)

    # ── Section 7: GDELT Heatmap ───────────────
    def get_gdelt_events(self, date_from=None, date_to=None):
        conds = ["1=1"]
        if date_from:
            conds.append(f"DATE(date) >= '{date_from}'")
        if date_to:
            conds.append(f"DATE(date) <= '{date_to}'")
        where = " AND ".join(conds)
        query = f"""
            SELECT
                strftime('%Y-%m-%d', date) AS day,
                AVG(gdelt_military_pct)    AS military,
                AVG(gdelt_sanctions_pct)   AS sanctions,
                AVG(gdelt_protest_pct)     AS protest,
                AVG(gdelt_avg_tone)        AS tone,
                SUM(gdelt_total_events)    AS total_events
            FROM truth_social
            WHERE {where}
            GROUP BY day
            ORDER BY day
        """
        with self._get_conn() as conn:
            df = pd.read_sql(query, conn)
            df["day"] = pd.to_datetime(df["day"])
            return df

    # ── Section 2 extended: raw daily correlations
    def get_daily_metrics_full(self, date_from=None, date_to=None):
        conds = ["1=1"]
        if date_from:
            conds.append(f"DATE(date) >= '{date_from}'")
        if date_to:
            conds.append(f"DATE(date) <= '{date_to}'")
        where = " AND ".join(conds)
        query = f"""
            SELECT strftime('%Y-%m-%d', date) AS day,
                COUNT(*)                    AS posts,
                AVG(sp500_close)            AS sp500_close,
                AVG(gdelt_avg_tone)         AS tone,
                SUM(gdelt_total_events)     AS gdelt_events
            FROM truth_social
            WHERE {where}
            GROUP BY day ORDER BY day
        """
        with self._get_conn() as conn:
            df = pd.read_sql(query, conn)
            df["day"] = pd.to_datetime(df["day"])
            return df

    # pie chart data
    def get_category_ratio(self, start: str = (datetime.date.today() - datetime.timedelta(days=10)).isoformat(),
                           end: str = datetime.date.today()) -> pd.DataFrame:
        CAT_LABELS = {
            "cat_attacking_individual": "Attacking Individual",
            "cat_attacking_opposition": "Attacking Opposition",
            "cat_threatening_intl": "Threatening (Intl)",
            "cat_enacting_aggressive": "Enacting Aggressive",
            "cat_enacting_nonaggressive": "Enacting Non-Aggressive",
            "cat_deescalating": "De-escalating",
            "cat_praising_endorsing": "Praising / Endorsing",
            "cat_self_promotion": "Self-Promotion",
            "cat_other": "Other",
        }

        cols_sql = ",\n    ".join(f"AVG({c}) AS {c}" for c in CAT_LABELS)
        query = f"""
               SELECT
                   COUNT(*) AS total_posts,
                   {cols_sql}
               FROM truth_social
               WHERE DATE(date) >= '{start}'
                 AND DATE(date) <= '{end}'
           """
        with self._get_conn() as conn:
            row = pd.read_sql(query, conn).iloc[0]

        total_posts = int(row["total_posts"])
        if total_posts == 0:
            raise ValueError(f"No data found between {start} and {end}")

        scores = pd.to_numeric(row[list(CAT_LABELS.keys())], errors="coerce").fillna(0)
        total_score = scores.sum()
        print('*'*40)

        print(scores)
        df = pd.DataFrame({
            "category": list(CAT_LABELS.values()),
            "ratio_pct": scores.astype(float).values.round(4),
            # "ratio_pct": (scores.values / total_score * 100).round(2),
        })
        df["date_from"] = start
        df["date_to"] = end
        df["total_posts"] = total_posts

        return df[["date_from", "date_to", "total_posts", "category", "ratio_pct"]]

    def get_market_impact(
            self,
            start: str = (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
            end: str = datetime.date.today(),
    ) -> pd.DataFrame:
        """
        返回开市时间内每条帖子发布后，sp500/qqq/dia 的价格变动幅度。

        计算方式：
            5min_pct  = (_5min_after  - _at_post) / _at_post * 100
            1hr_pct   = (_1hr_after   - _at_post) / _at_post * 100

        只返回 during_market_hours = 1 且三支标的 at_post 均不为空的帖子。

        Parameters
        ----------
        start : str, optional  YYYY-MM-DD，默认最近一条开市帖子所在日期
        end   : str, optional  YYYY-MM-DD，默认同 start

        Returns
        -------
        pd.DataFrame
            每行一条帖子，列包含：
            post_id, date, text_snippet,
            sp500_5min_pct, sp500_1hr_pct,
            qqq_5min_pct,   qqq_1hr_pct,
            dia_5min_pct,   dia_1hr_pct
        """
        if start is None or end is None:
            # 找最近一条开市帖子的日期作为默认
            with self._get_conn() as conn:
                row = pd.read_sql(
                    """SELECT DATE (date) AS day
                       FROM truth_social
                       WHERE during_market_hours = 1
                         AND sp500_at_post IS NOT NULL
                       ORDER BY date DESC LIMIT 1""",
                    conn,
                )
            if row.empty:
                raise ValueError("No market-hours posts with price data found.")
            latest = row.iloc[0]["day"]
            start = start or latest
            end = end or latest

        end_inclusive = (
                pd.to_datetime(end) + pd.Timedelta(days=1)
        ).strftime("%Y-%m-%d")

        query = f"""
            SELECT
                post_id,
                datetime                                   AS date,
                SUBSTR(text, 1, 120)                       AS text_snippet,

                -- sp500
                sp500_at_post,
                sp500_5min_after,
                sp500_1hr_after,

                -- qqq
                qqq_at_post,
                qqq_5min_after,
                qqq_1hr_after,

                -- dia
                dia_at_post,
                dia_5min_after,
                dia_1hr_after

            FROM truth_social
            WHERE during_market_hours = 1
              AND sp500_at_post IS NOT NULL
              AND qqq_at_post   IS NOT NULL
              AND dia_at_post   IS NOT NULL
              AND sp500_at_post != 0
              AND qqq_at_post   != 0
              AND dia_at_post   != 0
              AND date >= '{start}'
              AND date <  '{end_inclusive}'
            ORDER BY date ASC
        """

        with self._get_conn() as conn:
            df = pd.read_sql(query, conn, parse_dates=["date"])

        if df.empty:
            raise ValueError(f"No market-hours posts with price data between {start} and {end}")

        # 计算百分比变动
        for ticker in ["sp500", "qqq", "dia"]:
            base = df[f"{ticker}_at_post"]
            df[f"{ticker}_5min_pct"] = (
                    (df[f"{ticker}_5min_after"] - base) / base * 100
            ).round(4)
            df[f"{ticker}_1hr_pct"] = (
                    (df[f"{ticker}_1hr_after"] - base) / base * 100
            ).round(4)

        return df[[
            "post_id", "date", "text_snippet",
            "sp500_5min_pct", "sp500_1hr_pct",
            "qqq_5min_pct", "qqq_1hr_pct",
            "dia_5min_pct", "dia_1hr_pct",
        ]]

    def get_stock_series(self, index: str = "sp500", days: int = 30) -> pd.DataFrame:
        """
        Return stock series data for the given index.
        Uses 5-min % change for sp500/qqq/dia, and daily close prices for others.
        """
        from datetime import datetime, timedelta
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        # For indices that have 5-min impact data
        if index in ("sp500", "qqq", "dia"):
            df = self.get_market_impact(start=start_date, end=end_date)
            if not df.empty:
                col = f"{index}_5min_pct"
                if col in df.columns:
                    result = df[["date", col]].copy()
                    result = result.rename(columns={col: "price"})
                    result["price"] = pd.to_numeric(result["price"], errors="coerce")
                    result["has_big_post"] = result["price"].abs() > 0.3
                    result["pct_change"] = result["price"].round(4)
                    return result.dropna(subset=["price"]).reset_index(drop=True)

        # Fallback for other indices (use daily close prices)
        close_col = f"{index}_close"
        dm = self.get_daily_metrics(date_from=start_date, date_to=end_date)
        if not dm.empty and close_col in dm.columns:
            result = dm[["day", close_col]].copy()
            result = result.rename(columns={"day": "date", close_col: "price"})
            result["price"] = pd.to_numeric(result["price"], errors="coerce")
            result["has_big_post"] = False
            result["pct_change"] = result["price"].pct_change().fillna(0).round(4)
            return result.dropna(subset=["price"]).reset_index(drop=True)

        # Return empty DataFrame with expected columns
        return pd.DataFrame(columns=["date", "price", "has_big_post", "pct_change"])

    def get_category_market_impact(
            self,
            start: str = (datetime.date.today() - datetime.timedelta(days=1)).isoformat(),
            end: str = datetime.date.today(),
    ) -> pd.DataFrame:
        """
        按帖子类别统计开市时间内发帖后 sp500/qqq/dia 的平均价格变动幅度。

        逻辑：
        - 只取 during_market_hours = 1 的帖子
        - 只取三支标的 at_post 均不为空的帖子
        - 一条帖子可属于多个类别（multi-label），每个类别=1的帖子都纳入该类别的统计
        - 变动幅度 = (_5min_after - _at_post) / _at_post * 100

        Parameters
        ----------
        start : str, optional  YYYY-MM-DD
        end   : str, optional  YYYY-MM-DD

        Returns
        -------
        pd.DataFrame
            每行一个类别，列包含：
            category, post_count,
            sp500_5min_avg, sp500_1hr_avg,
            qqq_5min_avg,   qqq_1hr_avg,
            dia_5min_avg,   dia_1hr_avg
        """
        if start is None or end is None:
            with self._get_conn() as conn:
                row = pd.read_sql(
                    """SELECT DATE (date) AS day
                       FROM truth_social
                       WHERE during_market_hours = 1
                         AND sp500_at_post IS NOT NULL
                         AND cat_self_promotion IS NOT NULL
                       ORDER BY date DESC LIMIT 1""",
                    conn,
                )
            if row.empty:
                raise ValueError("No scored market-hours posts with price data found.")
            latest = row.iloc[0]["day"]
            start = start or latest
            end = end or latest

        end_inclusive = (
                pd.to_datetime(end) + pd.Timedelta(days=1)
        ).strftime("%Y-%m-%d")

        query = f"""
            SELECT
                -- categories (0/1)
                cat_attacking_individual,
                cat_attacking_opposition,
                cat_threatening_intl,
                cat_enacting_aggressive,
                cat_enacting_nonaggressive,
                cat_deescalating,
                cat_praising_endorsing,
                cat_self_promotion,
                cat_other,

                -- price at post
                sp500_at_post,
                sp500_5min_after,
                sp500_1hr_after,

                qqq_at_post,
                qqq_5min_after,
                qqq_1hr_after,

                dia_at_post,
                dia_5min_after,
                dia_1hr_after

            FROM truth_social
            WHERE during_market_hours = 1
              AND sp500_at_post IS NOT NULL
              AND qqq_at_post   IS NOT NULL
              AND dia_at_post   IS NOT NULL
              AND sp500_at_post != 0
              AND qqq_at_post   != 0
              AND dia_at_post   != 0
              AND cat_self_promotion IS NOT NULL
              AND date >= '{start}'
              AND date <  '{end_inclusive}'
        """

        with self._get_conn() as conn:
            df = pd.read_sql(query, conn)

        if df.empty:
            raise ValueError(f"No valid posts found between {start} and {end}")

        # 计算每条帖子的价格变动 %
        for ticker in ["sp500", "qqq", "dia"]:
            base = df[f"{ticker}_at_post"]
            df[f"{ticker}_5min_pct"] = (df[f"{ticker}_5min_after"] - base) / base * 100
            df[f"{ticker}_1hr_pct"] = (df[f"{ticker}_1hr_after"] - base) / base * 100

        cat_cols = {
            "cat_attacking_individual": "Attacking Individual",
            "cat_attacking_opposition": "Attacking Opposition",
            "cat_threatening_intl": "Threatening (Intl)",
            "cat_enacting_aggressive": "Enacting Aggressive",
            "cat_enacting_nonaggressive": "Enacting Non-Aggressive",
            "cat_deescalating": "De-escalating",
            "cat_praising_endorsing": "Praising / Endorsing",
            "cat_self_promotion": "Self-Promotion",
            "cat_other": "Other",
        }

        impact_cols = [
            "sp500_5min_pct", "sp500_1hr_pct",
            "qqq_5min_pct", "qqq_1hr_pct",
            "dia_5min_pct", "dia_1hr_pct",
        ]

        rows = []
        for col, label in cat_cols.items():
            mask = df[col] == 1
            subset = df.loc[mask, impact_cols]
            rows.append({
                "category": label,
                "post_count": int(mask.sum()),
                **subset.mean().round(4).to_dict(),
            })

        result = pd.DataFrame(rows)
        result = result[[
            "category", "post_count",
            "sp500_5min_pct", "sp500_1hr_pct",
            "qqq_5min_pct", "qqq_1hr_pct",
            "dia_5min_pct", "dia_1hr_pct",
        ]]
        return result

    def get_gdelt_correlation(
            self,
            start: str = None,
            end: str = None,
    ) -> pd.DataFrame:
        """
        计算 GDELT 全球事件指标 与 Trump 帖子类别 的 Pearson 相关系数矩阵。

        GDELT 指标（行）vs 帖子类别（列）

        Parameters
        ----------
        start : str, optional  YYYY-MM-DD
        end   : str, optional  YYYY-MM-DD

        Returns
        -------
        pd.DataFrame
            相关系数矩阵，index=GDELT指标, columns=帖子类别
            附加 p_value 矩阵作为第二个返回值
        """
        if start is None or end is None:
            with self._get_conn() as conn:
                row = pd.read_sql(
                    """SELECT DATE (date) AS day
                       FROM truth_social
                       WHERE cat_self_promotion IS NOT NULL
                         AND gdelt_total_events IS NOT NULL
                       ORDER BY date DESC LIMIT 1""",
                    conn,
                )
            if row.empty:
                raise ValueError("No posts with both category and GDELT data found.")
            latest = row.iloc[0]["day"]
            start = start or latest
            end = end or latest

        end_inclusive = (
                pd.to_datetime(end) + pd.Timedelta(days=1)
        ).strftime("%Y-%m-%d")

        query = f"""
            SELECT
                -- 帖子类别
                cat_attacking_individual,
                cat_attacking_opposition,
                cat_threatening_intl,
                cat_enacting_aggressive,
                cat_enacting_nonaggressive,
                cat_deescalating,
                cat_praising_endorsing,
                cat_self_promotion,
                cat_other,

                -- GDELT 全球事件指标
                gdelt_avg_tone,
                gdelt_total_events,
                gdelt_goldstein_avg,
                gdelt_military,
                gdelt_sanctions,
                gdelt_threat,
                gdelt_protest,
                gdelt_verbal_conflict,
                gdelt_material_conflict,
                gdelt_verbal_cooperation,
                gdelt_material_cooperation

            FROM truth_social
            WHERE cat_self_promotion   IS NOT NULL
              AND gdelt_total_events   IS NOT NULL
              AND date >= '{start}'
              AND date <  '{end_inclusive}'
        """

        with self._get_conn() as conn:
            df = pd.read_sql(query, conn)

        if df.empty:
            raise ValueError(f"No data found between {start} and {end}")

        cat_cols = [
            "cat_attacking_individual",
            "cat_attacking_opposition",
            "cat_threatening_intl",
            "cat_enacting_aggressive",
            "cat_enacting_nonaggressive",
            "cat_deescalating",
            "cat_praising_endorsing",
            "cat_self_promotion",
            "cat_other",
        ]

        gdelt_cols = [
            "gdelt_avg_tone",
            "gdelt_total_events",
            "gdelt_goldstein_avg",
            "gdelt_military",
            "gdelt_sanctions",
            "gdelt_threat",
            "gdelt_protest",
            "gdelt_verbal_conflict",
            "gdelt_material_conflict",
            "gdelt_verbal_cooperation",
            "gdelt_material_cooperation",
        ]

        cat_labels = {
            "cat_attacking_individual": "Attacking Individual",
            "cat_attacking_opposition": "Attacking Opposition",
            "cat_threatening_intl": "Threatening (Intl)",
            "cat_enacting_aggressive": "Enacting Aggressive",
            "cat_enacting_nonaggressive": "Enacting Non-Aggressive",
            "cat_deescalating": "De-escalating",
            "cat_praising_endorsing": "Praising / Endorsing",
            "cat_self_promotion": "Self-Promotion",
            "cat_other": "Other",
        }

        gdelt_labels = {
            "gdelt_avg_tone": "Avg Tone",
            "gdelt_total_events": "Total Events",
            "gdelt_goldstein_avg": "Goldstein Score",
            "gdelt_military": "Military Events",
            "gdelt_sanctions": "Sanctions Events",
            "gdelt_threat": "Threat Events",
            "gdelt_protest": "Protest Events",
            "gdelt_verbal_conflict": "Verbal Conflict",
            "gdelt_material_conflict": "Material Conflict",
            "gdelt_verbal_cooperation": "Verbal Cooperation",
            "gdelt_material_cooperation": "Material Cooperation",
        }

        from scipy.stats import pearsonr

        # 构建相关系数矩阵 + p值矩阵
        corr_data = {}
        pval_data = {}

        for gc in gdelt_cols:
            corr_row = {}
            pval_row = {}
            for cc in cat_cols:
                valid = df[[gc, cc]].dropna()
                if len(valid) < 10:
                    corr_row[cat_labels[cc]] = float("nan")
                    pval_row[cat_labels[cc]] = float("nan")
                else:
                    r, p = pearsonr(valid[gc], valid[cc])
                    corr_row[cat_labels[cc]] = round(r, 4)
                    pval_row[cat_labels[cc]] = round(p, 4)
            corr_data[gdelt_labels[gc]] = corr_row
            pval_data[gdelt_labels[gc]] = pval_row

        corr_df = pd.DataFrame(corr_data).T  # index=GDELT, columns=category
        pval_df = pd.DataFrame(pval_data).T

        return corr_df, pval_df

    def get_gdelt_trend(
            self,
            start: str = None,
            end: str = None,
    ) -> pd.DataFrame:
        """
        按天聚合 GDELT 全球事件指标 与 Trump 每日发帖量/类别占比，用于趋势折线图。

        Parameters
        ----------
        start : str, optional  YYYY-MM-DD
        end   : str, optional  YYYY-MM-DD

        Returns
        -------
        pd.DataFrame
            每行一天，列包含：
            day, post_count,
            cat_attacking_opposition_rate, cat_threatening_intl_rate, ... (各类别当天占比)
            gdelt_avg_tone, gdelt_total_events, gdelt_goldstein_avg,
            gdelt_military, gdelt_sanctions, gdelt_threat, gdelt_protest,
            gdelt_verbal_conflict, gdelt_material_conflict
        """
        if start is None or end is None:
            with self._get_conn() as conn:
                row = pd.read_sql(
                    """SELECT DATE (date) AS day
                       FROM truth_social
                       WHERE gdelt_total_events IS NOT NULL
                       ORDER BY date DESC LIMIT 1""",
                    conn,
                )
            if row.empty:
                raise ValueError("No posts with GDELT data found.")
            latest = row.iloc[0]["day"]
            # 默认取最近30天趋势
            end = end or latest
            start = start or (
                    pd.to_datetime(latest) - pd.Timedelta(days=30)
            ).strftime("%Y-%m-%d")

        end_inclusive = (
                pd.to_datetime(end) + pd.Timedelta(days=1)
        ).strftime("%Y-%m-%d")

        query = f"""
            SELECT
                DATE(date)                          AS day,
                COUNT(*)                            AS post_count,

                -- 类别每日占比 (avg of 0/1 = 当天有该标签的帖子比例)
                AVG(cat_attacking_individual)       AS cat_attacking_individual_rate,
                AVG(cat_attacking_opposition)       AS cat_attacking_opposition_rate,
                AVG(cat_threatening_intl)           AS cat_threatening_intl_rate,
                AVG(cat_enacting_aggressive)        AS cat_enacting_aggressive_rate,
                AVG(cat_enacting_nonaggressive)     AS cat_enacting_nonaggressive_rate,
                AVG(cat_deescalating)               AS cat_deescalating_rate,
                AVG(cat_praising_endorsing)         AS cat_praising_endorsing_rate,
                AVG(cat_self_promotion)             AS cat_self_promotion_rate,
                AVG(cat_other)                      AS cat_other_rate,

                -- GDELT 全球事件指标（每天多条帖子共享同一天的GDELT，取AVG去重）
                AVG(gdelt_avg_tone)                 AS gdelt_avg_tone,
                AVG(gdelt_total_events)             AS gdelt_total_events,
                AVG(gdelt_goldstein_avg)            AS gdelt_goldstein_avg,
                AVG(gdelt_military)                 AS gdelt_military,
                AVG(gdelt_sanctions)                AS gdelt_sanctions,
                AVG(gdelt_threat)                   AS gdelt_threat,
                AVG(gdelt_protest)                  AS gdelt_protest,
                AVG(gdelt_verbal_conflict)          AS gdelt_verbal_conflict,
                AVG(gdelt_material_conflict)        AS gdelt_material_conflict,
                AVG(gdelt_verbal_cooperation)       AS gdelt_verbal_cooperation,
                AVG(gdelt_material_cooperation)     AS gdelt_material_cooperation

            FROM truth_social
            WHERE gdelt_total_events IS NOT NULL
              AND date >= '{start}'
              AND date <  '{end_inclusive}'
            GROUP BY day
            ORDER BY day ASC
        """

        with self._get_conn() as conn:
            df = pd.read_sql(query, conn, parse_dates=["day"])

        if df.empty:
            raise ValueError(f"No GDELT trend data found between {start} and {end}")

        return df
    

def get_category_summary(self, date_from=None, date_to=None):
    df = self.get_category_ratio(start=date_from, end=date_to)

    # 🔥 Convert ratio → fake count (for UI compatibility)
    df["count"] = (df["ratio_pct"] * df["total_posts"]).astype(int)

    return df[["category", "count"]]

if __name__ == '__main__':
    client = TrumpDataClient()
    print(client.get_kpis())
    print(client.get_daily_metrics().head())
    print(client.get_category_distribution())
    print(client.get_engagement_by_category())
    print(client.get_top_posts())
    print(client.get_gdelt_events().head())
    print(client.get_category_ratio())
    print(client.get_market_impact(start="2026-01-01", end="2026-01-31").head())
    print(client.get_category_market_impact(start="2026-01-01", end="2026-01-31"))
    print(client.get_gdelt_correlation(start="2026-01-01", end="2026-01-31")[0])
    print(client.get_gdelt_trend(start="2026-01-01", end="2026-01-31").head())