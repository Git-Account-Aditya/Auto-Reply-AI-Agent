import re
from typing import Literal
from .llms import (check_sentiment_email_chain, chain_to_run_diagnosis, chain_for_negative_email,
                  chain_for_positive_email, chain_for_neutral_email)


# to extract information from text and store it in state
async def email_preprocess(state):
    text = state['input_text']

    # change multiple whitespaces into 1
    text = re.sub(r'\s+',' ', text)

    state['input_text'] = text
    return state


# to check overall sentiment of text
async def email_check_sentiment(state):
    text = state['input_text']

    chain = check_sentiment_email_chain()

    sentiment = await chain.ainvoke({'text' : text})

    state['sentiment'] = sentiment
    return state


# function to divert flow to one direction either to positive or negative or neutral.
async def email_decide_flow(state) -> Literal['email_positive_response', 'email_run_diagnosis', 'email_neutral_response']:
    sentiment = state['sentiment']

    # it returns the name of next possible node based on sentiment
    if sentiment == 'positive':
        return 'email_positive_response'
    elif sentiment == 'negative':
        return 'email_run_diagnosis'
    elif sentiment == 'neutral':
        return 'email_neutral_response'
    else:
        raise ValueError(f"Unknown sentiment: {sentiment}")


# to run diagnosis
async def email_run_diagnose(state):
    text = state['input_text']

    chain = chain_to_run_diagnosis()
    diagnose = await chain.ainvoke({'text' : text})

    if 'email_data' not in state or state['email_data'] is None:
        state['email_data'] = {}

    state['email_data']['diagnose'] = diagnose.model_dump()

    return state


# to generate response for negative sentiment
async def email_generate_reply_for_negative_sentiment(state):
    text = state['input_text']

    issue_type = state['email_data']['diagnose']['issue_type']
    tone = state['email_data']['diagnose']['tone']
    urgency = state['email_data']['diagnose']['urgency']
    issue = state['email_data']['diagnose']['issue']

    chain = chain_for_negative_email()

    response = await chain.ainvoke({'email' : text,
                                    'issue_type' : issue_type,
                                    'tone' : tone,
                                    'urgency' : urgency,
                                    'issue' : issue})

    if 'email_data' not in state or state['email_data'] is None:
        state['email_data'] = {}

    state['email_data']['email_info'] = response.model_dump()
    state['reply'] = response.model_dump()
    return state


# to generate response for positive sentiment
async def email_generate_reply_for_positive_sentiment(state):
    text = state['input_text']

    chain = chain_for_positive_email()

    response = await chain.ainvoke({'email': text})

    if 'email_data' not in state or state['email_data'] is None:
        state['email_data'] = {}
    state['email_data']['email_info'] = response.model_dump()
    state['reply'] = response.model_dump()
    return state


# to generate response for positive sentiment
async def email_generate_reply_for_neutral_sentiment(state):
    text = state['input_text']

    chain = chain_for_neutral_email()

    response = await chain.ainvoke({'email': text})

    if 'email_data' not in state or state['email_data'] is None:
        state['email_data'] = {}
    state['email_data']['email_info'] = response.model_dump()
    state['reply'] = response.model_dump()
    return state


