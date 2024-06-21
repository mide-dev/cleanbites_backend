import math
import pandas as pd
from fuzzywuzzy import fuzz

restaurant_data = pd.read_csv("./cleaned_data/place_name_match.csv")
hygiene_data = pd.read_csv("./cleaned_data/place_hygiene.csv")


def find_best_match(restaurant_row):
    # Filter hygiene data by matching postcode
    matching_hygiene = hygiene_data[
        hygiene_data["PostCode"] == restaurant_row["post_code"]
    ]

    best_match = None
    highest_match = 0

    for _, hygiene_row in matching_hygiene.iterrows():
        similarity = fuzz.partial_ratio(
            restaurant_row["business_name"], hygiene_row["BusinessName"]
        )
        if similarity > highest_match:
            highest_match = similarity
            best_match = hygiene_row
    if highest_match < 51:
        best_match = None
    print(f"match for - {restaurant_row['business_name']}: {highest_match}")
    return best_match


for idx, row in restaurant_data.iterrows():
    try:
        if math.isnan(row["RatingValue"]):
            best_match = find_best_match(row)
            if best_match is not None:
                print("-----------------")
                print(f'prev_rate - {row["RatingValue"]}')
                row["RatingValue"] = best_match["RatingValue"]
                row["compare_name"] = best_match["BusinessName"]
                print(
                    f"rest_csv - {row['business_name']}, hyg_csv - {best_match['BusinessName']}"
                )
                print(f'final_rate - {row["RatingValue"]}')
                print("-----------------")
    except TypeError:
        continue

restaurant_data.to_csv("ayo_merge.csv", index=False)

