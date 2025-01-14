from flask import Response
from typing import Any, AsyncGenerator, Union
from backend.agents.agent import Agent
from openai import OpenAI
import json
import time
from backend.tools.searchtool import Search
import requests
from urllib.parse import quote_plus
from colorama import Fore, Back, Style

class AssistantAgent(Agent):
    def __init__(
        self,
        openai_client: OpenAI,
        search_client: Search,
        openai_base: str,
        openai_model: str,
        openai_embed_model: str,
        openai_type: str,
        openai_version: str,
        openai_key: str,
        search_endpoint: str,
        search_key: str,
        search_index: str,
        bing_subscription_key: str,
    ):
        self.openai_client = openai_client
        self.search_client = search_client
        self.openai_base = openai_base
        self.openai_model = openai_model
        self.openai_embed_model = openai_embed_model
        self.openai_type = openai_type
        self.openai_version = openai_version
        self.openai_key = openai_key
        self.search_endpoint = search_endpoint
        self.search_key = search_key
        self.search_index = search_index
        self.bing_subscription_key = bing_subscription_key
        
    def create_json_object(self, id, message_content, role, created_at, finish_reason="stop", index=0, model="gpt-4-1106-preview"):
        json_object = {
            "id": id,
            "choices": [
                {
                    "finish_reason": finish_reason,
                    "index": index,
                    "message": {
                        "content": message_content,
                        "role": role,
                        "function_call": None,
                        "tool_calls": None
                    }
                }
            ],
            "created": created_at,
            "model": model,
            "object": "chat.completion",
            "system_fingerprint": "",
            "usage": {
                "completion_tokens": 0,
                "prompt_tokens": 0,
                "total_tokens": 0,
            }
        }

        return json.dumps(json_object, indent=2)
    
    # Function to perform a Shadow Search
    def shadow_search(self, query):
        search_result = self.search_client.search_hybrid(query)
        return search_result

    # OPENAI FUNCTION: Function to perform a Bing search
    def profile_prospect(self, prospect, context):
        print(f"Generating a search_query for bing based on this user request: {prospect} - {context}")

        bing_response = self.run_bing_search(prospect + context)
        return bing_response
    
    # OPENAI FUNCTION: Function to perform a Bing search
    def run_bing_search(self, search_query):
        # Returns data of type SearchResponse 
        try:
            encoded_query = quote_plus(search_query)
            bing_search_query = base_url + 'q=' + encoded_query # + '&' + 'customconfig=' + custom_config_id --> uncomment this if you are using 'Bing Custom Search'
            r = requests.get(bing_search_query, headers={'Ocp-Apim-Subscription-Key': self.bing_subscription_key})
        except Exception as err:
            print("Encountered exception. {}".format(err))
            raise err
        
        response_data = json.loads(r.text)
        results_text = ""
        for result in response_data.get("webPages", {}).get("value", []):
            results_text += result["name"] + "\n"
            results_text += result["url"] + "\n"
            results_text += result["snippet"] + "\n\n"
            print(f"Title: {result['name']}")
            print(f"URL: {result['url']}")
            print(f"Snippet: {result['snippet']}\n")
        print(results_text)  
        return results_text


    # Function to handle tool output submission
    async def submit_tool_outputs(self, thread_id, run_id, tools_to_call):
        tool_output_array = []
        for tool in tools_to_call:
            output = None
            tool_call_id = tool.id
            function_name = tool.function.name
            function_args = tool.function.arguments

            if function_name == "shadow_search":
                print(Fore.GREEN + f"make call to shadow_search {json.loads(function_args)['query']}")
                print(Style.RESET_ALL)
                output = self.search_client.search_hybrid(query=json.loads(function_args)["query"])

            elif function_name == "profile_prospect":
                print(Fore.GREEN + f"make call to profile_prospect {json.loads(function_args)['prospect']} - {json.loads(function_args)['context']} ")
                print(Style.RESET_ALL)
                output = self.profile_prospect(prospect=json.loads(function_args)["prospect"], context=json.loads(function_args)["context"])
            
            if output:
                print(Fore.CYAN + f"[function result] Appending tool output array... {output}")
                print(Style.RESET_ALL)
                tool_output_array.append({"tool_call_id": tool_call_id, "output": output})

        return self.openai_client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run_id,
            tool_outputs=tool_output_array
        )

    # Function to print messages from a thread
    def print_messages_from_thread(self, thread_id):
        messages = self.openai_client.beta.threads.messages.list(thread_id=thread_id)
        #print(messages.model_dump_json())
        for msg in messages.data:
            #print(f"{msg.thread_id}:  {msg.role}: {msg.content[0].text.value}")
            if msg.role == "assistant":
                m_json = self.create_json_object(msg.thread_id, msg.content[0].text.value, msg.role, msg.created_at)
                return m_json

    # Function to wait for a run to complete
    async def wait_for_run_completion(self, thread_id, run_id):
        while True:
            run = self.openai_client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            print(f"Current run status: {run.status}")
            time.sleep(2)
            if run.status in ['completed', 'failed', 'requires_action']:
                return run

    def get_user_query(self, lst):
        if lst:
            return lst[-1]
        else:
            return None
                
    async def chatbot(self, messages: list, assistant_thread_id: str):

        # Retrieve an existing assistant
        assistant = self.openai_client.beta.assistants.retrieve(
                        assistant_id,
                        )  
        
        query = self.get_user_query(
            messages
        )  # get the current user question to use for search

        self.openai_client.beta.threads.messages.create(  # create a message on the thread that is a user message
                    thread_id=assistant_thread_id, 
                    role="user",
                    content=query["content"]
                    )
        while True:
            try:
                run = self.openai_client.beta.threads.runs.create(  # create a run of the thread
                        thread_id=assistant_thread_id,
                        assistant_id=assistant.id,
                        )
                run = await self.wait_for_run_completion(assistant_thread_id, run.id)  # wait for the completion of the run which should return the run

                if run.status == 'failed':
                    print(run.error)
                    continue
                elif run.status == 'requires_action':
                    run = await self.submit_tool_outputs(assistant_thread_id, run.id, run.required_action.submit_tool_outputs.tool_calls)
                    run = await self.wait_for_run_completion(assistant_thread_id, run.id)

                # Print messages from the thread
                response = self.print_messages_from_thread(assistant_thread_id)
                #print(f"Response:  {response}")

                return Response(
                    response,
                    mimetype="application/json",
                )
            except Exception as yikes:
                print(f'\n\nError communicating with OpenAI: "{yikes}"')


    async def run(
        self, messages: list[dict], assistant_thread_id: str, stream: bool = False
    ) -> Union[dict[str, Any], AsyncGenerator[dict[str, Any], None]]:
        #print(f"thread_id:  {assistant_thread_id}")
        if not assistant_thread_id.strip() == "":  # check if there is a string value for thread_id
            thread = self.openai_client.beta.threads.retrieve(thread_id)  # use the thread passed in
            print(f" We have thread!: {thread.id}")
        else:
            thread = self.openai_client.beta.threads.create()   # create a thread
            print(f"Creating new thread: {thread.id}")

        r = await self.chatbot(messages, thread.id)
        return r