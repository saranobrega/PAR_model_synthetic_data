#  Wind Speed Turbine Synthetic Data Generation

## Project Overview

This code aims to create synthetic wind speed data for wind turbines. Wind speed is a critical parameter for optimizing the performance of wind turbines and ensuring efficient energy generation. The synthetic data generation process involves utilizing machine learning models, particularly the Parallel AutoRegressive (PAR) model, to simulate realistic wind speed patterns.

## Project Structure

### **app.py:**

**Description:**
The main script for processing input data and generating synthetic data. It utilizes modules for data validation, preprocessing, and training.

**Key Functions:**
- `main(input_file, size)`: The main entry point, reads input data, performs data processing steps, and generates synthetic data.

### **preprocessing.py:**

**Description:**
Module for preprocessing input data, including splitting by wind turbine, deleting columns and rows, and removing outliers.

**Key Functions:**
- `split_dataframe_by_wt(input_df)`: Groups data by the "WT" column.
- `delete_columns_and_nan(dataframes_dict)`: Deletes specified columns and removes rows with NaN in "WindSpeed."
- `remove_outliers_from_df(dict_dataframes, column_of_interest="WindSpeed", z_threshold=3)`: Cleans data by removing outliers.

### **train.py:**

**Description:**
Contains functions for training the LightGBM model, detecting index horizons for forecasting, creating lag features, and performing multistep forecasting.

**Key Functions:**
- `plot_scatter_plot(synth_data, original_data)`: Plots scatter plot of WindSpeed vs Index.
- `apply_PARModel(df, size)`: Applies PARModel for synthetic data generation.
- `generate_synthetic_data(data, size)`: Generates synthetic data for multiple wind turbines.

### **validate_data.py:**

**Description:**
Validates input data, checks for required columns, ensures correct data types, and handles negative values.

**Key Functions:**
- `validate_data(data)`: Validates data columns and types, removes unnecessary columns, and checks for negative values.

## Install Dependencies

```bash
pip install -r requirements.txt
```
## How to Run

```bash
python app.py <input_file_path> <size_parameter>
```
