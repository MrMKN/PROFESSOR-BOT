import asyncio, re, ast, math, logging
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
from utils import get_shortlink 
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, make_inactive
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, PM_IMDB, SINGLE_BUTTON, PROTECT_CONTENT, \
    SPELL_CHECK_REPLY, IMDB_TEMPLATE, IMDB_DELET_TIME, START_MESSAGE, PMFILTER, G_FILTER, BUTTON_LOCK, BUTTON_LOCK_TEXT, SHORT_URL, SHORT_API

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums 
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.filters_mdb import del_all, find_filter, get_filters
from database.gfilters_mdb import find_gfilter, get_gfilters
from plugins.helper.admin_check import admin_fliter
from plugins.group_filter import manual_filters, auto_filter
from plugins.pm_filter import pm_AutoFilter

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("oKda", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = temp.BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await get_settings(query.message.chat.id)
    nxreq  = query.from_user.id if query.from_user else 0
    if SHORT_URL and SHORT_API:          
        if settings["button"]:
            btn = [[InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=await get_shortlink(f"https://telegram.dog/{temp.U_NAME}?start=files_{file.file_id}"))] for file in files ]
        else:
            btn = [[InlineKeyboardButton(text=f"{file.file_name}", url=await get_shortlink(f"https://telegram.dog/{temp.U_NAME}?start=files_{file.file_id}")),
                    InlineKeyboardButton(text=f"{get_size(file.file_size)}", url=await get_shortlink(f"https://telegram.dog/{temp.U_NAME}?start=files_{file.file_id}"))] for file in files ]
    else:        
        if settings["button"]:
            btn = [[InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{nxreq}#{file.file_id}')] for file in files ]
        else:
            btn = [[InlineKeyboardButton(text=f"{file.file_name}", callback_data=f'files#{nxreq}#{file.file_id}'),
                    InlineKeyboardButton(text=f"{get_size(file.file_size)}", callback_data=f'files#{nxreq}#{file.file_id}')] for file in files ]

    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"📃 Pages {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}",
                                  callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
             InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}")
            ],
        )
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()


async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("okDa", show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = temp.SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    k = await manual_filters(bot, query.message, text=movie)
    if k == False:
        files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
        if files:
            k = (movie, files, offset, total_results)
            await auto_filter(bot, query, k)
        else:
            k = await query.message.edit('This Movie Not Found In DataBase')
            await asyncio.sleep(10)
            await k.delete()


 
async def pm_next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    try:
        offset = int(offset)
    except:
        offset = 0
    search = temp.PM_BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.", show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    
    if SHORT_URL and SHORT_API:          
        if SINGLE_BUTTON:
            btn = [[InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", url=await get_shortlink(f"https://telegram.dog/{temp.U_NAME}?start=files_{file.file_id}"))] for file in files ]
        else:
            btn = [[InlineKeyboardButton(text=f"{file.file_name}", url=await get_shortlink(f"https://telegram.dog/{temp.U_NAME}?start=files_{file.file_id}")),
                    InlineKeyboardButton(text=f"{get_size(file.file_size)}", url=await get_shortlink(f"https://telegram.dog/{temp.U_NAME}?start=files_{file.file_id}"))] for file in files ]
    else:        
        if SINGLE_BUTTON:
            btn = [[InlineKeyboardButton(text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'pmfile#{file.file_id}')] for file in files ]
        else:
            btn = [[InlineKeyboardButton(text=f"{file.file_name}", callback_data=f'pmfile#{file.file_id}'),
                    InlineKeyboardButton(text=f"{get_size(file.file_size)}", callback_data=f'pmfile#{file.file_id}')] for file in files ]

    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⏪ BACK", callback_data=f"pmnext_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"📃 Pages {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages")]                                  
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
             InlineKeyboardButton("NEXT ⏩", callback_data=f"pmnext_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("⏪ BACK", callback_data=f"pmnext_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"🗓 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)}", callback_data="pages"),
                InlineKeyboardButton("NEXT ⏩", callback_data=f"pmnext_{req}_{key}_{n_offset}")
            ],
        )
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()


async def pm_spoll_tester(bot, query):
    _, user, movie_ = query.data.split('#')
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movies = temp.PM_SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
    if files:
        k = (movie, files, offset, total_results)
        await pm_AutoFilter(bot, query, k)
    else:
        k = await query.message.edit('This Movie Not Found In DataBase')
        await asyncio.sleep(10)
        await k.delete()

















