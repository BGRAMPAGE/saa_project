# Nexora Support Assistant

> An AI-powered customer support assistant built using Retrieval-Augmented Generation (RAG), Amazon Bedrock Knowledge Bases, Amazon S3, FastAPI, React, and local Ollama inference.

Nexora Support Assistant allows users to ask natural-language questions about Nexora Electronics products, shipping, returns, refunds, warranty, payments, account security, and other customer-support information.

The system uses **Amazon Bedrock Managed Knowledge Base** for retrieving relevant information from company documents and **Ollama** for generating the final response locally.

---

## ✨ Features

- 🤖 AI-powered customer support chatbot
- 🔎 Retrieval-Augmented Generation (RAG)
- ☁️ Amazon Bedrock Managed Knowledge Base
- 📦 Amazon S3 document storage
- 🧠 Local LLM inference using Ollama
- ⚡ Qwen3 for response generation
- 🚀 FastAPI backend
- 💬 React + Vite frontend
- 📚 Source document display
- 🛡️ Context-grounded responses
- 📱 Responsive chat interface
- 💡 Suggested customer questions
- 🔌 REST API architecture
- 🔐 Separation between retrieval and generation

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────────┐
                         │      React Frontend     │
                         │        Vite :5173       │
                         └────────────┬────────────┘
                                      │
                                  POST /chat
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │       FastAPI API       │
                         │        :8000            │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │         rag.py          │
                         │      RAG Pipeline       │
                         └────────────┬────────────┘
                                      │
                         ┌────────────┴────────────┐
                         │                         │
                         ▼                         ▼
              ┌─────────────────────┐   ┌─────────────────────┐
              │  Amazon Bedrock     │   │       Ollama        │
              │  Managed KB         │   │    qwen3:latest     │
              │                     │   │                     │
              │     Retrieval       │   │     Generation      │
              └──────────┬──────────┘   └──────────┬──────────┘
                         │                         │
                         ▼                         │
                 Relevant PDF Chunks ─────────────┘
                                      │
                                      ▼
                              Final AI Response
                                      │
                                      ▼
                              React Chat Interface
```

---

# 🔄 RAG Workflow

The application follows this pipeline:

```text
User Question
      │
      ▼
React Frontend
      │
      ▼
FastAPI /chat
      │
      ▼
Amazon Bedrock Managed Knowledge Base
      │
      ▼
Relevant Document Chunks
      │
      ▼
Context Construction
      │
      ▼
Ollama - Qwen3
      │
      ▼
Generated Answer
      │
      ▼
Answer + Sources
      │
      ▼
React Frontend
```

### Example

A user asks:

```text
What are Nexora's shipping and delivery policies?
```

The system:

1. Sends the question from the React frontend.
2. FastAPI receives the question.
3. The RAG pipeline queries the Bedrock Knowledge Base.
4. Bedrock retrieves relevant document chunks.
5. The retrieved chunks are combined into a context.
6. The question and context are sent to Ollama.
7. Qwen3 generates the final answer.
8. The API returns the answer and source documents.
9. React displays the response and sources.

---

# 🧰 Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Frontend Tooling | Vite |
| Backend | FastAPI |
| API Server | Uvicorn |
| RAG | Amazon Bedrock Managed Knowledge Base |
| Document Storage | Amazon S3 |
| Local LLM Runtime | Ollama |
| Generation Model | `qwen3:latest` |
| Programming Languages | Python, JavaScript |
| Cloud Region | `ap-south-1` |

---

# 📚 Knowledge Base

The Nexora Knowledge Base contains the following documents:

```text
01_company_overview.pdf
02_shipping_delivery_policy.pdf
03_returns_refunds_policy.pdf
04_warranty_support_policy.pdf
05_products_and_faq.pdf
06_payments_account_security.pdf
```

These documents are stored in Amazon S3 and synchronized with the Amazon Bedrock Managed Knowledge Base.

---

# 📁 Project Structure

```text
nexora-support-assistant/
│
├── main.py
├── rag.py
├── .env
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
│
└── frontend/
    ├── public/
    │
    ├── src/
    │   ├── App.jsx
    │   ├── App.css
    │   └── main.jsx
    │
    ├── package.json
    └── vite.config.js
