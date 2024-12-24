from address_process import process_and_match_addresses
from name_process import process_excel
import pandas as pd
from models_our import process_folder
from difflib import SequenceMatcher

def uid_matching(filename):
    df = pd.read_excel(filename)

    # Step 4: Process the folder to extract UIDs
    result = process_folder("documents")

    # Step 5: Select relevant columns from the DataFrame
    selected = df[['SrNo', 'UID', 'UID Extracted From OVD', 'UID Match Score']]

    # Step 6: Extract UIDs from the folder processing results
    extracted_uids = {}
    for key, value in result.items():
        if value['status'] == 'success' and 'uid' in value['data']:
            extracted_uids[key] = value['data']['uid']
        if value['status'] == 'failure':
            extracted_uids[key] = ""

    # Remove duplicate words in extracted UIDs
    for key in extracted_uids:
        extracted_uids[key] = ' '.join(dict.fromkeys(extracted_uids[key].split()))

    # Remove spaces in extracted UIDs
    for image in extracted_uids:
        extracted_uids[image] = extracted_uids[image].replace(" ", "")

    # Step 7: Prepare a dictionary for SrNo -> UID mapping from the DataFrame
    excel_data = {}
    for index, row in selected.iterrows():
        excel_data[row['SrNo']] = str(row['UID'])

    # Step 8: Update 'UID Extracted From OVD' and 'UID Match Score' columns
    for index, row in df.iterrows():
        sr_no = row['SrNo']
        if sr_no in extracted_uids:
            extracted_uid = extracted_uids[sr_no]
            original_uid = str(row['UID'])

            # Update 'UID Extracted From OVD'
            df.at[index, 'UID Extracted From OVD'] = extracted_uid

            # Calculate and update 'UID Match Score'
            if extracted_uid and original_uid:
                match_score = SequenceMatcher(None, extracted_uid, original_uid).ratio() * 100
            else:
                match_score = 0
            df.at[index, 'UID Match Score'] = match_score

    # Step 9: Save the updated DataFrame back to the Excel file
    df.to_excel('output.xlsx', index=False)

    print("Output.xlsx updated successfully.")
