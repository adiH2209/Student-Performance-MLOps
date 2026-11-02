"""Train the configured XGBoost classifier and save the API-compatible model bundle."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from ml.model_utils import train_and_evaluate, save_bundle

if __name__ == "__main__":
    bundle, metrics = train_and_evaluate()
    print("XGBoost evaluation:", metrics)
    print("Saved:", save_bundle(bundle))
