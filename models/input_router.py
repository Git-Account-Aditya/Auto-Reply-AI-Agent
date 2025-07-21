from .input_router_chain import chain_input_router
from typing import Literal


# function to separate emails and reviews
async def check_input_type(state):
    text = state['input_text']

    chain = chain_input_router()

    response = await chain.ainvoke({'text' : text})

    # store response in state
    state['input_type'] = response

    return state


async def data_router(state) -> Literal['email_preprocess', 'review_preprocess']:
    text_type = state['input_type']

    if text_type == 'email':
        return 'email_preprocess'
    elif text_type == 'review':
        return 'review_preprocess'
    else:
        raise ValueError(f"Unknown type: {text_type}")





