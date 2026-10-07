
import os
import sys 
import math
import time, re
import asyncio 
import logging
import random
from .utils import STS
from database import Db, db
from .test import CLIENT, get_client, iter_messages
from config import Config, temp
from script import Script
from pyrogram import Client, filters 
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message 
from .db import connect_user_db
from pyrogram.types import Message


CLIENT = CLIENT()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
TEXT = Script.TEXT


@Client.on_callback_query(filters.regex(r'^start_public'))
async def pub_(bot, message):
    user = message.from_user.id
    temp.CANCEL[user] = False
    frwd_id = message.data.split("_")[2]
    if temp.lock.get(user) and str(temp.lock.get(user))=="True":
      return await message.answer("please wait until previous task complete", show_alert=True)
    sts = STS(frwd_id)
    if not sts.verify():
      await message.answer("your are clicking on my old button", show_alert=True)
      return await message.message.delete()
    i = sts.get(full=True)
    if i.TO in temp.IS_FRWD_CHAT:
      return await message.answer("In Target chat a task is progressing. please wait until task complete", show_alert=True)
    m = await msg_edit(message.message, "<code>verifying your data's, please wait.</code>")
    _bot, caption, forward_tag, datas, protect, button = await sts.get_data(user)
    filter = datas['filters']
    max_size = datas['max_size']
    min_size = datas['min_size']
    keyword = datas['keywords']
    exten = datas['extensions']
    keywords = ""
    extensions = ""
    if keyword:
        for key in keyword:
            keywords += f"{key}|"
        keywords  = keywords.rstrip("|")
    else:
        keywords = None
    if exten:
        for ext in exten:
            extensions += f"{ext}|"
        extensions = extensions.rstrip("|")
    else:
        extensions = None
    if not _bot:
      return await msg_edit(m, "<code>You didn't added any bot. Please add a bot using /settings !</code>", wait=True)
    if _bot['is_bot'] == True:
        data = _bot['token']
    else:
        data = _bot['session']
    try:
      il = True if _bot['is_bot'] == True else False
      client = await get_client(data, is_bot=il)
      await client.start()
    except Exception as e:  
      return await m.edit(e)
    await msg_edit(m, "<code>processing..</code>")
    try: 
       await client.get_messages(sts.get("FROM"), sts.get("limit"))
    except:
       await msg_edit(m, f"**Source chat may be a private channel / group. Use userbot (user must be member over there) or  if Make Your [Bot](t.me/{_bot['username']}) an admin over there**", retry_btn(frwd_id), True)
       return await stop(client, user)
    try:
       k = await client.send_message(i.TO, "Testing")
       await k.delete()
    except:
       await msg_edit(m, f"**Please Make Your [UserBot / Bot](t.me/{_bot['username']}) Admin In Target Channel With Full Permissions**", retry_btn(frwd_id), True)
       return await stop(client, user)
    user_have_db = False
    dburi = datas['db_uri']
    if dburi is not None:
        connected, user_db = await connect_user_db(user, dburi, i.TO)
        if not connected:
            await msg_edit(m, "<code>Cannot Connected Your db Errors Found Dup files Have Been Skipped after Restart</code>")
        else:
            user_have_db = True
    temp.forwardings += 1
    await db.add_frwd(user)
    await send(client, user, "<b>Fᴏʀᴡᴀᴅɪɴɢ sᴛᴀʀᴛᴇᴅ🔥</b>")
    sts.add(time=True)
    sleep = 0.5 if _bot['is_bot'] else getattr(Config, "FORWARD_SLEEP", 1.8)
    await msg_edit(m, "<code>processing...</code>") 
    temp.IS_FRWD_CHAT.append(i.TO)
    temp.lock[user] = locked = True
    dup_files = []
    if locked:
        try:
          MSG = []
          pling=0
          await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
          async for message in iter_messages(client, chat_id=sts.get("FROM"), limit=sts.get("limit"), offset=sts.get("skip"), filters=filter, max_size=max_size):
                if await is_cancelled(client, user, m, sts):
                   if user_have_db:
                      await user_db.drop_all()
                      await user_db.close()
                   return
                if pling %20 == 0: 
                   await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
                pling += 1
                sts.add('fetched')
                if message == "DUPLICATE":
                   sts.add('duplicate')
                   continue
                elif message == "FILTERED":
                   sts.add('filtered')
                   continue 
                elif message.empty or message.service:
                   sts.add('deleted')
                   continue
                elif message.document and await extension_filter(extensions, message.document.file_name):
                   sts.add('filtered')
                   continue 
                elif message.document and await keyword_filter(keywords, message.document.file_name):
                   sts.add('filtered')
                   continue 
                elif message.document and await size_filter(max_size, min_size, message.document.file_size):
                   sts.add('filtered')
                   continue 
                elif message.document and message.document.file_id in dup_files:
                   sts.add('duplicate')
                   continue
                if message.document and datas['skip_duplicate']:
                    dup_files.append(message.document.file_id)
                    if user_have_db:
                        await user_db.add_file(message.document.file_id)
                if forward_tag:
                   MSG.append(message.id)
                   notcompleted = len(MSG)
                   completed = sts.get('total') - sts.get('fetched')
                   if ( notcompleted >= 100 
                        or completed <= 100): 
                      await forward(user, client, MSG, m, sts, protect)
                      sts.add('total_files', notcompleted)
                      await asyncio.sleep(5)
                      MSG = []
                else:
                   new_caption = custom_caption(message, caption)
                   details = {"msg_id": message.id, "media": media(message), "caption": new_caption, 'button': button, "protect": protect}
                   await copy(user, client, details, m, sts)
                   sts.add('total_files')
                   actual_sleep = sleep if _bot['is_bot'] else random.uniform(max(1.0, sleep * 0.9), sleep * 1.15)
                   await asyncio.sleep(actual_sleep) 
        except Exception as e:
            await msg_edit(m, f'<b>ERROR:</b>\n<code>{e}</code>', wait=True)
            print(e)
            if user_have_db:
                await user_db.drop_all()
                await user_db.close()
            temp.IS_FRWD_CHAT.remove(sts.TO)
            return await stop(client, user)
        temp.IS_FRWD_CHAT.remove(sts.TO)
        await send(client, user, "<b>🎉 ғᴏʀᴡᴀᴅɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</b>")
        await edit(user, m, 'ᴄᴏᴍᴘʟᴇᴛᴇᴅ', "completed", sts) 
        if user_have_db:
            await user_db.drop_all()
            await user_db.close()
        await stop(client, user)


