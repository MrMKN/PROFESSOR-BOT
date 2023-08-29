from pyrogram import Client, filters
from pyrogram.types import *
from aiohttp import ClientSession
from telegraph import upload_file
from io import BytesIO

ai_client = ClientSession()

async def make_carbon(code, tele=False):
    url = "https://carbonara.solopov.dev/api/cook"
    async with ai_client.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    if tele:
        uf = upload_file(image)
        image.close()
        return f"https://graph.org{uf[0]}"
    return image


@Client.on_message(filters.command("carbon"))
async def carbon_func(b, message):
    if not message.reply_to_message:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ.")
    if not message.reply_to_message.text:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ ᴛᴏ ᴍᴀᴋᴇ ᴄᴀʀʙᴏɴ.")
    user_id = message.from_user.id
    m = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("ᴜᴘʟᴏᴀᴅɪɴɢ..")
    await message.reply_photo(
        photo=carbon,
        caption="**ᴍᴀᴅᴇ ʙʏ: @mkn_bots_updates**",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ꜱᴜᴩᴩᴏʀᴛ ᴜꜱ", url="https://t.me/mkn_bots_updates")]]),                   
    )
    await m.delete()
    carbon.close()
