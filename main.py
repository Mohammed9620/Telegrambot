import os
import json
from dotenv import load_dotenv

load_dotenv()

from telethon import TelegramClient, events
from classifier import is_tech_related

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

with open("groups.json", "r", encoding="utf-8") as f:
    GROUPS = json.load(f)["groups"]

client = TelegramClient("job_bot_session", API_ID, API_HASH)


@client.on(events.NewMessage(chats=GROUPS))
async def handler(event):
    text = event.raw_text
    if not text:
        return

    try:
        relevant = is_tech_related(text)
    except Exception as e:
        print(f"[classifier error] {e}")
        return

    if relevant:
        await client.forward_messages("me", event.message)
        print(f"[forwarded] {text[:60]}...")


def main():
    client.start()
    print("Bot is running. Listening to:", GROUPS)
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