async def copy(user, bot, msg, m, sts):
   try:                               
     if msg.get("media") and msg.get("caption"):
        try:
           await bot.send_cached_media(
                 chat_id=sts.get('TO'),
                 file_id=msg.get("media"),
                 caption=msg.get("caption"),
                 reply_markup=msg.get('button'),
                 protect_content=msg.get("protect"))
        except Exception:
           await bot.copy_message(
                 chat_id=sts.get('TO'),
                 from_chat_id=sts.get('FROM'),    
                 caption=msg.get("caption"),
                 message_id=msg.get("msg_id"),
                 reply_markup=msg.get('button'),
                 protect_content=msg.get("protect"))
     elif not msg.get("media") and msg.get("caption"):
        await bot.send_message(
              chat_id=sts.get('TO'),
              text=msg.get("caption"),
              reply_markup=msg.get('button'),
              protect_content=msg.get("protect"))
     else:
        await bot.copy_message(
              chat_id=sts.get('TO'),
              from_chat_id=sts.get('FROM'),    
              caption=msg.get("caption"),
              message_id=msg.get("msg_id"),
              reply_markup=msg.get('button'),
              protect_content=msg.get("protect"))
   except FloodWait as e:
     await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', e.value, sts)
     await asyncio.sleep(e.value)
     await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
     await copy(user, bot, msg, m, sts)
   except Exception as e:
     print(e)
     sts.add('deleted')


