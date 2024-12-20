import pandas as pd
from models_our import process_folder
from address_matching import address_matching

def process_and_match_addresses(input_file, output_file):

# Step 1: Process the folder
    result = process_folder("documents")

    # Step 2: Read the Excel file
    df = pd.read_excel(input_file)

    # Step 3: Select relevant columns
    selected_columns = df[["SrNo", "House Flat Number", "Street Road Name", "Town", "City", "Floor Number", "Country", "PINCODE", "Premise Building Name", "Landmark", "State"]]

    # Step 4: Create input data dictionary
    excel_data = {}
    for index, row in selected_columns.iterrows():
        input_fields_1 = {
            'House Flat Number': str(row['House Flat Number']),
            'Town': str(row['Town']),
            'Street Road Name': str(row['Street Road Name']),
            'City': str(row['City']),
            'Floor Number': str(row['Floor Number']),
            'PINCODE': str(row['PINCODE']),
            'Premise Building Name': str(row['Premise Building Name']),
            'Landmark': str(row['Landmark']),
            'State': str(row['State'])
        }
        excel_data[row["SrNo"]] = input_fields_1

    # Step 5: Initialize lists to store results
    house_flat_number_matches = []
    street_road_name_matches = []
    city_matches = []
    floor_number_matches = []
    pincode_matches = []
    premise_building_name_matches = []
    landmark_matches = []
    state_matches = []
    address_extracted_from_ovd = []
    final_address_matches = []
    final_address_match_scores = []

    # Step 6: Iterate over excel_data and result to get match details
    for items in excel_data:
        for item2 in result:
            if items == item2:
                input_addr = excel_data[items]
                if result[item2].get('data'):
                    data = result[item2]['data']
                    extracted_addr = data.get("address'", None)
                    if extracted_addr:
                        field_scores_1, average_score_1, final_match_1 = address_matching(input_addr, extracted_addr)
                        house_flat_number_matches.append(field_scores_1['House Flat Number'])
                        street_road_name_matches.append(field_scores_1['Street Road Name'])
                        city_matches.append(field_scores_1['City'])
                        floor_number_matches.append(field_scores_1['Floor Number'])
                        pincode_matches.append(field_scores_1['PINCODE'])
                        premise_building_name_matches.append(field_scores_1['Premise Building Name'])
                        landmark_matches.append(field_scores_1['Landmark'])
                        state_matches.append(field_scores_1['State'])
                        address_extracted_from_ovd.append(extracted_addr)
                        final_address_matches.append(final_match_1)
                        final_address_match_scores.append(round(average_score_1, 2))
                    else:
                        house_flat_number_matches.append(None)
                        street_road_name_matches.append(None)
                        city_matches.append(None)
                        floor_number_matches.append(None)
                        pincode_matches.append(None)
                        premise_building_name_matches.append(None)
                        landmark_matches.append(None)
                        state_matches.append(None)
                        address_extracted_from_ovd.append(None)
                        final_address_matches.append(False)
                        final_address_match_scores.append(None)
                else:
                    house_flat_number_matches.append(None)
                    street_road_name_matches.append(None)
                    city_matches.append(None)
                    floor_number_matches.append(None)
                    pincode_matches.append(None)
                    premise_building_name_matches.append(None)
                    landmark_matches.append(None)
                    state_matches.append(None)
                    address_extracted_from_ovd.append(None)
                    final_address_matches.append(False)
                    final_address_match_scores.append(None)

    # Step 7: Update the original DataFrame with the new columns
    df['House Flat Number Match Score'] = house_flat_number_matches
    df['Street Road Name Match Score'] = street_road_name_matches
    df['City Match Score'] = city_matches
    df['Floor Number Match Score'] = floor_number_matches
    df['PINCODE Match Score'] = pincode_matches
    df['Premise Building Name Match Score'] = premise_building_name_matches
    df['Landmark Match Score'] = landmark_matches
    df['State Match Score'] = state_matches
    df['Address Extracted From OVD'] = address_extracted_from_ovd
    df['Final Address Match'] = final_address_matches
    df['Final Address Match Score'] = final_address_match_scores

    # Step 8: Save the updated DataFrame to output.xlsx
    df.to_excel(output_file, index=False)

    print("Output saved to output.xlsx")


# process_and_match_addresses("input.xlsx", "output.xlsx")