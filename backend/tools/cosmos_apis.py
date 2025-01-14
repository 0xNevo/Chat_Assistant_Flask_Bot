import os
import json
import azure.cosmos.cosmos_client as cosmos_client
from dotenv import load_dotenv
from flask import jsonify
import azure.cosmos.exceptions as exceptions

load_dotenv()

class Cosmos:
    
    def __init__(self):
        HOST = os.environ.get("HOST")
        MASTER_KEY = os.environ.get("MASTER_KEY")
        DATABASE_ID = os.environ.get("DATABASE_ID")
        CONTAINER_ID = os.environ.get("CONTAINER_ID")

    async def upsert_thread(self, options: dict):
        try:
            self.container.upsert_item(options)
        except exceptions.CosmosClientTimeoutError as e:
            return ('ERROR: cosmos.upsert_item - Timeout error')
        
        return (jsonify(options))

    
    async def get_threads(self, user: str):
        try:
            items = list(self.container.query_items(
                query,
                parameters,
                enable_cross_partition_query,
            ))
        except exceptions.CosmosResourceNotFoundError as e:
            return ('ERROR: cosmos.get_threads - Cannot find threads')

        return (json.dumps(items))
    
    async def get_thread_by_id(self, id: str):
        try:
            items = list(self.container.query_items(
                query,
                parameters,
                enable_cross_partition_query,
            ))
        except exceptions.CosmosResourceNotFoundError as e:
            return ('ERROR: cosmos.get_thread_by_id - Cannot find thread')
    
        return (json.dumps(items))
    
    async def delete_thread(self, id: str):
        try:
            self.container.delete_item(item,partition_key)
        except exceptions.CosmosResourceNotFoundError  as e:
            return ('ERROR: cosmos.delete_thread - Resource does not exist')
        
        return ('cosmos.delete_thread - Deleted item\'s Id is {0}'.format(id))
    
    async def rename_thread(self, id: str, newTitle: str):
        try:

            item = self.container.read_item(id, partition_key=id)
            item["title"] = newTitle
            updated_item = self.container.upsert_item(item)

        except exceptions.CosmosResourceNotFoundError  as e:
            return ('ERROR: cosmos.rename_thread - Resource does not exist')
        
        return ('cosmos.rename_thread - Renamed items Id is {0}'.format(id))