import streamlit as st
import requests
import datetime
import time

# Configure page
st.set_page_config(
    page_title="Legal Advisory Chatbot",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

def apply_theme():
    if st.session_state.theme == "dark":
        st.markdown("""
        <style>
        .stApp {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        /* Chat Messages */
        .chat-container {
            max-height: 60vh;
            overflow-y: auto;
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .user-message {
            background: linear-gradient(135deg, #0084ff, #0066cc);
            color: white;
            padding: 12px 16px;
            border-radius: 18px 18px 4px 18px;
            margin: 8px 0 8px auto;
            max-width: 75%;
            display: block;
            text-align: left;
            font-size: 15px;
            line-height: 1.4;
            box-shadow: 0 2px 8px rgba(0, 132, 255, 0.3);
        }
        
        .bot-message {
            background-color: #404040;
            color: #ffffff;
            padding: 12px 16px;
            border-radius: 18px 18px 18px 4px;
            margin: 8px auto 8px 0;
            max-width: 75%;
            display: block;
            font-size: 15px;
            line-height: 1.4;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        /* Typing Animation */
        .typing-indicator {
            background-color: #404040;
            color: #ffffff;
            padding: 12px 16px;
            border-radius: 18px 18px 18px 4px;
            margin: 8px auto 8px 0;
            max-width: 75px;
            display: block;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
        }
        
        .typing-dots {
            display: flex;
            align-items: center;
            height: 20px;
        }
        
        .typing-dots span {
            height: 8px;
            width: 8px;
            background-color: #888;
            border-radius: 50%;
            display: inline-block;
            margin: 0 2px;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dots span:nth-child(1) {
            animation-delay: -0.32s;
        }
        
        .typing-dots span:nth-child(2) {
            animation-delay: -0.16s;
        }
        
        @keyframes typing {
            0%, 80%, 100% {
                transform: scale(0.8);
                opacity: 0.5;
            }
            40% {
                transform: scale(1);
                opacity: 1;
            }
        }
        
        /* Input Section */
        .input-container {
            position: sticky;
            bottom: 0;
            background-color: #1e1e1e;
            padding: 20px;
            border-top: 1px solid #404040;
        }
        
        .stTextInput > div > div > input {
            background-color: #2d2d2d !important;
            border: 2px solid #404040 !important;
            border-radius: 25px !important;
            color: #ffffff !important;
            padding: 12px 20px !important;
            font-size: 16px !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #0084ff !important;
            box-shadow: 0 0 0 2px rgba(0, 132, 255, 0.2) !important;
        }
        
        .stButton > button {
            background: linear-gradient(135deg, #0084ff, #0066cc) !important;
            color: white !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 12px 24px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            width: 100% !important;
            margin-top: 10px !important;
            transition: all 0.3s ease !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #0066cc, #0052a3) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(0, 132, 255, 0.3) !important;
        }
        
        /* Sidebar */
        .sidebar .element-container {
            background-color: #2d2d2d;
        }
        
        .chat-item {
            background-color: #404040;
            border-radius: 12px;
            padding: 12px;
            margin: 8px 0;
            cursor: pointer;
            border: 1px solid #555555;
            transition: all 0.3s ease;
        }
        
        .chat-item:hover {
            background-color: #505050;
            transform: translateX(5px);
        }
        
        .new-chat-btn {
            background: linear-gradient(135deg, #0084ff, #0066cc) !important;
            color: white !important;
            border: none !important;
            padding: 12px 20px !important;
            border-radius: 12px !important;
            width: 100% !important;
            margin-bottom: 20px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
        }
        
        .theme-toggle {
            background-color: #404040 !important;
            color: white !important;
            border: 1px solid #555555 !important;
            padding: 8px 12px !important;
            border-radius: 8px !important;
            margin-bottom: 10px !important;
            transition: all 0.3s ease !important;
        }
        
        /* Welcome screen */
        .welcome-container {
            text-align: center;
            padding: 60px 20px;
            color: #888888;
        }
        
        .welcome-container h2 {
            color: #ffffff;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp {
            background-color: #f8f9fa;
            color: #212529;
        }
        
        /* Main content area */
        .main .block-container {
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            margin-top: 20px;
        }
        
        /* Chat Messages */
        .chat-container {
            max-height: 60vh;
            overflow-y: auto;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #ffffff;
        }
        
        .user-message {
            background: linear-gradient(135deg, #007bff, #0056b3);
            color: white;
            padding: 12px 16px;
            border-radius: 18px 18px 4px 18px;
            margin: 8px 0 8px auto;
            max-width: 75%;
            display: block;
            text-align: left;
            font-size: 15px;
            line-height: 1.4;
            box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3);
            font-weight: 500;
        }
        
        .bot-message {
            background-color: #e9ecef;
            color: #212529;
            padding: 12px 16px;
            border-radius: 18px 18px 18px 4px;
            margin: 8px auto 8px 0;
            max-width: 75%;
            display: block;
            font-size: 15px;
            line-height: 1.4;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border: 1px solid #dee2e6;
            font-weight: 500;
        }
        
        /* Typing Animation */
        .typing-indicator {
            background-color: #e9ecef;
            color: #212529;
            padding: 12px 16px;
            border-radius: 18px 18px 18px 4px;
            margin: 8px auto 8px 0;
            max-width: 75px;
            display: block;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            border: 1px solid #dee2e6;
        }
        
        .typing-dots {
            display: flex;
            align-items: center;
            height: 20px;
        }
        
        .typing-dots span {
            height: 8px;
            width: 8px;
            background-color: #6c757d;
            border-radius: 50%;
            display: inline-block;
            margin: 0 2px;
            animation: typing 1.4s infinite ease-in-out;
        }
        
        .typing-dots span:nth-child(1) {
            animation-delay: -0.32s;
        }
        
        .typing-dots span:nth-child(2) {
            animation-delay: -0.16s;
        }
        
        @keyframes typing {
            0%, 80%, 100% {
                transform: scale(0.8);
                opacity: 0.5;
            }
            40% {
                transform: scale(1);
                opacity: 1;
            }
        }
        
        /* Input Section */
        .input-container {
            position: sticky;
            bottom: 0;
            background-color: #ffffff;
            padding: 20px;
            border-top: 2px solid #e9ecef;
            box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
        }
        
        /* Input field styling */
        .stTextInput > div > div > input {
            background-color: #ffffff !important;
            border: 2px solid #ced4da !important;
            border-radius: 25px !important;
            color: #212529 !important;
            padding: 14px 20px !important;
            font-size: 16px !important;
            font-weight: 500 !important;
            box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #6c757d !important;
            opacity: 1 !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #007bff !important;
            box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25) !important;
            outline: none !important;
        }
        
        /* Input label */
        .stTextInput > label {
            color: #495057 !important;
            font-weight: 600 !important;
            font-size: 14px !important;
            margin-bottom: 8px !important;
        }
        
        /* Send button styling */
        .stButton > button {
            background: linear-gradient(135deg, #007bff, #0056b3) !important;
            color: white !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 14px 24px !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            width: 100% !important;
            margin-top: 12px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 8px rgba(0, 123, 255, 0.3) !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #0056b3, #004085) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0, 123, 255, 0.4) !important;
        }
        
        .stButton > button:disabled {
            background: #6c757d !important;
            cursor: not-allowed !important;
            transform: none !important;
            box-shadow: none !important;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f8f9fa !important;
        }
        
        .chat-item {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 12px;
            margin: 8px 0;
            cursor: pointer;
            border: 1px solid #dee2e6;
            transition: all 0.3s ease;
            color: #212529;
            font-weight: 500;
        }
        
        .chat-item:hover {
            background-color: #e9ecef;
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Sidebar buttons */
        .css-1d391kg .stButton > button {
            background: linear-gradient(135deg, #007bff, #0056b3) !important;
            color: white !important;
            border: none !important;
            padding: 12px 20px !important;
            border-radius: 12px !important;
            width: 100% !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 6px rgba(0, 123, 255, 0.3) !important;
        }
        
        .css-1d391kg .stButton > button:hover {
            background: linear-gradient(135deg, #0056b3, #004085) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 10px rgba(0, 123, 255, 0.4) !important;
        }
        
        /* Theme toggle button */
        .theme-toggle {
            background-color: #ffffff !important;
            color: #212529 !important;
            border: 2px solid #dee2e6 !important;
            padding: 10px 16px !important;
            border-radius: 10px !important;
            margin-bottom: 15px !important;
            transition: all 0.3s ease !important;
            font-weight: 600 !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
        }
        
        .theme-toggle:hover {
            background-color: #e9ecef !important;
            border-color: #adb5bd !important;
            transform: translateY(-1px) !important;
        }
        
        /* Sidebar text styling */
        .css-1d391kg h3 {
            color: #212529 !important;
            font-weight: 700 !important;
        }
        
        .css-1d391kg p, .css-1d391kg em {
            color: #6c757d !important;
        }
        
        /* Welcome screen */
        .welcome-container {
            text-align: center;
            padding: 60px 20px;
            color: #6c757d;
            background-color: #ffffff;
            border-radius: 12px;
            margin: 20px 0;
        }
        
        .welcome-container h2 {
            color: #212529;
            margin-bottom: 15px;
            font-weight: 700;
        }
        
        .welcome-container p {
            color: #495057;
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        
        .welcome-container strong {
            color: #007bff;
        }
        
        /* Page title */
        h1 {
            color: #212529 !important;
            font-weight: 700 !important;
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #c1c1c1;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #a8a8a8;
        }
        </style>
        """, unsafe_allow_html=True)

def create_new_chat():
    chat_id = f"chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    st.session_state.current_chat_id = chat_id
    st.session_state.messages = []
    st.rerun()

def load_chat(chat_id):
    st.session_state.current_chat_id = chat_id
    st.session_state.messages = st.session_state.chat_history.get(chat_id, [])
    st.rerun()

def save_current_chat():
    if st.session_state.current_chat_id and st.session_state.messages:
        st.session_state.chat_history[st.session_state.current_chat_id] = st.session_state.messages.copy()

def delete_chat(chat_id):
    if chat_id in st.session_state.chat_history:
        del st.session_state.chat_history[chat_id]
        if st.session_state.current_chat_id == chat_id:
            st.session_state.current_chat_id = None
            st.session_state.messages = []
        st.rerun()

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
    st.rerun()

def show_typing_animation():
    """Display typing animation"""
    return st.markdown("""
    <div class="typing-indicator">
        <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def submit():
    user_input = st.session_state.user_input.strip()
    if not user_input:
        return

    # Create new chat if none exists
    if not st.session_state.current_chat_id:
        create_new_chat()

    # Append user message
    st.session_state.messages.append({"sender": "user", "text": user_input})
    
    # Save chat immediately
    save_current_chat()
    
    # Clear input box
    st.session_state.user_input = ""
    
    # Set typing state
    st.session_state.is_typing = True
    
    # Rerun to show the user message and typing indicator
    st.rerun()

def get_bot_response():
    """Get bot response and handle the API call"""
    if st.session_state.is_typing and st.session_state.messages:
        last_message = st.session_state.messages[-1]
        if last_message["sender"] == "user":
            try:
                res = requests.post("http://localhost:5000/chat", json={"query": last_message["text"]})
                if res.ok:
                    answer = res.json().get("response", "Sorry, no response.")
                else:
                    answer = f"Error: {res.status_code}"
            except Exception as e:
                answer = f"Error: {e}"
            
            # Add bot response
            st.session_state.messages.append({"sender": "bot", "text": answer})
            st.session_state.is_typing = False
            
            # Save chat
            save_current_chat()
            
            # Rerun to show bot response
            st.rerun()

# Apply theme
apply_theme()

# Sidebar
with st.sidebar:
    st.markdown("### ⚖️ Legal Advisory")
    
    # Theme toggle
    theme_icon = "🌙" if st.session_state.theme == "dark" else "☀️"
    theme_text = "Light Mode" if st.session_state.theme == "dark" else "Dark Mode"
    if st.button(f"{theme_icon} {theme_text}", key="theme_toggle", use_container_width=True):
        toggle_theme()
    
    st.markdown("---")
    
    # New chat button
    if st.button("✨ New Chat", key="new_chat", help="Start a new conversation", use_container_width=True):
        create_new_chat()
    
    st.markdown("---")
    
    # Chat history
    st.markdown("### 💬 Chat History")
    
    if st.session_state.chat_history:
        for chat_id in reversed(list(st.session_state.chat_history.keys())):
            chat_messages = st.session_state.chat_history[chat_id]
            if chat_messages:
                # Get first user message as title
                first_message = next((msg for msg in chat_messages if msg["sender"] == "user"), None)
                title = first_message["text"][:35] + "..." if first_message and len(first_message["text"]) > 35 else (first_message["text"] if first_message else "Empty Chat")
                
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.button(f"💬 {title}", key=f"load_{chat_id}", help="Load this conversation", use_container_width=True):
                        load_chat(chat_id)
                with col2:
                    if st.button("🗑️", key=f"delete_{chat_id}", help="Delete this chat"):
                        delete_chat(chat_id)
    else:
        st.markdown("*No previous chats*")

# Main content area
col1, col2, col3 = st.columns([1, 6, 1])

with col2:
    # Title
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>⚖️ Legal Advisory Chatbot</h1>", unsafe_allow_html=True)
    
    # Chat messages container
    chat_container = st.container()
    
    with chat_container:
        if st.session_state.messages:
            # Display all messages
            for msg in st.session_state.messages:
                if msg["sender"] == "user":
                    st.markdown(f'<div class="user-message">{msg["text"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="bot-message">{msg["text"]}</div>', unsafe_allow_html=True)
            
            # Show typing animation if bot is typing
            if st.session_state.is_typing:
                show_typing_animation()
                # Auto-trigger bot response
                get_bot_response()
                
        else:
            # Welcome screen
            st.markdown("""
            <div class="welcome-container">
                <h2>👋 Welcome to Legal Advisory</h2>
                <p>I'm here to help you with legal questions and provide guidance.</p>
                <p>Ask me anything about law, legal procedures, or get advice on legal matters.</p>
                <p><strong>Start by typing your question below!</strong></p>
            </div>
            """, unsafe_allow_html=True)
    
    # Spacer to push input to bottom
    st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
    
    # Input section - Fixed at bottom
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    
    # Text input with visible label
    st.text_input(
        "💬 Ask your legal question:", 
        key="user_input", 
        on_change=submit, 
        placeholder="Type your message here and press Enter to send...",
        help="Enter your legal question or concern here"
    )
    
    # Send button below input
    st.button("📤 Send Message", on_click=submit, use_container_width=True, disabled=st.session_state.is_typing)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-scroll script
st.markdown("""
<script>
setTimeout(function() {
    window.parent.document.querySelector('section.main').scrollTop = window.parent.document.querySelector('section.main').scrollHeight;
}, 100);
</script>
""", unsafe_allow_html=True)