import pandas as pd
import os
import chardet


def detect_csv_encoding(file_path):
    with open(file_path, "rb") as f:
        result = chardet.detect(f.read())
    return result["encoding"]


def merge_csv_files(directory_path, output_csv_file):
    csv_files = [f for f in os.listdir(directory_path) if f.endswith(".csv")]
    data_frames = []

    for file in csv_files:
        file_path = os.path.join(directory_path, file)
        encoding = detect_csv_encoding(file_path)

        try:
            df = pd.read_csv(file_path, encoding=encoding)
        except UnicodeDecodeError:
            print(
                f"Error reading file {file} with encoding {encoding}. Skipping this file."
            )

        data_frames.append(df)

    merged_data = pd.concat(data_frames, ignore_index=True)
    merged_data.to_csv(output_csv_file, index=False)


# call
merge_csv_files("./converted", "merged_data.csv")
