import asyncio
import logging
import sys

# Ensure UTF-8 output encoding on Windows terminals to prevent charmap crashes
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from config import Config
from pyrogram import Client, idle
from plugins.regix import restart_forwards

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("Mr.Guardian_bot")

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Mr.Guardian_bot is alive and running.")

    def log_message(self, format, *args):
        pass

def start_health_server():
    port = int(os.environ.get("PORT", 0) or 0)
    if port > 0:
        try:
            server = HTTPServer(("0.0.0.0", port), HealthHandler)
            threading.Thread(target=server.serve_forever, daemon=True).start()
            logger.info(f"🌐 Heroku Web health server listening on port {port}")
        except Exception as e:
            logger.warning(f"Could not bind to PORT {port}: {e}")

if __name__ == "__main__":
    if not Config.BOT_TOKEN or not Config.API_ID or not Config.API_HASH:
        logger.error("❌ CRITICAL: BOT_TOKEN, API_ID, and API_HASH must be configured in environment variables!")
        sys.exit(1)

    Bot = Client(
        "Mr.Guardian_bot",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        sleep_threshold=120,
        plugins=dict(root="plugins")
    )

    async def init_owner_session():
        if Config.STRING_SESSION and Config.BOT_OWNER:
            try:
                from database import db
                if not await db.is_userbot_exist(Config.BOT_OWNER):
                    logger.info("🔄 Auto-linking owner UserBot from STRING_SESSION...")
                    user_client = Client("OWNER_USERBOT", Config.API_ID, Config.API_HASH, session_string=Config.STRING_SESSION, in_memory=True)
                    await user_client.start()
                    user_me = user_client.me
                    details = {
                        'id': user_me.id,
                        'is_bot': False,
                        'user_id': Config.BOT_OWNER,
                        'name': user_me.first_name,
                        'session': Config.STRING_SESSION,
                        'username': user_me.username
                    }
                    await db.add_userbot(details)
                    await user_client.stop()
                    logger.info(f"✅ Owner UserBot (@{user_me.username or user_me.first_name}) successfully registered in database!")
            except Exception as e:
                err_str = str(e)
                if "SSL" in err_str or "handshake" in err_str or "tlsv1" in err_str.lower():
                    logger.warning("⚠️ MongoDB Atlas SSL Handshake failed! Please add 0.0.0.0/0 to MongoDB Atlas Network Access IP Whitelist.")
                else:
                    logger.warning(f"⚠️ STRING_SESSION auto-registration skipped: {e}")

    async def main():
        start_health_server()
        await Bot.start()
        bot_info = await Bot.get_me()
        await init_owner_session()
        await restart_forwards(Bot)
        logger.info(f"Bot Started successfully as @{bot_info.username}!")
        print(f"[SUCCESS] Bot Started successfully as @{bot_info.username}!", flush=True)
        await idle()

    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user.")
