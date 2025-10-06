import os
import sys
import requests

def upload_files():
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    CHAT_ID = os.environ.get("CHAT_ID")
    
    if not BOT_TOKEN or not CHAT_ID:
        print("[-] Missing BOT_TOKEN or CHAT_ID")
        return False
        
    files = sys.argv[1:]
    if not files:
        print("[-] No files to upload")
        return False
        
    print(f"[+] Uploading {len(files)} files to Telegram")
    
    # 先发送文本消息
    commit_message = os.environ.get("COMMIT_MESSAGE", "Build completed")
    commit_url = os.environ.get("COMMIT_URL", "")
    run_url = os.environ.get("RUN_URL", "")
    version = os.environ.get("VERSION", "")
    title = os.environ.get("TITLE", "Build")
    
    caption = f"**{title}**\n#ci_{version}\n```{commit_message}```\n"
    if commit_url:
        caption += f"[Commit]({commit_url})\n"
    if run_url:
        caption += f"[Workflow run]({run_url})"
    
    # 逐个发送文件
    for file_path in files:
        if not os.path.exists(file_path):
            print(f"[-] File not found: {file_path}")
            continue
            
        print(f"[+] Uploading: {file_path}")
        
        try:
            with open(file_path, 'rb') as file:
                # 使用 Telegram Bot API 发送文档
                response = requests.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument",
                    data={
                        'chat_id': CHAT_ID,
                        'caption': caption if file_path == files[-1] else "",  # 只在最后一个文件添加标题
                        'parse_mode': 'Markdown'
                    },
                    files={'document': (os.path.basename(file_path), file)},
                    timeout=60
                )
                
                if response.status_code == 200:
                    print(f"[+] Successfully uploaded: {file_path}")
                else:
                    print(f"[-] Failed to upload {file_path}: {response.text}")
                    
        except Exception as e:
            print(f"[-] Error uploading {file_path}: {e}")
            return False
    
    return True

if __name__ == "__main__":
    success = upload_files()
    sys.exit(0 if success else 1)