```

---

# ⚙️ Prerequisites

Make sure the following software is installed:

- Python 3.11+
- Node.js
- npm
- AWS CLI
- Ollama
- `uv`

Verify the installations:

```powershell
python --version
node --version
npm --version
aws --version
ollama --version
uv --version
```

---

# 🧠 Ollama Setup

The project currently uses:

```text
qwen3:latest
```

Check installed models:

```powershell
ollama list
```

If Qwen3 is not installed:

```powershell
ollama pull qwen3:latest
```

Test the model:

```powershell
ollama run qwen3:latest
```

Ollama should be running locally before using the application.

---

# ☁️ AWS Configuration

The application uses Amazon Bedrock Managed Knowledge Base for document retrieval.

Current configuration:

```text
AWS Region:
ap-south-1

Knowledge Base ID:
FLEIRPWEK7
```

Verify that your AWS CLI credentials are working:

```powershell
aws sts get-caller-identity
```

The AWS identity used by the application must have the required permissions to retrieve information from the Bedrock Knowledge Base.

> **Security:** Never commit AWS access keys, secret keys, session tokens, or other credentials to Git.

---

# 🔐 Environment Variables

Create a `.env` file in the project root:

```env
AWS_REGION=ap-south-1
KNOWLEDGE_BASE_ID=FLEIRPWEK7

OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=qwen3:latest
```

Add `.env` to `.gitignore`:

```gitignore
.env
.env.*
```

---

# 🐍 Backend Setup

From the project root:

```powershell
uv sync
```

If the dependencies have not been installed yet:

```powershell
uv add boto3 python-dotenv requests fastapi uvicorn
```

---

# 🚀 Start the Backend

From the project root:

```powershell
uv run uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

FastAPI provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

---

# 🧪 Test the Backend

Open:

```text
http://127.0.0.1:8000/docs
```

Find:

```text
POST /chat
```

Click **Try it out** and use:

```json
{
  "question": "What are Nexora's shipping and delivery policies?"
}
```

Example response:

```json
{
  "answer": "Nexora's standard delivery policy...",
  "sources": [
    "s3://nexora-support-assistant-2026/02_shipping_delivery_policy.pdf"
  ]
}
```

---

# 🎨 Frontend Setup

Navigate to the frontend:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# ▶️ Running the Complete Application

The application requires:

- Ollama
- FastAPI backend
- React frontend
- AWS credentials
- Bedrock Knowledge Base access

## Terminal 1 — Backend

From the project root:

```powershell
uv run uvicorn main:app --reload
```

---

## Terminal 2 — Frontend

```powershell
cd frontend
npm run dev
```

---

## Ollama

Make sure Ollama is running and the model is available:

```powershell
ollama list
```

The application uses:

```text
qwen3:latest
```

---

# 🔌 API Reference

## `GET /`

Health-check endpoint.

### Response

```json
{
  "message": "Nexora Support Assistant API is running"
}
```

---

## `POST /chat`

Processes a customer question through the complete RAG pipeline.

### Request

```json
{
  "question": "What is Nexora's return policy?"
}
```

### Response

```json
{
  "answer": "Nexora's return policy...",
  "sources": [
    "s3://nexora-support-assistant-2026/03_returns_refunds_policy.pdf"
  ]
}
```

---

# 💬 Example Questions

The assistant can answer questions such as:

```text
What are Nexora's shipping policies?

How long does standard delivery take?

What is the return policy?

How do I request a refund?

What does the warranty cover?

What payment methods does Nexora accept?

How can I protect my Nexora account?

What products does Nexora offer?
```

---

# 🛡️ RAG Safety

The generation prompt is designed to keep the LLM grounded in the retrieved knowledge.

