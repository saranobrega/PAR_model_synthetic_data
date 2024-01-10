import argparse
import pandas as pd
from tqdm import tqdm  # Assuming you want to use tqdm for a progress bar
from validate_data import validate_data
from preprocessing import split_dataframe_by_wt,delete_columns_and_nan , remove_outliers_from_df
from train import generate_synthetic_data



    

def main(input_file,size):
    print(f"Input file: {input_file}")
   
    try:
        # Read the file content
        df = pd.read_csv(input_file,sep=",")
        df=df[:100]
        # Validate the data first
        validated_data = validate_data(df)

        if "error" in validated_data:
            print(validated_data)
            return

        # Split the DataFrame by "WT" values
        split_data = split_dataframe_by_wt(validated_data)

        # Interpolate NaN values in each split DataFrame
        processed_data = delete_columns_and_nan(split_data)

        # Remove outliers from the interpolated data
        data_without_outliers = remove_outliers_from_df(processed_data)



        # Initialize the progress bar
        total_dataframes = len(data_without_outliers)
        progress_bar = tqdm(total=total_dataframes, desc="Generating Synthetic Data")
        print(f"Number of Turbines", len(data_without_outliers))




        synthetic_data_frames = {}
        for wt, df in data_without_outliers.items():
            print(f"Generating synthetic data for WT={wt}")
            synthetic_data_dict = generate_synthetic_data({wt: df},size)
            synthetic_data_frames[wt] = synthetic_data_dict
            print(f"Finished generating synthetic data for WT={wt}")
     # Update the progress bar
            progress_bar.update(1)
        progress_bar.close()

        list_of_dfs = []

        for turbine_data in synthetic_data_frames.values():
    # Extract DataFrames from the inner dictionary
            list_of_dfs.extend(turbine_data.values())

    # Concatenate the list of DataFrames
        final_synth_df = pd.concat(list_of_dfs, ignore_index=True)

        final_synth_df =final_synth_df.sort_values(by=['DATE', 'WT'])
        final_synth_df = final_synth_df.reset_index(drop=True)
        
        print(f"Final dataframe is completed")
        
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Process input data and generate synthetic data.")
    parser.add_argument("input_file", type=str, help="Path to the input data file (CSV format).")
    parser.add_argument("size", type=int, help="Size parameter for synthetic data generation.")

    args = parser.parse_args()

    # Call the main function with command-line arguments
    main(args.input_file, args.size)