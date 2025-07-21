# Automatic Reply Generator

An AI-powered agent built with **LangGraph** and **Groq API** that classifies text (email or review), detects sentiment, extracts key information, and generates professional replies. Designed for high-speed, scalable automation of customer communications.

---

## 🔍 Features

- 📧 Detects whether the input is an email or a review
- 😊 Analyzes sentiment: Positive, Negative, Neutral
- 🧠 Extracts structured data like issue type, tone, urgency, and problem summary
- ✉️ Generates professional context-aware responses
- ⚡ Powered by **Groq API** for ultra-fast inference
- 🔁 LangGraph used for agentic flow and stateful graph design

---

## 📦 Tech Stack

- Python
- [LangGraph](https://docs.langgraph.dev/)
- [LangChain](https://docs.langchain.com/)
- Groq API 
- AsyncIO for efficient event handling

---

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Git-Account-Aditya/Auto-Reply-AI-Agent.git
   
2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    Set your API key:

3. **Create a .env file:**
    ```bash
    GROQ_API_KEY=your_groq_api_key

4. **Run the app:**

    ```bash
    python main.py
