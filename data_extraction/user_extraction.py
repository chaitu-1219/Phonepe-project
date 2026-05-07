import os
import json
import pandas as pd

path = "data/raw/data/aggregated/user/country/india/state/"

data = []

for state in os.listdir(path):
    state_path = os.path.join(path, state)

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)

        for file in os.listdir(year_path):
            file_path = os.path.join(year_path, file)

            with open(file_path, "r") as f:
                content = json.load(f)

                # ✅ Safe check
                if (
                    "data" in content and
                    content["data"] is not None and
                    "usersByDevice" in content["data"] and
                    content["data"]["usersByDevice"] is not None
                ):
                    for item in content["data"]["usersByDevice"]:
                        data.append({
                            "state": state,
                            "year": int(year),
                            "brand": item["brand"],
                            "registeredUsers": item["count"],
                            "appOpens": item["percentage"]
                        })

df = pd.DataFrame(data)

os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/user_data.csv", index=False)

print("✅ User data extracted")
print("Rows:", len(df))