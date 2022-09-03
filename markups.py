from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btnProfile = KeyboardButton('😼ПРОФИЛЬ')
btnSub = KeyboardButton('❤️ПОДПИСКА')
btnChk = KeyboardButton('💳ПРОВЕРКА СС')

mainMenu = ReplyKeyboardMarkup(resize_keyboard= True)
mainMenu.add(btnProfile, btnSub, btnChk)

btnSubDay = InlineKeyboardButton(text="🤨1 ДЕНЬ", callback_data="subday")
#btnSubWeek = InlineKeyboardButton(text="😼7 ДНЕЙ", callback_data="subweek")
#btnSubMonth = InlineKeyboardButton(text="🥵30 ДНЕЙ", callback_data="submonth")
submenu = InlineKeyboardMarkup(row_width=1)
submenu.add(btnSubDay)

def buy_menu(isUrl=True, url="", bill=""):
    qiwiMenu = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        btnUrlQIWI = InlineKeyboardButton(text="Ссылка на оплату", url=url)
        qiwiMenu.insert(btnUrlQIWI)

    btnCheckQIWI = InlineKeyboardButton(text="Проверить оплату", callback_data="check_" + bill)
    qiwiMenu.insert(btnCheckQIWI)
    return qiwiMenu
