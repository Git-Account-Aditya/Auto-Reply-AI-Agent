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


# llm for input router node

def chain_input_router():
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""
            You are an intelligent classifier. Determine whether the following input text is an **email** or a **product/service review**.
            Analyze the structure, tone, and intent. Respond strictly with: **email** or **review**
            
            ### Examples:
            
            Text:
            "Dear Customer Support,  
            I recently purchased your SmartWatch Pro, but I’m experiencing syncing issues with my iPhone.  
            Could you please assist me in resolving this? I’ve attached screenshots for your reference.  
            Looking forward to your help.  
            
            Best regards,  
            Aditya Rawat"
            Return: email
            
            Text:
            "I wanted to check if you're available for a quick catch-up call this Friday regarding the Q3 updates.  
            Let me know your availability.  
            
            Thanks,  
            Priya"
            Return: email
            
            Text:
            "To whom it may concern,  
            I am writing to formally request a refund for order #44521, which was never delivered despite multiple follow-ups.  
            Please advise on the next steps.  
            
            Sincerely,  
            Rahul Verma"
            Return: email
            
            Text:
            "This is by far the worst vacuum cleaner I’ve ever bought. It’s noisy, clunky, and barely picks up anything from the carpet. Waste of money."
            Return: review
            
            Text:
            "Absolutely love the way this speaker sounds. Great bass, long battery life, and compact size make it perfect for outdoor use."
            Return: review
            
            Text:
            "I’ve been using this face cream for a month now and have noticed a significant difference in my skin texture. Highly recommended!"
            Return: review
            
            ### Classify the following:
            
            Text: {text}
            Return:
        """
    )

    chain = prompt | llm | parser
    return chain

