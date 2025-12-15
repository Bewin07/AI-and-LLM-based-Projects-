import streamlit as st
import os
import tempfile
import sys
sys.path.append('src')

from src.dataprocessor import run as process_pdf
from src.QueryProcessor import process_user_query

# Page Config
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖", layout="wide")

# Custom CSS for "Awesome & Beautiful" Look
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Title Styling */
    h1 {
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 20px;
    }

    /* File Uploader */
    .stFileUploader > div > div > div > div {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px dashed #4a4a6a;
        border-radius: 12px;
    }
    
    /* Chat Message Bubbles */
    .user-message {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        padding: 12px 18px;
        border-radius: 20px 20px 0 20px;
        margin: 10px 0;
        text-align: right;
        float: right;
        clear: both;
        max-width: 70%;
        box-shadow: 0 4px 15px rgba(0, 210, 255, 0.3);
    }
    
    .bot-message {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        color: #e0e0e0;
        padding: 12px 18px;
        border-radius: 20px 20px 20px 0;
        margin: 10px 0;
        float: left;
        clear: both;
        max-width: 70%;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(90deg, #ff00cc 0%, #333399 100%);
        border: none;
        color: white;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
        transition: transform 0.2s;
        width: 100%;
        font-weight: 600;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        opacity: 0.9;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(30, 30, 46, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Main Title
st.markdown("<h1>✨ Intelligent Document Chat</h1>", unsafe_allow_html=True)

# Application Logic
def main():
    # Sidebar for File Upload
    with st.sidebar:
        st.header("📂 Upload Document")
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        
        if uploaded_file is not None:
            if st.button("Process Document"):
                with st.spinner("Processing... Chunking... Embedding..."):
                    # Save uploaded file to temp file
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                        tmp_file.write(uploaded_file.read())
                        tmp_path = tmp_file.name
                    
                    try:
                        # process_pdf with the temp file path
                        process_pdf(tmp_path)
                        st.success("✅ Document processed and added to Knowledge Base!")
                    except Exception as e:
                        st.error(f"Error processing file: {e}")
                    finally:
                        # Cleanup temp file
                        if os.path.exists(tmp_path):
                            os.remove(tmp_path)

    # Main Chat Interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="bot-message">{message["content"]}</div>', unsafe_allow_html=True)
            # st.markdown(f'<div style="clear:both; font-size: 0.8em; color: gray; margin-left: 20px;">Context Used: {message.get("context", "")[:100]}...</div>', unsafe_allow_html=True)

    # Chat Input
    query = st.chat_input("Ask something about your document...")
    
    if query:
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": query})
        st.markdown(f'<div class="user-message">{query}</div>', unsafe_allow_html=True)
        
        with st.spinner("Thinking..."):
            try:
                response, context = process_user_query(query)
                
                # Add bot response to history
                st.session_state.messages.append({"role": "assistant", "content": response, "context": context})
                st.markdown(f'<div class="bot-message">{response}</div>', unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error generating response: {e}")

if __name__ == "__main__":
    main()
