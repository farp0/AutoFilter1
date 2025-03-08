from pyrogram import filters, Client
import bs4, requests, re, asyncio
import os, traceback, random
from info import LOG_CHANNEL as DUMP_GROUP
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Length": "99",
    "Origin": "https://saveig.app",
    "Connection": "keep-alive",
    "Referer": "https://saveig.app/en",
}

@Client.on_message(filters.regex(r'https?://.*instagram[^\s]+') & filters.incoming)
async def link_handler(Mbot, message):
    link = message.matches[0].group(0)
    global headers
    try:
        m = await message.reply_sticker("CAACAgUAAxkBAAITAmWEcdiJs9U2WtZXtWJlqVaI8diEAAIBAAPBJDExTOWVairA1m8eBA")
        url = link.replace("instagram.com", "ddinstagram.com")
        url = url.replace("==", "%3D%3D")

        # Handling video URLs
        if "/reel/" in url or "/stories" in url:
            if url.endswith("="):
                dump_file = await message.reply_video(url[:-1], caption="ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @Lucy_Filter_bot")
            else:
                dump_file = await message.reply_video(url, caption="ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @Lucy_Filter_bot")
        elif "/p/" in url:
            # Instagram photo URL
            response = requests.get(link, headers=headers)
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            meta_tag = soup.find('meta', attrs={'property': 'og:image'})
            if meta_tag:
                photo_url = meta_tag['content']
                # Download and send the photo
                downfile = f"{os.getcwd()}/{random.randint(1, 10000000)}.jpg"
                with open(downfile, 'wb') as f:
                    f.write(requests.get(photo_url, headers=headers).content)
                dump_file = await message.reply_photo(downfile, caption="ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @Lucy_Filter_bot")
                os.remove(downfile)  # Clean up the downloaded photo file
            else:
                return await message.reply("Could not fetch image, please make sure the post is publicly available.")
        else:
            # Fallback: try general media handler for other types of posts
            dump_file = await message.reply_video(url, caption="ᴅᴏᴡɴʟᴏᴀᴅᴇᴅ ʙʏ @Lucy_Filter_bot")

        if 'dump_file' in locals():
            await dump_file.forward(DUMP_GROUP)
        await m.delete()
    except Exception as e:
        try:
            await message.reply(f"400: Sorry, Unable To Find It  try another or report it to @VeldXd or support chat https://t.me/+DnmZbLjS0iw0YWI1")
            if LOG_GROUP:
                await Mbot.send_message(LOG_GROUP, f"Instagram error: {e} {link}")
                await Mbot.send_message(LOG_GROUP, traceback.format_exc())
        except Exception as e:
            await message.reply(f"Error: {str(e)}")

    finally:
        if 'dump_file' in locals():
            if DUMP_GROUP:
                await dump_file.copy(DUMP_GROUP)
        await m.delete()

