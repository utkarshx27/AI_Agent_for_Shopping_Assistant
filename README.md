# Agentic AI Virtual Shopping Assistant
The goal of this project is to develop a virtual shopping assistant that helps users navigate multiple fashion e-commerce platforms by interpreting user requests, utilizing external tools, and providing coherent responses.
## Scope
It can perform tasks like search aggregation, shipping estimation, discount checking, price comparison, and return policy checking.
## Block Diagram
![Test Image](https://raw.githubusercontent.com/utkarshx27/virtual_shopping_assistant/d86fa2a44c09bf1b1644089493000560740f2a9d/docs/User%20Prompt.png)
---
## Analysis
### Task A: Basic Item Search + Price Constraint
####	E-Commerce Search Aggregator (search_products)
-	Purpose: Searches for products across multiple e-commerce platforms based on user-specified criteria (e.g., name, colour, price range, size, brand).
-	Implementation: Filters a mock inventory dataset to return matching products.
-	Example Use Case: "Find a floral skirt under $40 in size S."
####	Discount / Promo Checker (discount_checker):
-	Purpose: Checks if a discount or promo code is applicable to a specific product and calculates the discounted price.
-	Implementation: Validates discount availability and returns discount details for a given product ID.
-	Example Use Case: "Can I apply the discount code ‘SAVE10’ to this product?"

![Test Image](https://raw.githubusercontent.com/utkarshx27/virtual_shopping_assistant/d0e41f7336dedf911a5e78502d1e76e6f5105554/logs/test1.png)
### Task B: Shipping Deadline
####	3.	Shipping Time Estimator (estimate_shipping): 
-	Purpose: Estimates shipping feasibility, cost, and delivery date based on the user's location and desired delivery date.
-	Implementation: Uses a mock shipping dataset to calculate shipping details.
-	Example Use Case: "Can I get this product delivered to New York by Friday?"
-	
![Test Image](https://raw.githubusercontent.com/utkarshx27/virtual_shopping_assistant/d0e41f7336dedf911a5e78502d1e76e6f5105554/logs/test2.png)
### Task C: Competitor Price Comparison
#### Competitor Price Comparison (price_comparison):
-	Purpose: Compares prices of a specific product across different online stores.
-	Implementation: Searches a mock competitor prices dataset to find better deals.
- Example Use Case: "I found this denim jacket for $80 on SiteA. Are there any better deals?"

![Test Image](https://raw.githubusercontent.com/utkarshx27/virtual_shopping_assistant/d0e41f7336dedf911a5e78502d1e76e6f5105554/logs/task3.png)
### Task D: Returns & Policies
#### Return Policy Checker (return_policy_checker):
-	Purpose: Provides summaries of return policies for specific e-commerce platforms.
-	Implementation: Retrieves return policy details from a mock dataset.
-	Example Use Case: "Does SiteB offer hassle-free returns for this dress?"

![Test Image](https://raw.githubusercontent.com/utkarshx27/virtual_shopping_assistant/d0e41f7336dedf911a5e78502d1e76e6f5105554/logs/task4.png)
### Task E: Combine multiple tool usages
![Test Image](https://raw.githubusercontent.com/utkarshx27/virtual_shopping_assistant/d0e41f7336dedf911a5e78502d1e76e6f5105554/logs/test1.png)
---
## Design Decisions
### Design Overview:
The Personal Online Fashion Shopping Agent is designed to assist users in navigating multiple fashion e-commerce platforms by interpreting user queries, invoking appropriate tools, and integrating the results to provide coherent and helpful responses. The architecture is modular and consists of three main components:
####	Reasoning Engine:
-	The agent analyses user queries to determine the intent and required actions.
-	It identifies which tools to invoke based on the query (e.g., searching for products, checking discounts, estimating shipping, comparing prices, or verifying return policies).
####	Tool Calls:
-	Once the required tools are identified, the agent executes them with the appropriate parameters.
-	Each tool is implemented as a Python function that processes the input and returns structured data.
####	Observation and Integration:
-	The agent collects the outputs from the invoked tools and integrates them into a final response.
-	It ensures the response is user-friendly and addresses the user's query comprehensively.

This architecture allows the agent to handle a variety of user requests efficiently and provides a seamless shopping experience.

### How Tools Work Together:
The agent dynamically selects and combines tools based on the user's query. For example:
####	If a user asks, "Find a floral skirt under $40 in size S. Is it in stock, and can I apply a discount code ‘SAVE10’?", the agent will:
1.	Invoke the E-Commerce Search Aggregator to find matching products.
2.	Use the Discount Checker to validate the discount code and calculate the final price.
3.	Integrate the results and present them to the user.
This modular approach ensures flexibility and scalability, allowing new tools to be added easily in the future.

### Tools Module (tools.py)
1.	E-Commerce Search Aggregator
**Purpose:** Search for products in the inventory based on user-specified filters like name, color, price range, size, and brand.
**Implementation:**
-	The function search_products takes a DataFrame (df) and optional filters (name, color, min_price, max_price, size, brand).
-	It validates the input DataFrame and filters, then applies the filters to the DataFrame.
-	The results are returned as a list of dictionaries, where each dictionary represents a product matching the criteria.

2.	Shipping Time Estimator
**Purpose:** Estimate the shipping cost and delivery date for a given city and desired delivery date.

**Implementation:**
-	The function estimate_shipping takes a DataFrame (df), a city, and a desired delivery date.
-	It calculates the estimated delivery date based on the shipping days from the warehouse to the city and adds a fixed doorstep delivery time.
-	It checks if the desired delivery date is feasible and returns the shipping cost and estimated delivery date.

3.	Discount / Promo Checker
**Purpose:** Check if a discount is available for a specific product and provide details like discounted price and coupon code.

**Implementation:**
-	The function discount_checker takes a DataFrame (df) and a product ID.
-	It checks if the product has a discount and returns the discounted price, discount percentage, and coupon code if available.
  
4.	Competitor Price Comparison
**Purpose:** Compare prices of a specific product across different competitor stores.

**Implementation:**
-	The function price_comparison takes a DataFrame (df) and a product name.
-	It searches for the product in the competitor prices DataFrame and returns a list of stores with their prices and discount details.
  
5.	Return Policy Checker
**Purpose:** Provide details of the return policy for a specific store.

**Implementation:**
-	The function return_policy_checker takes a DataFrame (df) and a store name.
-	It retrieves the return policy details (return period, conditions, and refund method) for the specified store.

### Agent Script (agent.py)
I have used Open AI Assistant ([OpenAI Assistants API Documentation](https://platform.openai.com/docs/api-reference/assistants)). This assistant can call models and use tools to perform tasks. Model: gpt-4o.
#### Prompt Template:
-	**Prompt 1:** You are a helpful online shopping assistant. Use the provided tools to answer user queries. Always ask for necessary information like the delivery city before making any assumptions. Avoid answering question that are not related to online shopping.
- **Prompt 2:** Always stay on the topic of online shopping and use the tools provided to assist the user. Ask for necessary information before making any assumptions.
-	User queries are passed to the assistant via the client.beta.threads.messages.create method.
-	The assistant processes these queries and determines which tools to invoke.
#### Parsing Logic:
-	The parsing logic is responsible for interpreting the user's query, identifying the required tools, and extracting the necessary parameters for those tools.
-	The OpenAI Assistant uses the tools_list to determine which tools are available and their respective parameters.
-	When the assistant detects that a tool needs to be invoked (based on the user's query), it triggers the requires_action status.
-	The required actions are extracted from the run_status object:
```
required_actions = run_status.required_action.submit_tool_outputs.model_dump()
```

-	For each tool call, the assistant extracts:
  -	The function name (e.g., search_products, estimate_shipping).
  -	The arguments (e.g., city, desired_date, product_name).
#### Integration of Tool Outputs: 
-	Once the tools are invoked and their outputs are generated, the assistant integrates these outputs into a coherent response for the user.
-	The assistant retrieves the tool outputs and formats them into a response.
-	The tools_output list is populated with the results of each tool call:
```
tools_output.append({
    "tool_call_id": action["id"],
    "output": output
})

```

•	The assistant submits these outputs back to the OpenAI API:
```
client.beta.threads.runs.submit_tool_outputs(
    thread_id=thread.id,
    run_id=run.id,
    tool_outputs=tools_output
)

```

-	The assistant then generates a final response based on the integrated tool outputs and sends it to the user.
---
## Challenges & Improvements:
- **API Limits & Latency:** OpenAI API calls have rate limits affecting response speed. But in a same way we can use any open source model with Langchain.
- **Use Web Crawling** For Competitor Price Comparison, we can use web web crawler.
- **Use Small Model (Fine Tuned)** We can finetune any smaller model because it is a domain-specific task, potentially reducing computational costs.
- **Voice Assistant** We can explore text to speech models, so that user can use voice commands.
- **Reviews Summary** Provide summary of reviews and rating.
- **Visual Search** Using Computer Vision we can implement a visual search to find similer items.

##  Open Questions & References:
- https://platform.openai.com/docs/api-reference/assistants
- https://platform.openai.com/docs/guides/function-calling
