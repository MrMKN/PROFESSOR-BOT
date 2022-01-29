#Kanged From @TroJanZheX
import asyncio
import re
import ast

from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, make_inactive
from info import ADMINS, AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, P_TTI_SHOW_OFF, IMDB, SINGLE_BUTTON, SPELL_CHECK_REPLY, IMDB_TEMPLATE
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import get_size, is_subscribed, get_poster, search_gagala, temp
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results
from database.filters_mdb import(
   del_all,
   find_filter,
   get_filters,
)
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

from image.edit_1 import (  # pylint:disable=import-error
    bright,
    mix,
    black_white,
    g_blur,
    normal_blur,
    box_blur,
)
from image.edit_2 import (  # pylint:disable=import-error
    circle_with_bg,
    circle_without_bg,
    sticker,
    edge_curved,
    contrast,
    sepia_mode,
    pencil,
    cartoon,
)
from image.edit_3 import (  # pylint:disable=import-error
    green_border,
    blue_border,
    black_border,
    red_border,
)
from image.edit_4 import (  # pylint:disable=import-error
    rotate_90,
    rotate_180,
    rotate_270,
    inverted,
    round_sticker,
    removebg_white,
    removebg_plain,
    removebg_sticker,
)
from image.edit_5 import (  # pylint:disable=import-error
    normalglitch_1,
    normalglitch_2,
    normalglitch_3,
    normalglitch_4,
    normalglitch_5,
    scanlineglitch_1,
    scanlineglitch_2,
    scanlineglitch_3,
    scanlineglitch_4,
    scanlineglitch_5,
)

BUTTONS = {}
SPELL_CHECK = {}

