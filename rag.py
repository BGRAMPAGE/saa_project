import boto3
import requests
from botocore.exceptions import ClientError



AWS_REGION = "us-east-1"
KNOWLEDGE_BASE_ID = "FLEIRFWEK7"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen3:latest"



def retrieve_from_kb(question: str, number_of_results: int = 5):
    """
    Retrieve relevant documents from the Amazon Bedrock
    Managed Knowledge Base.
    """

    client = boto3.client(
        "bedrock-agent-runtime",
        region_name=AWS_REGION
    )

    response = client.retrieve(
        knowledgeBaseId=KNOWLEDGE_BASE_ID,
        retrievalQuery={
            "text": question
        },
        retrievalConfiguration={
            "managedSearchConfiguration": {
                "numberOfResults": number_of_results,
                "rerankingModelType": "MANAGED"
            }
        }
    )

    return response


def get_context(question: str):
    """
    Retrieve relevant chunks and prepare them as context
    for the local Ollama model.
    """

    response = retrieve_from_kb(question)

    contexts = []
    sources = []

    for result in response.get("retrievalResults", []):

        text = result.get("content", {}).get("text", "").strip()

        if text:
            contexts.append(text)

        location = result.get("location", {})

        s3_location = location.get("s3Location", {})
        uri = s3_location.get("uri")

        if uri and uri not in sources:
            sources.append(uri)

    context = "\n\n---\n\n".join(contexts)

    return context, sources




def generate_with_ollama(question: str, context: str):
    """
    Generate the final answer using the local Ollama model.
    """

    prompt = f"""
You are Nexora Electronics' customer support assistant.

Answer the customer's question using ONLY the information
provided in the knowledge-base context below.

IMPORTANT RULES:
1. Do not invent information.
2. Do not make up prices, policies, delivery dates, refund status,
   warranty terms, product specifications, or account information.
3. If the answer cannot be found in the context, clearly say:
   "I don't have enough information in the Nexora knowledge base
   to answer that."
4. Give a clear and concise customer-support response.
5. Do not mention that you are using a language model.
6. Do not mention the internal retrieval process.
7. If multiple pieces of context are relevant, combine them logically.
8. "Standard shipping is free for orders of 1,000 or more.
• Orders below 1,000 have a standard shipping fee of 79.
• Express shipping, where available, costs 149 per order.

KNOWLEDGE BASE CONTEXT:
-----------------------
{context}
-----------------------

CUSTOMER QUESTION:
{question}

FINAL ANSWER:
"""

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    response.raise_for_status()

    data = response.json()

    return data.get("response", "").strip()




def ask_nexora(question: str):
    """
    Complete RAG pipeline:

    User Question
        ↓
    Bedrock Knowledge Base Retrieval
        ↓
    Retrieved Context
        ↓
    Ollama Qwen3 Generation
        ↓
    Final Answer
    """

    context, sources = get_context(question)

    if not context:
        return {
            "answer": (
                "I don't have enough information in the "
                "Nexora knowledge base to answer that."
            ),
            "sources": []
        }

    answer = generate_with_ollama(
        question=question,
        context=context
    )

    return {
        "answer": answer,
        "sources": sources
    }




if __name__ == "__main__":

    question = "What are Nexora's shipping and delivery policies?"

    try:

        print("\n" + "=" * 70)
        print("NEXORA SUPPORT ASSISTANT")
        print("=" * 70)

        print(f"\nQuestion: {question}")

        print("\n[1/2] Retrieving from Bedrock Knowledge Base...")

        context, sources = get_context(question)

        print(f"Retrieved context successfully.")
        print(f"Sources found: {len(sources)}")

        print("\n[2/2] Generating answer with Ollama...")
        print(f"Model: {OLLAMA_MODEL}")

        answer = generate_with_ollama(
            question,
            context
        )

        print("\n" + "=" * 70)
        print("FINAL ANSWER")
        print("=" * 70)

        print(answer)

        print("\n" + "=" * 70)
        print("SOURCES")
        print("=" * 70)

        for source in sources:
            print(source)

    except ClientError as e:

        print("\nAWS ERROR:")
        print(e)

    except requests.exceptions.ConnectionError:

        print("\nOLLAMA ERROR:")
        print(
            "Could not connect to Ollama. "
            "Make sure Ollama is running."
        )

    except requests.exceptions.Timeout:

        print("\nOLLAMA ERROR:")
        print("Ollama took too long to generate the response.")

    except Exception as e:

        print("\nERROR:")
        print(e)