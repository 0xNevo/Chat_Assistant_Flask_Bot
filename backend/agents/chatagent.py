from flask import Response
from typing import Any, AsyncGenerator, Union
from backend.agents.agent import Agent
from openai import OpenAI
from backend.tools.searchtool import Search

class ChatAgent(Agent):
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

    def open_file(self, filepath):
        with open(filepath, "r", encoding="utf-8", errors="ignore") as infile:
            return infile.read()

    async def chatbot(self, messages: list):
        while True:
            try:
                chat_completion = self.openai_client.chat.completions.create(
                    model,
                    messages,
                    max_tokens,
                )
                return Response(
                    chat_completion.model_dump_json().replace("\n", "\\n"),
                    mimetype,
                )
            except Exception as yikes:
                print(f'\n\nError communicating with OpenAI: "{yikes}"')

    async def run(
        self, messages: list[dict], stream: bool = False
    ) -> Union[dict[str, Any], AsyncGenerator[dict[str, Any], None]]:
        if len(messages) < 20:  
            system_message = ({'role': 'system'})
            conversation = [
                system_message
            ] + messages  # add the system message to the beginning of the messages list
            r = await self.chatbot(conversation)
        else:
            all_messages = list()      
            for msg in messages:
                if msg['role'] == 'user':
                    all_messages.append('SELLER: %s' % msg["content"]) 
                elif msg["role"] == "assistant":
                    all_messages.append('SHADOW: %s' % msg["content"])
            text_block = '\n\n'.join(all_messages)
            chat_log = '<<BEGIN SELLER INTAKE CHAT>>\n\n%s\n\n<<END SELLER INTAKE CHAT>>' % text_block   

            conversation_chat = list()
            conversation_chat.append({'role': 'system', 'content': self.open_file('./backend/prompts/system_02_prepare_notes.md')})
            conversation_chat.append({'role': 'user', 'content': chat_log})
            notes = await self.chatbot(conversation_chat)

            conversation_notes = list()
            conversation_notes.append({'role': 'system', 'content': self.open_file('./backend/prompts/system_03_suggestions.md').replace('<<CONTEXT>>', self.search_client.search_hybrid(notes.json['choices'][0]['message']['content']))})
            conversation_notes.append({'role': 'user', 'content': notes.json['choices'][0]['message']['content']})
            r = await self.chatbot(conversation_notes)

        return r
