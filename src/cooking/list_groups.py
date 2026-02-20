import os
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.environ.get("TELEGRAM_API_ID", "0"))
api_hash = os.environ.get("TELEGRAM_API_HASH", "")
async def main():
    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            print(dialog.name, dialog.id)

with TelegramClient("session", api_id, api_hash) as client:
    client.loop.run_until_complete(main())