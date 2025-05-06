import streamlit as st
import requests
import json
import pandas as pd
import io
import docx
import PyPDF2
import base64
import json
from datetime import datetime
import uuid

# Set page config
st.set_page_config(
    page_title="Prospect AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling the chat interface
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem; 
        border-radius: 0.5rem; 
        margin-bottom: 1rem; 
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #f0f2f6;
    }
    .chat-message.bot {
        background-color: #e6f3ff;
    }
    .chat-message .message-content {
        display: flex;
        flex-direction: column;
    }
    .chat-message .avatar {
        width: 2.5rem;
        height: 2.5rem;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-message .message {
        color: #333;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = {}
if 'n8n_webhook_url' not in st.session_state:
    st.session_state.n8n_webhook_url = ""
# Add session_id to session state if not present
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Sidebar configuration
with st.sidebar:
    st.title("AI Chatbot Settings")
    
    # N8N Webhook URL Configuration
    st.session_state.n8n_webhook_url = st.text_input(
        "N8N Webhook URL",
        value=st.session_state.n8n_webhook_url,
        help="Enter the URL of your n8n webhook"
    )
    
    # Clear conversation button
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.processed_files = {}
        st.success("Conversation cleared!")

# Main chat interface
st.title("AI Chatbot")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(message["content"], unsafe_allow_html=True)
        else:
            st.write(message["content"])
            if "files" in message and message["files"]:
                st.write("📎 Attached files:")
                for file_info in message["files"]:
                    st.write(f"- {file_info['name']} ({file_info['type']})")

# Function to extract text from different file types
def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.type
    file_content = uploaded_file.getvalue()
    extracted_text = ""
    
    try:
        if file_type == "text/csv":
            df = pd.read_csv(io.StringIO(file_content.decode('utf-8')))
            extracted_text = df.to_string()
        
        elif file_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(io.BytesIO(file_content))
            extracted_text = df.to_string()
        
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(io.BytesIO(file_content))
            extracted_text = "\n".join([para.text for para in doc.paragraphs])
        
        elif file_type == "application/pdf":
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            extracted_text = "\n".join([page.extract_text() for page in pdf_reader.pages])
        
        else:
            try:
                extracted_text = file_content.decode('utf-8')
            except UnicodeDecodeError:
                extracted_text = "Binary file content (preview not available)"
    
    except Exception as e:
        extracted_text = f"Error extracting content: {str(e)}"
    
    return extracted_text, file_content

# Function to send message to n8n webhook
def send_to_n8n(message_content, files=None):
    if not st.session_state.n8n_webhook_url:
        return {
            "error": "N8N Webhook URL not configured. Please set it in the sidebar."
        }
    
    # Prepare the multipart form data
    files_data = []
    if files:
        for file_info in files:
            # Create a file-like object from the binary data
            file_obj = io.BytesIO(file_info["binary"])
            files_data.append(
                ('files', (file_info["name"], file_obj, file_info["type"]))
            )
    
    # Prepare the form data, now including session_id
    data = {
        "message": message_content,
        "timestamp": datetime.now().isoformat(),
        "session_id": st.session_state.session_id
    }
    
    try:
        # Send the request with both form data and files
        response = requests.post(
            st.session_state.n8n_webhook_url,
            data=data,
            files=files_data,
            headers={"Accept": "application/json"}
        )
        
        if response.status_code == 200:
            try:
                json_response = response.json()
                
                # Handle response format: [{"output": "content"}]
                if isinstance(json_response, list) and len(json_response) > 0 and "output" in json_response[0]:
                    return {"content": json_response[0]["output"]}
                # Handle response format: {"content": "content"}
                elif isinstance(json_response, dict) and "content" in json_response:
                    return json_response
                # Handle any other JSON format
                else:
                    return {"content": str(json_response)}
            except json.JSONDecodeError:
                return {"content": response.text}
        else:
            return {
                "error": f"Error: Received status code {response.status_code} from webhook"
            }
    
    except requests.RequestException as e:
        return {"error": f"Connection error: {str(e)}"}

# File uploader
uploaded_files = st.file_uploader(
    "Upload files to analyze (CSV, XLSX, DOCX, PDF, etc.)",
    accept_multiple_files=True,
    type=["csv", "xlsx", "docx", "pdf", "txt", "json", "xml", "html"]
)

# Process uploaded files
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        
        if file_id not in st.session_state.processed_files:
            file_content, file_binary = extract_text_from_file(uploaded_file)
            file_preview = file_content[:1000] + "..." if len(file_content) > 1000 else file_content
            
            st.session_state.processed_files[file_id] = {
                "name": uploaded_file.name,
                "type": uploaded_file.type,
                "size": uploaded_file.size,
                "content": file_content,
                "preview": file_preview,
                "binary": file_binary
            }
    
    # Display previews of processed files
    if st.session_state.processed_files:
        st.write("File Previews:")
        for file_id, file_info in st.session_state.processed_files.items():
            with st.expander(f"{file_info['name']} ({file_info['type']})"):
                st.text(file_info['preview'])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat
    files_info = []
    if st.session_state.processed_files:
        for file_id, file_info in st.session_state.processed_files.items():
            files_info.append({
                "name": file_info["name"],
                "type": file_info["type"],
                "content": file_info["content"],
                "binary": file_info["binary"]
            })
    
    user_message = {
        "role": "user",
        "content": user_input,
        "files": files_info if files_info else None
    }
    
    st.session_state.messages.append(user_message)
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
        if files_info:
            st.write("📎 Attached files:")
            for file_info in files_info:
                st.write(f"- {file_info['name']} ({file_info['type']})")
    
    # Get response from n8n webhook
    with st.spinner("AI is thinking..."):
        response = send_to_n8n(user_input, files_info if files_info else None)
    
    # Display assistant response
    if "error" in response:
        error_message = {
            "role": "assistant",
            "content": f"⚠️ **Error**: {response['error']}"
        }
        st.session_state.messages.append(error_message)
        with st.chat_message("assistant"):
            st.markdown(error_message["content"], unsafe_allow_html=True)
    else:
        # Process the response from n8n
        bot_response = response.get("content", "No response received from webhook")
        
        assistant_message = {
            "role": "assistant",
            "content": bot_response
        }
        st.session_state.messages.append(assistant_message)
        
        with st.chat_message("assistant"):
            st.markdown(bot_response, unsafe_allow_html=True)
    
    # Clear processed files after sending
    st.session_state.processed_files = {} 