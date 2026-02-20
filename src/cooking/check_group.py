import os
from telethon import TelegramClient
from dotenv import load_dotenv

# load environment variables from .env file if present
load_dotenv()

api_id = int(os.environ.get("TELEGRAM_API_ID", "0"))
api_hash = os.environ.get("TELEGRAM_API_HASH", "")
group_id = int(os.environ.get("GROUP_ID", "0"))   # where topics exist

async def main():
    entity = await client.get_entity(group_id)

    print("Title:", entity.title)
    print("Megagroup:", getattr(entity, "megagroup", None))
    print("Forum (topics enabled):", getattr(entity, "forum", None))

with TelegramClient("session", api_id, api_hash) as client:
    client.loop.run_until_complete(main())