import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

@Client.on_message(filters.command(["json", 'js']))
async def jsonify(_, message):
    the_real_message = None
    reply_to_id = None
    pk = InlineKeyboardMarkup([[InlineKeyboardButton(text="𝙲𝙻𝙾𝚂𝙴", callback_data="close_data")]])  
                
    if message.reply_to_message:
        the_real_message = message.reply_to_message
    else:
        the_real_message = message

    try:        
        await message.reply_text(f"<code>{the_real_message}</code>", reply_markup=pk, quote=True)
    except Exception as e:
        with open("json.text", "w+", encoding="utf8") as out_file:
            out_file.write(str(the_real_message))       
        await message.reply_document(
            document="json.text",
            caption=str(e),
            disable_notification=True,
            quote=True,
            reply_markup=reply_markup
        )            
        os.remove("json.text")


@Client.on_message(filters.command("written"))
async def create_file(c, message):
    content = message.reply_to_message.text
    file_name = message.text.split(" ", 1)[1]   
    try:
        with open(str(file_name), "w+") as out:
            out.write(str(content))       
        await message.reply_document(
            document=str(file_name),
            caption="out put file"
        )            
        os.remove(str(file_name))
    except Exception as e:
        await message.reply(e)




