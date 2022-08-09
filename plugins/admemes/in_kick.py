from info import ADMINS
from Script import script
from time import time, sleep
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid


@Client.on_message(filters.incoming & ~filters.private & filters.command('inkick'))
def inkick(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status == ("creator"):
    if len(message.command) > 1:
      input_str = message.command
      sent_message = message.reply_text(script.START_KICK)
      sleep(20)
      sent_message.delete()
      message.delete()
      count = 0
      for member in client.iter_chat_members(message.chat.id):
        if member.user.status in input_str and not member.status in ('administrator', 'creator'):
          try:
            client.kick_chat_member(message.chat.id, member.user.id, int(time() + 45))
            count += 1
            sleep(1)
          except (ChatAdminRequired, UserAdminInvalid):
            sent_message.edit(script.ADMIN_REQUIRED)
            client.leave_chat(message.chat.id)
            break
          except FloodWait as e:
            sleep(e.x)
      try:
        sent_message.edit(script.KICKED.format(count))
      except ChatWriteForbidden:
        pass
    else:
      message.reply_text(script.INPUT_REQUIRED)
  else:
    sent_message = message.reply_text(script.CREATOR_REQUIRED)
    sleep(5)
    sent_message.delete()
    message.delete()

@Client.on_message(filters.incoming & ~filters.private & filters.command('dkick'))
def dkick(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status == ("creator"):
    sent_message = message.reply_text(script.START_KICK)
    sleep(20)
    sent_message.delete()
    message.delete()
    count = 0
    for member in client.iter_chat_members(message.chat.id):
      if member.user.is_deleted and not member.status in ('administrator', 'creator'):
        try:
          client.kick_chat_member(message.chat.id, member.user.id, int(time() + 45))
          count += 1
          sleep(1)
        except (ChatAdminRequired, UserAdminInvalid):
          sent_message.edit(script.ADMIN_REQUIRED)
          client.leave_chat(message.chat.id)
          break
        except FloodWait as e:
          sleep(e.x)
    try:
      sent_message.edit(script.DKICK.format(count))
    except ChatWriteForbidden:
      pass
  else:
    sent_message = message.reply_text(script.CREATOR_REQUIRED)
    sleep(5)
    sent_message.delete()
    message.delete()

@Client.on_message(filters.incoming & ~filters.private & filters.command('instatus'))
def instatus(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status in ('administrator', 'creator', 'ADMINS'):
    sent_message = message.reply_text(script.FETCHING_INFO)
    recently = 0
    within_week = 0
    within_month = 0
    long_time_ago = 0
    deleted_acc = 0
    uncached = 0
    bot = 0
    for member in client.iter_chat_members(message.chat.id):
      user = member.user
      if user.is_deleted:
        deleted_acc += 1
      elif user.is_bot:
        bot += 1
      elif user.status == "recently":
        recently += 1
      elif user.status == "within_week":
        within_week += 1
      elif user.status == "within_month":
        within_month += 1
      elif user.status == "long_time_ago":
        long_time_ago += 1
      else:
        uncached += 1
    sent_message.edit(script.STATUS.format(message.chat.title, recently, within_week, within_month, long_time_ago, deleted_acc, bot, uncached))
