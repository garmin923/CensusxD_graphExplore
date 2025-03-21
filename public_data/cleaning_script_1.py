# This script is used to map the variables and questions from the Census Bureau data to a more user-friendly format. It creates a dictionary for variable mapping and another for question mapping. The variable mapping dictionary contains keys that represent the variable names and values that are lists of possible values or categories for those variables. The question mapping dictionary contains keys that represent the variable names and values that are dictionaries with keys representing the type of question (e.g., 'person') and values representing the corresponding index or identifier.
# Packages
import json
import csv
import pandas as pd
import string

# Import the data
# Define file path
file_path = "01_raw/acs2023_1yr_variables_LABEL_CONCEPT_Btables.json"

# Load the JSON data from file
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Data Mapping
variable_map = {
    'Age': ['16 to 19 years', '20 to 24 years', '25 to 44 years', '45 to 54 years', '55 to 59 years', '60 to 64 years', '65 years and over', '1 to 4 years', '5 to 17 years', '18 and 19 years ', '20 to 24 years', '25 to 29 years', '30 to 34 years', '35 to 39 years', '40 to 44 years', '45 to 49 years', '50 to 54 years', '55 to 59 years', '60 to 64 years', '65 to 69 years', '70 to 74 years', '75 years and over', '35 to 44 years', '45 to 54 years', 'Age', '18 to 24 years', '25 to 34 years', '55 to 64 years', '65 to 74 years', '75 to 84 years', '85 years and over', 'under 15 years', '15 to 17 years', 'under 19 years', 'Age'], 
    'Sex': ['Sex', 'male', 'female'],
    'Race': ['American Indian', 'Alaskan Native', 'Asian', 'Black or African American', 'Native Hawaiian and Other Pacific Islander', 'White', 'Black Alone', 'Alaska Native', 'Some Other Race', 'Two or More Races'],
    'Hispanic or Latino Origin': ['Hispanic or Latino Origin', "(Hispanic or Latino"],
    'Ancestry': ['Ancestry'],
    'Citizenship Status': ["US citizen born ", "US citizen born abroad of American parents", "US citizen born in Puerto Rico", "US citizen born in Puerto Rico or US Island Areas", "US citizen born in US or US Island Areas", "US citizen by naturalization", "Naturalized US citizen", "Not a US citizen", 'Citizenship Status', 'Year of naturalization'],
    'Year of Entry': ['Year of Entry'],
    'Foreign Born Place of Birth': ['Place of Birth', 'World Region of Birth', 'Nativity', 'foreign born', 'native'],
    'Migration/Residence 1 Year Ago': ['living in area 1 year ago', 'Geographical Mobility in the Past Year'],
    'Commuting/Journey to Work': ['car', 'truck', 'van', 'car, truck, or van', 'bus', 'subway', 'elevated rail', 'long distance train', 'commuter rail', 'light rail', 'streetcar', 'trolley', 'ferryboat', 'taxi', 'ride-hailing service', 'motorcycle', 'bicycle', 'walked', 'worked at home', 'other method', 'travel time to work', 'time of departure to go to work', 'Time arriving at work', "commuting/journey to work", "means of transportation", "public transport", "walked"],
    'Relationship to Householder': ['Relationship to Householder', 'Living Arrangement', 'Grandparent householder', 'Cohabiting Couple Households', 'Coupled Households by Type', 'Nonfamily Households', 'Households by Presence of Nonrelatives', 'Multigenerational Households', 'Unrelated Individuals', 'Families'],
    'Grandparents as Caregivers': ['own grandchildren'],
    'Household Type': ['Household Type', 'Family Type', 'Subfamily Type'],
    'Marital Status and History': ['Marital Status', 'First Marriage', 'Divorced in the Past 12 Months' 'Married in the Past 12 Months', 'Widowed in the Past 12 Months', 'times married', 'year last married'],
    'Fertility': ['Birth in the Past 12 Months', 'fertility'],
    'School Enrollment': ['School Enrollment'],
    'Educational Attainment': ['grade 1 to grade 4', 'grade 5 to grade 8', 'grade 9 to grade 12', 'Enrolled in kindergarten', 'Enrolled in school', 'Enrolled in nursery school', 'undergraduate years', 'graduate or professional school', 'not enrolled in school', 'no diploma', 'Less than 9th grade', '9th to 12th grade, no diploma', 'high school graduate', 'some college, no degree', "associate's degree", "bachelor's degree", 'graduate or professional degree', 'no schooling completed', 'nursery to 4th grade', '5th and 6th grade', '7th and 8th grade', '9th grade', '10th grade', '11th grade', '12th grade', 'high school graduate', 'some college',  "associate's degree", "bachelor's degree", "master's degree", 'professional school degree', "doctorate degree", 'Regular high school diploma', 'GED or alternative credential', 'Educational Attainment'],
    'Field of Degree': ["Detailed Field of Bachelor's Degree", "Fields of Bachelor's Degrees", 'first major', 'Field of degree'],
    'Language Spoken at Home': ['Language and Ability to Speak English', 'Language Spoken at Home', 'Detailed Household Language'],
    'Poverty': ['Poverty'],
    'Disability': ['Hearing Difficulty', 'Vision Difficulty', 'Cognitive Difficulty', 'Ambulatory Difficulty', 'Self-Care Difficulty', 'Independent Living Difficulty', 'Number of Disabilities', 'Disability'],
    'Income': ['Income', 'Earnings in the Past 12 Months', 'Aggregate Earnings', 'Median Earnings', "median income", "per capita income", "household income"],
    'Veteran Status': ['Veteran Status', 'veteran', 'nonveteran'],
    'Food Stamps/SNAP Beneft': ['Food Stamps/SNAP', 'SNAP', "food stamps"],
    'Employment Status': ['Employment Status', 'Unemployed', 'Not in Labor Force', 'Civilian Labor Force', 'In labor force', 'Employed', 'Work Status'],
    'Work Status Last Year': ['Work Experience', 'Work Status', 'Usual Hours Worked', 'Weeks Worked'],
    'Industry': ['Industry'],
    'Occupation': ['Occupation'],
    'Class of Worker': ['Class of Worker'],
    'Housing Characteristics': ['Vacancy Status', 'Vacancy Duration', 'Plumbing', 'Kitchen', 'Telephone Service', 'Year Structure Built', 'year built','Units in Structure', 'Structure Type', 'Bedrooms', 'Rooms'],
    'Health Insurance': ['Health Insurance', 'Medicare Coverage', 'Medicaid/Means-Tested Public Coverage', 'TRICARE/Military Health Coverage', 'VA Health Care', 'insured', 'uninsured'],
    'Computer and Internet Use': ['Computers', 'Computer', 'internet'],
    'Citizen Voting Age Population': ['Citizen, Voting-Age Population'],
    'Quality Measures': ['unweighted', 'coverage', 'response and nonresponse rates', 'overall person characteristic'] ,
    'Allocation': ['Allocation'], 
    'Computer and Internet Use': ['Computers in Household', 'Internet Subscription', 'Presence of a Computer', 'Computer Ownership', 'Internet Subscription', 'Internet Access', 'Computer Type', "computer and internet use"], 
    'Home Heating Fuel': ['House Heating Fuel', "fuel oil", "natural gas", "electricity", "wood", "coal", "other fuel"], 
    'Housing Costs for Owners': ['Homeowners Insurance Costs', 'Fuel Costs', 'Electricity Costs', 'Gas Costs', 'Water and Sewer Costs', 'Other Fuel Costs', 'Monthly Owner Costs', 'Real Estate Taxes', 'Mortgage Status'], 
    'Rent': ['Rent'], 
    'Home Ownership, Home Value': ['Mortgage Status', 'Housing Costs', 'Median Value', 'Price Asked', 'home value'], 
    'Vehicles Available': ['Private Vehicle', 'Vehicles Available'], 
    'Year Moved In': ['Year Householder Moved Into Unit', 'Tenure', 'year moved in'],
    'Group Quarters': ['Group Quarters'],
    'Puerto Rico': ['Puerto Rico']
}

# Mapping Variables to Tables
table_data = data
table_variable_matches = {}
matching_keys = set()
unmatched_tables = []

for variable, details in table_data.items():
    table_id = variable.split("_")[0]
    concept = details["concept"].lower()
    label = details["label"].lower()

    for var, keywords in variable_map.items():
        if any(k.lower().strip() in concept or k.lower().strip() in label for k in keywords):
            matching_keys.add(var)

    if matching_keys:
        table_variable_matches[table_id] = list(matching_keys)
    else:
        unmatched_tables.append(table_id)

# Export
# Define output file path
json_export_file_path = "02_review/table_variable_matches.json"

# Save the formatted data to a new JSON file
with open(json_export_file_path, "w", encoding="utf-8") as outfile:
    json.dump(table_variable_matches, outfile, indent=4)
