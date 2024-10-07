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
   

# download status
def downstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as downread:
            txt = downread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
            time.sleep(1)
        except:
            time.sleep(5)

# upload status
def upstatus(statusfile, message):
    while True:
        if os.path.exists(statusfile):
            break

    time.sleep(3)      
    while os.path.exists(statusfile):
        with open(statusfile, "r") as upread:
            txt = upread.read()
        try:
            bot.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
            time.sleep(1)
        except:
            time.sleep(5)

# progress writter
def progress(current, total, message, type):
    with open(f'{message.id}{type}status.txt', "w") as fileup:
        fileup.write(f"{current * 100 / total:.1f}%")

# start command
@bot.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bot.send_message(message.chat.id, f"**__👋 Hi** **{message.from_user.mention}**, **𝙸 𝚊𝚖 𝚂𝚊𝚟𝚎 𝚁𝚎𝚜𝚝𝚛𝚒𝚌𝚝𝚎𝚍 𝙱𝚘𝚝 𝙱𝚘𝚝 𝙸 𝚌𝚊𝚗 𝚢𝚘𝚞 𝚛𝚎𝚜𝚝𝚛𝚒𝚌𝚝𝚎𝚍 𝚌𝚘𝚗𝚝𝚎𝚗𝚝 𝚋𝚢 𝚙𝚘𝚜𝚝 𝚕𝚒𝚗𝚔\n🫡 🚫 🛡️ 🛡️ :: 𝙽𝚘 𝚙𝚘𝚛𝚗 𝚌𝚘𝚗𝚝𝚎𝚗𝚝 𝚢𝚘𝚞 𝚠𝚒𝚕𝚕 𝚐𝚎𝚝 𝚋𝚊𝚗 \n 𝚌𝚊𝚗 𝚜𝚊𝚟𝚎 𝙾𝚗 𝚕 𝚢 𝚏𝚛𝚘𝚖 𝚙𝚞𝚙𝚕𝚒𝚌 𝚊𝚗𝚍 𝚊𝚗𝚍 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 𝚌𝚑𝚊𝚗𝚗𝚎𝚕 \n🛡️𝚃𝚑𝚊𝚗𝚔𝚜 𝙵𝚘𝚛 𝚄𝚜𝚒𝚗𝚐 𝚖𝚎 ❤️__**\n\n{USAGE}",
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌐 𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛 ", url="https://t.me/X_XF8")]]), reply_to_message_id=message.id)

@bot.on_message(filters.text)
def save(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    print(message.text)

    # joining chats
    if "https://t.me/+" in message.text or "https://t.me/joinchat/" in message.text:
        try:
            bot.send_message(message.chat.id, f"**Chat Joined**", reply_to_message_id=message.id)
        except UserAlreadyParticipant:
            bot.send_message(message.chat.id, "**Chat already Joined**", reply_to_message_id=message.id)
        except InviteHashExpired:
            bot.send_message(message.chat.id, "**Invalid Link**", reply_to_message_id=message.id)

    # getting message
    elif "https://t.me/" in message.text:
        datas = message.text.split("/")
        temp = datas[-1].replace("?single", "").split("-")
        fromID = int(temp[0].strip())
        try: toID = int(temp[1].strip())
        except: toID = fromID

        for msgid in range(fromID, toID+1):
            # private
            if "https://t.me/c/" in message.text:
                chatid = int("-100" + datas[4])
                handle_private(message, chatid, msgid)
                
            # bot
            elif "https://t.me/b/" in message.text:
                username = datas[4]
                try: handle_private(message, username, msgid)
                except Exception as e: bot.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)

            # public
            else:
                username = datas[3]
                try: msg = bot.get_messages(username, msgid)
                except UsernameNotOccupied: 
                    bot.send_message(message.chat.id, f"**The username is not occupied by anyone**", reply_to_message_id=message.id)
                    return

                try: bot.copy_message(message.chat.id, msg.chat.id, msg.id, reply_to_message_id=message.id)
                except:
                    try: handle_private(message, username, msgid)
                    except Exception as e: bot.send_message(message.chat.id, f"**Error** : __{e}__", reply_to_message_id=message.id)

            # wait time
            time.sleep(3)

# handle private
def handle_private(message: pyrogram.types.messages_and_media.message.Message, chatid: int, msgid: int):
    msg: pyrogram.types.messages_and_media.message.Message = bot.get_messages(chatid, msgid)
    msg_type = get_message_type(msg)

    if "Text" == msg_type:
        bot.send_message(message.chat.id, msg.text, entities=msg.entities, reply_to_message_id=message.id)
        return

    smsg = bot.send_message(message.chat.id, '__Downloading__', reply_to_message_id=message.id)
    dosta = threading.Thread(target=lambda: downstatus(f'{message.id}downstatus.txt', smsg), daemon=True)
    dosta.start()
    file = bot.download_media(msg, progress=progress, progress_args=[message, "down"])
    os.remove(f'{message.id}downstatus.txt')

    upsta = threading.Thread(target=lambda: upstatus(f'{message.id}upstatus.txt', smsg), daemon=True)
    upsta.start()
    
    if "Document" == msg_type:
        try:
            thumb = bot.download_media(msg.document.thumbs[0].file_id)
        except: thumb = None
        
        bot.send_document(message.chat.id, file, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        if thumb is not None: os.remove(thumb)

    elif "Video" == msg_type:
        try: 
            thumb = bot.download_media(msg.video.thumbs[0].file_id)
        except: thumb = None

        bot.send_video(message.chat.id, file, duration=msg.video.duration, width=msg.video.width, height=msg.video.height, thumb=thumb, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        if thumb is not None: os.remove(thumb)

    elif "Animation" == msg_type:
        bot.send_animation(message.chat.id, file, reply_to_message_id=message.id)
        
    elif "Sticker" == msg_type:
        bot.send_sticker(message.chat.id, file, reply_to_message_id=message.id)

    elif "Voice" == msg_type:
        bot.send_voice(message.chat.id, file, caption=msg.caption, thumb=thumb, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])

    elif "Audio" == msg_type:
        try:
            thumb = bot.download_media(msg.audio.thumbs[0].file_id)
        except: thumb = None
        
        bot.send_audio(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id, progress=progress, progress_args=[message, "up"])
        if thumb is not None: os.remove(thumb)

    elif "Photo" == msg_type:
        bot.send_photo(message.chat.id, file, caption=msg.caption, caption_entities=msg.caption_entities, reply_to_message_id=message.id)

    os.remove(file)
    if os.path.exists(f'{message.id}upstatus.txt'): os.remove(f'{message.id}upstatus.txt')
    bot.delete_messages(message.chat.id, [smsg.id])

# get the type of message
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):
	try:
		msg.document.file_id
		return "Document"
	except: pass

	try:
		msg.video.file_id
		return "Video"
	except: pass

	try:
		msg.animation.file_id
		return "Animation"
	except: pass

	try:
		msg.sticker.file_id
		return "Sticker"
	except: pass

	try:
		msg.voice.file_id
		return "Voice"
	except: pass

	try:
		msg.audio.file_id
		return "Audio"
	except: pass

	try:
		msg.photo.file_id
		return "Photo"
	except: pass

	try:
		msg.text
		return "Text"
	except: pass



USAGE = """
                      للدردشات العامة

               فقط أرسل رابط المشاركة

                     للدردشات الخاصة

                
                     🚫غير مدعومة🚫
      
      … 
🏴 𝐅𝐨𝐫 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 𝐓𝐚𝐥𝐤 𝐃𝐞𝐯𝐥𝐨𝐩𝐞𝐫 𝐅𝐫𝐨𝐦 𝐇𝐞𝐫𝐞            🛡️ @X_XF8  ☠️
      …
      … 
"""


# infinty polling
bot.run()




