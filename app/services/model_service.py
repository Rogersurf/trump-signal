from backend.model_predict import predict_latest

def run_prediction():
    import pandas as pd
    import numpy as np

    result = predict_latest()

    # 🔥 convert DataFrame → dict
    if isinstance(result, pd.DataFrame):
        result = result.to_dict(orient="records")

    # 🔥 recursive conversion (numpy → python)
    def convert(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert(v) for v in obj]
        else:
            return obj

    return convert(result)