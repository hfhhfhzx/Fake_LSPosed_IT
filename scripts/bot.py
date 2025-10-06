import os
import sys
from telethon.sync import TelegramClient
from telethon.sessions import MemorySession

API_ID = 2040
API_HASH = "b18441a1ff607e10a989891a5462e627"

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
COMMIT_URL = os.environ.get("COMMIT_URL")
COMMIT_MESSAGE = os.environ.get("COMMIT_MESSAGE")
RUN_URL = os.environ.get("RUN_URL")
TITLE = os.environ.get("TITLE")
VERSION = os.environ.get("VERSION")
MSG_TEMPLATE = """
**{title}**
#ci_{version}
```
{commit_message}
```
[Commit]({commit_url})
[Workflow run]({run_url})
""".strip()


def get_caption():
    msg = MSG_TEMPLATE.format(
        title=TITLE,
        version=VERSION,
        commit_message=COMMIT_MESSAGE,
        commit_url=COMMIT_URL,
        run_url=RUN_URL,
    )
    if len(msg) > 1024:
        return COMMIT_URL
    return msg


def check_environ():
    if not BOT_TOKEN:
        print("[-] Invalid BOT_TOKEN")
        exit(1)
    if not CHAT_ID:
        print("[-] Invalid CHAT_ID")
        exit(1)
    if not COMMIT_URL:
        print("[-] Invalid COMMIT_URL")
        exit(1)
    if not COMMIT_MESSAGE:
        print("[-] Invalid COMMIT_MESSAGE")
        exit(1)
    if not RUN_URL:
        print("[-] Invalid RUN_URL")
        exit(1)
    if not TITLE:
        print("[-] Invalid TITLE")
        exit(1)
    if not VERSION:
        print("[-] Invalid VERSION")
        exit(1)


def main():
    print("[+] Uploading to telegram")
    check_environ()
    files = sys.argv[1:]
    print("[+] Files:", files)
    
    if len(files) <= 0:
        print("[-] No files to upload")
        exit(1)
        
    print("[+] Logging in Telegram with bot token")
    
    # 使用同步客户端和 MemorySession
    with TelegramClient(MemorySession(), API_ID, API_HASH) as client:
        client.start(bot_token=BOT_TOKEN)
        print("[+] Bot logged in successfully")
        
        # 验证连接
        me = client.get_me()
        print(f"[+] Logged in as: {me.username}")
        
        caption = [""] * len(files)
        caption[-1] = get_caption()
        print("[+] Caption prepared")
        print("[+] Sending files to Telegram...")
        
        # 发送文件
        client.send_file(
            entity=int(CHAT_ID), 
            file=files, 
            caption=caption, 
            parse_mode="markdown"
        )
        print("[+] Files sent successfully!")

if __name__ == "__main__":
    main()