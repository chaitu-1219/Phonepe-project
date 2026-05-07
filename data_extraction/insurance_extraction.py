import os
import json
import pandas as pd

path = "data/raw/data/aggregated/insurance/country/india/state/"

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
                            "count": item["paymentInstruments"][0]["count"],
                            "amount": item["paymentInstruments"][0]["amount"]
                        })

df = pd.DataFrame(data)

os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/insurance_data.csv", index=False)

print("✅ Insurance data extracted")
print("Rows:", len(df))