import pandas as pd


# dtype_dict = {
#     "business_name": str,
#     "category_desc": str,
#     "street": str,
#     "city": str,
#     "post_code": str,
#     "latitude": float,
#     "longitude": float,
#     "google_review_count": int,
#     "google_review_score": float,
#     "google_place_id": str,
#     "hygiene_score": int,
# }

df = pd.read_csv("./scripts/final_output.csv")

for idx, row in df.iterrows():
    if (
        row["hygiene_score"] == "Awaiting Inspection"
        or row["hygiene_score"] == "AwaitingPublication"
    ):
        df.at[idx, "hygiene_score"] = -1
        print("changed")

df["business_name"] = df["business_name"].astype(str)
df["category_desc"] = df["category_desc"].astype(str)
df["street"] = df["street"].astype(str)
df["city"] = df["city"].astype(str)
df["post_code"] = df["post_code"].astype(str)
df["latitude"] = df["latitude"].astype(float)
df["longitude"] = df["longitude"].astype(float)
df["google_review_count"] = df["google_review_count"].astype(int)
df["google_review_score"] = df["google_review_score"].astype(float)
df["google_place_id"] = df["google_place_id"].astype(str)
df["hygiene_score"] = df["hygiene_score"].astype(int)

df.to_csv("final_output2.csv", index=False)
