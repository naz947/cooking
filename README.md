# cooking

Describe your project here.

## Setup environment variables

This project reads sensitive settings from a `.env` file at the project root. Create or update the file with your Telegram API credentials and group information:

```dotenv
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
GROUP_ID=-1001234567890    # numeric ID of the group
GROUP_NAME=YourGroupName   # optionally used by scripts
TOPIC_ID=123456            # if needed for `test.py`
```

You'll also need to install dependencies (e.g. via `pip install -e .` or using the configured package manager).
