import random
import os
from typing import List, Dict
import openai
import streamlit as st


openai.api_key = os.getenv('OPENAI_API_KEY')

REASON_FOR_SELLING = ""
TIME_OF_SALE = ""
STRATEGY_FOR_SELLING = ""
STEPS_TAKEN_SO_FAR = ""
CONSTRAINTS_FOR_SELLING = ""

SELLER_MESSAGES = []

# App title
st.set_page_config(page_title="ChitChat")

avatar = {
    "ai": "src/static/media/logo-purple-circle-50.png",
    "assistant": "src/static/media/logo-purple-circle-50.png",
    "user": "src/static/media/seller-avatar.png",
    "human": "src/static/media/seller-avatar.png",
    "system": "src/static/media/logo-purple-circle-50.png"
}

lead_validation = """
You are an experienced expert in the field of real estate sales. Your job is to get information about the sellers 
and their properties. During the conversation, you will ask a couple of questions about the seller's plans for selling 
their properties, their personal circumstances and their motivations to sell. Be as polite as possible. Have a casual 
tone which is not robotic but friendly. Never advise the sellers to rent out their properties. Only ask one question at
a time. Make sure that the seller gives a valid answer to all of your questions but only ask for details if the answers 
are not sufficient for your validation. The questions are:

1. Why do you want to sell your property? (Ask for the seller's motivations and reasons for selling.) 
2. When will you sell your property? (Is there a delay or a condition that must be fulfilled?) 
3. How do you plan to sell your property?
4. Steps taken? (Where is he at? If he has met professionals)
5. Are there any constraints? (What happens if he cannot sell?)

When the seller has answered all the questions summarize the reasons in a list:

* The reason to sell the property.
* When the property should be sold.
* What the sellers strategy will be.
* The steps the seller has already taken.
* What are possible constraints for selling.

And say that the seller will be contacted by a seller from Meilleurs Agents in the next 24 hours.

"""

responses = {}

initial_message = [
        {"role": "system", "content": lead_validation },
        {"role": "assistant", "content": "Hi I am your AVIV virtual assistant. In order to help you sell your property "
                                         "I need to understand your personal circumstances at this point. "},
        {"role": "assistant", "content": "Please tell me why do you want to sell your property? "}
    ]

st.session_state.responses = responses
for response in responses:
    print(f"Response: {response}")

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = initial_message.copy()

# Store seller responses
if "seller_response" not in st.session_state.keys():
    st.session_state.seller_response = []

# Display or clear chat messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"], avatar=avatar[message["role"]]):
            st.write(message["content"])


def clear_chat_history():
    st.session_state.messages = initial_message.copy()


st.sidebar.image("src/static/media/logo-text-black-500.png",width=200)
st.sidebar.button("Clear ChitChat History", on_click=clear_chat_history)


# Function to get a random phrase
def get_random_phrase(phrases):
    return random.choice(phrases)


def get_completion(
        messages: str, model: str = "gpt-3.5-turbo", temp: float = 0.0
) -> List[Dict[str, any]]:
    """
    Get the response of Chat-GPT with a give prompt.

    :rtype: object
    :param messages: The prompt formulated toward Chat-GPT
    :param model: The selected model (usually 'gpt-3.5-turbo')
    :param temp: The temperature (The randomness of the token selected)
        This represents the freedom/creativity in the response of the model.
        The higher the temperature, the higher the creativity but also the lower control other the response of Chat-GPT
        (temp = 0.0 means every time the model will output the same response).
    :return: The response of Chat-GPT regarding the prompt.
    """
    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=temp, stream=False
    ).choices[0].message["content"]

    return response


# User-provided prompt
if prompt := st.chat_input(disabled=False):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=avatar["user"]):
        st.write(prompt)

# Generate a new response if the last message is not from the assistant
if st.session_state.messages[-1]["role"] != "assistant":
    # global SELLER_MESSAGES
    st.session_state.seller_response.append(st.session_state.messages[-1]['content'])
    with st.chat_message("assistant", avatar=avatar["assistant"]):
        with st.spinner("Thinking..."):
            response = get_completion(st.session_state.messages)
            message = {"role": "assistant", "content": response}
        st.write(response)
        st.session_state.messages.append(message)
