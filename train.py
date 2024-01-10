from contextlib import redirect_stdout
import os
import pandas as pd
from deepecho import PARModel
import warnings
from sklearn.exceptions import DataConversionWarning
import matplotlib.pyplot as plt
# Suppress FutureWarning from sdmetrics
warnings.simplefilter(action='ignore', category=FutureWarning)

# Suppress DataConversionWarning
warnings.filterwarnings(action='ignore', category=DataConversionWarning)

def plot_scatter_plot(synth_data, original_data):
    plt.figure(figsize=(12, 6))
    plt.scatter(synth_data.index, synth_data['WindSpeed'], color='orange', label="Synthetic Data (WS only)", s=5)
    plt.scatter(original_data.index, original_data['WindSpeed'], color='blue', label="Original Data", s=5)
    plt.title(f'Scatter Plot of Wind Speed vs Index')
    plt.xlabel('Index')
    plt.ylabel('Wind Speed')
    plt.legend()
    plt.show()

def apply_PARModel(df,  size):
   
    df = df.iloc[0:size]
    df['DATE'] = pd.to_datetime(df['DATE'], errors='coerce')
    date_column = df['DATE'].copy()

            # Entity column
    entity_columns = ['WT']  # Replace with your entity column
            
            # Data types
    data_types = {'WindSpeed': "continuous"}
            
            # Initialize PARModel
    model = PARModel(cuda=False)
            
            # Fit the model
            
            
    # Suppress PARModel's stdout
    with open(os.devnull, 'w') as fnull, redirect_stdout(fnull):
        # Fit the model
        model.fit(data=df, entity_columns=entity_columns, data_types=data_types, sequence_index="DATE")

    #model.fit(data=df, entity_columns=entity_columns, data_types=data_types, sequence_index="DATE")
            
            # Sample synthetic data
    synth_data = model.sample(num_entities=1)
    synth_data['DATE'] = date_column
            # Plot synthetic data and original data
    plot_scatter_plot(synth_data, df)
    
    return synth_data

def generate_synthetic_data(data, size):
    all_merged_dataframes = {}
    
    for key, df in data.items():
        
        final_df = apply_PARModel(df,size)
    
        all_merged_dataframes[key] = final_df
    
    return all_merged_dataframes