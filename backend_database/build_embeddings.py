"""Build embeddings cache from the SQLite database."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend_database.embeddings import PostSearchEngine, CACHE_PATH
from backend_database.init_db import DEFAULT_DB_PATH

def upload_to_hf(cache_path: str, repo_id: str = "Rogersurf/trump-pulse-embeddings"):
    """Upload the embeddings pickle file to Hugging Face Dataset."""
    from huggingface_hub import HfApi
    api = HfApi()
    api.upload_file(
        path_or_fileobj=cache_path,
        path_in_repo="trump_embeddings.pkl",
        repo_id=repo_id,
        repo_type="dataset"
    )
    print(f"✅ Embeddings uploaded to {repo_id}")

if __name__ == "__main__":
    engine = PostSearchEngine(DEFAULT_DB_PATH)
    engine.build_index(force=True)
    print("✅ Embeddings cache built successfully.")
    
    # Upload the built cache to Hugging Face Dataset
    upload_to_hf(CACHE_PATH)