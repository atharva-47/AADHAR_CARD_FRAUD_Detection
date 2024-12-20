# address_matching.py

import re
from difflib import SequenceMatcher

ignore_terms = [
    "PO-", "PO", "Marg", "Peeth", "Veedhi", "Rd", "Lane", "NR", 
    "Beside", "Opposite", "OPP", "Behind", "near", "Enclave", 
    "Township", "Society", "Soc", "Towers", "Block", "S/o", "C/o", 
    "D/o", "W/o",
]

def remove_ignore_terms(address):
    """Remove stopwords and non-alphanumeric characters from the address."""
    if not isinstance(address, str):
        return ""
    # Remove ignore terms (case-insensitive)
    for term in ignore_terms:
        address = re.sub(r'\b' + re.escape(term) + r'\b', '', address, flags=re.IGNORECASE)
    # Remove non-alphanumeric characters and extra spaces
    address = re.sub(r'[^a-zA-Z0-9\s]', '', address)
    address = re.sub(r'\s+', ' ', address).strip()
    return address

def calculate_similarity(str1, str2):
    """Calculate the similarity score between two strings using SequenceMatcher."""
    return SequenceMatcher(None, str1, str2).ratio()

def address_matching(input_fields, extracted_address):
    # Clean both the input fields and the extracted address
    normalized_extracted_address = remove_ignore_terms(extracted_address)
    
    # Normalize input fields by cleaning each value
    normalized_input_fields = {field: remove_ignore_terms(value) for field, value in input_fields.items()}
    
    # Extract pincode
    input_pincode = input_fields.get('PINCODE', '').replace(' ', '')
    extracted_pincode = re.search(r'\d{6}', normalized_extracted_address)
    extracted_pincode = extracted_pincode.group(0) if extracted_pincode else ''
    
    # Pincode Matching
    pincode_score = 100 if input_pincode == extracted_pincode else 0
    
    # Split the extracted address into a list of words/parts
    extracted_parts = normalized_extracted_address.split()
    
    # Initialize a dictionary to store the scores for each field
    field_scores = {}
    
    # Compare each part of the extracted address to the corresponding input field
    for field, input_value in normalized_input_fields.items():
        field_score = 0
        # Check similarity for each part of the extracted address
        for part in extracted_parts:
            part_score = calculate_similarity(part, input_value)
            if part_score > field_score:
                field_score = part_score
        
        # Store the field score regardless of threshold
        field_scores[field] = round(field_score * 100, 2)
    
    # Calculate the overall match score (average of field scores above the threshold)
    included_field_scores = [score for score in field_scores.values() if score >= 70]
    if included_field_scores:
        total_score = sum(included_field_scores)
        average_score = total_score / len(included_field_scores)
    else:
        average_score = 0

    # Check final match: If pincode matches and overall score is above 70, it's a match
    final_match = average_score >= 70 and pincode_score == 100
    
    return field_scores, average_score, final_match
# Example Usage:

# #Test 1: Exact Match (input and extracted addresses match exactly)
# input_fields_1 = {
#     'House Flat Number': "12A B Block",
#     'Town': "Greenfield",
#     'Street Road Name': "Main St",
#     'City': "Greenfield City",
#     'Floor Number': "3rd",
#     'PINCODE': "560002",
#     'Premise Building Name': "Sunshine Towers",
#     'Landmark': "Near River",
#     'State': "Stateville"
# }

# extracted_address_1 = "12A B Block, Main St, Greenfield City, Sunshine Towers, Near River, 560002, Stateville"

# field_scores_1, average_score_1, final_match_1 = address_matching(input_fields_1, extracted_address_1)
# print("Test 1 - Exact Match")
# print("Field Scores (including non-matching fields):", field_scores_1)
# print(f"Overall Match Score: {round(average_score_1, 2)}")
# print(f"Final Match: {final_match_1}")
# print()
