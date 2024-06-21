import xml.etree.ElementTree as ET
import csv


def extract_and_convert_to_csv(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Initialize lists to store extracted data
    business_data = []

    # Extract data
    for establishment in root.findall(".//EstablishmentDetail"):
        business_type_id = establishment.find("BusinessTypeID").text
        if business_type_id in ("1", "7843", "7844"):
            business_name = (
                establishment.find("BusinessName").text
                if establishment.find("BusinessName") is not None
                else ""
            )
            post_code = (
                establishment.find("PostCode").text
                if establishment.find("PostCode") is not None
                else ""
            )
            rating_value = (
                establishment.find("RatingValue").text
                if establishment.find("RatingValue") is not None
                else ""
            )
            business_data.append([business_name, post_code, rating_value])

    # Specify the CSV file name
    csv_file = xml_file.replace(".xml", ".csv")

    # Write data to the CSV file
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow(["BusinessName", "PostCode", "RatingValue"])

        # Write the data
        for data in business_data:
            writer.writerow(data)

    print(f"Data extracted from {xml_file} and saved to {csv_file}")


# Example usage:
# extract_and_convert_to_csv("data21.xml")
