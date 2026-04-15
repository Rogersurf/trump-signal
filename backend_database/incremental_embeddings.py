import pickle
import numpy as np
from backend_database.embeddings import CACHE_PATH, MODEL_NAME
from sentence_transformers import SentenceTransformer
import sqlite3
import pandas as pd
from huggingface_hub import HfApi

# Load existing cache
with open(CACHE_PATH, "rb") as f:
    data = pickle.load(f)
existing_posts = data["posts"]
existing_embeddings = data["embeddings"]

# Get new posts from SQLite (those not in existing_posts)
existing_ids = {p["post_id"] for p in existing_posts}
conn = sqlite3.connect("backend_database/trump_data.db")
new_posts_df = pd.read_sql(
    "SELECT post_id, date, text FROM truth_social WHERE post_id NOT IN ({})".format(
        ",".join("?" * len(existing_ids))
    ),
    conn,
    params=list(existing_ids)
)
conn.close()

if not new_posts_df.empty:
    model = SentenceTransformer(MODEL_NAME)
    new_texts = new_posts_df["text"].tolist()
    new_embeddings = model.encode(new_texts)
    
    # Combine
    all_posts = existing_posts + new_posts_df.to_dict("records")
    all_embeddings = np.vstack([existing_embeddings, new_embeddings])
    
    # Save locally
    with open(CACHE_PATH, "wb") as f:
        pickle.dump({"posts": all_posts, "embeddings": all_embeddings}, f)
    
    # Upload to HF
    api = HfApi()
    api.upload_file(
        path_or_fileobj=CACHE_PATH,
        path_in_repo="trump_embeddings.pkl",
        repo_id="Rogersurf/trump-pulse-embeddings",
        repo_type="dataset"
    )
    print("✅ Incremental embeddings updated and uploaded.")