from .config import co, DISCLAIMER
from .knowledge_base import LEGAL_FAQS

def get_legal_response(user_input: str) -> str:
    # Check knowledge base first
    for keyword, answer in LEGAL_FAQS.items():
        if keyword in user_input.lower():
            return answer + "\n\n" + DISCLAIMER

    # Cohere chat API call
    response = co.chat(
        model='command-r',
        message=user_input,
        temperature=0.3
    )

    generated_text = response.text.strip()
    return generated_text + "\n\n" + DISCLAIMER
