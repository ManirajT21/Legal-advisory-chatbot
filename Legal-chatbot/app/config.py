import cohere
from dotenv import load_dotenv
from .key import API_KEY

load_dotenv()

co = cohere.Client(API_KEY)

DISCLAIMER = (
    "⚠️ Disclaimer: This chatbot provides general legal information only "
    "and is not a substitute for professional legal advice. "
    "For specific legal issues, please consult a qualified attorney."
)
