

# Information System for Investigating Data, Orienting Public Opinion, and Improving Political Activities for Party Officials

## Overview


This project is designed as a chatbot system that aims to assist Party officials by answering questions about various issues related to **Vietnamese politics**. The system leverages advanced techniques such as **Retrieval-Augmented Generation (RAG)** to retrieve relevant documents from a vector store, enhancing the context for the **Large Language Model (LLM)** to provide precise and insightful responses. The project integrates **query routing** and **query transformation** to improve the accuracy of the responses and ensure that the chatbot answers in the most relevant context.

![Law_ChatBot (2)](https://github.com/user-attachments/assets/079e55b7-657a-43e3-b616-f23f05f0db97)


![image](https://github.com/user-attachments/assets/d1fc0fca-c361-4d08-a48d-5c7a0432792c)

---

## Objectives
- **Provide Accurate Answers**: The system enables Party officials to inquire about political issues, policy, and public opinion, offering insightful responses.
- **Orient Public Opinion**: By utilizing current political data, the system helps in shaping public opinion.
- **Enhance Political Activities**: The system serves as a decision-making aid, improving the actions and strategies of political leaders.

## Features
1. **Retrieval-Augmented Generation (RAG)**: This technique is used to retrieve documents that add context to the LLM, which improves response quality by integrating relevant data into the model's answers.
   
2. **Query Routing**: The system routes queries to appropriate databases or sub-systems that can provide the best possible context for the LLM's response.

3. **Query Transformer**: It enhances the query by generating more targeted follow-up questions, which helps obtain additional context from the document repository, making answers more precise.

4. **Fine-tuned Embedding Model**: The embedding model has been fine-tuned for better vector representation, ensuring that the information retrieved from the vector store is relevant and optimally aligned with the query.

5. **Rerank Model**: The rerank model is used to reorder retrieved documents based on their relevance, ensuring that the LLM receives the most pertinent data for generating an answer.

6. **Qdrant Integration**: The system uses **Qdrant**, a vector database, to store and retrieve document embeddings. The Qdrant vector store enables fast and efficient document retrieval based on the query’s semantic meaning.

7. **Optimization for Gemini Tokenization**: The document retrieval and reranking process is designed to reduce the number of tokens used, ensuring that the chatbot can operate efficiently with **Gemini**, a new language model, while still generating rich and accurate responses.

8. **Flask Integration**: The entire chatbot system is integrated into a website via **Flask**, allowing users to interact with the system through a user-friendly interface.

---

## Architecture

The system architecture consists of the following components:

1. **Frontend**: A simple web interface built with **Flask** that allows users to enter queries about political topics.

2. **Backend**: 
    - **Query Routing & Query Transformation**: These techniques ensure that the right context is retrieved and followed-up questions are generated as needed.
    - **Document Retrieval with RAG**: Uses embeddings to find the most relevant documents and provides context for the LLM to answer.
    - **Fine-tuned Embedding & Rerank Models**: Optimized models for embedding queries and documents into vectors, which are stored in **Qdrant**.
    - **Qdrant Vector Store**: A high-performance vector database that holds document embeddings and allows for fast retrieval based on semantic search.

3. **Large Language Model (LLM)**: Processes the input query and integrates the context retrieved from the Qdrant vector store to generate a high-quality response.

---

## How it Works

1. **User Input**: The user asks a question about Vietnamese politics via the web interface (Flask frontend).
   
2. **Query Routing**: Based on the nature of the question, the query is routed to the appropriate section of the system or database.

3. **Query Transformation**: The system enhances the query by generating follow-up questions, refining the context and expanding the information needed.

4. **Document Retrieval**: The **RAG model** uses embeddings to find the most relevant documents in the Qdrant vector store. This context is added to the query.

5. **Reranking**: The rerank model orders the documents based on relevance, ensuring the most pertinent information is used to generate the response.

6. **Response Generation**: The LLM generates a precise response using the augmented context from the retrieved documents.

7. **Output**: The system displays the response to the user on the web interface.

---

## Installation and Setup

To set up and run the system locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ZeusCoderBE/Vietnam-political-consulting-chatbot.git
   cd Vietnam-political-consulting-chatbot
   ```

2. **Install dependencies**:
   Install the required Python libraries using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask application**:
   ```bash
   python run_app.py
   ```

4. **Access the chatbot**:
   Open your browser and go to `http://127.0.0.1:5000` to interact with the chatbot.

---

## Dependencies
- **Flask**: Lightweight web framework for Python, used to serve the chatbot on the web.
- **Qdrant**: High-performance vector database used for storing and retrieving document embeddings.
- **Transformers**: Library for working with pre-trained language models, such as BERT, RoBERTa, or T5. It is specifically used for fine-tuning transformer-based models to generate document embeddings for downstream tasks like document retrieval and similarity matching.
- **paraphrase-multilingual-mpnet-base-v2**: A multilingual model from Hugging Face used for paraphrase identification and reranking tasks. This model can generate embeddings for sentences in multiple languages, helping in tasks like ranking or finding similar sentences/documents in a multilingual context.
- **vietnamese-bi-encoder**: A model specifically fine-tuned for Vietnamese language tasks, designed for generating high-quality embeddings for Vietnamese text. This model is used for tasks such as document retrieval, sentence similarity, and ranking in Vietnamese.
- **NumPy**: Numerical computing library used for handling matrix operations and data manipulation.
- **Pandas**: Data analysis library used for data manipulation and analysis.
- **TensorFlow**: Deep learning library used for model fine-tuning and evaluation.
- **Langchain**: Framework designed for developing applications powered by language models. It helps integrate and orchestrate LLMs (Large Language Models) with external tools, databases, and APIs, enabling complex conversational agents and workflows.

---
## Fine-Tuning Process

- The **embedding model** was fine-tuned using a dataset related to Vietnamese politics, ensuring that the embeddings captured the contextual meaning of political terms and issues.
- The **rerank model** was trained to ensure that the most relevant documents are selected and prioritized.
  
By combining these models with **RAG**, the system is able to provide answers that are not only contextually accurate but also optimized for the specific nature of the queries.

---

## Future Improvements

1. **Multilingual Support**: Expanding the system to support multiple languages, particularly to handle queries in Vietnamese and other languages used in Southeast Asia.
   
2. **Advanced User Interaction**: Introducing user-specific profiles that can personalize responses based on user history and preferences.

3. **Scalability**: Implementing solutions for scaling the system, such as using Kubernetes to manage containers and deploying on cloud platforms like AWS or GCP.

4. **Continuous Learning**: Allowing the system to continuously improve by integrating feedback loops from users and updating the model with new data on political events.

---

## Conclusion

This **Information System** serves as a powerful tool for **Party officials** and other stakeholders by providing quick, accurate, and contextually relevant answers to questions about Vietnamese politics. By combining **RAG**, **query routing**, and **fine-tuned models**, this system allows for efficient document retrieval and high-quality responses.

This approach not only supports **data-driven political decision-making** but also empowers **leaders to orient public opinion** and **improve political activities** in a rapidly changing political landscape.

---


