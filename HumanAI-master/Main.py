import os
from json_to_excel_converter import JsonToExcelConverter
from excel_graph_plotter import ExcelGraphPlotter  # Ensure to import this class

def find_json_files_and_convert(folder_path):
    """
    Finds all .json files in the specified folder, converts them to Excel files using JsonToExcelConverter,
    and then plots the emotions from the Excel files into graphs which are saved as a single image.
    """
    # Check if the given folder path exists
    if not os.path.exists(folder_path):
        print("The folder does not exist.")
        return

    # List all files in the directory
    files = os.listdir(folder_path)

    # Filter and convert files that end with .json
    json_files = [file for file in files if file.endswith('.json')]
    if json_files:
        print("JSON files found:")
        for file in json_files:
            json_file_path = os.path.join(folder_path, file)
            excel_file_path = os.path.join(folder_path, f"{os.path.splitext(file)[0]}.xlsx")
            converter = JsonToExcelConverter(json_file_path, excel_file_path)
            converter.save_to_excel()

        # After converting all JSON files to Excel, plot the graphs
        graph_plotter = ExcelGraphPlotter(folder_path)
        graph_plotter.plot_graphs()  # This will create and save the compiled graphs image
    else:
        print("No JSON files found in the directory.")

# Example usage:
folder_path = (
    'C:/Users/georg/Desktop/COMP 3647 - Human-AI Interaction Design/'
    'Assignment 2 Data/'
)
find_json_files_and_convert(folder_path)
