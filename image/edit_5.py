from pyrogram.enums import ChatAction
import asyncio
import shutil
import os


async def normalglitch_1(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "normalglitch_1.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            cd = ["glitch_this", "-c", "-o", edit_img_loc, download_location, "1"]
            process = await asyncio.create_subprocess_exec(
                *cd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await message.reply_to_message.reply_photo(edit_img_loc, quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        print("normalglitch_1-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def normalglitch_2(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "normalglitch_2.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            cd = ["glitch_this", "-c", "-o", edit_img_loc, download_location, "2"]
            process = await asyncio.create_subprocess_exec(
                *cd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await message.reply_to_message.reply_photo(edit_img_loc, quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        print("normalglitch_2-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def normalglitch_3(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "normalglitch_3.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            cd = ["glitch_this", "-c", "-o", edit_img_loc, download_location, "3"]
            process = await asyncio.create_subprocess_exec(
                *cd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await message.reply_to_message.reply_photo(edit_img_loc, quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        print("normalglitch_3-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def normalglitch_4(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "normalglitch_4.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            cd = ["glitch_this", "-c", "-o", edit_img_loc, download_location, "4"]
            process = await asyncio.create_subprocess_exec(
                *cd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await message.reply_to_message.reply_photo(edit_img_loc, quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        print("normalglitch_4-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def normalglitch_5(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "normalglitch_5.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            cd = ["glitch_this", "-c", "-o", edit_img_loc, download_location, "5"]
            process = await asyncio.create_subprocess_exec(
                *cd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await message.reply_to_message.reply_photo(edit_img_loc, quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        print("normalglitch_5-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def scanlineglitch_1(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "scanlineglitch_1.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            cd = ["glitch_this", "-c", "-s", "-o", edit_img_loc, download_location, "1"]
            process = await asyncio.create_subprocess_exec(
                *cd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await message.reply_to_message.reply_photo(edit_img_loc, quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        print("scanlineglitch_1-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def scanlineglitch_2(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "scanlineglitch_2.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            cd = ["glitch_this", "-c", "-s", "-o", edit_img_loc, download_location, "2"]
            process = await asyncio.create_subprocess_exec(
                *cd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await message.reply_to_message.reply_photo(edit_img_loc, quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        print("scanlineglitch_2-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def scanlineglitch_3(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "scanlineglitch_3.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            cd = ["glitch_this", "-c", "-s", "-o", edit_img_loc, download_location, "3"]
            process = await asyncio.create_subprocess_exec(
                *cd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await message.reply_to_message.reply_photo(edit_img_loc, quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        print("scanlineglitch_3-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def scanlineglitch_4(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "scanlineglitch_4.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            cd = ["glitch_this", "-c", "-s", "-o", edit_img_loc, download_location, "4"]
            process = await asyncio.create_subprocess_exec(
                *cd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await message.reply_to_message.reply_photo(edit_img_loc, quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        print("scanlineglitch_4-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def scanlineglitch_5(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "scanlineglitch_5.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            cd = ["glitch_this", "-c", "-s", "-o", edit_img_loc, download_location, "5"]
            process = await asyncio.create_subprocess_exec(
                *cd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            await process.communicate()
            await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await message.reply_to_message.reply_photo(edit_img_loc, quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        print("scanlineglitch_5-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return
