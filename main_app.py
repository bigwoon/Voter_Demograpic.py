import sys
import subprocess
import logging
import argparse
import pandas as pd
from geopy.geocoders import Nominatim
from time import sleep
from tableauhyperapi import HyperProcess, Connection, Telemetry, TableDefinition, SqlType, Inserter

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to install missing packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Check and install `tableauhyperapi` if missing
try:
    from tableauhyperapi import HyperProcess, Connection, Telemetry, TableDefinition, SqlType, Inserter
except ModuleNotFoundError:
    print("The 'tableauhyperapi' library is not installed. Installing now...")
    install("tableauhyperapi")
    from tableauhyperapi import HyperProcess, Connection, Telemetry, TableDefinition, SqlType, Inserter

# Function to load voter data
def load_voter_data(file_path):
    logging.info(f"Loading voter data from {file_path}")
    return pd.read_csv(file_path)

# Function to load Census data
def load_census_data(file_path):
    logging.info(f"Loading Census data from {file_path}")
    return pd.read_csv(file_path)

# Function to geocode voter addresses
def geocode_addresses(voter_data):
    geolocator = Nominatim(user_agent="voter_geocoder")
    voter_data["Latitude"] = None
    voter_data["Longitude"] = None
    for idx, row in voter_data.iterrows():
        retries = 3
        while retries > 0:
            try:
                location = geolocator.geocode(f"{row['Address']}, {row['City']}, {row['State']}")
                if location:
                    voter_data.at[idx, "Latitude"] = location.latitude
                    voter_data.at[idx, "Longitude"] = location.longitude
                    logging.info(f"Geocoded address: {row['Address']}")
                break
            except Exception as e:
                retries -= 1
                logging.warning(f"Retrying geocoding for address {row['Address']}... ({3-retries}/3)")
                sleep(2)  # Delay between retries
                if retries == 0:
                    logging.error(f"Failed to geocode address {row['Address']}: {e}")
    return voter_data

# Function to merge voter data with census data
def merge_voter_census_data(voter_data, census_data):
    logging.info("Merging voter data with Census data")
    return pd.merge(voter_data, census_data, on="ZIP", how="left")

# Function to calculate racial percentages
def calculate_racial_percentages(data):
    logging.info("Calculating racial percentages")
    for col in ["White", "Black", "Hispanic", "Asian", "Other"]:
        data[f"{col}_Percentage"] = (data[col] / data["Total_Population"]) * 100
    return data

# Function to export data to CSV
def export_to_csv(data, output_path):
    logging.info(f"Exporting data to CSV at {output_path}")
    data.to_csv(output_path, index=False)
    logging.info("CSV export successful")

# Function to export data to Tableau Hyper
def export_to_hyper(data, output_path):
    logging.info(f"Exporting data to Tableau Hyper file at {output_path}")
    with HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA) as hyper:
        with Connection(endpoint=hyper.endpoint, database=output_path) as connection:
            table_definition = TableDefinition(
                table_name="VoterDemographics",
                columns=[
                    ("Voter_ID", SqlType.text()),
                    ("Name", SqlType.text()),
                    ("Address", SqlType.text()),
                    ("ZIP", SqlType.text()),
                    ("White_Percentage", SqlType.double()),
                    ("Black_Percentage", SqlType.double()),
                    ("Hispanic_Percentage", SqlType.double()),
                    ("Asian_Percentage", SqlType.double()),
                    ("Other_Percentage", SqlType.double()),
                ]
            )
            connection.catalog.create_table(table_definition)
            with Inserter(connection, table_definition) as inserter:
                for _, row in data.iterrows():
                    inserter.add_row([
                        row["Voter_ID"], row["Name"], row["Address"], row["ZIP"],
                        row["White_Percentage"], row["Black_Percentage"],
                        row["Hispanic_Percentage"], row["Asian_Percentage"],
                        row["Other_Percentage"]
                    ])
                inserter.execute()
            logging.info("Hyper export successful")

# Main script
def main():
    parser = argparse.ArgumentParser(description="Voter Demographics Analysis")
    parser.add_argument("--voter_data", required=True, help="Path to the voter data CSV file")
    parser.add_argument("--census_data", required=True, help="Path to the Census data CSV file")
    parser.add_argument("--csv_output", default="voter_demographics.csv", help="Output CSV file path")
    parser.add_argument("--hyper_output", default="voter_demographics.hyper", help="Output Hyper file path")
    args = parser.parse_args()

    # Load data
    voter_data = load_voter_data(args.voter_data)
    census_data = load_census_data(args.census_data)

    # Geocode voter addresses
    voter_data = geocode_addresses(voter_data)

    # Merge datasets
    merged_data = merge_voter_census_data(voter_data, census_data)

    # Calculate racial percentages
    final_data = calculate_racial_percentages(merged_data)

    # Export results
    export_to_csv(final_data, args.csv_output)
    export_to_hyper(final_data, args.hyper_output)

if __name__ == "__main__":
    main()
