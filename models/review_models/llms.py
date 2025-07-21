from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from pydantic import BaseModel, Field
from typing import TypedDict, Literal

import os
from dotenv import load_dotenv

load_dotenv()

groq_api = os.getenv('GROQ_API_KEY')

parser = StrOutputParser()

llm = ChatGroq(model = 'llama-3.3-70b-versatile',
               api_key = groq_api)


# --------------- Structured Output Class
class DiagnoseReview(BaseModel):
    issue_type : str = Field(description='Identify the type of issue discussed in text')
    tone : str = Field(description='Identify the tone in the message.')
    urgency : Literal['low', 'medium', 'high'] = Field(description='Identify the urgency to resolve issue.')


# llm to predict sentiment for reviews
def check_sentiment_review_chain():
    prompt = PromptTemplate(
        input_variables=['text'],
        template='''
        You are a sentiment analysis assistant.
        Just return the sentiment, no other text.
        Your task is to classify the sentiment of the review as one of the following:
        - positive
        - negative
        - neutral

        Examples:
        Review: "I absolutely love this product! It exceeded my expectations."  
        Sentiment: positive

        Review: "The service was average, nothing special."  
        Sentiment: neutral

        Review: "I'm disappointed. The item arrived broken and customer service was unhelpful."  
        Sentiment: negative

        Review: {text}

        Sentiment:
    '''
    )
    chain = prompt | llm | parser
    return chain


# # llm to predict sentiment for email
# def check_sentiment_email_chain():
#     prompt = PromptTemplate('''
#         You have to identify the sentiment in this email text.
#
#         Text : {text}
#
#         Sentiment : choose from (positive, negative, neutral)
#     ''')
#     chain = prompt | llm | parser
#     return chain


# chain to run diagnosis on negative reviews
def chain_to_run_diagnosis():
    structured_model = llm.with_structured_output(DiagnoseReview)

    prompt = PromptTemplate(
        input_variables=['text'],
        template='''
        You are a helpful assistant diagnosing a negative product or service review.
        
        Your task is to extract:
        - issue_type: Short one-word category (e.g., "delivery", "quality", "support")
        - tone: Overall tone of user (e.g., "angry", "frustrated", "disappointed")
        - urgency: Response urgency as "low", "medium", or "high"
        
        Examples:
        
        Review: "I ordered a phone and it arrived 4 days late. Very frustrating experience."
        Output: {{"issue_type": "delivery", "tone": "frustrated", "urgency": "medium"}}
        
        Review: "The support team never picked up my call. I’m really angry about this."
        Output: {{"issue_type": "support", "tone": "angry", "urgency": "high"}}
        
        Review: "The material quality is not good. Not what I expected for the price."
        Output: {{"issue_type": "quality", "tone": "disappointed", "urgency": "low"}}
        
        Review: {text}
        
        Return a JSON with keys: issue_type, tone, urgency.
    '''
    )

    chain = prompt | structured_model
    return chain


# chain to generate reply for negative reviews
def chain_for_negative_reviews():
    prompt = PromptTemplate(
        input_variables=['review', 'issue_type', 'tone', 'urgency'],
        template='''
        You are a professional assistant responding to a negative review. Your response should be empathetic and helpful.
        
        Details to consider:
        Review: {review}
        Issue Type: {issue_type}
        User Tone: {tone}
        Urgency: {urgency}
        
        Examples:
        
        Review: "I waited a week for my order to arrive and still nothing."
        Issue Type: delivery
        Tone: frustrated
        Urgency: high
        
        Response:
        We truly apologize for the delay in your order. We understand how frustrating this can be. Our team is already working on prioritizing your delivery, and we’ll ensure it reaches you as soon as possible. Thank you for your patience.
        
        ---
        
        Review: "Customer support was unhelpful and didn’t resolve my issue."
        Issue Type: support
        Tone: angry
        Urgency: medium
        
        Response:
        We’re very sorry for the inconvenience caused. Your experience is not what we aim for, and we’re escalating this to our support lead immediately. Someone will reach out to you shortly to resolve the issue.
        
        ---
        
        Review: {review}
        Issue Type: {issue_type}
        Tone: {tone}
        Urgency: {urgency}
        
        Response:
    '''
    )

    chain = prompt | llm | parser
    return chain


# chain to generate reply for positive reviews
def chain_for_positive_reviews():
    prompt = PromptTemplate(
        input_variables=['review'],
        template='''
        You are a friendly assistant replying to positive reviews. Show appreciation and encourage further feedback.
        
        Examples:
        
        Review: "Great service and fast delivery!"
        Response:
        Thank you so much for your kind words! We’re thrilled to hear you enjoyed the service. If there’s anything else we can do for you, or any suggestions you’d like to share, we’re all ears!
        
        ---
        
        Review: "Loved the product. It works exactly as described."
        Response:
        We really appreciate your feedback! It’s great to know the product met your expectations. Feel free to let us know how we can serve you even better in the future.
        
        ---
        
        Review: {review}
        
        Response:
    '''
    )

    chain = prompt | llm | parser
    return chain


# chain to generate neutral response to user
def chain_for_neutral_reviews():
    prompt = PromptTemplate(
        input_variables=['review'],
        template='''
        You are a support assistant responding to a neutral review. Acknowledge the user and encourage feedback for improvements.
        
        Examples:
        
        Review: "The product is okay. Nothing special."
        Response:
        Thank you for your honest feedback. We’re always working to improve and would love to hear any suggestions you might have.
        
        ---
        
        Review: "Not bad, but could be better."
        Response:
        We appreciate your review. If there’s anything specific we could improve, feel free to share — your input helps us grow.
        
        ---
        
        Review: {review}
        
        Response:
    '''
    )
    chain = prompt | llm | parser
    return chain

