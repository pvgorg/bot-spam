from pyrogram.enums import ChatType
import psutil , sqlite3 , random
from pyrogram import Client, filters 
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pyrogram import Client, filters, errors
from pathlib import Path
import config

admin = config.admin
api_id = 23136380
api_hash = '6ae6541159e229499615953de667675c'


client = Client("self", api_id, api_hash)
scheduler = AsyncIOScheduler()
cnx = sqlite3.connect("data.db")
cursor = cnx.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS bot(model TEXT DEFAULT 'text' , tag TEXT DEFAULT 'off', setid TEXT , setgp TEXT , texttag TEXT , repcht INTEGER , repmes INTEGER , enchat INTEGER , enmes INTEGER ,  time INTEGER DEFAULT '1')''')
cursor.execute('''CREATE TABLE IF NOT EXISTS listfosh(fosh TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS listadmin(admin TEXT)''')
cursor.execute(f"SELECT * FROM listadmin WHERE admin = '{admin}'")
existing_record = cursor.fetchone()
if existing_record is None:
    cursor.execute("INSERT INTO listadmin (admin) VALUES (?)" , (admin,))
    cnx.commit()

# =========== def =========== #
async def jobfosh(model , chatid , tag , Userid , textfosh):
    if model == 'rep':
        await client.forward_messages(int(chatid) , from_chat_id= int(getdata('repcht' , 'bot')[0]) ,message_ids= int(getdata('repmes' , 'bot')[0]))

    elif model == 'text':
        listfosh = getdata('fosh','listfosh')
        fosh = random.choice(listfosh)

        if tag == 'on':
            await client.send_message(chatid,  text= f'[{textfosh}](tg://user?id={int(Userid)}){fosh}')
        elif tag == 'off':
            await client.send_message(chatid,  text= fosh)

async def jobenemi(chatid,mesid):
    listfosh = getdata('fosh','listfosh')
    fosh = random.choice(listfosh)

    await client.send_message(chatid , reply_to_message_id = mesid ,  text= fosh)


def senddata(data , value , namevalue):
        if len(data) > 0:
                    if data[0] == None:
                        cursor.execute(f"UPDATE bot SET {namevalue} = ? WHERE {namevalue} IS NULL", (value,))
                        cnx.commit()
                        return "سیو شد"
                    
                    else:
                        cursor.execute(f"UPDATE bot SET {namevalue} = ? WHERE {namevalue} = '{data[0]}'" , (value,))
                        cnx.commit()
                        return "تغییر پیدا کرد"                    

        elif not data:
            cursor.execute(f'''INSERT INTO bot({namevalue}) VALUES (?)''', (value,))
            cnx.commit()
            return "سیو شد"

def getdata(value , table):
    list = []

    cursor.execute(f'''SELECT {value} FROM {table}''')
    rows = cursor.fetchall()
    for row in rows:
            list.append(row[0])
    return list
# =========== Handlers =========== #
@client.on_message(filters.text , filters.photo)
async def spamer_handler(client, message):

    text = message.text
    Userid = message.from_user.id
    listadmin = getdata('admin','listadmin')

    if str(Userid) in listadmin:
        if text == "bot":
            await message.reply_text('انلاینم!🦦' , quote = True)

        elif text == "help2":
            await message.reply_text("""🌵 راهنمای سلف
    ❋ `admin`(id) ⤳ با استفاده از دستور زیر ادمین جدید اضافه کنید به اتکر  
    ❋ `deladmin`(id) ⤳ با استفاده از دستور زیر ادمین مورد نظر را حذف کنی   
    ❋ `delalladmin` ⤳ با استفاده از دستور زیر تمام ادمین ها را حذف کنید                    
    ❋ `listadmin` ⤳ با استفاده از دستور زیر لیست ادمین ها را مشاهده کنید 
        
    ❋ owner ⤳ @mer_py 🧑‍💻
            """)

        elif text == "help":
            await message.reply_text("""🌵 راهنمای سلف
    ❋ `bot` ⤳ بررسی آنلاین بودن بات
    ❋ `stats` ⤳ اطلاع از وضعیت کلی بات
    ❋ `id` (rep) ⤳ دریافت ایدی گپ و فرد مقابل                     
    ❋ `mode` (text/rep) ⤳ دستوره تغییر مدل ارسال پیام
    ❋ `setid` (id) ⤳ ست کردن ایدی شخص برای میشن                            
    ❋ `setgp` (id gp) ⤳ ست کردن گروه برای ارسال پیام
    ❋ `setrep` (id gp) ⤳ ست کردن پیامی پست برای فروارد 
    ❋ `settime` (1~99999) ⤳ تنظیم زمان ارسال پیام به گروه یا پیوی        
    ❋ `setenemi`reply ⤳ تنظیم پیام برا اتک                        
    ❋ `addfosh` reply ⤳ اضافه کردن فوش مورد نظر
    ❋ `delallfosh` ⤳ حذف تمامی فوش های ربات                                                           
    ❋ `tag` (on/off) ⤳ روشن خاموش کردن میشن کردن شخص
    ❋ `fosh`(on/off)⤳ ارسال پیام به گروه یا پیوی
    ❋ `attack`(on/off)⤳ ارسال رگبار بر روی پیام                            
    ❋ `join` @telegram ⤳ جوین شدن در گروه ها
    ❋ `left` @telegram ⤳ لفت دادن از گروه مورد نظر
    ❋ `texttag` ⤳ ست کردن متن برای میشن  
    ❋ `setphoto` ⤳ تغییر عکس پروفایل
    


    ❋ `help2` ⤳ باز کردن راهنمای افزودن ادمین به ربات                                             
    ❋ owner ⤳ @La_shy 🧑‍💻
            """)
        
        elif text == "id":
            if message.reply_to_message is not None:
                if message.reply_to_message.forward_from is not None:
                    await message.reply_text(f"وضعیت فورواد\n\n ایدی عددی :`{message.reply_to_message.forward_from.id}`\nاسم:`{message.reply_to_message.forward_from.first_name}`\nایدی: @{message.reply_to_message.forward_from.username}")
                elif message.reply_to_message.from_user is not None:
                    await message.reply_text(f"وضعیت فورواد\n\n ایدی عددی :`{message.reply_to_message.from_user.id}`\nاسم:`{message.reply_to_message.from_user.first_name}`\nایدی: @{message.reply_to_message.from_user.username}")
            elif message.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
                    await message.reply_text(f"وضعیت فورواد\n\nایدی عددی :`{message.chat.id}`\nاسم:`{message.chat.title}`\nایدی: @{message.chat.username}")    
            
            else: 
                await message.reply_text("روی متن فورارد شده ازش ریپلای کن")  

        elif text == "stats":
            await message.reply_text(f"وضعیت بات \n\n model:{getdata('model','bot')[0]} \n tag:{getdata('tag','bot')[0]} \n setid:{getdata('setid','bot')[0]} \n setgp:{getdata('setgp','bot')[0]} \n time:{getdata('time','bot')[0]}")

        elif text == 'setrep':
            if message.reply_to_message is not None:
                senddata(data= getdata('repcht' , 'bot') , namevalue= 'repcht' , value= message.reply_to_message.chat.id)
                senddata(data= getdata('repmes' , 'bot') , namevalue= 'repmes' , value= message.reply_to_message.id)
                await message.reply_text('پیام فورواردی ست شد')

        elif text.startswith("tag"):
            text = text.split()
            listmod = ["on" , "off"]

            if len(text) == 2:
                if text[1] in listmod:
                    respons = senddata(data= getdata('tag','bot') , value=text[1] , namevalue= 'tag')
                    await message.reply_text(f'{respons}')
                else:
                    await message.reply_text('لطفا از 2 مورد `off` , `on` یکی رو انتخاب کنید')
            else:
                await message.reply_text('لطفا تایم بعد `tag` بفرستید \n مثال : tag on')

        elif text.startswith("mode"):
            text = text.split()
            listmod = ["text" , "rep"]

            if len(text) == 2:
                if text[1] in listmod:
                    respons = senddata(data= getdata('model','bot') , value=text[1] , namevalue= 'model')
                    await message.reply_text(f'{respons}')
                else:
                    await message.reply_text('لطفا از 2 مود `text` , `rep` یکی رو انتخاب کنید')
            else:
                await message.reply_text('لطفا تایم بعد `mode` بفرستید \n مثال : mode text')

        elif text.startswith("texttag"):
            text = text.split()
            

            if len(text) >= 2:
                text = ' '.join((text[1:]))
                respons = senddata(data= getdata('texttag','bot') , value=text , namevalue= 'texttag')
                await message.reply_text(f'{respons}')
            else:
                await message.reply_text('لطفا متن بعد `texttag` بفرستید \n مثال : texttag مهدی')

        elif text == 'setenemi':

            if message.reply_to_message is not None:
                    senddata(data= getdata('enchat' , 'bot') , namevalue= 'enchat' , value= message.reply_to_message.chat.id)
                    senddata(data= getdata('enmes' , 'bot') , namevalue= 'enmes' , value= message.reply_to_message.id)
                    await message.reply_text(f'پیام مورد نطر شما به عنوان انمی ذخیره شد')
                    
            elif message.reply_to_message is  None:
                await message.reply('روی پیام مورد نطر ریپلای کن') 

        elif text.startswith("settime"):
            text = text.split()


            if len(text) == 2:
                respons = senddata(data= getdata('time','bot') , value=text[1] , namevalue= 'time')
                await message.reply_text(f'{respons}')
            else:
                await message.reply_text('لطفا تایم بعد `time` بفرستید \n مثال : time 1')

        elif text.startswith("setid"):
            text = text.split()

            if len(text) == 2:
                respons = senddata(data= getdata('setid','bot') , value=text[1] , namevalue= 'setid')
                await message.reply_text(f'{respons}')
            else:
                await message.reply_text('لطفا ایدی بعد `setid` بفرستید \n مثال : setid 000000000')

        elif text.startswith("setgp"):
            text = text.split()

            if len(text) == 2:
                respons = senddata(data= getdata('setgp','bot') , value=text[1] , namevalue= 'setgp')
                await message.reply_text(f'{respons}')
            else:
                await message.reply_text('لطفا ایدی بعد `setid` بفرستید \n مثال : setid 000000000')


        elif text.startswith('fosh'):

            text = text.split()

            if len(text) == 2 and text[1] == "on":
                time = getdata('time' , 'bot')

                try:
                    time = int(time[0])
                except ValueError:
                    return
                
                this_job = scheduler.get_job(job_id=f"job_fosh")
                if this_job is not None:
                    scheduler.remove_job(job_id=f"job_fosh")
                scheduler.add_job(jobfosh, "interval", seconds= time , id=f"job_fosh" ,args=(getdata('model' , 'bot')[0] , getdata('setgp' , 'bot')[0] , getdata('tag' , 'bot')[0], getdata('setid' , 'bot')[0],getdata('texttag' , 'bot')[0]))
                txt = f"حالت فوش روشن شد"


            elif len(text) == 2 and text[1] == "off":

                this_job = scheduler.get_job(job_id=f"job_fosh")
                if this_job is None:
                    txt = "حالت فوش خاموش بوده است"
                else:
                    scheduler.remove_job(job_id=f"job_fosh")
                    txt = " حالت فوش خاموش شد"

            await message.reply_text(f"{txt}")

        elif text.startswith('attack'):

            text = text.split()

            if len(text) == 2 and text[1] == "on":
                time = getdata('time' , 'bot')

                try:
                    time = int(time[0])
                except ValueError:
                    return
                
                this_job = scheduler.get_job(job_id=f"job_enemi")
                if this_job is not None:
                    scheduler.remove_job(job_id=f"job_enemi")
                scheduler.add_job(jobenemi, "interval", seconds= time , id=f"job_enemi" ,args=(getdata('enchat' , 'bot')[0] , getdata('enmes' , 'bot')[0]))
                txt = f"حالت اتک روشن شد"


            elif len(text) == 2 and text[1] == "off":

                this_job = scheduler.get_job(job_id=f"job_enemi")
                if this_job is None:
                    txt = "حالت اتک خاموش بوده است"
                else:
                    scheduler.remove_job(job_id=f"job_enemi")
                    txt = " حالت اتک خاموش شد"

            await message.reply_text(f"{txt}")

        elif text == 'addfosh':

            
            if message.reply_to_message is not None:

                text = message.reply_to_message.text.replace('\n', '\n')
                cursor.execute("""INSERT INTO listfosh(fosh) VALUES (?)""" , (text,))
                cnx.commit()
                await message.reply_text(f'فوش شما ست شد \n فوش: {text}')
                return
            
            elif message.reply_to_message is not None:
                await message.reply_text('روی متن فوش ریپلای بزن')

        
        elif text == 'delallfosh':
            cursor.execute("DELETE FROM listfosh;")
            cursor.execute('''CREATE TABLE IF NOT EXISTS listfosh(fosh TEXT)''')
            cnx.commit()

            await message.reply_text('تمام فوش های موجود حذف شد')


        elif text.startswith('join'):
            text = text.split()


            if len(text) == 2:
                try:
                    await client.join_chat(text[1])
                    await message.reply("عضو شد", quote=True)
                except errors.FloodWait:
                    await message.reply("اکانت در حال حاضر محدود شده است", quote=True)
                except:
                    await message.reply("نتونست جوین شه", quote=True)
                
        elif text.startswith('left'):
            text = text.split()


            if len(text) == 2:
                try:
                    await client.leave_chat(text[1])
                    await message.reply("لفت دادم", quote=True)
                except errors.FloodWait:
                    await message.reply("اکانت در حال حاضر محدود شده است", quote=True)
                except:
                    await message.reply("نتونست لفت بده", quote=True)
                
            
        elif text.startswith('admin'):
            text = text.split()

            if len(text) == 2:
                    if str(text[1]) not in listadmin:
                        try:
                            time = int(text[1])
                        except ValueError:
                            await message.reply('باید ایدی عددی ادمین رو بدید')
                            return

                        cursor.execute("""INSERT INTO listadmin(admin) VALUES (?)""" , (text[1],))
                        cnx.commit()
                        await message.reply_text(f'کاربر {text[1]} به لیست ادمینا اضافه شد')

                    elif str(text[1]) in listadmin:
                        await message.reply('این ایدی در لیست ادمینها موجود است')
            else:
                await message.reply_text('لطفا ایدی بعد `admin` بفرستید \n مثال : admin 000000000')
        
        elif text.startswith('deladmin'):
            text = text.split()

            if len(text) == 2:
                if str(text[1]) in listadmin:
                    cursor.execute(f"DELETE FROM listadmin WHERE admin = '{text[1]}'")
                    cnx.commit()
                    await message.reply(f"کاربر {text[1]} از لیست ادمینها حذف شد")
                elif str(text[1]) not in listadmin:
                    await message.reply('این ایدی در لیست ادمینها موجود نیست')
            else:
                await message.reply_text('لطفا ایدی بعد `deladmin` بفرستید \n مثال : deladmin 000000000')
        
            
        elif text == 'delalladmin':
            cursor.execute("DELETE FROM listadmin;")
            cursor.execute("""INSERT INTO listadmin(admin) VALUES (?)""" , (admin,))
            cursor.execute('''CREATE TABLE IF NOT EXISTS listadmin(admin TEXT)''')
            cnx.commit()

            await message.reply_text('تمام ادمین های موجود حذف شد')


        elif text == 'listadmin':
            listadmin = '\n'.join(listadmin)


            await message.reply(f"لیست ادمیها \n\n {listadmin}")

        elif text.startswith('setphoto'):

            if message.reply_to_message is not None:
                await message.reply_to_message.download(file_name="image.jpg")
                await client.set_profile_photo(photo=f"/root/@Smorf1bot/bot-spam/downloads/image.jpg") #edit adrres
                await message.reply('عکس با موفقیت تنطیم شد')


            if message.reply_to_message is  None:
                await message.reply('روی عکس مورد نظر ریپلای کن')

        
    
    elif Userid not in listadmin:
        return

scheduler.start()
client.run()