async def forward(user, bot, msg, m, sts, protect):
   try:                             
     await bot.forward_messages(
           chat_id=sts.get('TO'),
           from_chat_id=sts.get('FROM'), 
           protect_content=protect,
           message_ids=msg)
   except FloodWait as e:
     await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', e.value, sts)
     await asyncio.sleep(e.value)
     await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
     await forward(user, bot, msg, m, sts, protect)


async def msg_edit(msg, text, button=None, wait=None):
    try:
        return await msg.edit(text, reply_markup=button)
    except MessageNotModified:
        pass 
    except FloodWait as e:
        if wait:
           await asyncio.sleep(e.value)
           return await msg_edit(msg, text, button, wait)


async def edit(user, msg, title, status, sts):
   i = sts.get(full=True)
   status = 'Forwarding' if status == 5 else f"sleeping {status} s" if str(status).isnumeric() else status
   percentage = "{:.0f}".format(float(i.fetched)*100/float(i.total))
   text = TEXT.format(i.fetched, i.total_files, i.duplicate, i.deleted, i.skip, i.filtered, status, percentage, title)
   await update_forward(user_id=user, last_id=None, start_time=i.start, limit=i.limit, chat_id=i.FROM, toid=i.TO, forward_id=None, msg_id=msg.id, fetched=i.fetched, deleted=i.deleted, total=i.total_files, duplicate=i.duplicate, skip=i.skip, filterd=i.filtered)
   now = time.time()
   diff = int(now - i.start)
   speed = sts.divide(i.fetched, diff)
   elapsed_time = round(diff) * 1000
   time_to_completion = round(sts.divide(i.total - i.fetched, int(speed))) * 1000
   estimated_total_time = elapsed_time + time_to_completion  
   progress = "●{0}{1}".format(
       ''.join(["●" for i in range(math.floor(int(percentage) / 4))]),
       ''.join(["○" for i in range(24 - math.floor(int(percentage) / 4))]))
   button =  [[InlineKeyboardButton(progress, f'fwrdstatus#{status}#{estimated_total_time}#{percentage}#{i.id}')]]
   estimated_total_time = TimeFormatter(milliseconds=estimated_total_time)
   estimated_total_time = estimated_total_time if estimated_total_time != '' else '0 s'
   if status in ["cancelled", "completed"]:
      button.append([InlineKeyboardButton('• ᴄᴏᴍᴘʟᴇᴛᴇᴅ •', url='https://t.me/moviesguardianss')])
   else:
      button.append([InlineKeyboardButton('• ᴄᴀɴᴄᴇʟ', 'terminate_frwd')])
   await msg_edit(msg, text, InlineKeyboardMarkup(button))


async def is_cancelled(client, user, msg, sts):
   if temp.CANCEL.get(user)==True:
      if sts.TO in temp.IS_FRWD_CHAT:
         temp.IS_FRWD_CHAT.remove(sts.TO)
      await edit(user, msg, 'ᴄᴀɴᴄᴇʟʟᴇᴅ', "cancelled", sts)
      await send(client, user, "<b>❌ ғᴏʀᴡᴀᴅɪɴɢ ᴄᴀɴᴄᴇʟʟᴇᴅ</b>")
      await stop(client, user)
      return True 
   return False 


async def stop(client, user):
   try:
     await client.stop()
   except:
     pass 
   await db.rmve_frwd(user)
   temp.forwardings -= 1
   temp.lock[user] = False 


async def send(bot, user, text):
   try:
      await bot.send_message(user, text=text)
   except:
      pass 


