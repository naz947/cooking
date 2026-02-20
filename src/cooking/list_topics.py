import os
from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.environ.get("TELEGRAM_API_ID", "0"))
api_hash = os.environ.get("TELEGRAM_API_HASH", "")
group_id = int(os.environ.get("GROUP_ID", "0"))   # where topics exist


async def main():
    entity = await client.get_entity(group_id)
    print(f"Channel: {entity.title}")
    print(f"Is Forum: {getattr(entity, 'forum', False)}\n")
    
    print("Searching for 'cooking' topic...\n")
    cooking_topic_id = None
    sample_message = None
    
    async for message in client.iter_messages(group_id, limit=5000):
        if message.text and "cooking" in message.text.lower():
            # Check if this message is in a forum topic
            reply_to = message.reply_to
            if reply_to and hasattr(reply_to, 'forum_topic') and reply_to.forum_topic:
                cooking_topic_id = reply_to.reply_to_msg_id
                sample_message = message.text[:60]
                break
    
    if cooking_topic_id:
        # Fetch the topic message to get its title
        topic_msg = await client.get_messages(group_id, ids=cooking_topic_id)
        topic_title = topic_msg.text if topic_msg and topic_msg.text else "(No explicit title)"
        
        print(f"✓ Found 'cooking' topic!")
        print(f"  Topic ID: {cooking_topic_id}")
        print(f"  Topic Title: {topic_title}")
        print(f"  Sample message in topic: {sample_message}...\n")
    else:
        print("'cooking' topic message not found")

with TelegramClient("session", api_id, api_hash) as client:
    client.loop.run_until_complete(main())
