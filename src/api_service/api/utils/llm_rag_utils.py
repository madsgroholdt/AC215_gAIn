import os
from typing import Dict, List
from fastapi import HTTPException
from datetime import datetime
import traceback
import chromadb
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from vertexai.generative_models import GenerativeModel, ChatSession

# Setup
GCP_PROJECT = os.environ["GCP_PROJECT"]
GCP_LOCATION = "us-central1"
EMBEDDING_MODEL = "text-embedding-004"
EMBEDDING_DIMENSION = 256
CHROMADB_HOST = os.environ["CHROMADB_HOST"]
CHROMADB_PORT = os.environ["CHROMADB_PORT"]
ENDPOINT_ID = "1336804928747732992"
MODEL_ENDPOINT = (
    "projects/ac215-final-project/locations/us-central1/endpoints/"
) + ENDPOINT_ID

# Configuration settings for the content generation
generation_config = {
    "max_output_tokens": 8192,  # Maximum number of tokens for output
    "temperature": 0.1,  # Control randomness in output
    "top_p": 0.95,  # Use nucleus sampling
}

# Get the current date to give to the LLM
today_date = datetime.now().strftime("%A, %B %d, %Y")

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
    f"Today's date is {today_date}. If you do not have data for "
    "a specific requested timeframe, just inform the user instead "
    "of giving them irrelevant information from the data you do have."
)
generative_model = GenerativeModel(
    MODEL_ENDPOINT,
    system_instruction=[SYSTEM_INSTRUCTION]
)
# https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/text-embeddings-api#python
embedding_model = TextEmbeddingModel.from_pretrained(EMBEDDING_MODEL)

# Initialize chat sessions
chat_sessions: Dict[str, ChatSession] = {}

# Connect to chroma DB
client = chromadb.HttpClient(host=CHROMADB_HOST, port=CHROMADB_PORT)
method = "recursive-split"
collection_name = f"{method}-collection"
# Get the collection
collection = client.get_collection(name=collection_name)


def generate_query_embedding(query):
    query_embedding_inputs = [TextEmbeddingInput(
        task_type='RETRIEVAL_DOCUMENT', text=query)]
    kwargs = dict(
        output_dimensionality=EMBEDDING_DIMENSION) if EMBEDDING_DIMENSION else {}
    embeddings = embedding_model.get_embeddings(
        query_embedding_inputs, **kwargs)
    return embeddings[0].values


def create_chat_session() -> ChatSession:
    """Create a new chat session with the model"""
    return generative_model.start_chat()


def generate_chat_response(chat_session: ChatSession, message: Dict) -> str:
    """
    Generate a response using the chat session to maintain history.

    Args:
        chat_session: The Vertex AI chat session
        message: Dict containing 'content' (text)

    Returns:
        str: The model's response
    """
    try:
        # Initialize parts list for the message
        message_parts = []

        # Add text content if present
        if message.get("content"):
            # Create embeddings for the message content
            query_embedding = generate_query_embedding(message["content"])
            # Retrieve chunks based on embedding value
            results = collection.query(
                query_embeddings=[query_embedding],
                n_results=5,
                # where={"source": {"$ne": ""}},
                # where_document={"$contains": " "}
            )
            content_text = message["content"]
            documents_text = "\n".join(results["documents"][0])
            INPUT_PROMPT = f"{content_text}\n{documents_text}"
            message_parts.append(INPUT_PROMPT)

        if not message_parts:
            raise ValueError(
                "Message must contain either text content or image")
        print(INPUT_PROMPT)
        # Send message with all parts to the model
        response = chat_session.send_message(
            message_parts,
            generation_config=generation_config
        )

        return response.text

    except Exception as e:
        print(f"Error generating response: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {str(e)}"
        )


def rebuild_chat_session(chat_history: List[Dict]) -> ChatSession:
    """Rebuild a chat session with complete context"""
    new_session = create_chat_session()

    for message in chat_history:
        if message["role"] == "user":
            generate_chat_response(new_session, message)

    return new_session
