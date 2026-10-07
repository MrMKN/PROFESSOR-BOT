import os
import sys
import asyncio

# Fix Windows unicode output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from dotenv import load_dotenv

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
local_env = os.path.join(SCRIPT_DIR, ".env")
if os.path.exists(local_env):
    load_dotenv(local_env, override=True)

# Dedicated credentials for Forwarding_bot
API_ID = int(os.getenv("API_ID") or 17030067)
API_HASH = str(os.getenv("API_HASH") or "df64deb205933fbe14e50237b5ab68f2").strip()

async def main():
    try:
        from telethon import TelegramClient
        from telethon.sessions import StringSession
    except ImportError:
        print("❌ Telethon is not installed. Run: pip install telethon")
        return

    print("=" * 65)
    print("🔑 Telethon String Session Generator (Forwarding Bot)")
    print(f"API_ID:   {API_ID}")
    print(f"API_HASH: {API_HASH[:6]}...{API_HASH[-4:]}")
    print("=" * 65)
    print("ℹ️ Telegram will send a login code to your Telegram app.")
    print("-" * 65)

    client = TelegramClient(StringSession(), API_ID, API_HASH)
    try:
        await client.start()
        session_str = client.session.save()
        me = await client.get_me()

        print("\n" + "=" * 65)
        print(f"✅ SUCCESS! Logged in as: {me.first_name} {me.last_name or ''}".strip())
        if me.username:
            print(f"   Username: @{me.username}")
        print(f"   User ID:  {me.id}")
        print("=" * 65)

        print("\n🔑 YOUR TELETHON STRING SESSION:\n")
        print("-" * 65)
        print(session_str)
        print("-" * 65)

        # Send copy to Saved Messages
        try:
            await client.send_message(
                "me",
                f"**🔑 Telethon String Session (Forwarding Bot)**\n\n"
                f"```{session_str}```\n\n"
                f"⚠️ *Keep this private! Do not share it.*"
            )
            print("\n📬 A backup copy has been sent to your Telegram 'Saved Messages'!")
        except Exception:
            pass

        # Save to E:\Forwarding_bot\.env
        save_env = os.path.join(SCRIPT_DIR, ".env")
        if os.path.exists(save_env):
            with open(save_env, "r", encoding="utf-8") as f:
                content = f.read()
            if "TELETHON_SESSION=" in content:
                import re
                content = re.sub(r"TELETHON_SESSION=.*", f"TELETHON_SESSION={session_str}", content)
            else:
                content += f"\nTELETHON_SESSION={session_str}\n"
            with open(save_env, "w", encoding="utf-8") as f:
                f.write(content)
            print("💾 Saved TELETHON_SESSION to E:\\Forwarding_bot\\.env!")

        await client.disconnect()

    except Exception as e:
        print(f"\n❌ Error during session creation: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n❌ Process cancelled.")
