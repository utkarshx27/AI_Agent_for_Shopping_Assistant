from datetime import datetime, timedelta
import pandas as pd
from datetime import datetime
from pydantic import BaseModel, Field
from openai import OpenAI
import os
import logging
import json
import time
from tools import search_products, discount_checker, estimate_shipping, price_comparison, return_policy_checker
from tools import inventory_info, shipping_info, competitor_prices_info, return_policies_info

from datetime import datetime, timedelta
import pandas as pd
from pydantic import BaseModel, Field
from openai import OpenAI
import os
import logging
import json
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4o"

today = datetime.now()
date_context = f"Today is {today.strftime('%A, %B %d, %Y')}."

# Define the tools
tools_list =[
    {   
        "type": "function",
        "function": {
            "name": "search_products",
            "description": "Search for products in the inventory based on filters like name, color, price range, size, and brand.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of the product to search for. Only Name"},
                    "color": {"type": "string", "description": "Color of the product to filter by. Only Color"},
                    "min_price": {"type": "number", "description": "Minimum price of the product."},
                    "max_price": {"type": "number", "description": "Maximum price of the product."},
                    "size": {"type": "string", "description": "Size of the product to filter by."},
                    "brand": {"type": "string", "description": "Brand of the product to filter by."},
                },
                "required": [],
            },
        },
    },
    {   
        "type": "function",
        "function": {
            "name": "discount_checker",
            "description": "Use the product_id to find discount availability and return details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_id": {"type": "integer", "description": "Product ID obtained from search_products function"},
                },
                "required": ["product_id"],
            },
        },
    }, 
    {   
        "type": "function",
        "function": {
            "name": "estimate_shipping",
            "description": f"{date_context}. Get shipping estimates for a product to a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "Name of the city to estimate shipping for."},
                    "desired_date": {"type": "string", "description": "Desired delivery date in format: 'YYYY-MM-DD'"},
                },
                "required": ["city", "desired_date"],
            },
        },
    },
    {   
        "type": "function",
        "function": {
            "name": "price_comparison",
            "description": "Try to find prices of the same product in other websites.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {"type": "string", "description": "Name of the product."},
                },
                "required": ["product_name"],
            },
        },
    },
    {   
        "type": "function",
        "function": {
            "name": "return_policy_checker",
            "description": "Check return policy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "store_name": {"type": "string", "description": "Name of the store."},
                },
                "required": ["store_name"],
            },
        },
    },
]

client = OpenAI()

try:
    assistant = client.beta.assistants.create(
        name="AI shopping assistant",
        instructions="You are a helpful online shopping assistant. Use the provided tools to answer user queries. Always ask for necessary information like the delivery city before making any assumptions.",
        model="gpt-4o",
        tools=tools_list,
    )

    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="""Hello! Please describe what you are looking for?"""
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Utkarsh Singh."
    )

   # print(run.model_dump_json(indent=4))
except Exception as e:
    logger.error(f"Error initializing OpenAI assistant: {e}")
    exit(1)

function_dispatch_table = {
    "search_products": search_products,
    "discount_checker": discount_checker,
    "estimate_shipping": estimate_shipping,
    "price_comparison": price_comparison,
    "return_policy_checker": return_policy_checker
}

def chat_with_assistant():
    last_message_id = None
    while True:
        try:
            user_query = input("\nYou: ")
            if user_query.lower() in ["exit", "quit", "bye"]:
                print("Assistant: Goodbye! 😊")
                break

            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_query
            )

            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id
            )

            while True:
                time.sleep(3)
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )

                if run_status.status == 'completed':
                    messages = client.beta.threads.messages.list(
                        thread_id=thread.id,
                        order="desc"
                    )

                    for msg in messages.data:
                        if msg.role == "assistant" and msg.id != last_message_id:
                            print(f"Assistant: {msg.content[0].text.value}")
                            last_message_id = msg.id
                            break
                    break
                elif run_status.status == 'requires_action':
                    logger.info("Assistant needs to call a function...")
                    tools_output = []
                    required_actions = run_status.required_action.submit_tool_outputs.model_dump()

                    for action in required_actions["tool_calls"]:
                        func_name = action["function"]["name"]
                        arguments = json.loads(action["function"]["arguments"])
                        print(arguments)
                        func = function_dispatch_table.get(func_name)
                        print(func)

                        if func:
                            if func_name == "estimate_shipping":
                                result = func(shipping_info, city=arguments["city"], desired_date=arguments["desired_date"])
                                print(result)
                            elif func_name =="price_comparison":
                                result = func(competitor_prices_info, product_name=arguments["product_name"])
                            elif func_name =="return_policy_checker":
                                result = func(return_policies_info, store_name=arguments["store_name"])
                            else:
                                result = func(inventory_info, **arguments)
                                
                            
                            output = json.dumps(result) if not isinstance(result, str) else result
                            tools_output.append({
                                "tool_call_id": action["id"],
                                "output": output
                            })
                        else:
                            logger.error(f"Function {func_name} not found")
                            
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread.id,
                        run_id=run.id,
                        tool_outputs=tools_output
                    )
                else:
                    time.sleep(5)
        except Exception as e:
            logger.error(f"Error during chat loop: {e}")
            break
chat_with_assistant()
