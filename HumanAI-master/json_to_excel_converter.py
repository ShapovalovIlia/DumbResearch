import json
import pandas as pd


class JsonToExcelConverter:
    def __init__(self, json_file, output_excel_file):
        """
        Initialize the JsonToExcelConverter with file paths.
        :param json_file: Path to the JSON file.
        :param output_excel_file: Path where the Excel file will be saved.
        """
        self.json_file = json_file
        self.output_excel_file = output_excel_file

    def extract_data(self):
        """
        Extracts data from the JSON file and processes it into a list of dictionaries.
        :return: List of dictionaries containing extracted data.
        """
        with open(self.json_file, 'r') as file:
            data = json.load(file)

        # Extract relevant fields into a list of dictionaries
        records = []
        for entry in data:
            if entry.get('type') == 'user_message':  # Extract only user messages for demonstration
                message = entry.get('message', {}).get('content', "")
                emotions = entry.get('models', {}).get('prosody', {}).get('scores', {})
                received_at = entry.get('receivedAt', "")  # Extracting the timestamp
                record = {
                    "Timestamp": received_at,
                    "Message": message,
                    **emotions  # Unpack the emotion scores into columns
                }
                records.append(record)
        return records

    def save_to_excel(self):
        """
        Extracts the data and saves it as an Excel file.
        """
        records = self.extract_data()
        if records:  # Ensure there is data to save
            df = pd.DataFrame(records)
            df.to_excel(self.output_excel_file, index=False)
            print(f"Data successfully saved to {self.output_excel_file}")
        else:
            print("No data to save. Check the JSON file structure or filter criteria.")
