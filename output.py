from address_process import process_and_match_addresses
from name_process import process_excel

process_and_match_addresses("input.xlsx", "output.xlsx")
process_excel("output.xlsx","output.xlsx","documents")