from telethon import TelegramClient
import json
import re, os
from dotenv import load_dotenv


load_dotenv()

api_id = int(os.environ.get("TELEGRAM_API_ID", "0"))
api_hash = os.environ.get("TELEGRAM_API_HASH", "")
group_id = int(os.environ.get("GROUP_ID", "0"))   # where topics exist
topic_id = 5
# optional: extract only URLs
url_pattern = re.compile(r"https?://\S+")

async def main():
    data = []

    async for msg in client.iter_messages(
        group_id,
        reply_to=topic_id,   # 🔑 this filters by topic
        limit=None           # fetch all messages
    ):
        if not msg.text:
            continue

        urls = url_pattern.findall(msg.text)

        data.append({
            "id": msg.id,
            "text": msg.text,
            "urls": urls,
            "date": str(msg.date)
        })

    # oldest → newest
    data.reverse()

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(data)} messages to data.json")

with TelegramClient("session", api_id, api_hash) as client:
    client.loop.run_until_complete(main())