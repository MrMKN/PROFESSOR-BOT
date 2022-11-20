from PIL import Image, ImageOps, ImageDraw 
from pyrogram.enums import ChatAction
import numpy as np
import requests
import shutil
import cv2
import io
import os
from info import RemoveBG_API 


async def rotate_90(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "rotate_90.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            a = await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            src = cv2.imread(a)
            image = cv2.rotate(src, cv2.cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite(edit_img_loc, image)
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
        print("rotate_90-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def rotate_180(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "rotate_180.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            a = await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            src = cv2.imread(a)
            image = cv2.rotate(src, cv2.ROTATE_180)
            cv2.imwrite(edit_img_loc, image)
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
        print("rotate_180-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def rotate_270(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "rotate_270.jpg"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            a = await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            src = cv2.imread(a)
            image = cv2.rotate(src, cv2.ROTATE_90_COUNTERCLOCKWISE)
            cv2.imwrite(edit_img_loc, image)
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
        print("rotate_270-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


def resize_photo(photo: str, userid: str) -> io.BytesIO:
    image = Image.open(photo)
    maxsize = 512
    scale = maxsize / max(image.width, image.height)
    new_size = (int(image.width * scale), int(image.height * scale))
    image = image.resize(new_size, Image.LANCZOS)
    resized_photo = io.BytesIO()
    resized_photo.name = "./DOWNLOADS" + "/" + userid + "resized.png"
    image.save(resized_photo, "PNG")
    return resized_photo


async def round_sticker(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "rounded.webp"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            a = await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            resized = resize_photo(a, userid)
            img = Image.open(resized).convert("RGB")
            npImage = np.array(img)
            h, w = img.size
            alpha = Image.new("L", img.size, 0)
            draw = ImageDraw.Draw(alpha)
            draw.pieslice([0, 0, h, w], 0, 360, fill=255)
            npAlpha = np.array(alpha)
            npImage = np.dstack((npImage, npAlpha))
            Image.fromarray(npImage).save(edit_img_loc)
            await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
            await message.reply_to_message.reply_sticker(edit_img_loc, quote=True)
            await msg.delete()
        else:
            await message.reply_text("Why did you delete that??")
        try:
            shutil.rmtree(f"./DOWNLOADS/{userid}")
        except Exception:
            pass
    except Exception as e:
        print("round_sticker-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def inverted(client, message):
    try:
        userid = str(message.chat.id)
        if not os.path.isdir(f"./DOWNLOADS/{userid}"):
            os.makedirs(f"./DOWNLOADS/{userid}")
        download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
        edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "inverted.png"
        if not message.reply_to_message.empty:
            msg = await message.reply_to_message.reply_text(
                "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
            )
            a = await client.download_media(
                message=message.reply_to_message, file_name=download_location
            )
            await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")
            image = Image.open(a)
            inverted_image = ImageOps.invert(image)
            inverted_image.save(edit_img_loc)
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
        print("inverted-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def removebg_plain(client, message):
    try:
        if not (RemoveBG_API == ""):
            userid = str(message.chat.id)
            if not os.path.isdir(f"./DOWNLOADS/{userid}"):
                os.makedirs(f"./DOWNLOADS/{userid}")
            download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
            edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "nobgplain.png"
            if not message.reply_to_message.empty:
                msg = await message.reply_to_message.reply_text(
                    "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
                )
                await client.download_media(
                    message=message.reply_to_message, file_name=download_location
                )
                await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")

                response = requests.post(
                    "https://api.remove.bg/v1.0/removebg",
                    files={"image_file": open(download_location, "rb")},
                    data={"size": "auto"},
                    headers={"X-Api-Key": RemoveBG_API},
                )
                if response.status_code == 200:
                    with open(f"{edit_img_loc}", "wb") as out:
                        out.write(response.content)
                else:
                    await message.reply_to_message.reply_text(
                        "Check if your api is correct", quote=True
                    )
                    return

                await message.reply_chat_action(ChatAction.UPLOAD_DOCUMENT)
                await message.reply_to_message.reply_document(edit_img_loc, quote=True)
                await msg.delete()
            else:
                await message.reply_text("Why did you delete that??")
            try:
                shutil.rmtree(f"./DOWNLOADS/{userid}")
            except Exception:
                pass
        else:
            await message.reply_to_message.reply_text(
                "Get the api from https://www.remove.bg/b/background-removal-api and add in Config Var",
                quote=True,
                disable_web_page_preview=True,
            )
    except Exception as e:
        print("removebg_plain-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def removebg_white(client, message):
    try:
        if not (RemoveBG_API == ""):
            userid = str(message.chat.id)
            if not os.path.isdir(f"./DOWNLOADS/{userid}"):
                os.makedirs(f"./DOWNLOADS/{userid}")
            download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
            edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "nobgwhite.png"
            if not message.reply_to_message.empty:
                msg = await message.reply_to_message.reply_text(
                    "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
                )
                await client.download_media(
                    message=message.reply_to_message, file_name=download_location
                )
                await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")

                response = requests.post(
                    "https://api.remove.bg/v1.0/removebg",
                    files={"image_file": open(download_location, "rb")},
                    data={"size": "auto"},
                    headers={"X-Api-Key": RemoveBG_API},
                )
                if response.status_code == 200:
                    with open(f"{edit_img_loc}", "wb") as out:
                        out.write(response.content)
                else:
                    await message.reply_to_message.reply_text(
                        "Check if your api is correct", quote=True
                    )
                    return

                await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
                await message.reply_to_message.reply_photo(edit_img_loc, quote=True)
                await msg.delete()
            else:
                await message.reply_text("Why did you delete that??")
            try:
                shutil.rmtree(f"./DOWNLOADS/{userid}")
            except Exception:
                pass
        else:
            await message.reply_to_message.reply_text(
                "Get the api from https://www.remove.bg/b/background-removal-api and add in Config Var",
                quote=True,
                disable_web_page_preview=True,
            )
    except Exception as e:
        print("removebg_white-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return


async def removebg_sticker(client, message):
    try:
        if not (RemoveBG_API == ""):
            userid = str(message.chat.id)
            if not os.path.isdir(f"./DOWNLOADS/{userid}"):
                os.makedirs(f"./DOWNLOADS/{userid}")
            download_location = "./DOWNLOADS" + "/" + userid + "/" + userid + ".jpg"
            edit_img_loc = "./DOWNLOADS" + "/" + userid + "/" + "nobgsticker.webp"
            if not message.reply_to_message.empty:
                msg = await message.reply_to_message.reply_text(
                    "<b>𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>", quote=True
                )
                await client.download_media(
                    message=message.reply_to_message, file_name=download_location
                )
                await msg.edit("<b>𝚄𝙿𝙻𝙾𝙰𝙳𝙸𝙽𝙶 𝙸𝙼𝙰𝙶𝙴....</b>")

                response = requests.post(
                    "https://api.remove.bg/v1.0/removebg",
                    files={"image_file": open(download_location, "rb")},
                    data={"size": "auto"},
                    headers={"X-Api-Key": RemoveBG_API},
                )
                if response.status_code == 200:
                    with open(f"{edit_img_loc}", "wb") as out:
                        out.write(response.content)
                else:
                    await message.reply_to_message.reply_text(
                        "Check if your api is correct", quote=True
                    )
                    return

                await message.reply_chat_action(ChatAction.UPLOAD_PHOTO)
                await message.reply_to_message.reply_sticker(edit_img_loc, quote=True)
                await msg.delete()
            else:
                await message.reply_text("Why did you delete that??")
            try:
                shutil.rmtree(f"./DOWNLOADS/{userid}")
            except Exception:
                pass
        else:
            await message.reply_to_message.reply_text(
                "Get the api from https://www.remove.bg/b/background-removal-api and add in Config Var",
                quote=True,
                disable_web_page_preview=True,
            )
    except Exception as e:
        print("removebg_sticker-error - " + str(e))
        if "USER_IS_BLOCKED" in str(e):
            return
        else:
            try:
                await message.reply_to_message.reply_text(
                    "Something went wrong!", quote=True
                )
            except Exception:
                return