def replace_channel_branding(text: str, target_channel: str = None) -> str:
    if not target_channel:
        target_channel = getattr(Config, "CHANNEL_USERNAME", "@moviesguardianss") or "@moviesguardianss"
    if not target_channel.startswith("@"):
        target_channel = "@" + target_channel
    target_link = f"https://t.me/{target_channel.lstrip('@')}"

    if not text:
        return f"<b>Channel:</b> {target_channel}"

    clean_target = target_channel.lstrip("@").lower()

    # 1. Replace telegram links: https://t.me/old_channel or t.me/old_channel
    def link_repl(match):
        slug = match.group(2)
        if slug.lower() == clean_target:
            return match.group(0)
        return target_link

    text = re.sub(r'(https?://t\.me/|t\.me/)([a-zA-Z0-9_]{4,})', link_repl, text, flags=re.IGNORECASE)

    # 2. Replace @mentions: @old_channel (not matching target_channel)
    def user_repl(match):
        u = match.group(0)
        if u.lower() == target_channel.lower():
            return u
        return target_channel

    text = re.sub(r'@[a-zA-Z0-9_]{4,}', user_repl, text)

    # 3. If target_channel is still not mentioned anywhere in the caption, append it
    if target_channel.lower() not in text.lower():
        text = text.rstrip() + f"\n\n<b>Channel:</b> {target_channel}"

    return text

def custom_caption(msg, caption):
  target_ch = getattr(Config, "CHANNEL_USERNAME", "@moviesguardianss") or "@moviesguardianss"
  if not target_ch.startswith("@"):
      target_ch = "@" + target_ch

  if msg.media:
    if (msg.video or msg.document or msg.audio or msg.photo):
      media = getattr(msg, msg.media.value, None)
      if media:
        raw_file_name = getattr(media, 'file_name', '') or ''
        # Replace any @mention in the file name for display in caption
        file_name = re.sub(r'@[a-zA-Z0-9_]{4,}', target_ch, raw_file_name)
        file_size = getattr(media, 'file_size', '')
        fcaption = getattr(msg, 'caption', '')
        if fcaption:
          fcaption = fcaption.html
        else:
          fcaption = ''

        if caption:
          clean_fcaption = replace_channel_branding(fcaption, target_ch) if fcaption else ''
          formatted = caption.format(filename=file_name, size=get_size(file_size), caption=clean_fcaption)
          return replace_channel_branding(formatted, target_ch)

        if fcaption:
          return replace_channel_branding(fcaption, target_ch)

        if file_name:
          return f"<b>{file_name}</b>\n\n<b>Channel:</b> {target_ch}"
        return f"<b>Channel:</b> {target_ch}"
  elif msg.text:
    text = msg.text.html if hasattr(msg.text, 'html') else msg.text
    return replace_channel_branding(text, target_ch)
  return None


def get_size(size):
  units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
  size = float(size)
  i = 0
  while size >= 1024.0 and i < len(units):
     i += 1
     size /= 1024.0
  return "%.2f %s" % (size, units[i]) 


async def keyword_filter(keywords, file_name):
    if keywords is None:
        return False
    if re.search(keywords, file_name):
        return False
    else:
        return True


async def extension_filter(extensions, file_name):
    if extensions is None:
        return False
    if not re.search(extensions, file_name):
        return False
    else:
        return True


async def size_filter(max_size, min_size, file_size):
    file_size = file_size / 1024 / 1024
    if max_size and min_size == 0:
        return False
    if max_size == 0:
        return file_size < min_size
    if min_size == 0:
        return file_size > max_size
    if not min_size <= file_size <= max_size:
        return True
    else:
        return False


def media(msg):
  if msg.media:
     media = getattr(msg, msg.media.value, None)
     if media:
        return getattr(media, 'file_id', None)
  return None 


def TimeFormatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]


def retry_btn(id):
    return InlineKeyboardMarkup([[InlineKeyboardButton('♻️ RETRY ♻️', f"start_public_{id}")]])