@Client.on_message(filters.group & filters.text & ~filters.edited & filters.incoming)
async def give_filter(client,message):
    group_id = message.chat.id
    name = message.text

    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            await message.reply_text(reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await message.reply_text(
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button)
                            )
                    elif btn == "[]":
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or ""
                        )
                    else:
                        button = eval(btn) 
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button)
                        )
                except Exception as e:
                    logger.exception(e)
                break 

    else:
        await auto_filter(client, message)   

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):

    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("oKda", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    if not search:
        await query.answer("You are using one of my old messages, please send the request again.",show_alert=True)
        return

    files, n_offset, total = await get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    if SINGLE_BUTTON:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}", callback_data=f'files#{file.file_id}'
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'files_#{file.file_id}',
                ),
            ]
            for file in files
        ]

    if 0 < offset <= 10:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"📃 Pages {round(int(offset)/10)+1} / {round(total/10)}", callback_data="pages")]
        )
    elif off_set is None:
        btn.append([InlineKeyboardButton(f"🗓 {round(int(offset)/10)+1} / {round(total/10)}", callback_data="pages"), InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"🗓 {round(int(offset)/10)+1} / {round(total/10)}", callback_data="pages"),
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

@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("okDa", show_alert=True)
    if movie_  == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.message_id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
    if files:
        k = (movie, files, offset, total_results)
        await auto_filter(bot, query, k)
    else:
        k = await query.message.edit('This Movie Not Found In DataBase')
        await asyncio.sleep(10)
        await k.delete()


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            grpid  = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == "creator") or (str(userid) in ADMINS):    
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!",show_alert=True)

    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == "creator") or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Thats not for you!!",show_alert=True)


    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]
        
        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
                InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode="md"
        )
        return

    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text('Some error occured!!', parse_mode="md")
        return

    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
        return
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
        return
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert,show_alert=True)

    if query.data.startswith("file"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size=get_size(files.file_size)
        f_caption=files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption=f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"
            
        try:
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={file_id}")
                return
            elif P_TTI_SHOW_OFF:
                await query.answer(url=f"https://t.me/{temp.U_NAME}?start={file_id}")
                return
            else:
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption
                    )
                await query.answer('Check PM, I have sent files in pm',show_alert = True)
        except UserIsBlocked:
            await query.answer('Unblock the bot mahn !',show_alert = True)
        except PeerIdInvalid:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={file_id}")
        except Exception as e:
            await query.answer(url=f"https://t.me/{temp.U_NAME}?start={file_id}")

    elif query.data.startswith("checksub"):
        if AUTH_CHANNEL and not await is_subscribed(client, query):
            await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
            return
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('No such file exist.')
        files = files_[0]
        title = files.file_name
        size=get_size(files.file_size)
        f_caption=files.caption
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
            except Exception as e:
                logger.exception(e)
                f_caption=f_caption
        if f_caption is None:
            f_caption = f"{title}"
        await query.answer()
        await client.send_cached_media(
            chat_id=query.from_user.id,
            file_id=file_id,
            caption=f_caption
            )

    elif query.data == "removebg":
        await query.message.edit_text(
            "**Select required mode**ㅤㅤㅤㅤ",
            reply_markup=InlineKeyboardMarkup(
                [[
                InlineKeyboardButton(text="𝖶𝗂𝗍𝗁 𝖶𝗁𝗂𝗍𝖾 𝖡𝖦", callback_data="rmbgwhite"),
                InlineKeyboardButton(text="𝖶𝗂𝗍𝗁𝗈𝗎𝗍 𝖡𝖦", callback_data="rmbgplain"),
                ],[
                InlineKeyboardButton(text="𝖲𝗍𝗂𝖼𝗄𝖾𝗋", callback_data="rmbgsticker"),
                ],[
                InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='photo')
             ]]
        ),)
    elif query.data == "stick":
        await query.message.edit(
            "**Select a Type**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝖭𝗈𝗋𝗆𝖺𝗅", callback_data="stkr"),
                        InlineKeyboardButton(
                            text="𝖤𝖽𝗀𝖾 𝖢𝗎𝗋𝗏𝖾𝖽", callback_data="cur_ved"
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="𝖢𝗂𝗋𝖼𝗅𝖾", callback_data="circle_sticker"
                        )
                    ],
                    [
                        InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='photo')
                    ],
                ]
            ),
        )
    elif query.data == "rotate":
        await query.message.edit_text(
            "**Select the Degree**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="180", callback_data="180"),
                        InlineKeyboardButton(text="90", callback_data="90"),
                    ],
                    [InlineKeyboardButton(text="270", callback_data="270")],
                    ],
                    [
                        InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='photo')
                ]
            ),
        )
    elif query.data == "glitch":
        await query.message.edit_text(
            "**Select required mode**ㅤㅤㅤㅤ",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="𝖭𝗈𝗋𝗆𝖺𝗅", callback_data="normalglitch"
                        ),
                        InlineKeyboardButton(
                            text="𝖲𝖼𝖺𝗇 𝖫𝖺𝗂𝗇𝗌", callback_data="scanlineglitch"
                        ),
                    ],
                    [
                        InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='photo')
                    ]
                ]
            ),
        )
    elif query.data == "normalglitch":
        await query.message.edit_text(
            "**Select Glitch power level**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="1", callback_data="normalglitch1"),
                        InlineKeyboardButton(text="2", callback_data="normalglitch2"),
                        InlineKeyboardButton(text="3", callback_data="normalglitch3"),
                    ],
                    [
                        InlineKeyboardButton(text="4", callback_data="normalglitch4"),
                        InlineKeyboardButton(text="5", callback_data="normalglitch5"),
                    ],
                    [
                        InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='glitch')
                    ],
                ]
            ),
        )
    elif query.data == "scanlineglitch":
        await query.message.edit_text(
            "**Select Glitch power level**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="1", callback_data="scanlineglitch1"),
                        InlineKeyboardButton(text="2", callback_data="scanlineglitch2"),
                        InlineKeyboardButton(text="3", callback_data="scanlineglitch3"),
                    ],
                    [
                        InlineKeyboardButton(text="4", callback_data="scanlineglitch4"),
                        InlineKeyboardButton(text="5", callback_data="scanlineglitch5"),
                    ],
                    [
                        InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='glitch')
                    ],
                ]
            ),
        )
    elif query.data == "blur":
        await query.message.edit(
            "**Select a Type**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝖡𝗈𝗑", callback_data="box"),
                        InlineKeyboardButton(text="𝖭𝗈𝗋𝗆𝖺𝗅", callback_data="normal"),
                    ],
                    [InlineKeyboardButton(text="𝖦𝖺𝗎𝗌𝗌𝗂𝖺𝗇", callback_data="gas")],
                    ],
                    [
                        InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='photo')
                ]
            ),
        )
    elif query.data == "circle":
        await query.message.edit_text(
            "**Select required mode**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝖶𝗂𝗍𝗁 𝖡𝖦", callback_data="circlewithbg"),
                        InlineKeyboardButton(text="𝖶𝗂𝗍𝗁𝗈𝗎𝗍 𝖡𝖦", callback_data="circlewithoutbg"),
                    ],
                    [
                        InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='photo')
                    ]
                ]
            ),
        )
    elif query.data == "border":
        await query.message.edit(
            "**Select Border**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="𝖱𝖾𝖽", callback_data="red"),
                        InlineKeyboardButton(text="𝖦𝗋𝖾𝖾𝗇", callback_data="green"),
                    ],
                    [
                        InlineKeyboardButton(text="𝖡𝗅𝖺𝖼𝗄", callback_data="black"),
                        InlineKeyboardButton(text="𝖡𝗅𝗎𝖾", callback_data="blue"),
                    ],
                    [
                        InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='photo')   
                    ],
                ]
            ),
        )
    elif query.data == "bright":
        await bright(client, query.message)
    elif query.data == "mix":
        await mix(client, query.message)
    elif query.data == "b|w":
        await black_white(client, query.message)
    elif query.data == "circlewithbg":
        await circle_with_bg(client, query.message)
    elif query.data == "circlewithoutbg":
        await circle_without_bg(client, query.message)
    elif query.data == "green":
        await green_border(client, query.message)
    elif query.data == "blue":
        await blue_border(client, query.message)
    elif query.data == "red":
        await red_border(client, query.message)
    elif query.data == "black":
        await black_border(client, query.message)
    elif query.data == "circle_sticker":
        await round_sticker(client, query.message)
    elif query.data == "inverted":
        await inverted(client, query.message)
    elif query.data == "stkr":
        await sticker(client, query.message)
    elif query.data == "cur_ved":
        await edge_curved(client, query.message)
    elif query.data == "90":
        await rotate_90(client, query.message)
    elif query.data == "180":
        await rotate_180(client, query.message)
    elif query.data == "270":
        await rotate_270(client, query.message)
    elif query.data == "contrast":
        await contrast(client, query.message)
    elif query.data == "box":
        await box_blur(client, query.message)
    elif query.data == "gas":
        await g_blur(client, query.message)
    elif query.data == "normal":
        await normal_blur(client, query.message)
    elif query.data == "sepia":
        await sepia_mode(client, query.message)
    elif query.data == "pencil":
        await pencil(client, query.message)
    elif query.data == "cartoon":
        await cartoon(client, query.message)
    elif query.data == "normalglitch1":
        await normalglitch_1(client, query.message)
    elif query.data == "normalglitch2":
        await normalglitch_2(client, query.message)
    elif query.data == "normalglitch3":
        await normalglitch_3(client, query.message)
    elif query.data == "normalglitch4":
        await normalglitch_4(client, query.message)
    elif query.data == "normalglitch5":
        await normalglitch_5(client, query.message)
    elif query.data == "scanlineglitch1":
        await scanlineglitch_1(client, query.message)
    elif query.data == "scanlineglitch2":
        await scanlineglitch_2(client, query.message)
    elif query.data == "scanlineglitch3":
        await scanlineglitch_3(client, query.message)
    elif query.data == "scanlineglitch4":
        await scanlineglitch_4(client, query.message)
    elif query.data == "scanlineglitch5":
        await scanlineglitch_5(client, query.message)
    elif query.data == "rmbgwhite":
        await removebg_white(client, query.message)
    elif query.data == "rmbgplain":
        await removebg_plain(client, query.message)
    elif query.data == "rmbgsticker":
        await removebg_sticker(client, query.message)
    elif query.data == "pages":
        await query.answer()
    elif query.data == "start":
        buttons = [[
            InlineKeyboardButton('➕ Add Me To Your Groups ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')
            ],[
            InlineKeyboardButton('🔍 Search', switch_inline_query_current_chat=''),
            InlineKeyboardButton('🤖 Updates', url='https://t.me/Latest_Movie_Mediaa')
            ],[
            InlineKeyboardButton('ℹ️ Help', callback_data='help'),
            InlineKeyboardButton('😊 About', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "photo":
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
            InlineKeyboardButton(text="𝖱𝖾𝗆𝗈𝗏𝖾 𝖡𝖦", callback_data="removebg")
            ],[
            InlineKeyboardButton(text="𝖢𝗅𝗈𝗌𝖾", callback_data="close_data")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="Select your required mode from below!",
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('Mᴀɴɴᴜᴀʟ Fɪʟᴛᴇʀ', callback_data='manuelfilter'),
            InlineKeyboardButton('Aᴜᴛᴏ Fɪʟᴛᴇʀ', callback_data='autofilter'),
            InlineKeyboardButton('Cᴏɴɴᴇᴄᴛɪᴏɴ', callback_data='coct')
            ],[
            InlineKeyboardButton('Sᴏɴɢ  🎶', callback_data='songs'),
            InlineKeyboardButton('Exᴛʀᴀ Mᴏᴅs', callback_data='extra'),
            InlineKeyboardButton("Vɪᴅᴇᴏ 📲", callback_data='video')
            ],[
            InlineKeyboardButton('📌 Pɪɴ', callback_data='pin'), 
            InlineKeyboardButton('🖥 Pᴀsᴛᴇ', callback_data='pastes'),
            InlineKeyboardButton("Iᴍᴀɢᴇ 💻", callback_data='image')
            ],[
            InlineKeyboardButton('🤡Fᴜɴ', callback_data='fun'), 
            InlineKeyboardButton('🧾 Jsᴏɴ', callback_data='son'),
            InlineKeyboardButton('🎤 Tᴛs', callback_data='ttss')
            ],[
            InlineKeyboardButton('💣 Pᴜʀɢᴇ', callback_data='purges'),
            InlineKeyboardButton('✴️ Pɪɴɢ', callback_data='pings'),
            InlineKeyboardButton('📸 Tᴇʟᴇɢʀᴀᴘʜ', callback_data='tele')
            ],[
            InlineKeyboardButton('🤔 Wʜᴏɪs', callback_data='whois'),
            InlineKeyboardButton('Mᴜᴛᴇ 🚫', callback_data='restric'),
            InlineKeyboardButton('Iɴ-Kɪᴄᴋ ⚠️', callback_data='zombies')
            ],[
            InlineKeyboardButton("Rᴇᴘᴏʀᴛ 📣", callback_data='report'),
            InlineKeyboardButton("Yᴛ- Tʜᴜᴍʙ🖥️ ", callback_data='ytthumb'),
            InlineKeyboardButton("Sᴛɪᴄᴋᴇʀ-Iᴅ 🔍", callback_data='sticker')
            ],[
            InlineKeyboardButton("Cᴏᴠɪᴅ 💉", callback_data='corona'),
            InlineKeyboardButton("Aᴜᴅɪᴏ Bᴏᴏᴋ 📑", callback_data='abook'),
            InlineKeyboardButton("Sʜᴏʀᴛ-Uʀʟ 🔖", callback_data='urlshort')
            ],[
            InlineKeyboardButton('🏠 Hᴏᴍᴇ', callback_data='start'),
            InlineKeyboardButton('𝖦𝗍𝗋𝖺𝗇𝗌', callback_data='gtrans'),
            InlineKeyboardButton('🔮 Sᴛᴀᴛᴜs', callback_data='stats')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "about":
        buttons= [[
            InlineKeyboardButton('🤖 Updates', url='https://t.me/Latest_Movie_Mediaa'),
            InlineKeyboardButton('♥️ Source', url='https://t.me/Latest_Movie_Media')
            ],[
            InlineKeyboardButton('🏠 Home', callback_data='start'),
            InlineKeyboardButton('🔐 Close', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "restric":
        buttons = [[
            InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.RESTRIC_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "image":
        buttons= [[
            InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.IMAGE_TXT.format(temp.B_NAME),
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "whois":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.WHOIS_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "corona":
        buttons = [[
            InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CORONA_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "urlshort":
        buttons = [[
            InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.URLSHORT_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "zombies":
        buttons = [[
            InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ZOMBIES_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "fun":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FUN_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "video":
        buttons = [[
            InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='song')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.VIDEO_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "pin":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.PIN_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "son":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.JSON_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "pastes":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.PASTE_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "pings":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.PINGS_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "ttss":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.GTRANS_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "purges":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.PURGE_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "tele":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.TELE_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )         
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "manuelfilter":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('⏹️ Buttons', callback_data='button')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "button":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='manuelfilter')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "coct":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('👮‍♂️ Admin', callback_data='admin')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "gtrans":
        buttons = [[
            InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='help'),
            InlineKeyboardButton('𝖫𝖺𝗇𝗀 𝖢𝗈𝖽𝖾𝗌', url='https://cloud.google.com/translate/docs/languages')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.GTRANS_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "report":
        buttons = [[
            InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.REPORT_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "sticker":
        buttons = [[
            InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.STICKER_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "ytthumb":
        buttons = [[
            InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.YTTHUMB_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "admin":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='extra')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ADMIN_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "abook":
        buttons = [[
            InlineKeyboardButton('🔙 𝖡𝖺𝖼𝗄', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOOK_TXT,
            disable_web_page_preview=True,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "songs":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SONG_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "stats":
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('♻️', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('♻️', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=script.STATUS_TXT.format(total, users, chats, monsize, free),
            reply_markup=reply_markup,
            parse_mode='html'
      )
    

async def auto_filter(client, msg, spoll=False):
    if not spoll:
        message = msg
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if 2 < len(message.text) < 100:
            search = message.text
            files, offset, total_results = await get_search_results(search.lower(), offset=0, filter=True)
            if not files:
                if SPELL_CHECK_REPLY:
                    return await advantage_spell_chok(msg)
                else:
                    return
        else:
            return
    else:
        message = msg.message.reply_to_message # msg will be callback query
        search, files, offset, total_results = spoll
    if SINGLE_BUTTON:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                ),
            ]
            for file in files
        ]
    else:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_name}",
                    callback_data=f'files#{file.file_id}',
                ),
                InlineKeyboardButton(
                    text=f"{get_size(file.file_size)}",
                    callback_data=f'files_#{file.file_id}',
                ),
            ]
            for file in files
        ]

    if offset != "":
        key = f"{message.chat.id}-{message.message_id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton(text=f"🗓 1/{round(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_{req}_{key}_{offset}")]
        )
    else:
        btn.append(
            [InlineKeyboardButton(text="🗓 1/1",callback_data="pages")]
        )
    imdb = await get_poster(search, file=(files[0]).file_name) if IMDB else None
    if imdb:
        cap = IMDB_TEMPLATE.format(
            query = search,
            title = imdb['title'],
            votes = imdb['votes'],
            aka = imdb["aka"],
            seasons = imdb["seasons"],
            box_office = imdb['box_office'],
            localized_title = imdb['localized_title'],
            kind = imdb['kind'],
            imdb_id = imdb["imdb_id"],
            cast = imdb["cast"],
            runtime = imdb["runtime"],
            countries = imdb["countries"],
            certificates = imdb["certificates"],
            languages = imdb["languages"],
            director = imdb["director"],
            writer = imdb["writer"],
            producer = imdb["producer"],
            composer = imdb["composer"],
            cinematographer = imdb["cinematographer"],
            music_team = imdb["music_team"],
            distributors = imdb["distributors"],
            release_date = imdb['release_date'],
            year = imdb['year'],
            genres = imdb['genres'],
            poster = imdb['poster'],
            plot = imdb['plot'],
            rating = imdb['rating'],
            url = imdb['url']
        )
    else:
        cap = f"Here is what i found for your query {search}"
    if imdb and imdb.get('poster'):
        try:
            await message.reply_photo(photo=imdb.get('poster'), caption=cap, reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            await message.reply_photo(photo=poster, caption=cap, reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(btn))
    if spoll:
        await msg.message.delete()
        

async def advantage_spell_chok(msg):
    query = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)", "", msg.text, flags=re.IGNORECASE) # plis contribute some common words 
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(msg.text)
    gs_parsed = []
    if not g_s:
        k = await msg.reply("I couldn't find any movie in that name.")
        await asyncio.sleep(8)
        await k.delete()
        return
    regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE) # look for imdb / wiki results
    gs = list(filter(regex.match, g_s))
    gs_parsed = [re.sub(r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)', '', i, flags=re.IGNORECASE) for i in gs]
    if not gs_parsed:
        reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*", re.IGNORECASE) # match something like Watch Niram | Amazon Prime 
        for mv in g_s:
            match  = reg.match(mv)
            if match:
                gs_parsed.append(match.group(1))
    user = msg.from_user.id if msg.from_user else 0
    movielist = []
    gs_parsed = list(dict.fromkeys(gs_parsed)) # removing duplicates https://stackoverflow.com/a/7961425
    if len(gs_parsed) > 3:
        gs_parsed = gs_parsed[:3]
    if gs_parsed:
        for mov in gs_parsed:
            imdb_s = await get_poster(mov.strip(), bulk=True) # searching each keyword in imdb
            if imdb_s:
                movielist += [movie.get('title') for movie in imdb_s]
    movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
    movielist = list(dict.fromkeys(movielist)) # removing duplicates
    if not movielist:
        k = await msg.reply("I couldn't find anything related to that. Check your spelling")
        await asyncio.sleep(8)
        await k.delete()
        return
    SPELL_CHECK[msg.message_id] = movielist
    btn = [[
                InlineKeyboardButton(
                    text=movie.strip(),
                    callback_data=f"spolling#{user}#{k}",
                )
            ] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'spolling#{user}#close_spellcheck')])
    await msg.reply("I couldn't find anything related to that\nDid you mean any one of these?", reply_markup=InlineKeyboardMarkup(btn))
    


