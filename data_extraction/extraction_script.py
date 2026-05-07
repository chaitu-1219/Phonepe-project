import os
import json
import pandas as pd

# Correct dataset path
path = "data/raw/data/aggregated/transaction/country/india/state/"

data = []

for state in os.listdir(path):
    state_path = os.path.join(path, state)

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)

        for file in os.listdir(year_path):
            file_path = os.path.join(year_path, file)

            with open(file_path, "r") as f:
                content = json.load(f)

                if "data" in content and content["data"] and "transactionData" in content["data"]:
                    
                    for item in content["data"]["transactionData"]:
                        data.append({
                            "state": state,
                            "year": int(year),
                            "type": item["name"],
                            "count": item["paymentInstruments"][0]["count"],
                            "amount": item["paymentInstruments"][0]["amount"]
                        })

# Convert to DataFrame
df = pd.DataFrame(data)

# Create processed folder if not exists
os.makedirs("data/processed", exist_ok=True)

# Save CSV
output_path = "data/processed/aggregated_transaction.csv"
df.to_csv(output_path, index=False)

print("✅ Extraction complete")
print("Rows:", len(df))
print("Saved at:", output_path)