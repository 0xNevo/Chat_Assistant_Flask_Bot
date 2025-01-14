# shadowsellerai
Repository for Chat Bot - React/Typescript + Flask

# Description
This repo contains a baseline Flask/React/Typescript application.

# Chat Assistant Flask Application

This Flask application serves as a backend for a chat assistant system. It provides endpoints for interacting with both the chat assistant and the chat history.

## Setup

1. **Environment Variables:** This application relies on environment variables for configuration. Ensure you have the following variables set:
   - `AZURE_SEARCH_ENDPOINT`: Azure Cognitive Search endpoint.
   - `AZURE_SEARCH_ADMIN_KEY`: Azure Cognitive Search admin key.
   - `AZURE_SEARCH_INDEX`: Azure Cognitive Search index for general search.
   - `AZURE_SEARCH_INDEX_CUSTOMER`: Azure Cognitive Search index for customer data search.
   - `OPENAI_MODEL`: OpenAI model for generating responses.
   - `OPENAI_EMBED_MODEL`: OpenAI model for embedding.
   - `OPEN_AI_TYPE`: Type of OpenAI API.
   - `OPENAI_API_BASE`: Base URL for the OpenAI API.
   - `OPENAI_API_VERSION`: Version of the OpenAI API.
   - `OPENAI_API_KEY`: API key for accessing the OpenAI API.
   - `BING_SEARCH_KEY`: Bing search subscription key.
   
2. **Dependencies:** Ensure you have the required dependencies installed. You can install them using pip:

3. **Run the Application:** You can run the Flask application using the following command:  ./start.cmd

By default, the application runs in debug mode.

## Endpoints

- `/assistant`: Endpoint for interacting with the chat assistant. Supports GET and POST methods.
- `/chat`: Endpoint for chatting with the assistant. Supports GET and POST methods.
- `/upsert_thread`: Endpoint for inserting or updating chat threads in the database. Supports GET and POST methods.
- `/get_threads`: Endpoint for retrieving chat threads for a specific user. Supports GET and POST methods.
- `/get_thread_by_id`: Endpoint for retrieving a chat thread by its ID. Supports GET and POST methods.
- `/get_all_threads`: Endpoint for retrieving all chat threads. Supports GET and POST methods.
- `/delete_thread`: Endpoint for deleting a chat thread by its ID. Supports GET and POST methods.
- `/rename_thread`: Endpoint for renaming a chat thread. Supports GET and POST methods.
- `/upload_file`: Endpoint for uploading files. Supports POST method.

## Usage

- Send requests to the respective endpoints with the required parameters to interact with the chat assistant and manage chat history.

## Authors

- [Felix Martel](https://github.com/0xNevo)