@Client.on_callback_query(filters.regex(r'^terminate_frwd$'))
async def terminate_frwding(bot, m):
    user_id = m.from_user.id 
    temp.lock[user_id] = False
    temp.CANCEL[user_id] = True 
    await m.answer("Forwarding cancelled !", show_alert=True)


@Client.on_callback_query(filters.regex(r'^fwrdstatus'))
async def status_msg(bot, msg):
    _, status, est_time, percentage, frwd_id = msg.data.split("#")
    sts = STS(frwd_id)
    if not sts.verify():
       fetched, forwarded, remaining = 0
    else:
       fetched, limit, forwarded = sts.get('fetched'), sts.get('limit'), sts.get('total_files')
       remaining = limit - fetched 
    est_time = TimeFormatter(milliseconds=est_time)
    start_time = sts.get('start')
    uptime = await get_bot_uptime(start_time)
    total = sts.get('limit') - sts.get('fetched')
    time_to_comple = await complete_time(total)
    est_time = est_time if (est_time != '' or status not in ['completed', 'cancelled']) else '0 s'
    return await msg.answer(PROGRESS.format(percentage, fetched, forwarded, remaining, status, time_to_comple, uptime), show_alert=True)


@Client.on_callback_query(filters.regex(r'^close_btn$'))
async def close(bot, update):
    await update.answer()
    await update.message.delete()


@Client.on_message(filters.private & filters.command(['stop']))
async def stop_forward(client, message):
    user_id = message.from_user.id
    sts = await message.reply('<code>Stoping...</code>')
    await asyncio.sleep(0.5)
    if not await db.is_forwad_exit(message.from_user.id):
        return await sts.edit('**No Ongoing Forwards To Cancel**')
    temp.lock[user_id] = False
    temp.CANCEL[user_id] = True
    mst = await db.get_forward_details(user_id)
    msg = await client.get_messages(user_id, mst['msg_id'])
    link = f"tg://openmessage?user_id={6648261085}&message_id={mst['msg_id']}"
    await sts.edit(f"<b>Successfully Canceled </b>", disable_web_page_preview=True)


