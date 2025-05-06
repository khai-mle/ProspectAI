# AI Chatbot with n8n Integration

A Streamlit web application that provides a ChatGPT/Claude-style interface for an AI chatbot with n8n webhook integration and file upload capabilities.

## Features

- **Interactive Chat Interface**: Clean, modern UI mimicking ChatGPT/Claude style
- **n8n Webhook Integration**: Connect to n8n for processing messages and generating responses
- **File Upload Support**: Upload and process various file types:
  - CSV and Excel spreadsheets
  - Word documents (DOCX)
  - PDF files
  - Text files (TXT, JSON, XML, HTML)
- **Markdown Formatting**: Supports rich text formatting with bullet points, bold text, etc.

## Quick Start

### Windows
```
run.bat
```

### Linux/Mac
```
chmod +x run.sh
./run.sh
```

Or preview the UI without functionality:
```
streamlit run screenshot.py
```

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up an n8n webhook node:
   - Create a new workflow in n8n
   - Add a webhook node as a trigger
   - Configure your webhook to process incoming messages and return responses
   - The webhook should return JSON with a "content" field containing the response
   - **Note**: An example n8n workflow is provided in `n8n-workflow-example.json`

3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

4. In the app sidebar, enter your n8n webhook URL

## n8n Webhook Configuration

Your n8n webhook will receive JSON payloads with the following structure:

```json
{
  "message": "The user's message text",
  "timestamp": "2023-05-01T12:34:56.789Z",
  "files": [
    {
      "name": "example.pdf",
      "type": "application/pdf",
      "content": "Extracted text content from the file..."
    }
  ]
}
```

Your webhook should return JSON with the following structure:

```json
{
  "content": "The response message with **markdown** formatting"
}
```

### Example n8n Workflow

An example n8n workflow is included in this repository (`n8n-workflow-example.json`). To use it:

1. Go to your n8n instance
2. Click on "Workflows" in the main menu
3. Click the "Import from file" button
4. Select the `n8n-workflow-example.json` file
5. Activate the workflow
6. Copy the webhook URL from the Webhook node
7. Paste the URL into the Streamlit app sidebar

The example workflow includes:
- A Webhook node to receive messages
- A Code node that processes the message and simulates an AI response
- A Respond to Webhook node that returns the response to Streamlit

Note: The example workflow doesn't include actual AI processing. You'll need to modify the Code node to integrate with an AI service of your choice (like OpenAI, Claude, etc.).

## Preview Demo

To see a static demo of the UI without actual functionality, run:
```
streamlit run screenshot.py
```

This will show a mock conversation with sample data to help you visualize the interface before setting up the full application.

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