import re
from difflib import SequenceMatcher

def remove_stopwords(extracted_name):
    stop_words = [
        "dr",
        "mr.",
        "mrs.",
        "smt.",
        "ms.",
        "col.",
        "professor",
        "jt1",
        "jt",
        "prof.",
        "huf",
        "minor",
        "bhai",
    ]
    
    # Remove stop words properly, including periods
    for word in stop_words:
        extracted_name = extracted_name.lower().replace(word + " ", "")
        extracted_name = extracted_name.lower().replace(word, "")  # to handle no space after period

    return extracted_name


def remove_middle(extracted):
    name_split = extracted.split()
    if len(name_split) > 2:  # If there are more than two name parts
        # Remove middle name (keep first and last)
        extracted = " ".join([name_split[0], name_split[-1]])
    return extracted


def preprocess_name(name):
    name = remove_stopwords(name)
    name = remove_middle(name)
    return name.strip()


def exact_match(extracted, input_name):
    return extracted == input_name


def abbreviation_match(extracted, input_name):
    extracted_parts = extracted.split()
    input_parts = input_name.split()

    if len(input_parts) == 2 and len(extracted_parts) == 2:
        # Check if the second name part of the input is an abbreviation of the extracted name's second part
        if input_parts[0].lower() == extracted_parts[0].lower() and input_parts[1][0].lower() == extracted_parts[1][0].lower():
            return True
    return False


def ignore_middle_name_match(extracted, input_name):
    extracted_parts = extracted.split()
    input_parts = input_name.split()

    # Check if we have first and last name matching (ignore middle name)
    if len(extracted_parts) > 2 and len(input_parts) == 2:
        if extracted_parts[0].lower() == input_parts[0].lower() and extracted_parts[-1].lower() == input_parts[-1].lower():
            return True
    return False


def match_any_part(extracted, input_name):
    extracted_parts = extracted.split()
    input_parts = input_name.split()

    # If one name part matches the other name part
    if any(part in input_parts for part in extracted_parts) or any(part in extracted_parts for part in input_parts):
        return True
    return False


def circular_match(extracted, input_name):
    extracted_parts = extracted.split()
    input_parts = input_name.split()

    # If both names have the same parts, just in different order
    if set(extracted_parts) == set(input_parts):
        return True
    return False


def single_letter_abbreviation(extracted, input_name):
    extracted_parts = extracted.split()
    input_parts = input_name.split()

    # If the input has a single letter abbreviation for one part of the name
    if len(input_parts) == 2 and len(extracted_parts) == 2:
        if input_parts[0][0].lower() == extracted_parts[0][0].lower() and input_parts[1].lower() == extracted_parts[1].lower():
            return True
        elif input_parts[1][0].lower() == extracted_parts[1][0].lower() and input_parts[0].lower() == extracted_parts[0].lower():
            return True
    return False


def name_matching(extracted, input_name):
    # Preprocess both names
    extracted = preprocess_name(extracted)
    input_name = preprocess_name(input_name)

    # Case 1: Exact Match
    if exact_match(extracted, input_name):
        return True, 1.0

    # Case 2: Abbreviated Names
    if abbreviation_match(extracted, input_name):
        return True, 1.0

    # Case 3: Ignoring Middle Names
    if ignore_middle_name_match(extracted, input_name):
        return True, 1.0

    # Case 4: Matching Any Part of the Name
    if match_any_part(extracted, input_name):
        return True, 0.9

    # Case 5: Circular Matching
    if circular_match(extracted, input_name):
        return True, 1.0

    # Case 6: Single-Letter Abbreviation
    if single_letter_abbreviation(extracted, input_name):
        return True, 1.0

    # If none of the cases match
    return False, 0.0


# Function to provide final match result and score based on two strings
def overall_match_score(extracted, input_name):
    is_match, score = name_matching(extracted, input_name)
    return is_match, round(score, 2)


# # Example Usage:
# input_name = "Tripathi Devesh"  # User input
# extracted_name = "Devesh Tripathi"  # Extracted name from a database/document

# match_result, score = overall_match_score(extracted_name, input_name)
# print(f"Name Match result: {match_result}, Score: {score}")
