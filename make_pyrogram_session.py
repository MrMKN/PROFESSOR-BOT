"""
Pyrogram / Pyrofork String Session Generator for Forwarding_bot.
This generates the EXACT string session format required by Forwarding_bot (Pyrogram).
"""

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

API_ID = int(os.getenv("API_ID") or 17030067)
API_HASH = str(os.getenv("API_HASH") or "df64deb205933fbe14e50237b5ab68f2").strip()


async def main():
    try:
        from pyrogram import Client
    except ImportError:
        print("❌ Pyrofork/Pyrogram is not installed. Run: pip install pyrofork")
        return

    print("=" * 65)
    print("🔑 Pyrogram / Pyrofork String Session Generator")
    print(f"API_ID:   {API_ID}")
    print(f"API_HASH: {API_HASH[:6]}...{API_HASH[-4:]}")
    print("=" * 65)
    print("ℹ️ This generates the session required by Forwarding_bot.")
    print("   At the phone prompt, you can also type 'qrcode' to log in via QR code.")
    print("-" * 65)

    app = Client(
        name="userbot_session",
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True
    )

    try:
        await app.start()
        session_str = await app.export_session_string()
        me = await app.get_me()

        print("\n" + "=" * 65)
        print(f"✅ SUCCESS! Logged in as: {me.first_name} {me.last_name or ''}".strip())
        if me.username:
            print(f"   Username: @{me.username}")
        print(f"   User ID:  {me.id}")
        print("=" * 65)

        print("\n🔑 YOUR PYROGRAM STRING SESSION (Copy this):\n")
        print("-" * 65)
        print(session_str)
        print("-" * 65)

        # Save to Saved Messages
        try:
            await app.send_message(
                "me",
                f"**🔑 Pyrogram String Session for Forwarding_bot**\n\n"
                f"```{session_str}```\n\n"
                f"⚠️ *Keep this private! Paste this string into your Forwarding Bot.*"
            )
            print("\n📬 A backup copy has been sent to your Telegram 'Saved Messages'!")
        except Exception:
            pass

        # Save to .env
        save_env = os.path.join(SCRIPT_DIR, ".env")
        if os.path.exists(save_env):
            with open(save_env, "r", encoding="utf-8") as f:
                content = f.read()
            if "STRING_SESSION=" in content:
                import re
                content = re.sub(r"STRING_SESSION=.*", f"STRING_SESSION={session_str}", content)
            else:
                content += f"\nSTRING_SESSION={session_str}\n"
            with open(save_env, "w", encoding="utf-8") as f:
                f.write(content)
            print("💾 Saved STRING_SESSION to E:\\Forwarding_bot\\.env!")

        await app.stop()

    except Exception as e:
        print(f"\n❌ Error during session creation: {e}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n❌ Process cancelled.")
