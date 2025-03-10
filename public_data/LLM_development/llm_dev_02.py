# LLM Dev 02
from sentence_transformers import SentenceTransformer
from nomic import embed
import nomic
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
import uuid

# Key
#nk-f49D9IgInLd-NbLtYtY6mYjHSRpEG6TSMXlBf0cK91I
nomic.login("")

# Load the Nomic embedding model (e.g., nomic-embed-text-v1)
# embedding_model = embed.text(model="nomic-embed-text-v1")

# Initialize Chroma client
client = chromadb.PersistentClient(path="./chroma_db") #create a local database.
collection = client.get_or_create_collection(name="census_data")

def embed_and_store_data_chroma(text_chunks):
    """Embeds chunks using Nomic and stores them in ChromaDB."""
    embeddings = embed.text(model="nomic-embed-text-v1", texts=text_chunks) # encode multiple chunks at once.
    ids = [str(uuid.uuid4()) for _ in text_chunks]
    collection.add(
        embeddings=embeddings['embeddings'],
        documents=text_chunks,
        ids=ids
    )

def retrieve_relevant_chunks_chroma(query):
    """Retrieves relevant chunks from ChromaDB using Nomic embeddings."""
    query_embedding = embed.text(model="nomic-embed-text-v1", query = query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3  # Adjust as needed
    )
    return results["documents"][0]

def load_and_chunk_file(filepath, chunk_size=500):
    """Loads a text file and splits it into chunks."""
    with open(filepath, "r", encoding="utf-8") as file:
        text = file.read()
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks


# Load data and embed/store it
text_chunks = load_and_chunk_file("public_data/02_review/table_variable_matches.txt")
embed_and_store_data_chroma(text_chunks)

# Example query and retrieval
query = "What is the population of children under 5 in the United States?"
relevant_chunks = retrieve_relevant_chunks_chroma(query)

def retrieve_relevant_chunks(query):
    query_embedding = embed.text(model="nomic-embed-text-v1", prompt = query)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3  # Adjust as needed
    )
    return results["documents"][0]

def generate_response(user_input):
    relevant_chunks = retrieve_relevant_chunks(user_input)
    context = "\n".join(relevant_chunks)

    system_prompt = f"""
    You are an expert policy analyst working for the U.S. Census Bureau. Use the following context to answer the users question.
    Context:
    {context}

    **Instructions for Using the Data File:**

    1.  **Parsing:** Treat the text file above as a string representation of JSON data. You must be able to parse this string to extract the table information.
    2.  **Table Lookup:** When a user asks about a specific table (by ID or title), search the parsed data for the corresponding table entry.
    3.  **Variable Retrieval:** If a user requests the variables for a table, extract the "variables" list from the corresponding table entry.
    4.  **Table Type Identification:** Determine if a table is a B table or a C table using the "table_type" field.
    5.  **C Table Relationships:** For C tables, use the "derived_from" field to identify the corresponding B table.
    6.  **Response Generation:** When responding to user queries, include relevant information from the parsed data, such as:
        * Table ID
        * Table Title
        * Table Type (B or C)
        * List of Variables
        * Relationship to B table (for C tables)
    7.  **Data Limitations:** If the user asks about a table or variable that is not in the provided data file, respond that you do not have that information.
    8.  **B Table and C Table Definitions:** You must still utilize the base definitions of the B and C tables provided in the previous prompts to give context to the data.
    9.  **Clear Communication:** Present information in a clear and concise manner.
    10. **Offline Functionality:** Remember that you are operating in an offline environment. You must rely on the information provided in this prompt and data file.
    11. **Avoid Hallucinations:** When you do not have the data to answer a question, state that you do not have the data, do not make something up.

    **Example User Interactions:**

    * User: "What variables are in table B01001?"
    * User: "Tell me about table C17002."
    * User: "What is the difference between B01001 and C01001?"
    * User: "Is there data on income in the provided tables?"

    **Your goal is to accurately parse the provided text file and use the extracted data to answer user questions about ACS B and C tables.** 
    """

    prompt = f"{system_prompt}\n\nUser: {user_input}\nAssistant:"
    response = model.generate(prompt, max_tokens=500)
    return response

generate_response()