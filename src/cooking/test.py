from telethon import TelegramClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.environ.get("TELEGRAM_API_ID", "0"))
api_hash = os.environ.get("TELEGRAM_API_HASH", "")
group = os.environ.get("GROUP_NAME", "")   # where topics exist
topic_id = int(os.environ.get("TOPIC_ID", "0"))                    # your topic thread id

client = TelegramClient("session", api_id, api_hash)

async def main():
    data = []

    async for msg in client.iter_messages(group, reply_to=topic_id):
        if msg.text:
            data.append({
                "id": msg.id,
                "text": msg.text,
                "date": str(msg.date)
            })

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data[::-1], f, indent=2, ensure_ascii=False)

with client:
    client.loop.run_until_complete(main())