The assistant is instructed to:

- Use only information supplied by the Knowledge Base.
- Avoid hallucinating policies.
- Avoid inventing prices.
- Avoid inventing delivery dates.
- Avoid inventing refund status.
- Avoid inventing warranty terms.
- Avoid inventing customer-specific information.
- State clearly when the Knowledge Base does not contain enough information.
- Provide concise customer-support responses.

If the retrieved context does not contain enough information, the assistant should respond:

```text
I don't have enough information in the Nexora knowledge base to answer that.
```

---

# 🔎 Source Attribution

The Bedrock retrieval response contains source metadata for retrieved documents.

The application extracts the source URI and returns it with the generated response.

The frontend can therefore display:

```text
Sources

📄 02_shipping_delivery_policy.pdf
📄 03_returns_refunds_policy.pdf
```

This allows users to identify the documents used to answer their question.

---

# 🧩 RAG Implementation

The main RAG implementation is contained in `rag.py`.

## `retrieve_from_kb()`

Retrieves relevant document chunks from the Amazon Bedrock Managed Knowledge Base.

```python
retrieve_from_kb(question)
```

The retrieval layer uses the Bedrock Agent Runtime and managed search configuration.

---

## `get_context()`

Extracts the retrieved text and source information.

```python
get_context(question)
```

It returns:

```text
context
sources
```

---

## `generate_with_ollama()`

Sends the user question and retrieved context to the local Ollama model.

```python
generate_with_ollama(question, context)
```

The current generation model is:

```text
qwen3:latest
```

---

## `ask_nexora()`

Combines retrieval and generation into the complete RAG pipeline.

```python
ask_nexora(question)
```

Conceptually:

```text
Question
   ↓
Bedrock Retrieval
   ↓
Relevant Context
   ↓
Ollama
   ↓
Final Answer
```

---

# 🏛️ Architecture Decision

The project intentionally separates **retrieval** from **generation**.

```text
                 Amazon Bedrock
                       │
                       │ Retrieval
                       ▼
              Managed Knowledge Base
                       │
                       │ Context
                       ▼
                    Ollama
                       │
                       │ Generation
                       ▼
                  Final Answer
```

### Retrieval

Amazon Bedrock Managed Knowledge Base handles:

- Document retrieval
- Knowledge-base search
- Relevant chunk selection
- Source metadata

### Generation

Ollama handles:

- Context interpretation
- Natural-language generation
- Customer-facing response creation

This separation allows the generation model to be changed without redesigning the retrieval layer.

For example:

```text
qwen3:latest
      │
      ▼
llama3.1:8b
```

or:

```text
qwen3:latest
      │
      ▼
deepseek-r1:8b
```

without changing the fundamental Knowledge Base architecture.

---

# 📊 Current Project Status

| Component | Status |
|---|---|
| Amazon S3 document storage | ✅ Complete |
| Nexora PDF documents | ✅ Complete |
| Bedrock Managed Knowledge Base | ✅ Complete |
| Knowledge Base synchronization | ✅ Complete |
| Bedrock retrieval | ✅ Complete |
| Python RAG pipeline | ✅ Complete |
| Ollama integration | ✅ Complete |
| Qwen3 generation | ✅ Complete |
| FastAPI backend | ✅ Complete |
| React frontend | ✅ Complete |
| Source display | ✅ Complete |
| Production deployment | ⏳ Planned |
| Conversation memory | ⏳ Planned |
| Streaming responses | ⏳ Planned |
| Authentication | ⏳ Planned |
| Advanced guardrails | ⏳ Planned |
| Monitoring and logging | ⏳ Planned |

---

# 🚧 Future Improvements

## Frontend

- [ ] Markdown rendering
- [ ] Streaming AI responses
- [ ] Copy response button
- [ ] Clear conversation button
- [ ] Conversation history
- [ ] Better source cards
- [ ] Improved mobile interface
- [ ] Dark mode

## RAG

