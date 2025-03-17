# Combining B and C Tables
import json
import os

file_path_b = "02_review/table_variable_matches.json"
file_path_c = "03_processed/acs2023_1yr_c_tables_with_vars_LLM_cleaned.json"

# Load the JSON data from file
with open(file_path_b, "r", encoding="utf-8") as file:
    btables = json.load(file)

with open(file_path_c, "r", encoding="utf-8") as file:
    ctables = json.load(file)

# Extract table IDs and variables from the CTable JSON data
ctable_ids = []
ctable_vars = []
for table in range(len(ctables['tables'])):
    ctable_ids.append(ctables['tables'][table]['table_id'])
    ctable_vars.append(ctables['tables'][table]['variables'])

ctables = {k: v for k, v in zip(ctable_ids, ctable_vars)}

# Concatenate the two dictionaries
b_c_tables = btables
b_c_tables.update(ctables)

# Save the formatted data to a new JSON file
with open("03_processed/b_c_tables.json", "w", encoding="utf-8") as outfile:
    json.dump(b_c_tables, outfile, indent=4)

with open("03_processed/b_c_tables.txt", "w", encoding="utf-8") as outfile:
    json.dump(b_c_tables, outfile, indent=4)