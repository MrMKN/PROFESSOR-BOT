from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters


@Client.on_message(filters.photo & filters.private)
async def photo_handler(client, message):
    buttons = [[
        InlineKeyboardButton(text="𝖡𝗋𝗂𝗀𝗍𝗁", callback_data="bright"),
        InlineKeyboardButton(text="𝖬𝗂𝗑𝖾𝖽", callback_data="mix"),
        InlineKeyboardButton(text="𝖡 & 𝖶", callback_data="b|w"),
        ],[
        InlineKeyboardButton(text="𝖢𝗂𝗋𝖼𝗅𝖾", callback_data="circle"),
        InlineKeyboardButton(text="𝖡𝗅𝗎𝗋", callback_data="blur"),
        InlineKeyboardButton(text="𝖡𝗈𝗋𝖽𝖾𝗋", callback_data="border"),
        ],[
        InlineKeyboardButton(text="𝖲𝗍𝗂𝖼𝗄𝖾𝗋", callback_data="stick"),
        InlineKeyboardButton(text="𝖱𝗈𝗍𝖺𝗍𝖾", callback_data="rotate"),
        InlineKeyboardButton(text="𝖢𝗈𝗇𝗍𝗋𝖺𝗌𝗍", callback_data="contrast"),
        ],[
        InlineKeyboardButton(text="𝖲𝖾𝗉𝗂𝖺", callback_data="sepia"),
        InlineKeyboardButton(text="𝖯𝖾𝗇𝖼𝗂𝗅", callback_data="pencil"),
        InlineKeyboardButton(text="𝖢𝖺𝗋𝗍𝗈𝗈𝗇", callback_data="cartoon"),
        ],[
        InlineKeyboardButton(text="𝖨𝗇𝗏𝖾𝗋𝗍", callback_data="inverted"),
        InlineKeyboardButton(text="𝖦𝗅𝗂𝗍𝖼𝗁", callback_data="glitch"),
        InlineKeyboardButton(text="𝖱𝖾𝗆𝗈𝗏𝖾 𝖡𝖦", callback_data="removebg"),
        ],[
        InlineKeyboardButton(text="𝖢𝗅𝗈𝗌𝖾", callback_data="close_data"),
    ]]
    try:
        await message.reply(text="Select Your Required Mode From Below", quote=True, reply_markup=InlineKeyboardMarkup(buttons))            
    except Exception as e:
        print(e)
        if "USER_IS_BLOCKED" in str(e): return           
        try: await message.reply_text(f"{e} \nSomething Went Wrong!", quote=True)
        except Exception: return
