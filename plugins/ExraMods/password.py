import random, os
from pyrogram import Client, filters, enums 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command(["genpassword", 'genpw']))
async def password(bot, update):
    message = await update.reply_text(text="`Processing...`")
    password = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+".lower()
    ST = ["5", "7", "6", "9", "10", "12", "14", "8", "13"]
    qw = random.choice(ST)
    limit = int(qw)
    random_value = "".join(random.sample(password, limit))
    txt = f"<b>Limit:</b> {str(limit)} \n<b>Password: <code>{random_value}</code>"
    btn = InlineKeyboardMarkup([[InlineKeyboardButton('Mᴋɴ Bᴏᴛᴢ™️', url='https://t.me/mkn_bots_updates')]])
    await message.edit_text(text=txt, reply_markup=btn, parse_mode=enums.ParseMode.HTML)
