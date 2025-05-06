# Prospect AI Chatbot with n8n Integration

A Streamlit web application that provides a ChatGPT/Claude-style interface for an AI chatbot with n8n webhook integration and file upload capabilities. Now supports native file uploads (PDF, CSV, DOCX, etc.) and session tracking.

## Features

- **Interactive Chat Interface**: Clean, modern UI mimicking ChatGPT/Claude style
- **n8n Webhook Integration**: Connect to n8n for processing messages and generating responses
- **File Upload Support**: Upload and process various file types:
  - CSV and Excel spreadsheets
  - Word documents (DOCX)
  - PDF files
  - Text files (TXT, JSON, XML, HTML)
- **Native File Transfer**: Files are sent to the webhook in their original format (not just extracted text)
- **Session Tracking**: Each conversation is tagged with a unique session ID
- **Markdown Formatting**: Supports rich text formatting with bullet points, bold text, etc.

## Quick Start

### Windows
```sh
run.bat
```

### Linux/Mac
```sh
chmod +x run.sh
./run.sh
```

## Setup

1. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

2. Set up an n8n webhook node:
   - Create a new workflow in n8n
   - Add a webhook node as a trigger
   - Configure your webhook to process incoming messages and return responses
   - The webhook should return JSON with a `content` field containing the response

3. Run the Streamlit app:
   ```sh
   streamlit run app.py
   ```

4. In the app sidebar, enter your n8n webhook URL

## n8n Webhook Configuration

Your n8n webhook will receive a **multipart/form-data** payload with the following fields:

- `message`: The user's message text
- `timestamp`: ISO8601 timestamp of the message
- `session_id`: Unique session identifier for the conversation
- `files`: One or more files, each in its original format (PDF, CSV, DOCX, etc.)

### Example: Handling the Payload in n8n
- Use the Webhook node to receive the multipart form data
- Each file will be available in the `binary` property of the incoming item
- The text fields (`message`, `timestamp`, `session_id`) are available in the `body` property

#### Example n8n Webhook Node Output
```json
{
  "body": {
    "message": "The user's message text",
    "timestamp": "2024-06-01T12:34:56.789Z",
    "session_id": "a1b2c3d4-5678-90ab-cdef-1234567890ab"
  },
  "binary": {
    "files": {
      "data": "<base64-encoded file data>",
      "fileName": "example.pdf",
      "mimeType": "application/pdf"
    }
  }
}
```

### Webhook Response

Your webhook should return JSON with the following structure:
```json
{
  "content": "The response message with **markdown** formatting"
}
```
Or, if returning a list (for compatibility):
```json
[
  { "output": "The response message with **markdown** formatting" }
]
```

## Usage

1. Type messages in the chat input field
2. Upload files using the file upload area
3. View file previews before sending
4. Receive responses with markdown formatting

## Formatting Tips

The chatbot supports markdown formatting in responses:

- Use `**text**` for **bold text**
- Use `*text*` for *italic text*
- Use `- item` for bullet points
- Use `1. item` for numbered lists
- Use `> text` for block quotes
- Use triple backticks for code blocks 
