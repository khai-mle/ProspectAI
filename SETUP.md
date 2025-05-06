# 🧠 ProspectAI – Local Setup Guide

Welcome to **ProspectAI** – an internal research tool powered by Streamlit, n8n, and Docker.  
This guide walks you through cloning the repo, running the app, and accessing all features locally.

---

## ✅ Prerequisites

Before starting, ensure you have:

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running
- [Git](https://git-scm.com/downloads) installed
- Windows, macOS, or Linux

---

## Step 1: Clone the Repository

Open your terminal or PowerShell and run:

```bash
git clone https://github.com/khai-mle/ProspectAI.git
cd ProspectAI
``` 
## Step 2: Pull Prebuilt n8n Image
To avoid building locally, pull the pre-packaged n8n backend with built-in workflows:

```bash
docker pull ghcr.io/khai-mle/prospectai/n8n:latest
```
## Step 3: Start the App Stack
Run the following from the root folder:

```bash
docker compose up -d
```
This will start:

Service	Port	Description
Streamlit	- :8501	- Chat interface and PDF download
n8n -	:5678 -	LLM + data automation backend
Postgres - Internal	Stores - n8n credentials/workflows
Qdrant -	:6333 -	Vector store for LLM embeddings
Traefik -	:80, :443 -	Handles internal routing

Access the tool in your browser: http://localhost:8501

First-time startup may take a minute as services initialize.

📁 Repo Structure
├── streamlit_app/       # Python UI for user interaction
├── n8n/                 # Custom image folder (no build needed if pulling)
├── shared/              # Shared volume for logs, PDFs, etc.
├── docker-compose.yml   # Stack configuration
├── README.md
├── SETUP.md             # ← You are here

🧪 Stopping the App
To stop all services:

```bash
docker compose down
```
To stop and remove data volumes:

```bash
docker compose down -v
```
🔐 Notes
The n8n workflows and credentials are preloaded into the Docker image.
If changes are made to workflows, export and re-import as needed.

