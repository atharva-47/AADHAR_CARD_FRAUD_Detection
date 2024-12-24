from address_process import process_and_match_addresses
from name_process import process_excel
from uid_match import uid_matching
from final_match import put_final_result
process_and_match_addresses("input.xlsx", "output.xlsx")
process_excel("output.xlsx","output.xlsx","documents")
uid_matching('output.xlsx')
put_final_result('output.xlsx')