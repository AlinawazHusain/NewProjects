import pandas as pd
from datetime import datetime
import os
import config
import MailSender

# Dictionary to maintain aggregated data and track consecutive high temperatures
aggregated_data = {}
consecutive_high_temp = {}

def write_city_data(city_name, city_data):
    """Writes city data to an Excel file, updating metrics in the same sheet."""
    
    date_time = city_data['date_time']
    date_str = date_time.date().strftime('%Y-%m-%d')  # Extract date for sheet name

    if not os.path.exists(config.EXCEL_FILE_PATH):
        os.mkdir(config.EXCEL_FILE_PATH)

    # Define the Excel file name
    excel_file = f"{config.EXCEL_FILE_PATH}{city_name}.xlsx"

    # Prepare the new data to be written
    new_data = {
        "Main": [city_data['main']],
        'Temperature': [city_data['temperature']],
        'Feels Like': [city_data['feels_like']],
        'Time': [date_time.strftime('%H:%M:%S')]
    }

    # Initialize or update the aggregated data for the city
    if city_name not in aggregated_data:
        aggregated_data[city_name] = {
            'Temperatures': [],
            'Weather Conditions': []
        }
        consecutive_high_temp[city_name] = []

    # Append current data
    aggregated_data[city_name]['Temperatures'].append(city_data['temperature'])
    aggregated_data[city_name]['Weather Conditions'].append(city_data['main'])

    # Check for consecutive high temperatures
    if city_data['temperature'] > 35:
        consecutive_high_temp[city_name].append(date_str)
    else:
        consecutive_high_temp[city_name] = []  # Reset if the condition is not met

    if len(consecutive_high_temp[city_name]) >= 2:
        MailSender.sendMail(city_name)  # Print help if condition is met

    # Calculate metrics
    avg_temp = sum(aggregated_data[city_name]['Temperatures']) / len(aggregated_data[city_name]['Temperatures'])
    max_temp = max(aggregated_data[city_name]['Temperatures'])
    min_temp = min(aggregated_data[city_name]['Temperatures'])
    dominant_condition = max(set(aggregated_data[city_name]['Weather Conditions']),
                              key=aggregated_data[city_name]['Weather Conditions'].count)

    # Prepare DataFrame
    df = pd.DataFrame(new_data)

    # Write to Excel
    if os.path.exists(excel_file):
        with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            if date_str in writer.book.sheetnames:
                # Read existing data to update metrics
                existing_df = pd.read_excel(writer, sheet_name=date_str)

                # Add new data row
                updated_df = pd.concat([existing_df, df], ignore_index=True)

                # Update or add metric columns
                updated_df['Average Temperature'] = avg_temp
                updated_df['Maximum Temperature'] = max_temp
                updated_df['Minimum Temperature'] = min_temp
                updated_df['Dominant Weather Condition'] = dominant_condition

                updated_df.to_excel(writer, sheet_name=date_str, index=False)
            else:
                # Create a new sheet for the new date
                df['Average Temperature'] = avg_temp
                df['Maximum Temperature'] = max_temp
                df['Minimum Temperature'] = min_temp
                df['Dominant Weather Condition'] = dominant_condition
                df.to_excel(writer, sheet_name=date_str, index=False)
    else:
        # Create a new Excel file if it does not exist
        df['Average Temperature'] = avg_temp
        df['Maximum Temperature'] = max_temp
        df['Minimum Temperature'] = min_temp
        df['Dominant Weather Condition'] = dominant_condition
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=date_str, index=False)

    print(f"Data written for {city_name} in sheet '{date_str}'.")
