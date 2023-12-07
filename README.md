# RAG FAISS-base promptflow (Azure AI studio (Preview)) on local machine

# Promptflow architecture (RAG, FAISS-base)
![image](./images/Screenshot%20from%202023-12-03%2013-35-26.png)

- Feature
    - Intent-wise encoding to obtain respective embeddings
    - Take average embeddings between given number of embeddings (=given sentences in user query) to find resonable context representation in 1536 by using `text-embedding-ada-002`


Why I was required to develop promptflow on local machine even though is "Azure AI studio (__Preview__)"?
- There is the issue with runtime on Azure AI studio Preview [[link](https://ai.azure.com/?tid=20206f9d-8c1f-4fd7-99d5-4cc238adf2a6)] since it is still in development process, namely "__Preview__".
- We could not use runtime (the cloud computation resource for test promptflow) on the Azure platform to test our customized promptflow.


# Quick-start
- Ultimate goal
    - "execute customized chatBot on local machine using Docker"

- Prerequesties
    - Linux(tested on Manjaro linux)
    - Python 3.9
        - Packages
            - promptflow
            - promptflow-tools
            - promptflow_vectordb
            - numpy
            - openai
            - faiss-cpu == 1.7.4
            - langchain
    - conda
    - docker

- Setup

    Create virtual environment and start
    ```
    git clone this folder    

    conda create --name env_name python=3.9
    conda activate env_name
    
    pip install promptflow promptflow-tools
    
    nvim <your connection>.yaml
    ```
    Edit \<your connection\>.yaml as following:
    ```
    $schema: https://azuremlschemas.azureedge.net/promptflow/latest/AzureOpenAIConnection.schema.json
        name: connection_name_of_azure_open_ai
        type: azure_open_ai
        api_key: <test_key>
        api_base: <test_base>
        api_type: azure
        api_version: <test_version>
    ```
    Establish connection
    ```
    pf connection create -f ./<your/azure_cognitive_service.yaml
    ```
    
    Export environment variable for azure openAI authentication
    Azure OpenAI
    ```
    AZURE_OPENAI_KEY="****"
    AZURE_OPENAI_ENDPOINT="https://\<your resource name\>.openai.azure.com/"
    ```
    
    Test promptflow
    ```
    pf flow test --flow <flow directory path (relative)>
    ```
    
    Deployment
    build docker file
    ```
    pf flow build --source ./FAISS-RAG-TEST/ --output ./build/docker_test2 --format docker
    ```

    create docker image
    ```
    docker build dist -t <docker image name>
    ```

    Run docker daemon
    ```
    systemctl start docker
    ```

    Run docker app for RAG
    ```
    docker run -p 8080:8080 -e <Azure connection name>=****** -e AZURE_OPENAI_API_KEY=******** -e AZURE_OPENAI_ENDPOINT=********* <docker image name>
    ```
