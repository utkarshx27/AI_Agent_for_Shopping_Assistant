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



