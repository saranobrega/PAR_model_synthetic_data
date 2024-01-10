import pandas as pd
from scipy import stats

def split_dataframe_by_wt(input_df):
    # Group the input DataFrame by the "WT" column
    grouped = input_df.groupby('WT')

    # Create a dictionary of DataFrames, one for each unique "WT" value
    dataframes_dict = {name: group for name, group in grouped}

    return dataframes_dict

def delete_columns_and_nan(dataframes_dict):
    imputed_dataframes_dict = {}

    for key, df in dataframes_dict.items():
        df = df.reset_index(drop=True)
        wt1_df_imputation2 = df.copy()

        
        # Code to delete "ActivePower", "Index", and "WF" columns if present
        columns_to_drop = ["ActivePower", "Index", "WF"]
        existing_columns_to_drop = [col for col in columns_to_drop if col in wt1_df_imputation2.columns]

        if existing_columns_to_drop:
            wt1_df_imputation2.drop(columns=existing_columns_to_drop, inplace=True)
            print(f"Deleted {existing_columns_to_drop} columns for key={key}")
        else:
            print(f"Columns to delete not found for key={key}")


        # Code to delete rows with NaN 
        rows_before_drop = len(wt1_df_imputation2)
        wt1_df_imputation2 = wt1_df_imputation2.dropna()
        rows_after_drop = len(wt1_df_imputation2)
        
        rows_deleted = rows_before_drop - rows_after_drop
        print(f"Deleted {rows_deleted} rows with NaN in 'WindSpeed' for key={key}")

        imputed_dataframes_dict[key] = wt1_df_imputation2

    return imputed_dataframes_dict

def remove_outliers_from_df(dict_dataframes, column_of_interest="WindSpeed", z_threshold=3):
    cleaned_dataframes = {}  # Dictionary to store cleaned DataFrames

    # Check if input is a single DataFrame
    if not isinstance(dict_dataframes, dict):
        # If it's a single DataFrame, create a dictionary with a default key
        interpolated_dataframes = {'default_key': interpolated_dataframes}

    for wt, df in dict_dataframes.items():
        # Extract the DataFrame with interpolated data
        if isinstance(df, pd.DataFrame):
            df = pd.DataFrame.from_dict(df)

            #Outlier removal
            original_rows = len(df)
    
            # Calculate the Z-scores for the WindSpeed column
            z_scores = stats.zscore(df['WindSpeed'])

            # Define a threshold for considering values as outliers (e.g., Z-score greater than 3)
            threshold = z_threshold

            # Identify and remove rows with WindSpeed outliers
            df_no_outliers = df[(z_scores < threshold) & (z_scores > -threshold)]

            # Calculate the number of rows removed
            removed_rows = original_rows - len(df_no_outliers)

            # Display the result
            print(f"Number of outliers removed: {removed_rows}")
            
            cleaned_dataframes[wt] = df_no_outliers

    return cleaned_dataframes
