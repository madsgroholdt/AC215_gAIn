## RAG Container

### Run the RAG LLM Container
- Make sure you are inside the `models` folder and open a terminal at this location
- Make sure you have a `secrets` folder at the same level as the `models` folder that contains an `llm-service-account.json` file with the required permissions (Storage Admin and Vertex AI User)
- Run `sh docker-shell.sh` to run and enter the container

### Preprocess the RAG Documents
- In the CLI within the container, run `python model_rag.py --preprocess`
- Optionally, add `--chunk_type [recursive-split | char-split | semantic-split]` to use a specific chunking method
  - The default is recursive splitting (i.e., `--chunk_type recursive-split`)
  - This argument can be added in both of the commands below, as well
- This will access the user documents in the GCS bucket, chunk them, generate embeddings, and load them into the ChromaDB vector database.

### Query the Vector Database
- Run `python model_rag.py --query --prompt [USER PROMPT]`
  - For example, `python model_rag.py --query --prompt "How many flights of stairs did I climb in the second week of September?"`
- This will generate an embedding for the inputted query and perform similarity searches against the embedded chunks in the database.

### Chat with the LLM
- Run `python model_rag.py --chat --prompt [USER PROMPT]`
  - For example, `python model_rag.py --chat --prompt "How far did I run on September 11?"`
- This will output a response from the gAIn LLM, which can inspect your personal health and fitness data to help you learn more and achieve your goals!
