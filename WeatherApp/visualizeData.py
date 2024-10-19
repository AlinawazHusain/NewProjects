import pandas as pd
import matplotlib.pyplot as plt

def load_excel_file(file_path):
    """Load an Excel file and return the sheet names."""
    xls = pd.ExcelFile(file_path)
    return xls.sheet_names

def visualize_data(sheet_name, file_path):
    """Visualize data from a specified sheet in the Excel file."""
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Display the first few rows of the DataFrame
    print(f"Data from sheet '{sheet_name}':")
    print(df.head())

    # Visualize the data (assuming it has 'Temperature' column)
    if 'Temperature' in df.columns:
        plt.figure(figsize=(10, 5))
        plt.plot(df['Time'], df['Temperature'], marker='o', linestyle='-')
        plt.title(f'Temperature over Time - {sheet_name}')
        plt.xlabel('Time')
        plt.ylabel('Temperature (°C)')
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        plt.show()
    else:
        print("No 'Temperature' column found in the selected sheet.")

if __name__ == "__main__":
    FILE_PATH = 'weather_data/Delhi.xlsx'  # Update with your Excel file path

    # Load the Excel file and get sheet names
    sheets = load_excel_file(FILE_PATH)
    print("Available sheets:")
    for i, sheet in enumerate(sheets):
        print(f"{i + 1}: {sheet}")

    # Ask user to select a sheet
    sheet_index = int(input("Select a sheet number to visualize: ")) - 1

    if 0 <= sheet_index < len(sheets):
        selected_sheet = sheets[sheet_index]
        visualize_data(selected_sheet, FILE_PATH)
    else:
        print("Invalid sheet number.")
