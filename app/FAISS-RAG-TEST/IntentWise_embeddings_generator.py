from promptflow import tool
import os
import numpy as np
from openai import AzureOpenAI


# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need
@tool
def my_python_tool(input1: str) -> str:
    
    client = AzureOpenAI(
    api_key = os.getenv("AZURE_OPENAI_KEY"),  
    api_version = "2023-05-15",
    azure_endpoint =os.getenv("AZURE_OPENAI_ENDPOINT") 
    )

    list_intents = input1["search_intents"].split(',')
    num_intents = len(list_intents)
    print(num_intents)
    intents_list = []
    embeddings_list = []
    json_list = []

    for i in range(num_intents):
        intent = input1["search_intents"]
        intents_list.append(intent)
        response = client.embeddings.create(
            input = intent,
            model= "text-embedding-ada-002"
        )

        json = response.model_dump_json(indent=2)
        json_list.append(json)
        embeddings_list.append(response.data[0].embedding)
    
    array_embeddings = np.asarray(embeddings_list)
    print(array_embeddings.shape)
    ave_embeddings = np.mean(array_embeddings, axis = 0)

    list_embd = ave_embeddings.tolist()

    # out_str = ",".join(str(element) for element in list_embd)
    
    return list_embd
