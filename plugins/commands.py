import os
import sys
import asyncio
import logging
import psutil
import time
from os import environ, execle, system

from database import db
from config import Config, temp
from script import Script
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

logger = logging.getLogger(__name__)

START_TIME = time.time()

main_buttons = [
    [
        InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/moviesguardianss')
    ],
    [
        InlineKeyboardButton('👨‍💻 ʜᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('💁 ᴀʙᴏᴜᴛ', callback_data='about')
    ],
    [
        InlineKeyboardButton('⚙ sᴇᴛᴛɪɴɢs', callback_data='settings#main'),
        InlineKeyboardButton('📊 sᴛᴀᴛᴜs', callback_data='status')
    ]
]


def format_file_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    if not size_bytes or size_bytes <= 0:
        return "Unknown"
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


async def get_bot_uptime(start_time: float) -> str:
    """Calculate the uptime in readable format."""
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_weeks = uptime_days // 7
    uptime_string = ""
    if uptime_weeks > 0:
        uptime_string += f"{uptime_weeks}W "
    if uptime_days % 7 > 0:
        uptime_string += f"{uptime_days % 7}D "
    if uptime_hours % 24 > 0:
        uptime_string += f"{uptime_hours % 24}H "
    if uptime_minutes % 60 > 0:
        uptime_string += f"{uptime_minutes % 60}M "
    uptime_string += f"{uptime_seconds % 60}S"
    return uptime_string.strip()


# ==========================================
# /start Command Handler
# ==========================================
@Client.on_message(filters.command(['start']))
async def start(client: Client, message: Message):
    user = message.from_user
    user_id = user.id if user else message.chat.id
    first_name = (user.first_name if user else "User") or "User"

    # Deep-link arguments support (e.g., /start help)
    text_parts = message.text.split(maxsplit=1)
    if len(text_parts) > 1:
        param = text_parts[1].strip().lower()
        if param == "help":
            return await help_command(client, message)
        elif param == "about":
            return await about_command(client, message)
        elif param in ["status", "stats"]:
            return await stats_command(client, message)

    # Safely save user to database (never crash /start on DB network issues)
    if user:
        try:
            if not await db.is_user_exist(user.id):
                await db.add_user(user.id, first_name)
        except Exception as e:
            logger.debug(f"User registration in DB skipped: {e}")

    reply_markup = InlineKeyboardMarkup(main_buttons)
    await message.reply_text(
        text=Script.START_TXT.format(first_name),
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


# ==========================================
# /help Command Handler
# ==========================================
@Client.on_message(filters.command(['help']))
async def help_command(client: Client, message: Message):
    buttons = [
        [
            InlineKeyboardButton('🤔 ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ❓', callback_data='how_to_use'),
            InlineKeyboardButton('⚙ sᴇᴛᴛɪɴɢs', callback_data='settings#main')
        ],
        [
            InlineKeyboardButton('💁 ᴀʙᴏᴜᴛ', callback_data='about'),
            InlineKeyboardButton('📊 sᴛᴀᴛᴜs', callback_data='status')
        ],
        [
            InlineKeyboardButton('🤖 ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ', url='https://t.me/moviesguardianss')
        ]
    ]
    await message.reply_text(
        text=Script.HELP_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


# ==========================================
# /ping Command Handler (from tele_bot)
# ==========================================
@Client.on_message(filters.command(['ping']))
async def ping(client: Client, message: Message):
    start_t = time.time()
    reply = await message.reply_text("🏓 <i>Pinging...</i>")
    delta_ms = (time.time() - start_t) * 1000
    uptime_str = await get_bot_uptime(START_TIME)
    await reply.edit_text(
        f"<b>🏓 PONG!</b>\n\n"
        f"⚡ <b>Latency:</b> <code>{delta_ms:.2f} ms</code>\n"
        f"⏱ <b>Uptime:</b> <code>{uptime_str}</code>"
    )


# ==========================================
# /id Command Handler (from tele_bot)
# ==========================================
@Client.on_message(filters.command(['id']))
async def id_command(client: Client, message: Message):
    text = f"👤 <b>Your ID:</b> <code>{message.from_user.id if message.from_user else 'Unknown'}</code>\n"
    text += f"💬 <b>Chat ID:</b> <code>{message.chat.id}</code>\n"
    text += f"📨 <b>Message ID:</b> <code>{message.id}</code>"

    if message.reply_to_message:
        reply = message.reply_to_message
        if reply.from_user:
            uname = f" (@{reply.from_user.username})" if reply.from_user.username else ""
            text += f"\n\n👥 <b>Replied User ID:</b> <code>{reply.from_user.id}</code>{uname}"
        text += f"\n📩 <b>Replied Message ID:</b> <code>{reply.id}</code>"
        if reply.forward_from_chat:
            text += f"\n📢 <b>Forwarded Channel ID:</b> <code>{reply.forward_from_chat.id}</code>"
            if reply.forward_from_chat.title:
                text += f" (<b>{reply.forward_from_chat.title}</b>)"

    await message.reply_text(text)


# ==========================================
# /info Command Handler (from tele_bot)
# ==========================================
@Client.on_message(filters.command(['info']))
async def info_command(client: Client, message: Message):
    target = (
        message.reply_to_message.from_user 
        if message.reply_to_message and message.reply_to_message.from_user 
        else message.from_user
    )
    if not target:
        return await message.reply_text("Unable to determine user.")

    text = (
        f"<b>ℹ️ User Profile</b>\n\n"
        f"👤 <b>First Name:</b> {target.first_name}\n"
    )
    if target.last_name:
        text += f"👤 <b>Last Name:</b> {target.last_name}\n"
    if target.username:
        text += f"🔖 <b>Username:</b> @{target.username}\n"
    text += (
        f"🆔 <b>User ID:</b> <code>{target.id}</code>\n"
        f"🤖 <b>Is Bot:</b> <code>{target.is_bot}</code>\n"
        f"🔗 <b>Permanent Link:</b> <a href='tg://user?id={target.id}'>Profile</a>"
    )
    await message.reply_text(text)


# ==========================================
# /status and /stats Command Handler
# ==========================================
@Client.on_message(filters.command(['status', 'stats']))
async def stats_command(client: Client, message: Message):
    users_count, bots_count, forwardings = "N/A", "N/A", "N/A"
    try:
        users_count, bots_count = await db.total_users_bots_count()
        forwardings = await db.forwad_count()
    except Exception as e:
        logger.debug(f"DB stats fetch error: {e}")

    upt = await get_bot_uptime(START_TIME)
    buttons = [[
        InlineKeyboardButton('🖥️ System Stats', callback_data='systm_sts'),
        InlineKeyboardButton('⚙ Settings', callback_data='settings#main')
    ]]
    await message.reply_text(
        text=Script.STATUS_TXT.format(upt, users_count, bots_count, forwardings),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


# ==========================================
# /about Command Handler
# ==========================================
@Client.on_message(filters.command(['about']))
async def about_command(client: Client, message: Message):
    buttons = [[
        InlineKeyboardButton('👨‍💻 ʜᴇʟᴘ', callback_data='help'),
        InlineKeyboardButton('📊 sᴛᴀᴛᴜs', callback_data='status')
    ]]
    await message.reply_text(
        text=Script.ABOUT_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


# ==========================================
# /cancel Command Handler
# ==========================================
@Client.on_message(filters.command(['cancel']))
async def cancel_command(client: Client, message: Message):
    user_id = message.from_user.id if message.from_user else message.chat.id
    temp.CANCEL[user_id] = True
    temp.lock[user_id] = False
    await message.reply_text(Script.CANCEL)


# ==========================================
# /restart Command Handler (Owner Only)
# ==========================================
@Client.on_message(filters.command(['restart']) & filters.user(Config.BOT_OWNER))
async def restart(client: Client, message: Message):
    msg = await message.reply_text(text="<i>Restarting Mr.Guardian Bot...</i>")
    await asyncio.sleep(2)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    execle(sys.executable, sys.executable, "main.py", environ)


# ==========================================
# Callback Query Handlers
# ==========================================
@Client.on_callback_query(filters.regex(r'^help'))
async def helpcb(bot: Client, query: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton('🤔 ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴍᴇ ❓', callback_data='how_to_use')
        ],
        [
            InlineKeyboardButton('Aʙᴏᴜᴛ ✨️', callback_data='about'),
            InlineKeyboardButton('⚙ Sᴇᴛᴛɪɴɢs', callback_data='settings#main')
        ],
        [
            InlineKeyboardButton('• back', callback_data='back')
        ]
    ]
    await query.message.edit_text(text=Script.HELP_TXT, reply_markup=InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex(r'^how_to_use'))
async def how_to_use(bot: Client, query: CallbackQuery):
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    await query.message.edit_text(
        text=Script.HOW_USE_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex(r'^back'))
async def back(bot: Client, query: CallbackQuery):
    first_name = (query.from_user.first_name if query.from_user else "User") or "User"
    await query.message.edit_text(
        reply_markup=InlineKeyboardMarkup(main_buttons),
        text=Script.START_TXT.format(first_name)
    )


@Client.on_callback_query(filters.regex(r'^about'))
async def about(bot: Client, query: CallbackQuery):
    buttons = [
        [
            InlineKeyboardButton('• back', callback_data='help'),
            InlineKeyboardButton('Stats ✨️', callback_data='status')
        ]
    ]
    await query.message.edit_text(
        text=Script.ABOUT_TXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex(r'^status'))
async def status(bot: Client, query: CallbackQuery):
    users_count, bots_count, forwardings = "N/A", "N/A", "N/A"
    try:
        users_count, bots_count = await db.total_users_bots_count()
        forwardings = await db.forwad_count()
    except Exception as e:
        logger.debug(f"Stats DB fetch: {e}")

    upt = await get_bot_uptime(START_TIME)
    buttons = [
        [
            InlineKeyboardButton('• back', callback_data='help'),
            InlineKeyboardButton('System Stats ✨️', callback_data='systm_sts'),
        ]
    ]
    await query.message.edit_text(
        text=Script.STATUS_TXT.format(upt, users_count, bots_count, forwardings),
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True,
    )


@Client.on_callback_query(filters.regex(r'^systm_sts'))
async def sys_status(bot: Client, query: CallbackQuery):
    buttons = [[InlineKeyboardButton('• back', callback_data='help')]]
    try:
        ram = psutil.virtual_memory().percent
        cpu = psutil.cpu_percent()
        disk_usage = psutil.disk_usage('/')
        total_space = disk_usage.total / (1024**3)
        used_space = disk_usage.used / (1024**3)
        free_space = disk_usage.free / (1024**3)
    except Exception:
        total_space, used_space, free_space, cpu, ram = 0, 0, 0, 0, 0

    text = f"""
╔════❰ sᴇʀᴠᴇʀ sᴛᴀᴛs  ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ <b>ᴛᴏᴛᴀʟ ᴅɪsᴋ sᴘᴀᴄᴇ</b>: <code>{total_space:.2f} GB</code>
║┣⪼ <b>ᴜsᴇᴅ</b>: <code>{used_space:.2f} GB</code>
║┣⪼ <b>ꜰʀᴇᴇ</b>: <code>{free_space:.2f} GB</code>
║┣⪼ <b>ᴄᴘᴜ</b>: <code>{cpu}%</code>
║┣⪼ <b>ʀᴀᴍ</b>: <code>{ram}%</code>
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪
"""
    await query.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(buttons),
        disable_web_page_preview=True,
    )


# ==========================================
# Media Info Inspector (from tele_bot)
# Inspects any file sent in private chat
# ==========================================
@Client.on_message(filters.private & (filters.document | filters.video | filters.audio | filters.photo))
async def media_inspector(client: Client, message: Message):
    # Only inspect if the user is not in a dialogue/listen state
    user_id = message.from_user.id if message.from_user else 0
    if temp.lock.get(user_id):
        return  # Another task is currently processing

    file_name = "Unknown"
    file_size = 0
    file_type = "File"
    file_id = ""

    if message.document:
        doc = message.document
        file_name = doc.file_name or "document"
        file_size = doc.file_size or 0
        file_type = "Document 📄"
        file_id = doc.file_id
    elif message.video:
        vid = message.video
        file_name = vid.file_name or "video.mp4"
        file_size = vid.file_size or 0
        file_type = "Video 🎥"
        file_id = vid.file_id
    elif message.audio:
        aud = message.audio
        file_name = aud.file_name or (f"{aud.title}.mp3" if aud.title else "audio.mp3")
        file_size = aud.file_size or 0
        file_type = "Audio 🎵"
        file_id = aud.file_id
    elif message.photo:
        photo = message.photo
        file_name = "photo.jpg"
        file_size = photo.file_size or 0
        file_type = "Photo 🖼"
        file_id = photo.file_id

    size_str = format_file_size(file_size)
    text = (
        f"<b>📁 Media Details:</b>\n\n"
        f"<b>Type:</b> {file_type}\n"
        f"<b>Name:</b> <code>{file_name}</code>\n"
        f"<b>Size:</b> <code>{size_str}</code>\n"
        f"<b>File ID:</b> <code>{file_id[:35]}...</code>\n\n"
        f"<i>💡 To forward messages between channels, use /forward</i>"
    )
    await message.reply_text(text)
