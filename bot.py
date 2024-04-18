from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm
import requests
from bs4 import BeautifulSoup as bs
import asyncio
from config import API_HASH,API_ID,BOT_TOKEN,DOMAIN,DOMAIN_URL_POST,ADMIN
bot = Client("lientBdsot2",
             bot_token = BOT_TOKEN,
             api_id= API_ID,
             api_hash= API_HASH)

# Specify the group chat ID where the bot should work
group_chat_id = -1001996800596 # Replace this with your group chat ID

ADMINS = [int(admin_id) for admin_id in ADMIN.split(',')]

# Function to handle /start command
@bot.on_message(filters.command("start"))
async def start(bot, message):
    if message.chat.id == group_chat_id or message.chat.id in ADMINS:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Hello! I am your bot. How can I assist you?"
        )
    #if message.chat.id in ADMINS:
    #    await bot.send_message(
    #        chat_id=message.chat.id,
    #        text="Hello! I am your bot. How can I assist you?"
    #    )

    else:
        button1 = ikb("Join", url="https://t.me/cinemaluxerequest")
        reply_markup1 = ikm([[button1]])
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<b><i>Please use this bot in the specified group chat.\nTo use this bot and access its features, please join the group using <u>Join</u> button</i></b>",
            reply_markup=reply_markup1
        )


@bot.on_message(filters.command('link') & filters.private)
async def LInkTOPost(bot,message):
    if message.chat.id in ADMINS:
        LinkOne = message.text.lstrip("/link ")
        if LinkOne.startswith("https://"):
            print("Link is Valid")
            searchMSG = await bot.send_message(message.chat.id, "<i><b>Creating Post...</b></i>")
            req1 = requests.get(LinkOne)
            soup2 = bs(req1.text, 'html.parser')
            link3 = soup2.find('div', class_="poster")
            link2_1 =  soup2.find('div', class_='data')
            MovieName = link2_1.h1.text
            if link3:
                img_tag = link3.find('img')
                if img_tag:
                    src_value = img_tag.get('src')
                    print(src_value)
            MovieImage = src_value


            try:

                link4 = soup2.find('div', class_='fix-table')
            
                rows = link4.find_all('tr')
            #print(rows)
                quality_list = []
                audio_list = []
                size_list = []

# Lo        op through each row in the table body
                for row in rows:
            # Find all cells in the row
                    cells = row.find_all('td')
                    if len(cells) == 4:  # Ensure it's a data row (not header)
                # Extract Quality, Language, and Size from the cells
                        quality = cells[1].find('strong', class_='quality').text.strip()
                        audio = cells[2].text.strip()
                        size = cells[3].text.strip()
                # Append the extracted data to the respective lists
                        quality_list.append(quality)
                        audio_list.append(audio)
                        size_list.append(size)

# Pr        int the scraped data
                quality_str = ' '.join(set(quality_list))
                audio_str = ' '.join(set(audio_list))

# Pr        int the strings
                print("Quality:", quality_str)
                print("Audio:", audio_str)

                button = ikb("📥  Ｄｏｗｎｌｏａｄ Ｎｏｗ  📥", url= LinkOne)
                reply_markup = ikm([[button]])
                await searchMSG.delete()
                await bot.send_photo(-1002006956019,MovieImage,caption=f"<i><b>{MovieName}\n\n✔️ ᴀᴅᴅᴇᴅ ᴏɴ {DOMAIN_URL_POST}</b>\n\n🎞 Qᴜᴀʟɪᴛʏ ᴀᴅᴅᴇᴅ - {quality_str}\n🎶 ᴀᴜᴅɪᴏ ᴀᴅᴅᴇᴅ - {audio_str}\n\nᴡᴇʙꜱɪᴛᴇ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ\nᴊᴏɪɴ ɴᴏᴡ  @cinemaluxerequest \n\n⭐️ᴊᴏɪɴ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ - @cinemaluxeupdates </b></i>",reply_markup=reply_markup)
                CreatedPost = await bot.send_message(message.chat.id,"<i><b>Post Created Successfully..</b></i>")
                await asyncio.sleep(5)
                await CreatedPost.delete()
            
            except:
                await searchMSG.delete()
                button = ikb("📥  Ｄｏｗｎｌｏａｄ Ｎｏｗ  📥", url= LinkOne)
                reply_markup = ikm([[button]])
                await bot.send_photo(-1002006956019,MovieImage,caption=f"<i><b>{MovieName}\n\n✔️ ᴀᴅᴅᴇᴅ ᴏɴ {DOMAIN_URL_POST}</b>\n\nᴡᴇʙꜱɪᴛᴇ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ\nᴊᴏɪɴ ɴᴏᴡ  @cinemaluxerequest \n\n⭐️ᴊᴏɪɴ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ - @cinemaluxeupdates </b></i>",reply_markup=reply_markup)
                CreatedPost=await bot.send_message(message.chat.id,"<i><b>Post Created Successfully..</b></i>")
                await asyncio.sleep(5)
                await CreatedPost.delete()
        else:
            LimkInvalid =await bot.send_message(message.chat.id, "<b>Link is Invalid \n It Must Starts with 'https://'</b>")
            await asyncio.sleep(5)
            await LimkInvalid.delete()
    else:
        await bot.send_message(message.chat.id, "<b> ADMIN COMMAND ONLY....")
