from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton as ikb, InlineKeyboardMarkup as ikm
import requests
from bs4 import BeautifulSoup as bs
import asyncio
from pyrogram.enums import ChatMemberStatus
import pymongo
from config import *
ADMINS = [int(admin_id) for admin_id in ADMIN.split(',')]

#-------------------------------------------------------------------------------------------------------------------
bot = Client(
    "Tegfsz",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

#-------------------------------------------------------------------------------------------------------------------
premium_channel_id = -1002006956019
channel_username = '@cinemaluxeupdates'
#-------------------------------------------------------------------------------------------------------------------
client = pymongo.MongoClient("mongodb+srv://smit:smit@cluster0.pjccvjk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["CinemaLuxeBott"]
idstoring = db["ids"]
domain = db["domain"]
domainPost = db["domainPost"]
#-------------------------------------------------------------------------------------------------------------------
#DOMAIN = "https://cinemaluxe.life/?s="
#DOMAIN_URL_POST = "https://cinemaluxe.life/"
async def broadcast(BroadcastMsg,message):
    successCount = 0
    errCount = 0
    bMessage = await bot.send_message(message.chat.id,'<b><i>Broadcasting...</i></b>')
    for usr in idstoring.find():
        usrID = usr['idd']

        try:
            await bot.send_message(usrID,f"<b><i>{BroadcastMsg}</i></b>")
            successCount += 1
        except:
            errCount += 1

        if successCount == 100:
            await asyncio.sleep(60)
        elif successCount == 1000:
            await asyncio.sleep(500)

    await bMessage.edit(f'<b><i>Broadcast Completed.. \nMessage sent to {successCount} users. with {errCount} Errors.</i></b>')

def check_joined():
    async def func(flt, bot, message):
        join_msg = f"**To use this bot, Please join our channel.\nJoin From The Link Below 👇**"
        user_id = message.from_user.id
        chat_id = message.chat.id
        try:
            member_info = await bot.get_chat_member(channel_username, user_id)
            if member_info.status in (ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER):
                return True
            else:
                await bot.send_message(chat_id, join_msg, reply_markup=ikm([[ikb("✅ Join Channel", url="https://t.me/cinemaluxeupdates")]]))
                return False
        except Exception as e:
            await bot.send_message(chat_id, join_msg, reply_markup=ikm([[ikb("✅ Join Channel", url="https://t.me/cinemaluxeupdates")]]))
            return False
    return filters.create(func)

@bot.on_message(filters.command("start") & check_joined())
async def start(bot, message):
    usrid = message.from_user.id
    await message.reply(text=f"<b><i>Welcome {message.from_user.first_name} 👋 ,\nThis Bot Is Owned by ❤️CinemaLuxe❤️.\n\nType Your Movie,TV Show and Anime Name.⬇️</i></b>")
    if idstoring.find_one({"idd": usrid}) == None:
        idstoring.insert_one({"idd": message.from_user.id, "name": message.from_user.first_name})
    
    # Above code is for find user id in database.
    # if Not found then it will add user in the database.
@bot.on_message(filters.command('domain'))
async def domaain(bot, message):
    if message.chat.id not in ADMINS:
        await bot.send_message(message.chat.id,"You are not an admin.")
        return
    try:
        _,dm = message.text.split(" ")
    except:
        await bot.send_message(message.chat.id, "Please Use /domain + domain")
        return
    domain.delete_many({})
    print(dm)
    domain.insert_one({"dmn":dm})
    await bot.send_message(message.chat.id,f"<b><i>Domain Changed To {dm}</b></i>")
@bot.on_message(filters.command('stats'))
async def stats(bot, message):
    if message.chat.id not in ADMINS:
        await bot.send_message(message.chat.id,"You are not an admin.")
        return
    totalusr = idstoring.count_documents({})
    await message.reply_text(f"<b><i>Total Users: {totalusr}</b></i>")
@bot.on_message(filters.command('broadcast'))
async def bd(bot,message):
    if message.chat.id not in ADMINS:
        await bot.send_message(message.chat.id,"You are not an admin.")
        return
    try:
        _,bMsg = message.text.split('/broadcast ')
    except:
        await bot.send_message(message.chat.id, "Please Use /broadcast + message")
        return
    print(bMsg) #OUR BROADCAST MESSAGE..
    await broadcast(bMsg , message)#Broadcast MEssage , message for chat id. to send message to the admin.
@bot.on_message(filters.command('domainP'))
async def domainP(bot,message):
    if message.chat.id not in ADMINS:
        await bot.send_message(message.chat.id,"You are not an admin.")
        return
    try:
        _,dm = message.text.split(" ")
    except:
        await bot.send_message(message.chat.id, "Please Use /domainP + domainUrlPost")
        return
    domainPost.delete_many({})
    print(dm)
    domainPost.insert_one({"DomainPost":dm})
    await bot.send_message(message.chat.id,f"<b><i>DomainPost Changed To {dm}</b></i>")
@bot.on_message(filters.command('link') & filters.private)
async def LInkTOPost(bot, message):
    if message.chat.id in ADMINS:
        LinkOne = message.text.lstrip("/link ")
        if LinkOne.startswith("https://"):
            dcs = domainPost.find_one({})
            DOMAIN_URL_POST = dcs['DomainPost']
            print(DOMAIN_URL_POST)
            print("Link is Valid")
            searchMSG = await bot.send_message(message.chat.id, "<i><b>Creating Post...</b></i>")
            req1 = requests.get(LinkOne)
            soup2 = bs(req1.text, 'html.parser')
            link3 = soup2.find('div', class_="poster")
            link2_1 = soup2.find('div', class_='data')
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
                quality_list = []
                audio_list = []
                size_list = []
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) == 4:
                        quality = cells[1].find(
                            'strong', class_='quality').text.strip()
                        audio = cells[2].text.strip()
                        size = cells[3].text.strip()
                        quality_list.append(quality)
                        audio_list.append(audio)
                        size_list.append(size)
                quality_str = ' '.join(set(quality_list))
                audio_str = ' '.join(set(audio_list))
                print("Quality:", quality_str)
                print("Audio:", audio_str)
                button = ikb("📥  Ｄｏｗｎｌｏａｄ Ｎｏｗ  📥", url=LinkOne)
                reply_markup = ikm([[button]])
                await searchMSG.delete()
                
                await bot.send_photo(premium_channel_id, MovieImage, caption=f"<i><b>{MovieName}\n\n✔️ ᴀᴅᴅᴇᴅ ᴏɴ {DOMAIN_URL_POST}</b>\n\n🎞 Qᴜᴀʟɪᴛʏ ᴀᴅᴅᴇᴅ - {quality_str}\n🎶 ᴀᴜᴅɪᴏ ᴀᴅᴅᴇᴅ - {audio_str}\n\nᴡᴇʙꜱɪᴛᴇ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ\nᴊᴏɪɴ ɴᴏᴡ  @cinemaluxerequest \n\n⭐️ᴊᴏɪɴ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ - @cinemaluxeupdates </b></i>", reply_markup=reply_markup)
                CreatedPost = await bot.send_message(message.chat.id, "<i><b>Post Created Successfully..</b></i>")
                await asyncio.sleep(5)
                await CreatedPost.delete()
            except:
                await searchMSG.delete()
                button = ikb("📥  Ｄｏｗｎｌｏａｄ Ｎｏｗ  📥", url=LinkOne)
                reply_markup = ikm([[button]])
                await bot.send_photo(premium_channel_id, MovieImage, caption=f"<i><b>{MovieName}\n\n✔️ ᴀᴅᴅᴇᴅ ᴏɴ {DOMAIN_URL_POST}</b>\n\nᴡᴇʙꜱɪᴛᴇ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ\nᴊᴏɪɴ ɴᴏᴡ  @cinemaluxerequest \n\n⭐️ᴊᴏɪɴ ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ - @cinemaluxeupdates </b></i>", reply_markup=reply_markup)
                CreatedPost = await bot.send_message(message.chat.id, "<i><b>Post Created Successfully..</b></i>")
                await asyncio.sleep(5)
                await CreatedPost.delete()
        else:
            LimkInvalid = await bot.send_message(message.chat.id, "<b>Link is Invalid \n It Must Starts with 'https://'</b>")
            await asyncio.sleep(5)
            await LimkInvalid.delete()
    else:
        await bot.send_message(message.chat.id, "<b> ADMIN COMMAND ONLY....")

@bot.on_message(filters.text)
async def Movie(bot, message):
    dc = domain.find_one({})
    user_id = message.from_user.id
    chat_id = premium_channel_id
    try:
        await bot.get_chat_member(chat_id, user_id)
    except:
        if message.text.startswith("/start"):
            return
        await bot.send_message(message.chat.id, "<b>You haven't joined the Channel \nJoin by sending /start command in my DM.</b>")
        return

    try:
        mname = message.text
        print(mname)
        domainName = dc['dmn']
        print(domainName)
        url = domainName + mname
        searchMSG = await message.reply("<b>Searching ... </b>")
        r1 = requests.get(url)
        soup = bs(r1.text, 'html.parser')
        # print(soup)

        link = soup.find_all('div', class_="result-item")
        # print(link)
        try:
            resultsItem = []
            movieItem = []
            for i in link:
                MovieLink = i.a['href']
                resultsItem.append(MovieLink)
                r2 = requests.get(MovieLink)
                soup2 = bs(r2.text, 'html.parser')
                link2_1 = soup2.find('div', class_='data')
                MovieName = link2_1.h1.text
                movieItem.append(MovieName)
                if len(resultsItem) > 9:
                    break
        except:
            await searchMSG.delete()
        movie_links = dict(zip(movieItem, resultsItem))
        print(movie_links)
        keyboard = []
        for movie_name, url in movie_links.items():
            keyboard.append([ikb(movie_name, url=url)])

        reply_markup = ikm(keyboard)
        await searchMSG.delete()
        await message.reply_text("<i><b>Choose:</b></i>", reply_markup=reply_markup)
        if idstoring.find_one({"idd": message.from_user.id}) == None:
            idstoring.insert_one({"idd": message.from_user.id, "name": message.from_user.first_name})
    except:
        await searchMSG.delete()
        MvNotFound = await message.reply("<b>Not Found On Website..</b>")
        await asyncio.sleep(2)
        await MvNotFound.delete()


bot.run()
