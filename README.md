# Automatic Reply Generator

An AI-powered agent built with **LangGraph** and **Groq API** that classifies text (email or review), detects sentiment, extracts key information, and generates professional replies. Now with **Gmail integration** for automated email processing with human-in-the-loop approval.

## 🔍 Features

- 📧 Detects whether the input is an email or a review
- 😊 Analyzes sentiment: Positive, Negative, Neutral
- 🧠 Extracts structured data like issue type, tone, urgency, and problem summary
- ✉️ Generates professional context-aware responses
- 📬 **NEW: Gmail integration** - Fetch unread emails and generate replies
- 👤 **Human-in-the-loop** - Approve replies before sending
- ⚡ Powered by **Groq API** for ultra-fast inference
- 🔁 LangGraph used for agentic flow and stateful graph design

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
- Gmail API
- AsyncIO for efficient event handling

---

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Git-Account-Aditya/Auto-Reply-AI-Agent.git
   cd Auto-Reply-AI-Agent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file:
   ```bash
   GROQ_API_KEY=your_groq_api_key
   ```

4. **For Gmail Integration (Optional):**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project and enable Gmail API
   - Create OAuth 2.0 credentials
   - Download as `credentials.json` and place in project root
   - **Note:** `credentials.json` is in `.gitignore` for security

5. **Run the app:**
   ```bash
   python app.py
   ```

## 🔒 Security Notes

- **Never commit `credentials.json`** - This file contains sensitive OAuth credentials
- **Never commit `token.json`** - This file contains your authentication tokens
- Both files are automatically ignored by `.gitignore`
- If you accidentally commit these files, immediately revoke the credentials in Google Cloud Console

## 🎯 Usage

### Manual Mode
Choose option 1 to enter text manually and see generated replies.

### Gmail Integration Mode
Choose option 2 to:
1. Fetch unread emails from Gmail
2. Generate AI-powered replies
3. Ask for human approval before sending
4. Send approved replies and mark originals as read