async def restart_pending_forwads(bot, user):
    user = user['user_id']
    settings = await db.get_forward_details(user)
    try:
       skiping = settings['offset']
       fetch = settings['fetched'] - settings['skip']
       temp.forwardings += 1
       forward_id = await store_vars(user)
       sts = STS(forward_id)
       if settings['chat_id'] is None:
           return await db.rmve_frwd(user)
           temp.forwardings -= 1
       if not sts.verify():
          temp.forwardings -=1
          return 
       sts.add('fetched', value=fetch)
       sts.add('duplicate', value=settings['duplicate'])
       sts.add('filtered', value=settings['filtered'])
       sts.add('deleted', value=settings['deleted'])
       sts.add('total_files', value=settings['total'])
       m = await bot.get_messages(user, settings['msg_id'])#
       _bot, caption, forward_tag, datas, protect, button = await sts.get_data(user)
       i = sts.get(full=True)
       filter = datas['filters']
       max_size = datas['max_size']
       min_size = datas['min_size']
       keyword = datas['keywords']
       exten = datas['extensions']
       keywords = ""
       extensions = ""
       if keyword:
           for key in keyword:
               keywords += f"{key}|"
           keywords  = keywords.rstrip("|")
       else:
           keywords = None
       if exten:
           for ext in exten:
               extensions += f"{ext}|"
           extensions = extensions.rstrip("|")
       else:
           extensions = None
       if not _bot:
          return await msg_edit(m, "<code>You didn't added any bot. Please add a bot using /settings !</code>", wait=True)
       if _bot['is_bot'] == True:
          data = _bot['token']
       else:
          data = _bot['session']
       try:
          il = True if _bot['is_bot'] == True else False
          client = await get_client(data, is_bot=il)
          await client.start()
       except Exception as e:  
          return await m.edit(e)
       try:
          await msg_edit(m, "<code>processing..</code>")
       except:
          return await db.rmve_frwd(user)
       try: 
          await client.get_messages(sts.get("FROM"), sts.get("limit"))
       except:
          await msg_edit(m, f"**Source chat may be a private channel / group. Use userbot (user must be member over there) or  if Make Your [Bot](t.me/{_bot['username']}) an admin over there**", retry_btn(firwd_id), True)
          return await stop(client, user)
       try:
          k = await client.send_message(i.TO, "Testing")
          await k.delete()
       except:
          await msg_edit(m, f"**Please Make Your [UserBot / Bot](t.me/{_bot['username']}) Admin In Target Channel With Full Permissions**", retry_btn(forward_id), True)
          return await stop(client, user)
    except:
       return await db.rmve_frwd(user)
    user_have_db = False
    dburi = datas['db_uri']
    if dburi is not None:
        connected, user_db = await connect_user_db(user, dburi, i.TO)
        if not connected:
            await msg_edit(m, "<code>Cannot Connected Your db Errors Found Dup files Have Been Skipped after Restart</code>")
        else:
            user_have_db = True
    try:
        start = settings['start_time']
    except KeyError:
        start = None
    sts.add(time=True, start_time=start)
    sleep = 0.5 if _bot['is_bot'] else getattr(Config, "FORWARD_SLEEP", 1.8)
    #await msg_edit(m, "<code>processing...</code>") 
    temp.IS_FRWD_CHAT.append(i.TO)
    temp.lock[user] = locked = True
    dup_files = []
    if user_have_db and datas['skip_duplicate']:
        old_files = await user_db.get_all_files()
        async for ofile in old_files:
            dup_files.append(ofile["file_id"])
    if locked:
        try:
          MSG = []
          pling=0
          await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
          async for message in iter_messages(client, chat_id=sts.get("FROM"), limit=sts.get("limit"), offset=skiping, filters=filter, max_size=max_size):
                if await is_cancelled(client, user, m, sts):
                    if user_have_db:
                       await user_db.drop_all()
                       await user_db.close()
                       return
                    return
                if pling %20 == 0: 
                   await edit(user, m, 'ᴘʀᴏɢʀᴇssɪɴɢ', 5, sts)
                pling += 1
                sts.add('fetched')
                if message == "DUPLICATE":
                   sts.add('duplicate')
                   continue
                elif message == "FILTERED":
                   sts.add('filtered')
                   continue 
                elif message.empty or message.service:
                   sts.add('deleted')
                   continue
                elif message.document and await extension_filter(extensions, message.document.file_name):
                   sts.add('filtered')
                   continue 
                elif message.document and await keyword_filter(keywords, message.document.file_name):
                   sts.add('filtered')
                   continue 
                elif message.document and await size_filter(max_size, min_size, message.document.file_size):
                   sts.add('filtered')
                   continue 
                elif message.document and message.document.file_id in dup_files:
                   sts.add('duplicate')
                   continue
                if message.document and datas['skip_duplicate']:
                    dup_files.append(message.document.file_id)
                    if user_have_db:
                        await user_db.add_file(message.document.file_id)
                if forward_tag:
                   MSG.append(message.id)
                   notcompleted = len(MSG)
                   completed = sts.get('total') - sts.get('fetched')
                   if ( notcompleted >= 100 
                        or completed <= 100): 
                      await forward(user, client, MSG, m, sts, protect)
                      sts.add('total_files', notcompleted)
                      await asyncio.sleep(10)
                      MSG = []
                else:
                   new_caption = custom_caption(message, caption)
                   details = {"msg_id": message.id, "media": media(message), "caption": new_caption, 'button': button, "protect": protect}
                   await copy(user, client, details, m, sts)
                   sts.add('total_files')
                   actual_sleep = sleep if _bot['is_bot'] else random.uniform(max(1.0, sleep * 0.9), sleep * 1.15)
                   await asyncio.sleep(actual_sleep) 
        except Exception as e:
            await msg_edit(m, f'<b>ERROR:</b>\n<code>{e}</code>', wait=True)
            if user_have_db:
                await user_db.drop_all()
                await user_db.close()
            temp.IS_FRWD_CHAT.remove(sts.TO)
            return await stop(client, user)
        temp.IS_FRWD_CHAT.remove(sts.TO)
        await send(client, user, "<b>🎉 ғᴏʀᴡᴀᴅɪɴɢ ᴄᴏᴍᴘʟᴇᴛᴇᴅ</b>")
        if user_have_db:
            await user_db.drop_all()
            await user_db.close()
        await edit(user, m, 'ᴄᴏᴍᴘʟᴇᴛᴇᴅ', "completed", sts) 
        await stop(client, user)


