from flask import Response
from typing import Any, AsyncGenerator, Union
from backend.agents.agent import Agent
from openai import OpenAI
from backend.tools.searchtool import Search


class InsightAgent(Agent):
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

    def get_user_query(self, lst):
        if lst:
            return lst[-1]
        else:
            return None

    async def chatbot(self, messages: list):

        # this is the whole conversation and so to get the last user question we need the last msg in messages so we can search with that
        query = self.get_user_query(
            messages
        )  # get the current user question to use for search

        conversation = [
            system_message
        ] + messages  # add the system message to the beginning of the messages list

        while True:
            try:
                chat_completion = self.openai_client.chat.completions.create(
                    model,
                    messages,
                    max_tokens,
                )
                return Response(
                    chat_completion.model_dump_json().replace("\n", "\\n"),
                    mimetype="",
                )
            except Exception as yikes:
                print(f'\n\nError communicating with OpenAI: "{yikes}"')

    async def run(
        self, messages: list[dict], stream: bool = False
    ) -> Union[dict[str, Any], AsyncGenerator[dict[str, Any], None]]:
        r = await self.chatbot(messages)
        return r
