# A Workstudy Project with the Census xD Group
## Attempting to make the Census Data more accessible and understandable
## Gareth Minson-Efimov
### 2025

# To Implement
## Packages
Install gpt4all, streamlit

## Load Data
Have "acs2023_1yr_variables_LABEL_CONCEPT_Btables.json" in the 01_raw folder<br>
Have "acs2023_1yr_c_tables_with_vars_LLM_cleaned.json" in the 03_processed folder<br>

## Scripts
1. Run the "cleaning_script_1.py" file which takes the raw B Table information as input
2. Run the "Merging_B_C_tables.py" file which combines the processed B Table and the pre-cleaned C Table
3. Run the "llm_dev_03.py" file as: streamlit run  < insert path > llm_dev_03.py [ARGUMENTS]