import os, math, logging, datetime, pytz, logging.config
from aiohttp import web
from pyrogram import Client, types
from database.users_chats_db import db
from database.ia_filterdb import Media
from typing import Union, Optional, AsyncGenerator
from utils import temp, __repo__, __license__, __copyright__, __version__
from info import API_ID, API_HASH, BOT_TOKEN, LOG_CHANNEL, UPTIME, LOG_MSG
from pyrogram.errors import FloodWait
import asyncio  # Import asyncio for delays

# Get logging configurations
logging.config.fileConfig("logging.conf")
logging.getLogger(__name__).setLevel(logging.INFO)
logging.getLogger("cinemagoer").setLevel(logging.ERROR)


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Professor-Bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins")
        )

    async def start(self):
        try:
            # Fetch banned users and chats
            b_users, b_chats = await db.get_banned()
            temp.BANNED_USERS = b_users
            temp.BANNED_CHATS = b_chats        

            await super().start()
            await Media.ensure_indexes()
            me = await self.get_me()
            temp.U_NAME = me.username
            temp.B_NAME = me.first_name
            self.id = me.id
            self.name = me.first_name
            self.mention = me.mention
            self.username = me.username
            self.log_channel = LOG_CHANNEL
            self.uptime = UPTIME
            curr = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            date = curr.strftime('%d %B, %Y')
            time = curr.strftime('%I:%M:%S %p')

            # Log successful startup
            logging.info(LOG_MSG.format(me.first_name, date, time, __repo__, __version__, __license__, __copyright__))
            
            # Try sending a startup message to LOG_CHANNEL
            try:
                await self.send_message(
                    LOG_CHANNEL, 
                    text=LOG_MSG.format(me.first_name, date, time, __repo__, __version__, __license__, __copyright__), 
                    disable_web_page_preview=True
                )   
            except Exception as e:
                logging.warning(f"Bot isn't able to send message to LOG_CHANNEL \n{e}")
        
            # Web server starts on port 8080
            try:
                app = web.Application(client_max_size=30000000)
                runner = web.AppRunner(app)
                await runner.setup()
                site = web.TCPSite(runner, "0.0.0.0", 8080)
                await site.start()
                logging.info("Web response is running on port 8080 🕸️")
            except Exception as e:
                logging.error(f"Error starting web server: {e}")

        except FloodWait as e:
            # Handle FloodWait exception and wait for the required duration
            logging.warning(f"Flood wait error: Telegram requires waiting for {e.value} seconds.")
            await asyncio.sleep(e.value)  # Wait before retrying
            await self.start()  # Retry starting the bot

        except Exception as e:
            logging.error(f"Error during bot startup: {e}")

    async def stop(self, *args):
        await super().stop()
        logging.info(f"Bot is stopping ⟳...")

    async def iter_messages(self, chat_id: Union[int, str], limit: int, offset: int = 0) -> Optional[AsyncGenerator["types.Message", None]]:                       
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current + new_diff + 1)))
            for message in messages:
                yield message
                current += 1


if __name__ == '__main__':
    Bot().run()






















