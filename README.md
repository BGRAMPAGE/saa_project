Nexora Support Assistant

A RAG-based customer support assistant for Nexora Electronics, combining Amazon Bedrock Knowledge Bases for document retrieval with a local Ollama LLM for response generation.

The system allows users to ask natural-language questions about Nexora's shipping, returns, refunds, warranty, products, payments, and other support information.

Architecture
                         ┌─────────────────────┐
                         │    React Frontend   │
                         │      :5173           │
                         └──────────┬──────────┘
                                    │
                              POST /chat
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI          │
                         │      :8000           │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       rag.py         │
                         │    RAG Pipeline      │
                         └──────────┬──────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
                ┌─────────────────┐   ┌─────────────────┐
                │ Amazon Bedrock  │   │     Ollama      │
                │ Managed KB      │   │   qwen3:latest  │
                │                 │   │                 │
                │   Retrieval     │   │   Generation    │
                └────────┬────────┘   └────────┬────────┘
                         │                     │
                         ▼                     │
                Relevant PDF chunks ──────────┘
                                    │
                                    ▼
                              Final Answer
                                    │
                                    ▼
                             React Frontend
Core design

Amazon Bedrock is responsible for retrieving relevant information from the knowledge base.

Ollama runs locally and generates the final response using the retrieved context.

This avoids using a Bedrock foundation model for answer generation.

Features
Natural-language customer support
Retrieval-Augmented Generation (RAG)
Amazon Bedrock Managed Knowledge Base
Amazon S3 document storage
Local LLM inference using Ollama
Qwen3 8B-class local model
FastAPI backend
React + Vite frontend
Source display for retrieved documents
Loading/typing indicator
Suggested questions
Responsive chat interface
Context-grounded answers
Protection against unsupported/invented answers
Technology Stack
Component	Technology
Frontend	React
Frontend tooling	Vite
Backend	FastAPI
API server	Uvicorn
RAG	Amazon Bedrock Knowledge Base
Document storage	Amazon S3
Local LLM	Ollama
Generation model	qwen3:latest
Language	Python / JavaScript
Cloud region	ap-south-1
Knowledge Base

The Nexora Knowledge Base contains PDF documents covering:

01_company_overview.pdf
02_shipping_delivery_policy.pdf
03_returns_refunds_policy.pdf
04_warranty_support_policy.pdf
05_products_and_faq.pdf
06_payments_account_security.pdf

These documents are uploaded to Amazon S3 and synchronized with the Amazon Bedrock Managed Knowledge Base.

Project Structure
nexora-support-assistant/
│
├── rag.py
├── main.py
├── .env
├── pyproject.toml
├── uv.lock
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
How the RAG Pipeline Works

When a customer asks:

What is Nexora's shipping policy?

the request follows this pipeline:

1. User question

The React frontend sends:

POST /chat

with:

{
  "question": "What is Nexora's shipping policy?"
}
2. FastAPI

FastAPI receives the question and calls:

ask_nexora(question)

from rag.py.

3. Bedrock retrieval

The application calls the Bedrock Agent Runtime:

client.retrieve(...)

using the Managed Knowledge Base.

The retrieval configuration uses:

"managedSearchConfiguration": {
    "numberOfResults": 5,
    "rerankingModelType": "MANAGED"
}
4. Relevant chunks

Bedrock returns the most relevant chunks from the Nexora PDFs.

For example:

02_shipping_delivery_policy.pdf
03_returns_refunds_policy.pdf
05_products_and_faq.pdf
5. Context construction

The retrieved chunks are combined into a context passed to the local LLM.

6. Ollama generation

The context and original question are sent to:

Ollama
└── qwen3:latest

The model is instructed to answer only from the retrieved knowledge-base context.

7. Final response

FastAPI returns:

{
  "answer": "Nexora's standard delivery typically takes...",
  "sources": [
    "s3://.../02_shipping_delivery_policy.pdf"
  ]
}
8. Frontend

React displays:

Customer question
AI response
Retrieved source documents
Requirements
Software

Install the following:

Python 3.11+
Node.js
npm
AWS CLI
Ollama
uv package manager

Verify:

python --version
node --version
npm --version
aws --version
ollama --version
uv --version
Ollama Setup

Make sure Ollama is installed and running.

Check available models:

ollama list

The project currently uses:

qwen3:latest

If necessary:

ollama pull qwen3:latest

Test it:

ollama run qwen3:latest
Python Environment

From the project root:

uv sync

