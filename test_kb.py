import boto3
from botocore.exceptions import ClientError



AWS_REGION = "us-east-1"
KNOWLEDGE_BASE_ID = "FLEIRFWEK7"


def retrieve_from_kb(question: str):
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
                "numberOfResults": 5,
                "rerankingModelType": "MANAGED"
            }
        }
    )

    return response


if __name__ == "__main__":

    question = "What are Nexora's shipping and delivery policies?"

    try:
        response = retrieve_from_kb(question)

        print("\n" + "=" * 70)
        print("RETRIEVED RESULTS")
        print("=" * 70)

        for i, result in enumerate(response["retrievalResults"], start=1):

            print(f"\n--- Result {i} ---")

            score = result.get("score")
            print(f"Score: {score}")

            content = result.get("content", {})
            print(f"Text:\n{content.get('text', '')}")

            location = result.get("location", {})
            print(f"Location: {location}")

    except ClientError as e:
        print("\nAWS ERROR:")
        print(e)

    except Exception as e:
        print("\nERROR:")
        print(e)