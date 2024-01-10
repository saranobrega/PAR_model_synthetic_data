import pandas as pd

def validate_data(data: pd.DataFrame):
    # Check if the required columns are present
    required_columns = ["DATE", "WT",  "WindSpeed"]
    missing_columns = [col for col in required_columns if col not in data.columns]
     # Delete the 'Unnamed: 0' column if it exists
    if 'Unnamed: 0' in data.columns:
        print("Deleting 'Unnamed: 0' column...")
        data = data.drop(columns=['Unnamed: 0'])
    
    if missing_columns:
        return f"Missing required columns: {', '.join(missing_columns)}"
    
    # Validate the data types of columns
    try:
        data["DATE"] = pd.to_datetime(data["DATE"], errors="coerce")
        data["WT"] = data["WT"].astype(int)
        data["WindSpeed"] = pd.to_numeric(data["WindSpeed"], errors="coerce")
    except Exception as e:
        return f"Error in data type conversion: {str(e)}"
    
    
    # Check for rows with missing or invalid values
    
    # Check if the data meets the format requirements
    valid_date_format = pd.to_datetime(data["DATE"], errors="coerce").notna()
    valid_date_format_ratio = valid_date_format.mean()
    
    if valid_date_format_ratio < 0.95:
        return f"Less than 95% of 'DATE' column values are in the valid format."
    
   # Check for negative values in ActivePower and WindSpeed columns
    negative_active_power = (data['ActivePower'] < 0)
    negative_wind_speed = (data['WindSpeed'] < 0)

    # Print a message if negative values are found
    if negative_active_power.any():
        print(f"Warning: There are {negative_active_power.sum()} rows with negative values in 'ActivePower' column. Deleting...")
        data = data[~negative_active_power]

    if negative_wind_speed.any():
        print(f"Warning: There are {negative_wind_speed.sum()} rows with negative values in 'WindSpeed' column. Deleting...")
        data = data[~negative_wind_speed]
    
    return data