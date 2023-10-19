import openai
import os
import json

openai.api_key = os.getenv('OPENAI_API_KEY')

RENT_OR_BUY = ""
PROPERTY_TYPE = ""
NAME_OF_LOCATION = ""
PRICE = ""

openai_prompt = """
As an expert in data extraction, you'll interpret user queries, enclosed within triple back ticks, to consistently 
identify four vital parameters: [rent_or_buy, property_type, name_of_location, price]. These represent:

1. rent_or_buy: Indicates if the user wants to rent or buy a property.
2. property_type: Specifies the type of property, such as an apartment or a house.
3. name_of_location: Identifies the desired location for the property.
4. price: Shows the user's budget in Euros.

If any parameter is missing, ask for it using: "Please provide a (insert missing search criteria: [rent or buy, 
property type, name of location, price])". Don't return the JSON format with empty fields; instead, prompt the user 
to provide missing data.

Consider these examples:

**Example 1**
User says:
```I'm looking to rent in Berlin for less than 800 Euros.```
Missing information: Type of property. Your response: "Please provide a specific property type (for instance, 
apartment, house, studio, 1-bedroom, loft, etc.)."

**Example 2**
User says:
```I want a three-bedroom house.```
Missing information: Rent/buy, location, price. Your response: "Please provide if you want to rent or buy, the 
location you're interested in, and your budget in Euros."

**Example 3**
User says:
```I want to buy a villa in Rome.```
Missing information: Price. Your response: "Please provide your budget in Euros."

**Example 4**
User says:
```Looking for a studio to rent.```
Missing information: Location, price. Your response: "Please provide the name of the location you're interested in, 
and your budget in Euros."
Your primary goal is ensuring the user provides all necessary parameters, asking for any missing information 
accordingly.
Provide the response as a dictionary in python:
**Example 5**
User says:
```Looking for a studio to rent for 1500 Euros in Paris.```
{rent_or_buy: "rent", 
estate_type: "studio", 
price: 1500, 
user_query: "Looking for a studio to rent for 1500 Euros in Paris."}

Let's try:
"""

user_input = input("Enter your prompt: ")

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "assistant", "content": "Why do you sell?"},
    {"role": "user", "content": user_input}
  ]
)

print(completion.choices[0].message["content"])
