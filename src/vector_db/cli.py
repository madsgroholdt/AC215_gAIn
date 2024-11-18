import os
import argparse
import pandas as pd
import glob
import hashlib
import chromadb
from google.cloud import storage
from models import rag_agent_tools
# Vertex AI
import vertexai
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from vertexai.generative_models import (
    GenerativeModel,
    GenerationConfig,
    Content,
    Part,
    ToolConfig,
)

# Langchain
from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain_experimental.text_splitter import SemanticChunker
from semantic_splitter import SemanticChunker

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
BUCKET_NAME = "gain-bucket"  # Define your GCS bucket here
BUCKET_INPUT_FOLDER = "processed_user_data"  # Placeholder for the bucket folder
OUTPUT_FOLDER = "output"  # Placeholder for the bucket folder
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
GENERATIVE_MODEL = "gemini-1.5-flash-001"
# INPUT_FOLDER = "input"
# OUTPUT_FOLDER = "output"
print("CHROMADB_HOST:", os.environ.get("CHROMADB_HOST"))
print("CHROMADB_PORT:", os.environ.get("CHROMADB_PORT"))
CHROMADB_HOST = os.environ["CHROMADB_HOST"]
CHROMADB_PORT = os.environ["CHROMADB_PORT"]
vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)
# https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/text-embeddings-api#python
embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)
# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 8192,  # Maximum number of tokens for output
    "temperature": 0.2,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}
# Initialize the GenerativeModel with specific system instructions
SYSTEM_INSTRUCTION = (
    "You are an AI assistant with expert knowledge about everything "
    "related to health and fitness. In your responses, you should "
    "leverage the information in the provided documents for anything "
    'related to questions about historical events, such as "what was '
    'my step count on date x". Ensure that you do not state claims as '
    "factual without being able to refer to the specific texts where "
    "you found said claims. If you are making assumptions or reasonings "
    "about health and fitness advice, ensure to state that this is only "
    'your "professional" opinion, and not necessarily advice that should '
    "be followed directly without consideration. Beyond the documents "
    "with historical information about the user's health and fitness "
    "data, state that you are giving qualitative advice based on your "
    "experiences/acquired knowledge, not advice directly based on "
    "documents you have access to.\n\n"
    "When answering a query:\n"
    "1. Carefully read all the text chunks provided and provide "
    "information about the historical activity data if the user is "
    "asking for it.\n"
    "2. Identify the most relevant information from these chunks to "
    "address the user's question if they are asking about their "
    "historical activities.\n"
    "3. Try to leverage the information from the provided chunks when "
    "giving the user advice. Use the information about their historical "
    "activity and health levels to provide context-aware responses to "
    "their questions.\n"
    "4. Always maintain a professional and knowledgeable tone, befitting "
    "a successful, well-educated Personal Trainer, Physiotherapist, or "
    "other relevant health professional that fits the user's needs.\n\n"
    "Lastly, a few important points to remember:\n"
    "- You are an expert in health and fitness and should leverage all "
    "the knowledge you have, but should try your best to leverage the "
    "information provided in the chunks of text to personalize the "
    "responses to the user's historical levels of health and fitness.\n"
    "- If asked about topics unrelated to health and fitness, politely "
    "redirect the conversation back to subjects related to health and "
    "fitness.\n"
    "- Be concise in your responses while ensuring you cover all the "
    "relevant elements the user is asking about.\n\n"
    "Your goal is to provide accurate, helpful information about health "
    "and fitness to the user, by combining context from the provided "
    "chunks with your abundance of knowledge of the field."
)
generative_model = GenerativeModel(
    GENERATIVE_MODEL, system_instruction=[SYSTEM_INSTRUCTION]
)

document_mappings = {
    "Tomas Arevalo-2": {
        "type": "Activity Log",
        "source": "Apple Health",
        "user": "Tomas Arevalo",
    }
}