- [ ] Retrieval evaluation
- [ ] Query rewriting
- [ ] Retrieval quality metrics
- [ ] Better source citations
- [ ] Context compression
- [ ] RAG evaluation dataset

## AI Features

- [ ] Conversation memory
- [ ] Intent classification
- [ ] Follow-up question handling
- [ ] Tool calling
- [ ] Order-status integration
- [ ] Customer-specific workflows

## Production

- [ ] Dockerization
- [ ] CI/CD
- [ ] Authentication
- [ ] Rate limiting
- [ ] Application logging
- [ ] Monitoring
- [ ] Error tracking
- [ ] Production deployment

---

# 🔒 Security Considerations

Before deploying the project publicly:

- Never expose AWS credentials.
- Never commit `.env`.
- Add authentication to the API.
- Restrict CORS origins.
- Add API rate limiting.
- Validate user input.
- Implement request timeouts.
- Log errors without exposing secrets.
- Restrict AWS IAM permissions to the minimum required.
- Avoid exposing internal S3 paths unnecessarily.
- Protect customer-specific information if the system is later connected to customer databases.

The current permissive CORS configuration is suitable for local development but should be restricted before production deployment.

---

# 📈 Future Production Architecture

A future production deployment could follow:

```text
                    ┌─────────────────┐
                    │  Web / Mobile   │
                    │     Client      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Authentication  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   API Gateway   │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  RAG Backend    │
                    │    FastAPI      │
                    └───────┬─┬───────┘
                            │ │
                ┌───────────┘ └───────────┐
                ▼                         ▼
       ┌─────────────────┐       ┌─────────────────┐
       │ Amazon Bedrock  │       │ LLM Generation  │
       │ Knowledge Base  │       │     Service     │
       └────────┬────────┘       └─────────────────┘
                │
                ▼
       ┌─────────────────┐
       │    Amazon S3    │
       │ Knowledge Docs  │
       └─────────────────┘
```

---

# 🧑‍💻 Development

Clone the repository:

```bash
git clone <repository-url>
```

Enter the project:

```bash
cd nexora-support-assistant
```

Install backend dependencies:

```bash
uv sync
```

Install frontend dependencies:

```bash
cd frontend
npm install
```

Configure AWS credentials and environment variables.

Start the backend:

```bash
uv run uvicorn main:app --reload
```

Start the frontend in another terminal:

```bash
cd frontend
npm run dev
```

---

# 🗂️ Git Configuration

Recommended `.gitignore`:

```gitignore
# Environment
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
*.pyo
.venv/
venv/
project_venv/

# Testing
.pytest_cache/
.coverage
htmlcov/

# Node
node_modules/
frontend/dist/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Local data
*.sqlite
*.db
```

You can optionally commit a safe `.env.example`:

```env
AWS_REGION=ap-south-1
KNOWLEDGE_BASE_ID=your-knowledge-base-id
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=qwen3:latest
```

---

# 📝 License

This project is intended for educational, research, and development purposes.

If this project is distributed publicly, add an appropriate open-source license such as MIT, Apache 2.0, or another license appropriate for the project.

---

# 👨‍💻 Project Summary

**Nexora Support Assistant** demonstrates a practical hybrid RAG architecture:

```text
                 NEXORA SUPPORT ASSISTANT

                         User
                          │
                          ▼
                   React Frontend
                          │
                          ▼
                     FastAPI
                          │
                          ▼
                ┌──────────────────┐
                │   RAG Pipeline   │
                └────────┬─────────┘
                         │
             ┌───────────┴───────────┐
             ▼                       ▼
      Amazon Bedrock             Ollama
      Managed KB                Qwen3
       Retrieval              Generation
             │                       │
             └───────────┬───────────┘
                         ▼
                    AI Response
                         │
                         ▼
                   Source Documents
                         │
                         ▼
                  React Chat UI
```

The project combines **managed cloud-based retrieval** with **local LLM inference** to create a complete AI-powered customer-support application.