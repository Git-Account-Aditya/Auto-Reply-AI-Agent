import re
from typing import Literal
from .llms import (check_sentiment_review_chain, chain_to_run_diagnosis, chain_for_negative_reviews,
                   chain_for_positive_reviews, chain_for_neutral_reviews)


# to extract information from text and store it in state
async def preprocess(state):
    text = state['input_text']

    # change multiple whitespaces into 1
    text = re.sub(r'\s+',' ', text)

    state['input_text'] = text
    return state


# to check overall sentiment of text
async def check_sentiment(state):
    text = state['input_text']

    chain = check_sentiment_review_chain()

    sentiment = await chain.ainvoke({'text' : text})
    print(sentiment)

    state['sentiment'] = sentiment
    return state


# function to divert flow to one direction either to positive or negative or neutral.
async def decide_flow(state) -> Literal['review_positive_response', 'review_run_diagnosis', 'review_neutral_response']:
    sentiment = state['sentiment']

    # it returns the name of next possible node based on sentiment
    if sentiment == 'positive':
        return 'review_positive_response'
    elif sentiment == 'negative':
        return 'review_run_diagnosis'
    elif sentiment == 'neutral':
        return 'review_neutral_response'
    else:
        raise ValueError(f"Unknown sentiment: {sentiment}")


# to run diagnosis
async def run_diagnose(state):
    text = state['input_text']

    chain = chain_to_run_diagnosis()
    diagnose = await chain.ainvoke({'text' : text})

    if 'review_data' not in state or state['review_data'] is None:
        state['review_data'] = {}
    state['review_data']['diagnose'] = diagnose.model_dump()

    return state


# to generate response for negative sentiment
async def generate_reply_for_negative_sentiment(state):
    text = state['input_text']

    issue_type = state['review_data']['diagnose']['issue_type']
    tone = state['review_data']['diagnose']['tone']
    urgency = state['review_data']['diagnose']['urgency']

    chain = chain_for_negative_reviews()

    response = await chain.ainvoke({'review' : text,
                                    'issue_type' : issue_type,
                                    'tone' : tone,
                                    'urgency' : urgency})
    if 'review_data' not in state or state['review_data'] is None:
        state['review_data'] = {}
    state['review_data']['response'] = response
    state['reply'] = response
    return state


# to generate response for positive sentiment
async def generate_reply_for_positive_sentiment(state):
    text = state['input_text']

    chain = chain_for_positive_reviews()

    response = await chain.ainvoke({'review': text})

    if 'review_data' not in state or state['review_data'] is None:
        state['review_data'] = {}
    state['review_data']['response'] = response
    state['reply'] = response
    return state


# to generate response for positive sentiment
async def generate_reply_for_neutral_sentiment(state):
    text = state['input_text']

    chain = chain_for_neutral_reviews()

    response = await chain.ainvoke({'review': text})

    if 'review_data' not in state or state['review_data'] is None:
        state['review_data'] = {}
    state['review_data']['response'] = response
    state['reply'] = response
    return state


