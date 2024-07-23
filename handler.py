import boto3
import datetime
import json
import os
import re
import sys
import time
import base64
import requests

from openai import OpenAI

BOT_CURSOR = os.environ.get("BOT_CURSOR", ":robot_face:")

# Set up Discord API credentials
DISCORD_APPID = os.environ["DISCORD_APPID"]
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

# Keep track of conversation history by thread and user
DYNAMODB_TABLE_NAME = os.environ.get("DYNAMODB_TABLE_NAME", "discord-ai-bot-context")

# Set up ChatGPT API credentials
OPENAI_ORG_ID = os.environ.get("OPENAI_ORG_ID", None)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", None)
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o")

IMAGE_MODEL = os.environ.get("IMAGE_MODEL", "dall-e-3")
IMAGE_QUALITY = os.environ.get("IMAGE_QUALITY", "hd")  # standard, hd
IMAGE_SIZE = os.environ.get("IMAGE_SIZE", "1024x1024")
IMAGE_STYLE = os.environ.get("IMAGE_STYLE", "vivid")  # vivid, natural

# Set up System messages
SYSTEM_MESSAGE = os.environ.get("SYSTEM_MESSAGE", "None")

TEMPERATURE = float(os.environ.get("TEMPERATURE", 0))

MAX_LEN_SLACK = int(os.environ.get("MAX_LEN_SLACK", 3000))
MAX_LEN_OPENAI = int(os.environ.get("MAX_LEN_OPENAI", 4000))

KEYWARD_IMAGE = "그려줘"

MSG_PREVIOUS = "이전 대화 내용 확인 중... " + BOT_CURSOR
MSG_IMAGE_DESCRIBE = "이미지 감상 중... " + BOT_CURSOR
MSG_IMAGE_GENERATE = "이미지 생성 준비 중... " + BOT_CURSOR
MSG_IMAGE_DRAW = "이미지 그리는 중... " + BOT_CURSOR
MSG_RESPONSE = "응답 기다리는 중... " + BOT_CURSOR

COMMAND_DESCRIBE = "Describe the image in great detail as if viewing a photo."
COMMAND_GENERATE = "Convert the above sentence into a command for DALL-E to generate an image within 1000 characters. Just give me a prompt."

CONVERSION_ARRAY = [
    ["**", "*"],
    # ["#### ", "🔸 "],
    # ["### ", "🔶 "],
    # ["## ", "🟠 "],
    # ["# ", "🟡 "],
]


# Handle the Lambda function
def lambda_handler(event, context):
    body = json.loads(event["body"])

    if "challenge" in body:
        # Respond to the Slack Event Subscription Challenge
        return {
            "statusCode": 200,
            "headers": {"Content-type": "application/json"},
            "body": json.dumps({"challenge": body["challenge"]}),
        }

    print("lambda_handler: {}".format(body))

    # Duplicate execution prevention
    if "event" not in body or "client_msg_id" not in body["event"]:
        return {
            "statusCode": 200,
            "headers": {"Content-type": "application/json"},
            "body": json.dumps({"status": "Success"}),
        }

    return {
        "statusCode": 200,
        "headers": {"Content-type": "application/json"},
        "body": json.dumps({"status": "Success"}),
    }
