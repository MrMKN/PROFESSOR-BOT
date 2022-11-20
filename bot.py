#import logging
#import logging.config

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR, LOG_CHANNEL
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from datetime import datetime
import pytz

# Get logging configurations
#logging.config.fileConfig("logging.conf")
#logging.getLogger().setLevel(logging.INFO)
#logging.getLogger("pyrogram").setLevel(logging.ERROR)
#logging.getLogger("cinemagoer").setLevel(logging.ERROR)

class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=300,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        temp.B_LINK = me.mention 
        self.username = '@' + me.username
        IST = pytz.timezone('Asia/Kolkata')
        datetime_ist = datetime.now(IST)
        GMT = datetime_ist.strftime("%I:%M:%S %p - %d %B %Y")     
        #logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        #logging.info(LOG_STR)
        await self.send_message(LOG_CHANNEL, text=f"⚡️ BOT STARTED\n\nBot Namr: {me.first_name}\nUserName: @{me.username}\nPyrogram: v{__version__}\nLyer: {layer}\n\nTime : {GMT}")                         

    async def stop(self, *args):
        await super().stop()
        me = await self.get_me()
        #logging.info(f"{me.first_name} is_...  ♻️Restarting...")

    async def iter_messages(self, chat_id: Union[int, str], limit: int, offset: int = 0) -> Optional[AsyncGenerator["types.Message", None]]:                       
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1


        
app = Bot()
app.run()






