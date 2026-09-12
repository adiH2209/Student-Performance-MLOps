import pandas as pd
import os

input_file = "data/raw/student_raw.csv"
output_folder = "data/cleaned"
error_folder = "data/errors"

os.makedirs(output_folder, exist_ok=True)
os.makedirs(error_folder, exist_ok=True)

df = pd.read_csv(input_file)

print("================================")
print("DATA CLEANING AND VALIDATION")
print("================================")
print("Original rows:", len(df))

# Missing-value check
missing_values = df.isnull().sum().sum()
print("Missing values:", missing_values)

# Duplicate check
duplicates = df.duplicated().sum()
df = df.drop_duplicates()
print("Duplicates removed:", duplicates)

# Invalid marks check
invalid_mask = (
    (df["G1"] < 0) | (df["G1"] > 20) |
    (df["G2"] < 0) | (df["G2"] > 20) |
    (df["G3"] < 0) | (df["G3"] > 20)
)

invalid_records = df[invalid_mask].copy()

# Save rejected records
error_file = os.path.join(error_folder, "rejected_records.csv")

if len(invalid_records) > 0:
    invalid_records.to_csv(error_file, index=False)
else:
    pd.DataFrame({
        "status": ["No rejected records"],
        "reason": ["No invalid marks found"]
    }).to_csv(error_file, index=False)

print("Invalid mark records:", len(invalid_records))
print("Error log saved to:", error_file)

# Remove invalid records
df = df[~invalid_mask]

# Create average marks
df["average_marks"] = (
    df["G1"] + df["G2"] + df["G3"]
) / 3

# Calculate academic risk
def calculate_risk(row):
    if row["G3"] < 10 or row["absences"] > 15:
        return "High"
    elif row["G3"] < 14 or row["absences"] > 10:
        return "Medium"
    else:
        return "Low"

df["risk_level"] = df.apply(calculate_risk, axis=1)

# Save cleaned data
output_file = os.path.join(
    output_folder,
    "student_cleaned.csv"
)

df.to_csv(output_file, index=False)

print("Final rows:", len(df))
print("Cleaned data saved to:", output_file)

print("\nRisk distribution:")
print(df["risk_level"].value_counts())

print("\nCleaning completed successfully!")