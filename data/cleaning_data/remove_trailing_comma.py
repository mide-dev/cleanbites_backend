import pandas as pd

# reading the csv file
df = pd.read_csv("ScrapedData_PlacesUncleaned.csv")

for i, row in enumerate(df["category_desc"]):
    df["category_desc"][i] = row.rstrip(", ")


df.to_csv("output.csv", index=False)
