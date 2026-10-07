"""
Interactive Telegram String Session Generator for Pyrogram (Pyrofork) & Telethon.
Tailored for Forwarding_bot (E:\\Forwarding_bot).

Usage:
    python generate_session_string.py
"""

from __future__ import annotations

import os
import sys
import asyncio
from getpass import getpass

# Fix Windows Unicode output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Try loading from local .env
try:
    from dotenv import load_dotenv
    local_env = os.path.join(SCRIPT_DIR, ".env")
    if os.path.exists(local_env):
        load_dotenv(local_env, override=True)
    else:
        load_dotenv()
except ImportError:
    pass

DEFAULT_API_ID = os.getenv("API_ID") or "17030067"
DEFAULT_API_HASH = os.getenv("API_HASH") or "df64deb205933fbe14e50237b5ab68f2"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


async def generate_pyrogram_session(api_id: int, api_hash: str):
    try:
        from pyrogram import Client
    except ImportError:
        print("\n❌ Pyrofork/Pyrogram is not installed.")
        print("Run: pip install pyrofork tgcrypto\n")
        return

    print("\n" + "=" * 65)
    print("🔹 Generating Pyrogram / Pyrofork String Session")
    print("   (Required for E:\\Forwarding_bot)")
    print("=" * 65)
    print("ℹ️ Pyrogram will prompt you for your Phone number, OTP code,")
    print("   and 2FA password (if enabled). You can also type 'qrcode'")
    print("   at the phone prompt to log in via Telegram QR code.\n")

    app = Client(
        name="string_session_gen",
        api_id=api_id,
        api_hash=api_hash,
        in_memory=True
    )

    try:
        await app.start()
        session_str = await app.export_session_string()
        me = await app.get_me()

        print("\n" + "=" * 65)
        print("✅ SUCCESS! Logged in as:")
        print(f"   Name:     {me.first_name} {me.last_name or ''}".strip())
        print(f"   Username: @{me.username}" if me.username else "   Username: None")
        print(f"   User ID:  {me.id}")
        print("=" * 65)

        print("\n🔑 YOUR PYROGRAM STRING SESSION:\n")
        print("-" * 65)
        print(session_str)
        print("-" * 65)

        # Try sending to Saved Messages
        try:
            await app.send_message(
                "me",
                f"**🔑 Pyrogram String Session for Forwarding_bot**\n\n"
                f"```{session_str}```\n\n"
                f"⚠️ *Keep this string private! Anyone with this string can access your Telegram account.*"
            )
            print("\n📬 A copy of this session string has been saved to your Telegram Saved Messages.")
        except Exception:
            pass

        # Offer to save into .env
        save_choice = input("\nSave this session to E:\\Forwarding_bot\\.env? (y/n): ").strip().lower()
        if save_choice in ("y", "yes"):
            save_to_env("STRING_SESSION", session_str)
            print("💾 Saved to .env successfully!")

        await app.stop()

    except Exception as e:
        print(f"\n❌ Error during session generation: {e}")


async def generate_telethon_session(api_id: int, api_hash: str):
    try:
        from telethon import TelegramClient
        from telethon.sessions import StringSession
    except ImportError:
        print("\n❌ Telethon is not installed.")
        print("Run: pip install telethon\n")
        return

    print("\n" + "=" * 65)
    print("🔹 Generating Telethon String Session")
    print("   (Used for Telethon Indexer & Telethon bots)")
    print("=" * 65)

    client = TelegramClient(StringSession(), api_id, api_hash)
    try:
        await client.start()
        session_str = client.session.save()
        me = await client.get_me()

        print("\n" + "=" * 65)
        print("✅ SUCCESS! Logged in as:")
        print(f"   Name:     {me.first_name} {me.last_name or ''}".strip())
        print(f"   Username: @{me.username}" if me.username else "   Username: None")
        print(f"   User ID:  {me.id}")
        print("=" * 65)

        print("\n🔑 YOUR TELETHON STRING SESSION:\n")
        print("-" * 65)
        print(session_str)
        print("-" * 65)

        try:
            await client.send_message(
                "me",
                f"**🔑 Telethon String Session**\n\n"
                f"```{session_str}```\n\n"
                f"⚠️ *Keep this string private! Anyone with this string can access your Telegram account.*"
            )
            print("\n📬 A copy of this session string has been saved to your Telegram Saved Messages.")
        except Exception:
            pass

        await client.disconnect()

    except Exception as e:
        print(f"\n❌ Error during session generation: {e}")


def save_to_env(key: str, value: str, filepath: str = None):
    if filepath is None:
        filepath = os.path.join(SCRIPT_DIR, ".env")
    lines = []
    found = False
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith(f"{key}=") or line.startswith(f"{key} ="):
            new_lines.append(f"{key}={value}\n")
            found = True
        else:
            new_lines.append(line)

    if not found:
        if new_lines and not new_lines[-1].endswith("\n"):
            new_lines.append("\n")
        new_lines.append(f"{key}={value}\n")

    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


async def main():
    print("=" * 65)
    print("🤖 Telegram String Session Generator (E:\\Forwarding_bot)")
    print("=" * 65)
    print("Choose Library:")
    print("  [1] Pyrogram / Pyrofork (Recommended - used by Forwarding_bot)")
    print("  [2] Telethon (Used by tele_bot / Telethon indexer)")
    print("-" * 65)

    choice = input("Enter choice [1/2] (default: 1): ").strip()
    if choice not in ("1", "2"):
        choice = "1"

    print("\n--- Telegram API Credentials ---")
    api_id_input = input(f"Enter API_ID [{DEFAULT_API_ID}]: ").strip()
    api_id_val = api_id_input if api_id_input else DEFAULT_API_ID

    api_hash_input = input(f"Enter API_HASH [{DEFAULT_API_HASH}]: ").strip()
    api_hash_val = api_hash_input if api_hash_input else DEFAULT_API_HASH

    try:
        api_id_int = int(api_id_val)
    except ValueError:
        print("❌ Invalid API_ID. It must be an integer.")
        return

    if not api_hash_val:
        print("❌ API_HASH cannot be empty.")
        return

    if choice == "1":
        await generate_pyrogram_session(api_id_int, api_hash_val)
    else:
        await generate_telethon_session(api_id_int, api_hash_val)

    print("\n✅ Finished.")
    print("=" * 65)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n❌ Process cancelled by user.")
