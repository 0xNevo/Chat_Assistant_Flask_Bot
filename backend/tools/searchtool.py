import os
import json
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.models import Vector
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class Search:
    
    def __init__(self):
        # assign the Search variables for Azure Cogintive Search - use .env file and in the web app configure the application settings
    
    def get_embedding(self, text, model):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input = [text], model=model).data[0].embedding
    
    def search_hybrid(self, query: str) -> str:
        vector = Vector(value=self.get_embedding(query, self.model), k, fields)
        results = []

        r = self.sc.search(  
            search_text=query,  # set this to engage a Hybrid Search
            vectors=[vector],  
            select=["category", "sourcefile", "content"],
            top=3,
        )  
        for doc in r:
                results.append(f"[CATEGORY:  {doc['category']}]" + " " + f"[SOURCEFILE:  {doc['sourcefile']}]" + doc['content'])
        #print("\n".join(results))
        return ("\n".join(results))