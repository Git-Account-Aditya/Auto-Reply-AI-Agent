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

llm = ChatGroq(model='llama-3.3-70b-versatile',
               api_key=groq_api)


# --------------- Structured Output Classes
class DiagnoseEmail(BaseModel):
    issue_type : str = Field(description='Identify the type of issue discussed in text')
    tone: str = Field(description='Identify the tone in the message.')
    urgency: Literal['low', 'medium', 'high'] = Field(description='Identify the urgency to resolve issue.')
    issue: str = Field(description='Identify the actual issue from the given text')


class EmailSchema(BaseModel):
    to : str = Field(description='email id of the person.')
    subject : str = Field(description='subject of the mail.')
    body : str = Field(description='main body of the mail.')


# llm to predict sentiment for email
def check_sentiment_email_chain():
    prompt = PromptTemplate(
        input_variables=["text"],
        template='''
            You are an expert at analyzing the sentiment of email texts.
            Just return the sentiment, no other text.
            Label the sentiment as one of the following:
            - positive
            - negative
            - neutral
            
            ### Examples:
            
            Text: "Thank you so much for resolving my issue quickly. I appreciate your support."
            Sentiment: positive
            
            Text: "Why is your support team not replying to my emails? I'm frustrated and disappointed."
            Sentiment: negative
            
            Text: "I submitted a request last week regarding my account status. Please update me."
            Sentiment: neutral
            
            Now classify this:
            
            Text: "{text}"  
            Sentiment:
        ''')
    chain = prompt | llm | parser
    return chain


# chain to run diagnosis on negative emails
def chain_to_run_diagnosis():
    structured_model = llm.with_structured_output(DiagnoseEmail)

    prompt = PromptTemplate(
        input_variables=["text"],
        template='''
            You are diagnosing a **negative email**.  
            Extract the following details:
            - issue_type: e.g., account_problem, refund_request, service_complaint, delay_issue
            - tone: e.g., angry, frustrated, disappointed, assertive
            - urgency: low, medium, high
            - issue: a short summary of the issue in user's words
            
            ### Example:
            
            Email: "I’ve been charged twice for the same order and no one is replying to my complaint. This is unacceptable."
            issue_type: refund_request  
            tone: angry  
            urgency: high  
            issue: charged twice for the same order and no response
            
            Now analyze this:
            
            Email: "{text}"
        '''
    )
    chain = prompt | structured_model
    return chain


# chain to generate reply for negative email
def chain_for_negative_email():
    prompt = PromptTemplate(
        input_variables=["email", "issue_type", "tone", "urgency", "issue"],
        template='''
            You are a support assistant. Write a **professional, empathetic reply** to the user's negative email.
            
            - Acknowledge their issue.
            - Apologize if needed.
            - Mention the issue_type and urgency.
            - Maintain a calm and respectful tone.
            - Suggest next steps or resolution.
            
            ### Example:
            
            email: "Why am I being overcharged again? This keeps happening and I’m tired of it."
            issue type: billing_error  
            tone: frustrated  
            urgency: high  
            issue: being overcharged repeatedly
            
            Response:
            
            Dear User,  
            We sincerely apologize for the repeated overcharging issue you've encountered. This is not the experience we aim to provide. Our team has escalated this billing_error to our finance department and marked it as high urgency. You will receive an update within 24 hours.  
            Thank you for your patience.
            
            Now respond to:
            
            email: {email}  
            issue type: {issue_type}  
            tone of user: {tone}  
            urgency to reply: {urgency}  
            issue: {issue}
        ''')

    structured_email = llm.with_structured_output(EmailSchema)
    chain = prompt | structured_email
    return chain


# chain to generate reply for positive email
def chain_for_positive_email():
    prompt = PromptTemplate(
        input_variables=["email"],
        template='''
            You are a support assistant. Write a **friendly and positive** reply to the user's positive email.  
            - Thank them.
            - Express appreciation.
            - Ask for feedback politely.
            
            ### Example:
            
            email: "Just wanted to say thanks — your service was excellent!"
            response:
            Dear User,  
            Thank you so much for your kind words! We’re thrilled to hear you’re happy with our service. If you have a moment, we’d love to hear your feedback to help us serve you even better.
            
            Now respond to this email:
            {email}
            response:
        ''')

    structured_email = llm.with_structured_output(EmailSchema)
    chain = prompt | structured_email
    return chain


# chain to generate neutral email to user
def chain_for_neutral_email():
    prompt = PromptTemplate(
        input_variables=["email"],
        template='''
            You are a support assistant. Write a **neutral and helpful** reply to the user's email.  
            - Answer with clarity.
            - Avoid emotional or expressive language.
            
            ### Example:
            
            email: "I requested a refund last week. Can you tell me the status?"
            response:
            Dear User,  
            Your refund request is currently under review. We will update you within 2 business days. Thank you for your patience.
            
            Now respond to this email:
            {email}
            response:
        ''')

    structure_email = llm.with_structured_output(EmailSchema)
    chain = prompt | structure_email
    return chain