async def store_vars(user_id):
    settings = await db.get_forward_details(user_id)
    fetch = settings['fetched']
    forward_id = f'{user_id}-{fetch}'
    print(fetch)
    STS(id=forward_id).store(settings['chat_id'], settings['toid'], settings['skip'], settings['limit'])
    return forward_id


async def restart_forwards(client):
    try:
        users = await db.get_all_frwd()
        count = await db.forwad_count()
        tasks = []
        async for user in users:
            tasks.append(restart_pending_forwads(client, user))
        if tasks:
            await asyncio.gather(*tasks)
    except Exception as e:
        logger.warning(f"⚠️ Could not restart pending forwards: {e}")


async def update_forward(user_id, chat_id, start_time, toid, last_id, limit, forward_id, msg_id, fetched, total, duplicate, deleted, skip, filterd):
    details = {
        'chat_id': chat_id,
        'toid': toid,
        'forward_id': forward_id,
        'last_id': last_id,
        'limit': limit,
        'msg_id': msg_id,
        'start_time': start_time,
        'fetched': fetched,
        'offset': fetched,
        'deleted': deleted,
        'total': total,
        'duplicate': duplicate,
        'skip': skip,
        'filtered':filterd
    }
    await db.update_forward(user_id, details)


async def get_bot_uptime(start_time):
    # Calculate the uptime in seconds
    uptime_seconds = int(time.time() - start_time)
    uptime_minutes = uptime_seconds // 60
    uptime_hours = uptime_minutes // 60
    uptime_days = uptime_hours // 24
    uptime_weeks = uptime_days // 7
    uptime_string = ""
    if uptime_weeks != 0:
        uptime_string += f"{uptime_weeks % 7}w, "
    if uptime_days != 0:
        uptime_string += f"{uptime_days % 24}d, "
    if uptime_hours != 0:
        uptime_string += f"{uptime_hours % 24}h, "
    if uptime_minutes != 0:
        uptime_string += f"{uptime_minutes % 60}m, "
    uptime_string += f"{uptime_seconds % 60}s"
    return uptime_string  


async def complete_time(total_files, files_per_minute=30):
    minutes_required = total_files / files_per_minute
    seconds_required = minutes_required * 60
    weeks = seconds_required // (7 * 24 * 60 * 60)
    days = (seconds_required % (7 * 24 * 60 * 60)) // (24 * 60 * 60)
    hours = (seconds_required % (24 * 60 * 60)) // (60 * 60)
    minutes = (seconds_required % (60 * 60)) // 60
    seconds = seconds_required % 60
    time_format = ""
    if weeks > 0:
        time_format += f"{int(weeks)}w, "
    if days > 0:
        time_format += f"{int(days)}d, "
    if hours > 0:
        time_format += f"{int(hours)}h, "
    if minutes > 0:
        time_format += f"{int(minutes)}m, "
    if seconds > 0:
        time_format += f"{int(seconds)}s"
    return time_format

