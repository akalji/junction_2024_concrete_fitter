import json
import openai
import os
import meilisearch
from typing import List, Dict
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI


class Chatbot:
    def __init__(self):
        load_dotenv(find_dotenv())  # Load environment variables from .env file
        self.client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        self.message_history = [
            {
                "role": "system",
                "content": "Act as a construction engineer assistant. You have a knowledge base of documentation for different products of the construction company. The user may ask you questions or ask for recommendations that require knowledge about the product. You can use the documents to retrieve context to answer the questions."
            }
        ]

        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "meilisearch_products_info",
                    "description": "Get relevant information about different products of a construction company. Call this whenever you need to recommend a product for a specific case or if the user asks questions related to the products or available solutions.",
                    "properties": {
                        "search_query": {
                            "type": "string",
                            "description": "Search query"
                        }
                    },
                    "required": ["search_query"],
                    "additionalProperties": False
                }
            }
        ]

        self.meili_client = meilisearch.Client(os.environ["MEILI_HTTP_ADDR"], os.environ["MEILI_MASTER_KEY"])
        self.meili_client.get_keys()

    def meilisearch_products_info(self, search_query):
        search_result = self.meili_client.index('products').search(search_query)
        return search_result

    def add_message(self, role: str, content: str):
        self.message_history.append({"role": role, "content": content})

    def get_response(self, user_message: str) -> str:
        self.add_message("user", user_message)
        print("QUESTION:", user_message)
        
        # Call the chat completion API
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.message_history,
            tools=self.tools,
        )
        
        # Check if a tool call was requested by the model
        if completion.choices[0].message.tool_calls:
            tool_call = completion.choices[0].message.tool_calls[0]
            arguments = tool_call.function.arguments  # Access arguments as an attribute

            # Parse the arguments (assumed to be in JSON format)
            arguments_dict = json.loads(arguments)
            search_query = arguments_dict.get("search_query")
            search_result = self.meilisearch_products_info(search_query)
            
            # Prepare the function call result message
            function_call_result_message = {
                "role": "tool",
                "content": json.dumps(search_result),
                "tool_call_id": tool_call.id
            }
            
            # Send the tool result back to the model
            completion_with_result = self.client.chat.completions.create(
                model="gpt-4o",
                messages=self.message_history + [completion.choices[0].message, function_call_result_message]
            )
            
            assistant_message_content = completion_with_result.choices[0].message.content
        else:
            assistant_message_content = completion.choices[0].message.content  # No function call; just respond directly
        
        self.add_message("assistant", assistant_message_content)
        return assistant_message_content


# Example usage
chatbot = Chatbot()
#print("ANSWER:", chatbot.get_response("Hi! My name is Alex"))
#print("ANSWER:", chatbot.get_response("What connectors can we use for beam to column connection?"))

while True:
    print("ANSWER:", chatbot.get_response(input("Input your question here: ")))
