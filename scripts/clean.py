from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = ROOT / "data" / "staging" / "student_staging.csv"
OUTPUT_DIR = ROOT / "data" / "cleaned"
ERROR_DIR = ROOT / "data" / "errors"
OUTPUT_FILE = OUTPUT_DIR / "student_cleaned.csv"
ERROR_FILE = ERROR_DIR / "rejected_records.csv"
REQUIRED = {"G1", "G2", "G3", "absences"}

def calculate_risk(row):
    if row["G3"] < 10 or row["absences"] > 15:
        return "High"
    if row["G3"] < 14 or row["absences"] > 10:
        return "Medium"
    return "Low"

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Staging file not found: {INPUT_FILE}. Run scripts/pipeline.py.")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ERROR_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT_FILE)
    missing_cols = REQUIRED.difference(df.columns)
    if missing_cols:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing_cols)}")

    original_rows = len(df)
    duplicate_count = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    numeric_cols = ["G1", "G2", "G3", "absences"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    missing_mask = df[numeric_cols].isna().any(axis=1)
    invalid_marks = (
        (df[["G1", "G2", "G3"]] < 0).any(axis=1)
        | (df[["G1", "G2", "G3"]] > 20).any(axis=1)
        | (df["absences"] < 0)
    )
    rejected_mask = missing_mask | invalid_marks
    rejected = df.loc[rejected_mask].copy()
    if len(rejected):
        rejected["rejection_reason"] = [
            "Missing/non-numeric required value" if missing_mask.loc[idx]
            else "Grade outside 0-20 or negative absences"
            for idx in rejected.index
        ]
    else:
        rejected = pd.DataFrame(columns=list(df.columns) + ["rejection_reason"])
    rejected.to_csv(ERROR_FILE, index=False)

    clean = df.loc[~rejected_mask].copy()
    clean["average_marks"] = clean[["G1", "G2", "G3"]].mean(axis=1)
    clean["risk_level"] = clean.apply(calculate_risk, axis=1)
    clean.to_csv(OUTPUT_FILE, index=False)

    print("=" * 48)
    print("DATA CLEANING AND VALIDATION")
    print("=" * 48)
    print("Input rows:", original_rows)
    print("Duplicates removed:", duplicate_count)
    print("Rejected rows:", len(rejected))
    print("Clean rows:", len(clean))
    print("Missing values in required fields:", int(df[numeric_cols].isna().sum().sum()))
    print("Risk distribution:\n", clean["risk_level"].value_counts())
    print("Cleaned file:", OUTPUT_FILE.relative_to(ROOT))
    print("Rejected file:", ERROR_FILE.relative_to(ROOT))

if __name__ == "__main__":
    main()
