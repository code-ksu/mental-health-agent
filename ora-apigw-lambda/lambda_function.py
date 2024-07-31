import json
import boto3
from boto3.dynamodb.conditions import Attr
import datetime
import uuid

client_dynamodb = boto3.client("dynamodb", region_name="us-east-1")
dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
table = dynamodb.Table("ai_conversation")
tableName = "ai_conversation"

client_agent = boto3.client(
    "bedrock-agent-runtime",
    region_name="us-east-1",
)


def lambda_handler(event, context):
    user_current_posted = datetime.datetime.now().isoformat()
    print(event["requestContext"]["time"])
    print(event["requestContext"]["timeEpoch"])

    body = event.get("body", "{}")
    try:
        parsed_body = json.loads(body)
        message = parsed_body["message"]
        user_id = parsed_body["user_id"]
    except:
        print(body)
        return {"statusCode": 400, "body": "Invalid request"}

    # save the user input
    id_db_user = uuid.uuid4()
    table.put_item(
        Item={
            "id": str(id_db_user),
            "user_id": user_id,
            "role": "user",
            "message": message,
            "posted": user_current_posted,
            "deleted": False,
        }
    )

    # get old conversation
    dynamodb_body = table.scan(FilterExpression=Attr("user_id").eq(user_id))

    print("ITEMS----")
    items = dynamodb_body["Items"]
    print(items)
    history = ""
    for item in items:
        history += item["role"] + ": " + item["message"] + "\n"

    # get response from agent

    response = client_agent.invoke_agent(
        agentId="80OBUFCZVY",
        agentAliasId="DB3APGS6J1",
        enableTrace=False,
        endSession=False,
        inputText=message,
        sessionId=user_id,
        # sessionId="d244aa5e-0c51-44cf-ab6b-64ff2c5b8452",
        sessionState={"promptSessionAttributes": {"conversation_history": history}},
    )

    completion = ""
    for event in response.get("completion"):
        chunk = event["chunk"]
        completion += chunk["bytes"].decode()

    print("RESPONSE----")
    print(completion)

    # add new conversation
    # get current date in ISO 8601 format as string
    ai_current_posted = datetime.datetime.now().isoformat()
    id_db_ai = uuid.uuid4()
    table.put_item(
        Item={
            "id": str(id_db_ai),
            "user_id": user_id,
            "role": "assistant",
            "message": completion,
            "posted": ai_current_posted,
            "deleted": False,
        }
    )

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "https://code-ksu.github.io, https://mexb.ai",
        },
        "body": completion,
    }
