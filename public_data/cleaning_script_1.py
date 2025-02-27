import json
import networkx as nx
import os

with open("public_data/01_raw/acs2023_1yr_variables_LABEL_CONCEPT_Btables_part1 copy.txt", "r", encoding="utf-8") as infile:
    data = json.load(infile)

# Mapping of concepts to possible variables based on user-provided categories
concept_to_variable = {
    "Sex": ["sex"],
    "Age": ["age"],
    "Race": ["race", "white", "black or african american", "american indian and alaska native", 
    "asian", "native hawaiian and other pacific islander", "some other race",
    "two or more races", "hispanic or latino"],
    "Relationship to Householder": ["relationship to householder"],
    "Educational Attainment": ["education attainment", "undergraduate field of degree"],
    "Employment Status": ["employment status", "industry", "occupation", "class of worker"],
    "Income": ["income"],
    "Home Ownership": ["home ownership", "home value", "rent"],
    "Health Insurance Coverage": ["health insurance coverage"],
    "Residence 1 Year Ago": ["residence 1 year ago/migration"],
    "School Enrollment": ["school enrollment"],
    "Veteran Status": ["veteran status"],
    "Disability": ["disability"],
    "Commuting": ["commuting/journey to work"],
    "Computer and Internet Use": ["computer and internet use"],
    "Language Spoken at Home": ["language spoken at home"],
    "Marital Status": ["marital status/marital history"],
    "Fertility": ["fertility"],
    "Food Stamps Benefit": ["food stamps benefit"],
    "Grandparents as Caregivers": ["grandparents as caregivers"],
    "Housing": ["units in structure rooms bedrooms", "housing costs for owners"],
    "Vehicles Available": ["vehicles available"],
    "Work Status Last Year": ["work status last year"],
    "Year Built and Year Moved In": ["year built and year moved in"],
    "Plumbing Facilities": ["plumbing facilities"],
    "Kitchen Facilities": ["kitchen facilities"],
    "Telephone Service": ["telephone service"],
    "Place of Birth, Citizenship, Year of Entry": ["place of birth", "citizenship", "year of entry"],
    "Acreage and Agricultural Sales": ["acreage and agricultural sales"],
}

# Dictionary to store tables with mapped variables
table_variables = {}

# Process each variable in the dataset
for variable, details in data.items():
    table_id = variable.split("_")[0]  # Extract the table ID
    concept = details["concept"].lower()  # Normalize for matching

    # Initialize table entry if not present
    if table_id not in table_variables:
        table_variables[table_id] = {"variables": set()}

    # Map concept to variables using predefined dictionary
    for key, vars_list in concept_to_variable.items():
        if any(term in concept for term in vars_list):
            table_variables[table_id]["variables"].add(key)

# Convert sets to lists for JSON serialization
for table_id in table_variables:
    table_variables[table_id]["variables"] = list(table_variables[table_id]["variables"])

# Convert the dictionary into the requested JSON format
formatted_output = {"tables": []}

for table_id, details in table_variables.items():
    formatted_output["tables"].append({
        "table_id": table_id,
        "variables": details["variables"]
    })

# Define new output file path
formatted_output_file_path = "public_data/02_review/formatted_mapped_tables.json"

# Save the formatted data to a new JSON file
with open(formatted_output_file_path, "w", encoding="utf-8") as outfile:
    json.dump(formatted_output, outfile, indent=4)


# # Knowledge Graph
# # Create output directory if it doesn't exist
# output_dir = "public_data/02_review"
# os.makedirs(output_dir, exist_ok=True)

# # Define the path for the D3 JSON file
# d3_output_file_path = os.path.join(output_dir, "d3_knowledge_graph.json")

# # Prepare data for D3.js
# d3_data = {"nodes": [], "links": []}
# node_ids = set()

# # Add nodes and links to the D3 data structure
# for table_id, details in table_variables.items():
#     if table_id not in node_ids:
#         d3_data["nodes"].append({"id": table_id, "group": "Table"})
#         node_ids.add(table_id)
#     for variable in details["variables"]:
#         if variable not in node_ids:
#             d3_data["nodes"].append({"id": variable, "group": "Variable"})
#             node_ids.add(variable)
#         d3_data["links"].append({"source": table_id, "target": variable})

# # Save the D3 data to a JSON file
# with open(d3_output_file_path, "w", encoding="utf-8") as d3_outfile:
#     json.dump(d3_data, d3_outfile, indent=4)

# print(f"D3.js knowledge graph data saved to {d3_output_file_path}")

# import matplotlib.pyplot as plt

# # Create a directed graph
# G = nx.DiGraph()

# # Add nodes and edges based on the table_variables dictionary
# for table_id, details in table_variables.items():
#     G.add_node(table_id, label="Table")
#     for variable in details["variables"]:
#         G.add_node(variable, label="Variable")
#         G.add_edge(table_id, variable)

# # Draw the graph
# pos = nx.spring_layout(G)
# plt.figure(figsize=(12, 8))
# nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight="bold", arrows=True)
# plt.title("Knowledge Graph of Census Data")
# plt.show()

######
# Extract distinct labels for each table
# Define file path
file_path = "public_data/01_raw/acs2023_1yr_variables_LABEL_CONCEPT_Btables_part1 copy.txt"

# Load the JSON data from file
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Dictionary to store distinct labels for each table
table_labels = {}

# Process each variable in the dataset
for variable, details in data.items():
    table_id = variable.split("_")[0]  # Extract table ID
    label = details["label"]  # Extract label

    # Initialize table entry if not present
    if table_id not in table_labels:
        table_labels[table_id] = set()

    # Add label to the set to ensure uniqueness
    table_labels[table_id].add(label)

# Convert sets to lists for JSON serialization
formatted_labels = {"tables": []}
for table_id, labels in table_labels.items():
    formatted_labels["tables"].append({
        "table_id": table_id,
        "labels": list(labels)
    })

# Define output file path
labels_output_file_path = "public_data/02_review/table_labels.json"

# Save the extracted labels to a new JSON file
with open(labels_output_file_path, "w", encoding="utf-8") as outfile:
    json.dump(formatted_labels, outfile, indent=4)

all_labels = set()

# Collect labels from all tables
for details in data.values():
    all_labels.add(details["label"])

# Convert set to sorted list for consistency
distinct_labels = sorted(list(all_labels))

#####
# Extract distinct concepts for each table
# Define file path
file_path = "public_data/01_raw/acs2023_1yr_variables_LABEL_CONCEPT_Btables_part1 copy.txt"

# Load the JSON data from file
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Dictionary to store distinct labels for each table
table_labels = {}

# Process each variable in the dataset
for variable, details in data.items():
    table_id = variable.split("_")[0]  # Extract table ID
    label = details["concept"]  # Extract label

    # Initialize table entry if not present
    if table_id not in table_labels:
        table_labels[table_id] = set()

    # Add label to the set to ensure uniqueness
    table_labels[table_id].add(label)

# Convert sets to lists for JSON serialization
formatted_labels = {"tables": []}
for table_id, labels in table_labels.items():
    formatted_labels["tables"].append({
        "table_id": table_id,
        "concept": list(labels)
    })

# Define output file path
labels_output_file_path = "public_data/02_review/table_concepts.json"

# Save the extracted labels to a new JSON file
with open(labels_output_file_path, "w", encoding="utf-8") as outfile:
    json.dump(formatted_labels, outfile, indent=4)

all_concepts = set()

# Collect labels from all tables
for details in data.values():
    all_concepts.add(details["concept"])

# Convert set to sorted list for consistency
distinct_concepts = sorted(list(all_concepts))
print(distinct_concepts)