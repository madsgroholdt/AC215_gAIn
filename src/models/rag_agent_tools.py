from vertexai.generative_models import FunctionDeclaration, Tool, Part

# Specify a function declaration and parameters for an API request
get_file_by_source_func = FunctionDeclaration(
    name="get_file_by_data_source",
    description="Get activity log from a specific data source",
    # Function parameters are specified in OpenAPI JSON schema format
    parameters={
        "type": "object",
        "properties": {
            "data_source": {
                "type": "string",
                "description": "The data source",
                "enum": [
                    "Apple Health",
                    "Strava",
                    "Garmin Connect",
                    "Whoop",
                ],
            },
            "search_content": {
                "type": "string",
                "description": (
                    "The search text to filter content from text. The search "
                    "term is compared against the document text based on cosine "
                    "similarity. Expand the search term to a sentence or two to "
                    "get more exact matches."
                ),
            },
        },
        "required": ["data_source", "search_content"],
    },
)


def get_file_by_data_source(data_source, search_content, user,
                            collection, embed_func):

    query_embedding = embed_func(search_content)

    # Query based on embedding value
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        where={"source": data_source}
    )
    return "\n".join(results["documents"][0])


# Define all functions available to the health and fitness expert
fitness_expert_tool = Tool(function_declarations=[
    get_file_by_source_func])


def execute_function_calls(function_calls, user, collection, embed_func):
    parts = []
    for function_call in function_calls:
        print("Function:", function_call.name)
        if function_call.name == "get_file_by_data_source":
            print("Calling function with args:",
                  function_call.args["data_source"],
                  function_call.args["search_content"])
            response = get_file_by_data_source(
                function_call.args["data_source"],
                function_call.args["search_content"], user,
                collection, embed_func)
            print("Response:", response)
            parts.append(
                Part.from_function_response(
                    name=function_call.name,
                    response={
                        "content": response,
                    },
                ),
            )

    return parts
