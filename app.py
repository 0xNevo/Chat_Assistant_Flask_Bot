from flask import Flask, request, jsonify
import logging
import os
from dotenv import load_dotenv
from backend.agents.insightsagent import InsightAgent
from backend.agents.chatagent import ChatAgent
from backend.agents.assistantagent import AssistantAgent
from azure.core.credentials import AzureKeyCredential
from backend.tools.searchtool import Search
from openai import OpenAI
from backend.tools.cosmos_apis import Cosmos

load_dotenv()

app = Flask(__name__)

# assign the Search variables for Azure Cogintive Search - use .env file and in the web app configure the application settings
AZURE_SEARCH_ENDPOINT = os.environ.get("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_ADMIN_KEY = os.environ.get("AZURE_SEARCH_ADMIN_KEY")
AZURE_SEARCH_INDEX = os.environ.get("AZURE_SEARCH_INDEX")
credential_search = AzureKeyCredential(AZURE_SEARCH_ADMIN_KEY)
search: Search = Search() # get instance of cosmos to be able to make db calls for chat history

# Azure OpenAI variables from .env file
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
OPENAI_EMBED_MODEL = os.environ.get("OPENAI_EMBED_MODEL")

# set the openai required variables
OPEN_AI_TYPE = os.environ.get("OPENAI_API_TYPE")
OPENAI_BASE = os.environ.get("OPENAI_API_BASE")
OPENAI_VERSION = os.environ.get("OPENAI_API_VERSION")
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

# setup the OpenAI Client
openai_client = OpenAI()
search_client: Search = Search()  # get instance of search to query corpus
cosmos: Cosmos = Cosmos() # get instance of cosmos to be able to mmake db calls for chat history

#Bing
bing_subscription_key: str =  os.environ.get("BING_SEARCH_KEY")

@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def static_file(path):
    return app.send_static_file(path)

@app.route("/insights", methods=["GET", "POST"])
async def insights():
    request_json = request.get_json()
    #print(request_json)
    try:
        # the result will be a Flask response object which is what is expected in the UI
        result = await aa.run(request_json["messages"], request_json["assistantThreadId"])
        return result
    except Exception as e:
        logging.exception("Exception in /insights")
        return jsonify({"error": str(e)}), 500
    
@app.route("/chat", methods=["GET", "POST"])
async def chat():
    request_json = request.get_json()
    try:
        # the result will be a Flask response object which is what is expected in the UI
        result = await ca.run(request_json["messages"])
        return result
    except Exception as e:
        logging.exception("Exception in /chat")
        return jsonify({"error": str(e)}), 500
    
@app.route("/upsert_thread", methods=["GET", "POST"])
async def upsert_thread():
    request_json = request.get_json()
    try:
        # the result will be a Flask response object which is what is expected in the UI
        result = await cosmos.upsert_thread(request_json)
        return result
    except Exception as e:
        logging.exception("Exception in /create_thread")
        return jsonify({"error": str(e)}), 500
    
@app.route("/get_threads", methods=["GET", "POST"])
async def get_threads():
    request_json = request.get_json()
    try:
        # the result will be a Flask response object which is what is expected in the UI
        result = await cosmos.get_threads(request_json["user"])
        return result
    except Exception as e:
        logging.exception("Exception in /get_threads")
        return jsonify({"error": str(e)}), 500
    
@app.route("/get_thread_by_id", methods=["GET", "POST"])
async def get_thread_by_id():
    request_json = request.get_json()
    try:
        # the result will be a Flask response object which is what is expected in the UI
        result = await cosmos.get_thread_by_id(request_json["id"])
        return result
    except Exception as e:
        logging.exception("Exception in /get_thread_by_id")
        return jsonify({"error": str(e)}), 500
    
@app.route("/delete_thread", methods=["GET", "POST"])
async def delete_thread():
    request_json = request.get_json()
    #print(request_json)
    try:
        # the result will be a Flask response object which is what is expected in the UI
        result = await cosmos.delete_thread(request_json["id"])
        return result
    except Exception as e:
        logging.exception("Exception in /delete_thread")
        return jsonify({"error": str(e)}), 500
    
@app.route("/rename_thread", methods=["GET", "POST"])
async def rename_thread():
    request_json = request.get_json()
    print(request_json)
    try:
        # the result will be a Flask response object which is what is expected in the UI
        result = await cosmos.rename_thread(request_json["id"], request_json["title"])
        return result
    except Exception as e:
        logging.exception("Exception in /rename_thread")
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)