@bot.on_message(filters.command(["s","search"]))
async def Movie(bot, message):
    print(message.chat.id)
    if message.chat.id == group_chat_id or message.chat.id in ADMINS:
        try:
            if message.text.startswith('/s '):
                mname = message.text.lstrip("/s ")
            else:
                mname = message.text.lstrip("/search ")
            print(mname)
            domainName = DOMAIN
            url = domainName + mname
            searchMSG = await message.reply("<b>Searching ... </b>")
            r1 = requests.get(url)
            soup = bs(r1.text, 'html.parser')
            link = soup.find('div', class_="result-item")
            try:
                for i in link:
                    MovieLink = i.a['href']
            except:
                await searchMSG.delete()
            print(MovieLink)
            r2 = requests.get(MovieLink)
            soup2 = bs(r2.text, 'html.parser')
            link3 = soup2.find('div', class_="poster")
            print(link3)
            if link3:
                img_tag = link3.find('img')
                if img_tag:
                    src_value = img_tag.get('src')
                    print(src_value)
            MovieImage = src_value
            print(MovieImage)
            link2_1 =  soup2.find('div', class_='data')
            #print(link2_1.h1.text)
            MovieName = link2_1.h1.text
            print(MovieName)
            
            try:

                link4 = soup2.find('div', class_='fix-table')
            
                rows = link4.find_all('tr')
            #print(rows)
                quality_list = []
                audio_list = []
                size_list = []

# Lo        op through each row in the table body
                for row in rows:
            # Find all cells in the row
                    cells = row.find_all('td')
                    if len(cells) == 4:  # Ensure it's a data row (not header)
                # Extract Quality, Language, and Size from the cells
                        quality = cells[1].find('strong', class_='quality').text.strip()
                        audio = cells[2].text.strip()
                        size = cells[3].text.strip()
                # Append the extracted data to the respective lists
                        quality_list.append(quality)
                        audio_list.append(audio)
                        size_list.append(size)

# Pr        int the scraped data
                quality_str = ' '.join(set(quality_list))
                audio_str = ' '.join(set(audio_list))

# Pr        int the strings
                print("Quality:", quality_str)
                print("Audio:", audio_str)

                button = ikb("📥  Ｄｏｗｎｌｏａｄ Ｎｏｗ  📥", url= MovieLink)
                reply_markup = ikm([[button]])
                await searchMSG.delete()
                await bot.send_photo(message.chat.id,MovieImage,caption=f"<i><b>{MovieName}\n\n✔️ ᴀᴅᴅᴇᴅ ᴏɴ {DOMAIN_URL_POST}</b>\n\n🎞 Qᴜᴀʟɪᴛʏ ᴀᴅᴅᴇᴅ - {quality_str}\n🎶 ᴀᴜᴅɪᴏ ᴀᴅᴅᴇᴅ - {audio_str}\n\nᴡᴇʙꜱɪᴛᴇ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ\nᴊᴏɪɴ ɴᴏᴡ  @cinemaluxerequest \n\n⭐️ᴊᴏɪɴ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ - @cinemaluxeupdates </b></i>",reply_markup=reply_markup)
            except:
                await searchMSG.delete()
                button = ikb("📥  Ｄｏｗｎｌｏａｄ Ｎｏｗ  📥", url= MovieLink)
                reply_markup = ikm([[button]])
                await bot.send_photo(message.chat.id,MovieImage,caption=f"<i><b>{MovieName}\n\n✔️ ᴀᴅᴅᴇᴅ ᴏɴ {DOMAIN_URL_POST}</b>\n\nᴡᴇʙꜱɪᴛᴇ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ\nᴊᴏɪɴ ɴᴏᴡ  @cinemaluxerequest \n\n⭐️ᴊᴏɪɴ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ - @cinemaluxeupdates </b></i>",reply_markup=reply_markup) 
        except:
            await searchMSG.delete()
            MvNotFound = await message.reply("<b>Not Found On Website..</b>")
            await asyncio.sleep(5)
            await MvNotFound.delete()
    else:
        button1 = ikb("Join", url="https://t.me/cinemaluxerequest")
        reply_markup1 = ikm([[button1]])
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<b><i>Please use this bot in the specified group chat.\nTo use this bot and access its features, please join the group using <u>Join</u> button</i></b>",
            reply_markup=reply_markup1
        )


bot.run()