def download_from_gcs(folder_name, local_path):
    """Downloads files from the GCS bucket to a local directory."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)

    blobs = bucket.list_blobs(prefix=folder_name)
    for blob in blobs:
        if not blob.name.endswith("/"):  # Skip directory blobs
            destination = os.path.join(local_path, os.path.basename(blob.name))
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            blob.download_to_filename(destination)
            print(f"Downloaded {blob.name} to {destination}")


def generate_query_embedding(query):
    query_embedding_inputs = [
        TextEmbeddingInput(task_type="RETRIEVAL_DOCUMENT", text=query)
    ]
    kwargs = (
        dict(output_dimensionality=EMBEDDING_DIMENSION) if EMBEDDING_DIMENSION else {}
    )
    embeddings = embedding_model.get_embeddings(
        query_embedding_inputs, **kwargs)
    return embeddings[0].values


def generate_text_embeddings(chunks, dimensionality: int = 256,
                             batch_size=250):
    # Max batch size is 250 for Vertex AI
    all_embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i: i + batch_size]
        inputs = [TextEmbeddingInput(text, "RETRIEVAL_DOCUMENT")
                  for text in batch]
        kwargs = dict(
            output_dimensionality=dimensionality) if dimensionality else {}
        embeddings = embedding_model.get_embeddings(inputs, **kwargs)
        all_embeddings.extend([embedding.values for embedding in embeddings])

    return all_embeddings


def load_text_embeddings(df, collection, batch_size=500):
    # Generate ids
    df["id"] = df.index.astype(str)
    hashed_doc_names = df["doc_name"].apply(
        lambda x: hashlib.sha256(x.encode()).hexdigest()[:16]
    )
    df["id"] = hashed_doc_names + "-" + df["id"]

    metadata = {"doc_name": df["doc_name"].tolist()[0]}
    if metadata["doc_name"] in document_mappings:
        document_mapping = document_mappings[metadata["doc_name"]]
        metadata["type"] = document_mapping["type"]
        metadata["source"] = document_mapping["source"]
        metadata["user"] = document_mapping["user"]

    # Process data in batches
    total_inserted = 0
    for i in range(0, df.shape[0], batch_size):
        # Create a copy of the batch and reset the index
        batch = df.iloc[i: i + batch_size].copy().reset_index(drop=True)

        ids = batch["id"].tolist()
        documents = batch["chunk"].tolist()
        metadatas = [metadata for item in batch["doc_name"].tolist()]
        embeddings = batch["embedding"].tolist()

        collection.add(
            ids=ids, documents=documents, metadatas=metadatas, embeddings=embeddings
        )
        total_inserted += len(batch)
        print(f"Inserted {total_inserted} items...")

    print(
        f"Finished inserting {total_inserted} items into collection '{collection.name}'"
    )


def get_collection(method="recursive-split"):
    # Connect to chroma DB
    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    # Get a collection object from an existing collection, by name.
    # If it doesn't exist, create it.
    collection_name = f"{method}-collection"
    # Get the collection
    collection = client.get_collection(name=collection_name)

    return collection


def chunk(method="semantic-split"):
    print("chunk()")

    # Make dataset folders
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    download_from_gcs(BUCKET_INPUT_FOLDER, "local_input")

    # Get the list of text file
    # Replace with GCP bucket connection
    text_files = glob.glob(os.path.join("local_input", "*.txt"))
    print("Number of files to process:", len(text_files))

    # Process
    for text_file in text_files:
        print("Processing file:", text_file)
        filename = os.path.basename(text_file)
        doc_name = filename.split(".")[0]

        with open(text_file) as f:
            input_text = f.read()

        text_chunks = None

        if method == "recursive-split":
            chunk_size = 500
            # Init the splitter
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size)

            # Perform the splitting
            text_chunks = text_splitter.create_documents([input_text])
            text_chunks = [doc.page_content for doc in text_chunks]
            print("Number of chunks:", len(text_chunks))

        elif method == "semantic-split":
            # Init the splitter
            text_splitter = SemanticChunker(
                embedding_function=generate_text_embeddings)
            # Perform the splitting
            text_chunks = text_splitter.create_documents([input_text])

            text_chunks = [doc.page_content for doc in text_chunks]
            print("Number of chunks:", len(text_chunks))

        if text_chunks is not None:
            # Save the chunks
            data_df = pd.DataFrame(text_chunks, columns=["chunk"])
            data_df["doc_name"] = doc_name
            print("Shape:", data_df.shape)
            print(data_df.head())

            jsonl_filename = os.path.join(
                OUTPUT_FOLDER, f"chunks-{method}-{doc_name}.jsonl"
            )
            with open(jsonl_filename, "w") as json_file:
                json_file.write(data_df.to_json(orient="records", lines=True))


def embed(method="recursive-split"):
    print("embed()")

    # Get the list of chunk files
    jsonl_files = glob.glob(os.path.join(
        OUTPUT_FOLDER, f"chunks-{method}-*.jsonl"))
    print("Number of files to process:", len(jsonl_files))

    # Process
    for jsonl_file in jsonl_files:
        print("Processing file:", jsonl_file)

        data_df = pd.read_json(jsonl_file, lines=True)
        print("Shape:", data_df.shape)
        print(data_df.head())

        chunks = data_df["chunk"].values
        if method == "semantic-split":
            embeddings = generate_text_embeddings(
                chunks, EMBEDDING_DIMENSION, batch_size=15
            )
        else:
            embeddings = generate_text_embeddings(
                chunks, EMBEDDING_DIMENSION, batch_size=100
            )
        data_df["embedding"] = embeddings

        # Save
        print("Shape:", data_df.shape)
        print(data_df.head())

        jsonl_filename = jsonl_file.replace("chunks-", "embeddings-")
        with open(jsonl_filename, "w") as json_file:
            json_file.write(data_df.to_json(orient="records", lines=True))


def load(method="recursive-split"):
    print("load()")

    client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
    collection_name = f"{method}-collection"
    print("Creating collection:", collection_name)

    try:
        # Clear out any existing items in the collection
        client.delete_collection(name=collection_name)
        print(f"Deleted existing collection '{collection_name}'")
    except Exception:
        print(f"Collection '{collection_name}' did not exist. Creating new.")

    collection = client.create_collection(
        name=collection_name, metadata={"hnsw:space": "cosine"}
    )
    print(f"Created new empty collection '{collection_name}'")
    print("Collection:", collection)

    # Get the list of embedding files
    jsonl_files = glob.glob(os.path.join(
        OUTPUT_FOLDER, f"embeddings-{method}-*.jsonl"))
    print("Number of files to process:", len(jsonl_files))

    # Process
    for jsonl_file in jsonl_files:
        print("Processing file:", jsonl_file)

        data_df = pd.read_json(jsonl_file, lines=True)
        print("Shape:", data_df.shape)
        print(data_df.head())

        # Load data
        load_text_embeddings(data_df, collection)


def preprocess_files(method="recursive-split"):
    print("Chunking files...")
    chunk(method)
    print("Done chunking files.")

    print("Embedding files...")
    embed(method)
    print("Done embedding files.")

    print("Loading embeddings to vector db...")
    load(method)
    print("Done loading embeddings.")


def query(user, prompt, search_string=" ", method="recursive-split"):
    collection = get_collection(method)

    query_embedding = generate_query_embedding(prompt)

    # 3: Query based on embedding value + lexical search filter
    print(search_string)
    # search_string = "September 12th"
    # print(search_string)
    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": 10,
        "where": {"source": {"$ne": ""}},
        "where_document": {"$contains": search_string}
    }

    results = collection.query(**query_args)
    print("Query:", prompt)
    print("\n\nResults:", results)

    return results


def get_relevant_search_string(prompt):
    INPUT_PROMPT = (
        f"Analyze the below text, and return the most important text "
        f"string you believe is needed to get data that is the most "
        f"relevant for the sentence. Do not return anything else other "
        f"than that string. Do not return any other data format than a "
        f"string. If you do not believe there is any substring that is "
        f'particularly relevant, then answer me with "no relevant search '
        f'string", but only do this if you truly do not believe there is '
        f"any important substring in the text. Here is the text:\n{prompt}"
    )
    print("INPUT_PROMPT: ", INPUT_PROMPT)
    response = generative_model.generate_content(
        [INPUT_PROMPT],
        generation_config=generation_config,
        stream=False,
    )
    generated_text = response.text
    print("LLM Response:", generated_text)

    generated_text = generated_text.replace('"', "").strip()

    if generated_text == "no relevant search string":
        generated_text = " "

    return generated_text


def chat(user, prompt, method="recursive-split"):
    print("chat()")

    # search_string = get_relevant_search_string(prompt)

    results = query(user, prompt, method=method)

    print("\n\nResults:", results)

    print(len(results["documents"][0]))

    INPUT_PROMPT = f"""{prompt} {results['documents'][0]}"""

    print("INPUT_PROMPT: ", INPUT_PROMPT)
    response = generative_model.generate_content(
        [INPUT_PROMPT],  # Input prompt
        generation_config=generation_config,  # Configuration settings
        stream=False,  # Enable streaming for responses
    )
    generated_text = response.text
    print("LLM Response:", generated_text)


def get(user, method="recursive-split"):
    collection = get_collection(method)

    # Get documents with filters
    results = collection.get(where={"user": user}, limit=1)
    print("\n\nResults:", results)


def agent(user, prompt, method="recursive-split"):
    print("agent()")

    collection = get_collection(method)

    user_prompt_content = Content(
        role="user",
        parts=[
            Part.from_text(prompt),
        ],
    )

    # Step 1: Prompt LLM to find the tool(s) to execute to find
    # the relevant chunks in vector db
    print("user_prompt_content: ", user_prompt_content)
    response = generative_model.generate_content(
        user_prompt_content,
        generation_config=GenerationConfig(
            temperature=0),  # Configuration settings
        # Tools available to the model
        tools=[rag_agent_tools.fitness_expert_tool],
        tool_config=ToolConfig(
            function_calling_config=ToolConfig.FunctionCallingConfig(
                # ANY mode forces the model to predict only function calls
                mode=ToolConfig.FunctionCallingConfig.Mode.ANY,
            )
        ),
    )
    print("LLM Response:", response)

    # Step 2: Execute the function and send chunks back to LLM to answer
    # get the final response
    function_calls = response.candidates[0].function_calls
    print("Function calls:")
    print(function_calls)
    function_responses = rag_agent_tools.execute_function_calls(
        function_calls, user, collection, embed_func=generate_query_embedding
    )
    if len(function_responses) == 0:
        print("Function calls did not result in any responses...")
    else:
        # Call LLM with retrieved responses
        response = generative_model.generate_content(
            [
                user_prompt_content,  # User prompt
                response.candidates[0].content,  # Function call response
                Content(parts=function_responses),
            ],
            tools=[rag_agent_tools.fitness_expert_tool],
        )
        print("LLM Response:", response)


def main(args=None):
    print("CLI Arguments:", args)

    if args.chunk:
        chunk(method=args.chunk_type)

    if args.embed:
        embed(method=args.chunk_type)

    if args.load:
        load(method=args.chunk_type)

    if args.query:
        query(user=args.user, prompt=args.prompt, method=args.chunk_type)

    if args.chat:
        chat(user=args.user, prompt=args.prompt, method=args.chunk_type)

    if args.get:
        get(user=args.user, method=args.chunk_type)

    if args.agent:
        agent(user=args.user, prompt=args.prompt, method=args.chunk_type)
    if args.preprocess:
        preprocess_files(method=args.chunk_type)


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal '--help', it will provide the description
    parser = argparse.ArgumentParser(description="CLI")

    parser.add_argument(
        "--chunk",
        action="store_true",
        help="Chunk text",
    )
    parser.add_argument(
        "--embed",
        action="store_true",
        help="Generate embeddings",
    )
    parser.add_argument(
        "--load",
        action="store_true",
        help="Load embeddings to vector db",
    )
    parser.add_argument(
        "--query",
        action="store_true",
        help="Query vector db",
    )
    parser.add_argument(
        "--chat",
        action="store_true",
        help="Chat with LLM",
    )
    parser.add_argument(
        "--get",
        action="store_true",
        help="Get documents from vector db",
    )
    parser.add_argument(
        "--agent",
        action="store_true",
        help="Chat with LLM Agent",
    )
    parser.add_argument(
        "--preprocess",
        action="store_true",
        help="Preprocess txt files by chunking and embedding the content",
    )
    parser.add_argument(
        "--chunk_type",
        default="semantic-split",
        help="recursive-split | semantic-split",
    )
    parser.add_argument("--user", default="",
                        help="Str with the name of username")
    parser.add_argument("--prompt", default="",
                        help="Text prompt to pass to RAG model")

    args = parser.parse_args()

    main(args)
