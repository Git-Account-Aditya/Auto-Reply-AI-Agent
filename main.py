from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from langgraph.graph import StateGraph
from langgraph.graph import START, END

import os
from dotenv import load_dotenv
from typing import TypedDict, Optional, Literal
from pydantic import BaseModel, Field
import asyncio


# node imports
from models.email_models.nodes import (email_preprocess, email_check_sentiment, email_decide_flow, email_run_diagnose,
                                       email_generate_reply_for_positive_sentiment,
                                       email_generate_reply_for_negative_sentiment,
                                       email_generate_reply_for_neutral_sentiment)
from models.review_models.nodes import (preprocess, check_sentiment, run_diagnose, decide_flow,
                                        generate_reply_for_positive_sentiment, generate_reply_for_negative_sentiment,
                                        generate_reply_for_neutral_sentiment)
from models.input_router import check_input_type, data_router


# unify states
class UnifiedState(TypedDict):
    input_text: str
    input_type: Optional[Literal["review", "email"]]
    sentiment: Optional[Literal["positive", "negative", "neutral"]]
    review_data: Optional[dict]
    email_data: Optional[dict]
    reply: Optional[str]


# create graph
graph = StateGraph(state_schema=UnifiedState)

# add nodes
graph.add_node('identify input type', check_input_type)

# ------- adding nodes of review branch
graph.add_node('review_preprocess', preprocess)
graph.add_node('review_sentiment_check', check_sentiment)
graph.add_node('review_positive_response', generate_reply_for_positive_sentiment)

graph.add_node('review_run_diagnosis', run_diagnose)
graph.add_node('review_negative_response', generate_reply_for_negative_sentiment)

graph.add_node('review_neutral_response', generate_reply_for_neutral_sentiment)

# ------- adding nodes of email branch
graph.add_node('email_preprocess', email_preprocess)
graph.add_node('email_sentiment_check', email_check_sentiment)
graph.add_node('email_positive_response', email_generate_reply_for_positive_sentiment)

graph.add_node('email_run_diagnosis', email_run_diagnose)
graph.add_node('email_negative_response', email_generate_reply_for_negative_sentiment)

graph.add_node('email_neutral_response', email_generate_reply_for_neutral_sentiment)

# add edges
graph.add_edge(START, 'identify input type')

# ------- first conditional edge
graph.add_conditional_edges('identify input type', data_router)

# ======= adding edges to review branch
graph.add_edge('review_preprocess', 'review_sentiment_check')

# ------- second conditional edge
graph.add_conditional_edges('review_sentiment_check', decide_flow)

# ======= continue adding edges to review branch
graph.add_edge('review_positive_response', END)

graph.add_edge('review_run_diagnosis', 'review_negative_response')
graph.add_edge('review_negative_response', END)

graph.add_edge('review_neutral_response', END)

# ======= adding edges to email branch
graph.add_edge('email_preprocess', 'email_sentiment_check')

# ------- third conditional edge
graph.add_conditional_edges('email_sentiment_check', email_decide_flow)

# ======= continue adding edges to email branch
graph.add_edge('email_positive_response', END)

graph.add_edge('email_run_diagnosis', 'email_negative_response')
graph.add_edge('email_negative_response', END)

graph.add_edge('email_neutral_response', END)


# create final agent
agent = graph.compile()


async def run_agent(text: str):
    result = await agent.ainvoke({'input_text' : text})
    # print(result)
    return result


if __name__ == "__main__":
    test = '''
        Subject: Excellent Delivery Experience

        Hi Team,

        Just wanted to share my feedback. The recent order was delivered ahead of schedule and in perfect condition. It’s always a pleasure ordering from your platform.

        Keep up the great work!

        Regards,  
        Aditya Rawat

        '''
    asyncio.run(run_agent(test))




