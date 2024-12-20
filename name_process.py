import pandas as pd
from name_matching import overall_match_score
from models_our import process_folder
import os

# Function to read the Excel file and process the names
def process_excel(input_file, output_file, folder_path):
    # Read the input Excel file
    df = pd.read_excel(input_file)

    # Process the folder to get the extracted data
    extracted_data = process_folder(folder_path)

    # Iterate through the DataFrame rows
    for index, row in df.iterrows():
        sr_no = row['SrNo']
        input_name = row['Name']

        # Find the corresponding extracted data
        if sr_no in extracted_data:
            if extracted_data[sr_no]['status'] == 'success':
                extracted_names = extracted_data[sr_no]['data'].get('name', '')
                if extracted_names:
                    # Perform name matching
                    match_result, score = overall_match_score(extracted_names, input_name)
                    df.at[index, 'Name extracted from OVD'] = extracted_names
                    df.at[index, 'Name match percentage'] = score * 100
                    df.at[index, 'Name Match Score'] = score
                else:
                    df.at[index, 'Name extracted from OVD'] = ''
                    df.at[index, 'Name match percentage'] = 0
                    df.at[index, 'Name Match Score'] = 0
            else:
                df.at[index, 'Name extracted from OVD'] = ''
                df.at[index, 'Name match percentage'] = 0
                df.at[index, 'Name Match Score'] = 0
        else:
            df.at[index, 'Name extracted from OVD'] = ''
            df.at[index, 'Name match percentage'] = 0
            df.at[index, 'Name Match Score'] = 0

    # Save the updated DataFrame to the output Excel file
    df.to_excel(output_file, index=False)

# if __name__ == "__main__":
#     # Define the paths
#     input_file = "input.xlsx"
#     output_file = "output.xlsx"
#     folder_path = "documents/"

#     # Process the Excel file
#     process_excel(input_file, output_file, folder_path)

#     print(f"Processing complete. Results saved to {output_file}")