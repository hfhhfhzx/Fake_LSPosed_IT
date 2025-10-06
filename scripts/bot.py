import asyncio
import os
import sys
from telethon import TelegramClient
from telethon.sessions import StringSession

API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
COMMIT_URL = os.environ.get("COMMIT_URL")
COMMIT_MESSAGE = os.environ.get("COMMIT_MESSAGE")
RUN_URL = os.environ.get("RUN_URL")
TITLE = os.environ.get("TITLE")

BOT_SESSION = os.environ.get("BOT_SESSION")

MSG_TEMPLATE = """
**{title}**

```
{commit_message}
```
[Commit]({commit_url})
[Workflow run]({run_url})
""".strip()

def get_caption():
    msg = MSG_TEMPLATE.format(
        title=TITLE,
        commit_message=COMMIT_MESSAGE,
        commit_url=COMMIT_URL,
        run_url=RUN_URL,
    )
    if len(msg) > 1024:
        return COMMIT_URL
    return msg

async def main():
    print("[+] Uploading to telegram")
    files = sys.argv[1:]
    print("[+] Files:", files)
    
    if len(files) <= 0:
        print("[-] No files to upload")
        exit(1)
        
    print("[+] Using pre-authenticated session")
    
    session = StringSession(BOT_SESSION)
    
    async with TelegramClient(session, API_ID, API_HASH) as client:
        print("[+] Client initialized with pre-authenticated session")
        
        caption = [""] * len(files)
        caption[-1] = get_caption()
        print("[+] Caption prepared")
        
        print("[+] Sending files to Telegram...")
        await client.send_file(
            entity=int(CHAT_ID),
            file=files,
            caption=caption,
            parse_mode="markdown"
        )
        print("[+] Files sent successfully!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"[-] An error occurred: {e}")
        exit(1)