If the required packages have not been added:

uv add boto3 python-dotenv requests fastapi uvicorn
AWS Configuration

The application requires AWS credentials with permission to access the Bedrock Knowledge Base.

Verify the configured AWS identity:

aws sts get-caller-identity

The project currently uses:

Region: ap-south-1
Knowledge Base ID: FLEIRPWEK7

Do not commit AWS credentials to Git.

Environment Variables

Create a .env file if additional environment configuration is required.

Example:

AWS_REGION=ap-south-1
KNOWLEDGE_BASE_ID=FLEIRPWEK7
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=qwen3:latest

Never place AWS secret keys directly inside source code or commit them to the repository.

Running the Backend

From the project root:

uv run uvicorn main:app --reload

The backend will run at:

http://127.0.0.1:8000

FastAPI documentation:

http://127.0.0.1:8000/docs

You can test the API directly from Swagger UI.

Example request:

{
  "question": "What are Nexora's shipping and delivery policies?"
}
Running the Frontend

Open another terminal.

Navigate to:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will normally be available at:

http://localhost:5173
Running the Complete Application

You need the following services running:

Terminal 1 — FastAPI
uv run uvicorn main:app --reload
Ollama

Make sure Ollama is running locally.

Terminal 2 — React
cd frontend
npm run dev

Then open:

http://localhost:5173
API
GET /

Health check.

Response:

{
  "message": "Nexora Support Assistant API is running"
}
POST /chat

Send a customer question.

Request
{
  "question": "What is Nexora's return policy?"
}
Response
{
  "answer": "Nexora's return policy...",
  "sources": [
    "s3://bucket/03_returns_refunds_policy.pdf"
  ]
}
Example Questions

The frontend can answer questions such as:

What are Nexora's shipping policies?

How long does standard delivery take?

What is the return policy?

How do I request a refund?

What does the warranty cover?

What payment methods are supported?

How can I protect my Nexora account?

What products does Nexora offer?
RAG Safety Rules

The generation prompt instructs Ollama to:

Use only retrieved Nexora knowledge.
Avoid hallucinating information.
Avoid inventing prices or policies.
Avoid inventing delivery dates.
Avoid inventing refund or order status.
Avoid inventing warranty conditions.
State when the knowledge base does not contain sufficient information.
Provide concise customer-support answers.

If the retrieved context does not contain the answer, the assistant should respond:

I don't have enough information in the Nexora knowledge base to answer that.
Why Ollama?

The project separates retrieval from generation.

Bedrock
   ↓
Knowledge retrieval

Ollama
   ↓
Answer generation

This provides a useful hybrid architecture:

AWS handles managed knowledge retrieval.
The LLM runs locally.
No Bedrock generation model is required.
Local inference reduces dependence on cloud model inference.
The generation model can be changed without redesigning the knowledge base.

For example, the generation model can later be switched from:

qwen3:latest

to:

llama3.1:8b

or:

deepseek-r1:8b

without changing the retrieval layer.

Current Architecture Status
Component	Status
S3 document storage	✅ Complete
PDF knowledge documents	✅ Complete
Bedrock Managed Knowledge Base	✅ Complete
Knowledge Base synchronization	✅ Complete
Bedrock retrieval	✅ Complete
Python RAG pipeline	✅ Complete
Ollama integration	✅ Complete
Qwen3 generation	✅ Complete
FastAPI backend	✅ Complete
React frontend	✅ Complete
Source display	✅ Complete
Production deployment	⏳ Future
Authentication	⏳ Future
Conversation memory	⏳ Future
Streaming responses	⏳ Future
Advanced guardrails	⏳ Future
Future Improvements

Possible next development phases:

Phase 1 — UX
Markdown rendering
Better source cards
Copy-answer button
Clear conversation button
Conversation history
Improved mobile layout
Streaming responses
Phase 2 — RAG Improvements
Retrieval evaluation
Query rewriting
Better chunking strategy
Retrieval score analysis
Source-aware citations
Context compression
Phase 3 — AI Features
Conversation memory
Intent classification
Follow-up question handling
Customer-specific workflows
Tool calling
Order-status integration
Phase 4 — Production
React
   ↓
Production API
   ↓
Authentication
   ↓
RAG Service
   ↓
Bedrock Knowledge Base
   ↓
LLM

Potential additions include:

Docker
CI/CD
Logging
Monitoring
Authentication
Rate limiting
Error tracking
Production deployment
License

This project is intended for educational and project-development purposes.