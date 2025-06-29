# Legal-advisory-chatbot

Project-File-Structure

A fully functional legal chatbot built using:

1. Flask API (Backend)
2. Cohere LLM API (Language Model)
3. Streamlit (Frontend UI)

Legal-chatbot/
│
├── app/
│   ├── __init__.py
│   ├── chatbot.py           # LLM and knowledge base handler
│   ├── config.py            # API key and Cohere setup
│   ├── key.py               # API key storage
│   ├── knowledge_base.py    # Predefined legal FAQs
│   ├── main.py              # Flask backend
│
├── frontend/
│   └── streamlit_app.py     # Streamlit chat UI
│
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

setup-Instructions

1. Clone the Repository:

git clone https://github.com/yourusername/legal-chatbot.git
cd legal-chatbot

2. Create and Activate Virtual Environment:

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

3. Install required Packages:

pip install -r requirements.txt

4. Add Cohere API - Key

COHERE_API_KEY = "your_cohere_api_key_here"

Get your own api key from cohere
https://docs.cohere.com/v2/reference/about

Running Application

1. Start Flask Backend:

python -m app.main

2. Start streamlit frontend:

streamlit run frontend/streamlit_app.py

Api Testing

1. POST /chat Endpoint:

curl.exe -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d "{\"query\":\"What is a contract?\"}"

2. Example Responses:

{
  "response": "A contract requires an offer, acceptance, and consideration to be legally binding.\n\n⚠️ Disclaimer: This chatbot provides general legal information only and is not a substitute for professional legal advice. For specific legal issues, please consult a qualified attorney."
}


