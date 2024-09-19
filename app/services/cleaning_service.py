import pandas as pd
import os

def clean_data(filepath, processed_folder):
    """Function to clean data."""
    #Read file to Dataframe
    df = pd.read_csv(filepath)
    
    #drop duplicates
    cleaned_df = df.drop_duplicates()

    
    #Fill NaN if values are missing
    cleaned_df = cleaned_df.fillna(cleaned_df.mean(numeric_only=True))
    
    #Add data to a new file and save it in the "processed" folder
    #new_file_name is "cleaned_{old_file_name}"
    cleaned_filepath = os.path.join(processed_folder, 'cleaned_' + os.path.basename(filepath))
    cleaned_df.to_csv(cleaned_filepath, index=False)
    
    #Return processed file path
    return cleaned_filepath
