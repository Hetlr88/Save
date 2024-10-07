import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import psutil
from pyrogram import Client
import time
import os
import threading
import json
from os import environ

bot_token = environ.get("TOKEN", "") 
api_hash = environ.get("HASH", "") 
api_id = int(environ.get("ID", ""))
bot = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
   

            

def get_bot_link_button():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔗Advance Content Saver Bot ❤️ - بوت حفظ المحتوي المقيد 💾", url="https://t.me/Saveredicatbot")]]
    )

# download status
async def downstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break
        await asyncio.sleep(1)

    await asyncio.sleep(3)
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            await bot.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
            await asyncio.sleep(1)
        except:
            await asyncio.sleep(5)

# upload status
async def upstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break
        await asyncio.sleep(1)

    await asyncio.sleep(3)
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            await bot.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
            await asyncio.sleep(1)
        except:
            await asyncio.sleep(5)

# progress writer
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")

# start command
@bot.on_message(filters.command(["start"]))
async def send_start(client, message):
    await bot.send_message(
        message.chat.id,
        f"**__👋 Hi** **{message.from_user.mention}**, **I am Save Restricted Bot, I can send you public restricted content by post link note : only public__**\n\n{USAGE}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛 ", url="https://t.me/X_XF8")]]),
        reply_to_message_id=message.id
    )

# handle incoming text messages
@bot.on_message(filters.text)
async def save(client, message):
    print(message.text)

    # joining chats
    if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:
        try:
            await bot.send_message(message.chat.id, "**Chat Joined**", reply_to_message_id=message.id)
        except UserAlreadyParticipant:
            await bot.send_message(message.chat.id, "**Chat already Joined**", reply_to_message_id=message.id)
        except InviteHashExpired:
            await bot.send_message(message.chat.id, "**Invalid Link**", reply_to_message_id=message.id)

    # getting message
    elif "https://t.me/" in message.text:
        datas = message.text.split("/")
        temp = datas[-1].replace("?single", "").split("-")
        fromID = int(temp[0].strip())
        try:
            toID = int(temp[1].strip())
        except:
            toID = fromID

        for msgid in range(fromID, toID+1):
            # private
            if "https://t.me/c/" in message.text:
                chatid = int("-100" + datas[4])
                await handle_private(message, chatid, msgid)

            # bot
            elif "https://t.me/b/" in message.text:
                username = datas[4]
                try:
                    await handle_private(message, username, msgid)
                except Exception as e:
                    await bot.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)

            # public
            else:
                username = datas[3]
                try:
                    msg = await bot.get_messages(username, msgid)
                except UsernameNotOccupied:
                    await bot.send_message(message.chat.id, f"**The username is not occupied by anyone**", reply_to_message_id=message.id)
                    return

                try:
                    await bot.copy_message(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
                except:
                    try:
                        await handle_private(message, username, msgid)
                    except Exception as e:
                        await bot.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)

            # wait time
            await asyncio.sleep(3)

# handle private messages
async def handle_private(message, chatid, msgid):
    msg = await bot.get_messages(chatid, msgid)
    msg_type = get_message_type(msg)

    if msg_type == "Text":
        await bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id, reply_markup=get_bot_link_button())
        return

    smsg = await bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.id)
    dosta = threading.Thread(target=lambda: asyncio.create_task(downstatus(f'{message.id}downstatus.txt', smsg)), daemon=True)
    dosta.start()
    file = await bot.download_media(msg, progress=progress, progress_args=[message, "down"])
    os.remove(f'{message.id}downstatus.txt')

    upsta = threading.Thread(target=lambda: asyncio.create_task(upstatus(f'{message.id}upstatus.txt', smsg)), daemon=True)
    upsta.start()

    if msg_type == "Document":
        try:
            thumb = await bot.download_media(msg.document.thumbs[0].file_id)
        except:
            thumb = None
        await bot.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, reply_markup=get_bot_link_button(), progress=progress, progress_args=[message, "up"])
        if thumb:
            os.remove(thumb)

    elif msg_type == "Video":
        try:
            thumb = await bot.download_media(msg.video.thumbs[0].file_id)
        except:
            thumb = None
        await bot.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, reply_markup=get_bot_link_button(), progress=progress, progress_args=[message, "up"])
        if thumb:
            os.remove(thumb)

    elif msg_type == "Animation":
        await bot.send_animation(message.chat.id, file, reply_to_message_id=message.id, reply_markup=get_bot_link_button())

    elif msg_type == "Sticker":
        await bot.send_sticker(message.chat.id, file, reply_to_message_id=message.id, reply_markup=get_bot_link_button())

    elif msg_type == "Voice":
        await bot.send_voice(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, reply_markup=get_bot_link_button(), progress=progress, progress_args=[message, "up"])

    elif msg_type == "Audio":
        try:
            thumb = await bot.download_media(msg.audio.thumbs[0].file_id)
        except:
            thumb = None
        await bot.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, reply_markup=get_bot_link_button(), progress=progress, progress_args=[message, "up"])
        if thumb:
            os.remove(thumb)

    elif msg_type == "Photo":
        await bot.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, reply_markup=get_bot_link_button())

    os.remove(file)
    if os.path.exists(f'{message.id}upstatus.txt'):
        os.remove(f'{message.id}upstatus.txt')
    await bot.delete_messages(message.chat.id, [smsg.id])

# get the type of message
def get_message_type(msg):
    try:
        msg.document.file_id
        return "Document"
    except:
        pass

    try:
        msg.video.file_id
        return "Video"
    except:
        pass

    try:
        msg.animation.file_id
        return "Animation"
    except:
        pass

    try:
        msg.sticker.file_id
        return "Sticker"
    except:
        pass

    try:
        msg.voice.file_id
        return "Voice"
    except:
        pass

    try:
        msg.audio.file_id
        return "Audio"
    except:
        pass

    try:
        msg.photo.file_id
        return "Photo"
    except:
        pass

    try:
        msg.text
        return "Text"
    except:
        pass

USAGE = """
               للدردشات العامة

               فقط أرسل رابط المشاركة

                     للدردشات الخاصة

                
                     🚫غير مدعومة🚫
      
      … 
🏴 𝐅𝐨𝐫 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 𝐓𝐚𝐥𝐤 𝐃𝐞𝐯𝐥𝐨𝐩𝐞𝐫 𝐅𝐫𝐨𝐦 𝐇𝐞𝐫𝐞            🛡️ @X_XF8  ☠️
      …
"""

# infinty polling
bot.run()       

# Add this function to generate the keyboard with the bot link
