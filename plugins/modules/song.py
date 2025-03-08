import os
import random
import shutil
from pyrogram import Client, filters, enums
from yt_dlp import YoutubeDL
from pyrogram.types import InputMediaAudio
from spleeter.separator import Separator

async def download_songs(query, download_directory="."):
    query = f"{query} Lyrics".replace(":", "").replace("\"", "")
    ydl_opts = {
        "format": "bestaudio/best",
        "default_search": "ytsearch",
        "noplaylist": True,
        "nocheckcertificate": True,
        "outtmpl": f"{download_directory}/%(title)s.mp3",
        "quiet": True,
        "addmetadata": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        try:
            video = ydl.extract_info(f"ytsearch:{query}", download=False)["entries"][0]["id"]
            info = ydl.extract_info(video)
            filename = ydl.prepare_filename(info)
            if not filename:
                print(f"Track Not Found⚠️")
            else:
                path_link = filename
                return path_link, info 
        except Exception as e:
            raise Exception(f"Error downloading song: {e}")  

@Client.on_message(filters.command("song"))
async def song(_, message):
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)
        k = await message.reply("⌛")
        print("⌛")
        try:
            randomdir = f"/tmp/{str(random.randint(1, 100000000))}"
            os.mkdir(randomdir)
        except Exception as e:
            await message.reply_text(f"Fᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ sᴏɴɢ ʀᴇᴛʀʏ ᴀғᴛᴇʀ sᴏᴍᴇᴛɪᴍᴇ ʀᴇᴀsᴏɴ: {e}")
            return await k.delete()
        query = message.text.split(None, 1)[1]
        await message.reply_chat_action(enums.ChatAction.RECORD_AUDIO)
        path, info = await download_songs(query, randomdir)
        await message.reply_chat_action(enums.ChatAction.UPLOAD_AUDIO)
        await k.edit("ᴜᴘʟᴏᴀᴅɪɴɢ")
        song_title = info.get("title", "Unknown Title")   
        song_caption = f"**🍃 {song_title}**\n" + \
                       f"🍂 sᴜᴘᴘᴏʀᴛ: <a href='https://t.me/weebs_support'>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>" 

        await message.reply_audio(
            path,
            caption=song_caption
        )

    except IndexError:
        await message.reply("eg `/song lover`")
        return await k.delete()
    except Exception as e:
        await message.reply_text(f"Fᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ sᴏɴɢ ʀᴇᴀsᴏɴ: {e}")
    finally:
        try:
            shutil.rmtree(randomdir)
            return await k.delete()
        except:
            pass

# Create a function to remove vocals using Spleeter
def remove_vocals(input_file_path):
    separator = Separator('spleeter:2stems')  # 2 stems: vocals and accompaniment
    output_path = "output/"
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, "no_vocals.wav")
    
    separator.separate_to_file(input_file_path, output_path)
    
    return output_file

# Command handler to remove vocals from the song
@app.on_message(filters.command("rm_vocal") & filters.audio)
async def rm_vocal(client, message):
    # Download the audio file
    audio_file = await message.download()
    
    # Remove vocals
    output_file = remove_vocals(audio_file)
    
    # Send the processed file back to the user
    await message.reply_audio(output_file, caption="Here's your song without vocals.")
    
    # Clean up the files
    os.remove(audio_file)
    os.remove(output_file)
