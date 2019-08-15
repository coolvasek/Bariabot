import sqlalchemy
import telebot
import sqlAlc
import init_add
from init_add import Shop

from sqlalchemy.ext.declarative import declarative_base


error_in_input = 0;
msg_id =0;
error = "";
shop = Shop();

bot = telebot.TeleBot('729545618:AAGZsGxniK2HBrLtliLzhfwg48GAZgL4b7E')

@bot.message_handler(commands=['start'])
def start_message(message):
    #bot.send_message(message.chat.id, 'Привет, ты написал мне /start')
    bot.send_message(message.chat.id, ' Я бот-помощник по открытию нового магазина!');
    bot.send_message(message.chat.id, ' Давайте заполним заявку на открытие магазина. Напишите /reg');
    init_add();

def get_name(message): #получаем фамилию
    shop.name = message.text;
    bot.send_message(message.chat.id, 'Ваш номер телефона?');
    bot.register_next_step_handler(message, get_tel);

def get_tel(message):
    shop.tel = message.text;
    bot.send_message(message.chat.id, 'Напишите полный адрес объекта');
    bot.register_next_step_handler(message, get_adress);


def get_adress(message):
    shop.adress = message.text;
    #add(message);
    keyboard = telebot.types.InlineKeyboardMarkup()
    global error_in_input;
    global msg_id;
    error_in_input = 1;
    kb1 = telebot.types.InlineKeyboardButton(text="Помещение", callback_data="Помещение")
    kb2 = telebot.types.InlineKeyboardButton(text="З. участок", callback_data="Зем. участок")
    kb3 = telebot.types.InlineKeyboardButton(text="Отд. здание", callback_data="Отд. здание")
    keyboard.add(kb1, kb2, kb3)
    msg = bot.send_message(message.chat.id, "Выберите тип своего объекта:", reply_markup=keyboard)
    error_in_input = 1;
    global msg_id;
    msg_id = msg.message_id;


    @bot.callback_query_handler(func=lambda c: True)
    def ans(c):
        cid = c.message.chat.id
        keyboard = telebot.types.InlineKeyboardMarkup()
        bot.send_message(cid, " \" " + str.upper(c.data) +" \" ", reply_markup=keyboard)
        #bot.delete_message(message.chat.id, msg_id);
        #bot.edit_message_reply_markup(chatid=message.chat.id, message_id= msg_id)
        try:
            bot.edit_message_reply_markup(message.chat.id, msg_id, reply_markup=keyboard);
        except:
            error = "Ошибка обработки ввода";

        if (c.data in ["Помещение","Отд. здание"]):
            bot.send_message(message.chat.id, 'Напишите общую площадь ');
            shop.type = message.text;
            add(message);
            bot.register_next_step_handler(message, get_square);
        elif c.data == "Зем. участок":
            get_count_room(message);
        elif (c.data in ["1 зал","2 зала","3 зала", "более 3 залов"]):
            bot.send_message(message.chat.id, "Напишите количество парквочных мест");
            bot.register_next_step_handler(message, get_parking);
        elif (c.data in ["1 этаж","2 этаж","3 этаж"]):
            get_height(message);
        elif (c.data in ["Да","Нет"]):
            get_second_floor(message);
        elif (c.data in ["Да ","Нет "]):
            get_count_room(message);
        elif (c.data in ["Да  ","Нет  "]):
            bot.send_message(message.chat.id, "Спасибо!");

def get_square(message):
    global square;
    square = message.text;
    bot.send_message(message.chat.id, 'Напишите ТОРГОВУЮ площадь ');
    bot.register_next_step_handler(message, get_square_sell);

def get_square_sell(message):
    global square_sell;
    square_sell = message.text;
    get_floor(message);


def get_count_room(message):
    global error_in_input;
    keyboard = telebot.types.InlineKeyboardMarkup()
    kb1 = telebot.types.InlineKeyboardButton(text="  1 зал ", callback_data="1 зал")
    kb2 = telebot.types.InlineKeyboardButton(text="  2 зала  ", callback_data="2 зала")
    kb3 = telebot.types.InlineKeyboardButton(text="  3 зала ", callback_data="3 зала")
    kb4 = telebot.types.InlineKeyboardButton(text="  более 3  ", callback_data="более 3 залов")

    keyboard.add(kb1, kb2, kb3, kb4)
    error_in_input = 2;
    msg = bot.send_message(message.chat.id, "Выберите количество торговых залов:", reply_markup=keyboard)
    global msg_id;
    msg_id = msg.message_id;

def get_parking(message):
    global parking;
    parking = message.text;
    bot.send_message(message.chat.id, 'Укажите стоимость аренды ');
    bot.register_next_step_handler(message, get_rent);

def  get_floor(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    kb1 = telebot.types.InlineKeyboardButton(text="  1  ", callback_data="1 этаж")
    kb2 = telebot.types.InlineKeyboardButton(text="  2  ", callback_data="2 этаж")
    kb3 = telebot.types.InlineKeyboardButton(text="  3  ", callback_data="3 этаж")
    keyboard.add(kb1, kb2, kb3)
    msg = bot.send_message(message.chat.id, "Выберите этаж торгового зала:", reply_markup=keyboard)
    global msg_id;
    msg_id = msg.message_id;

def  get_height(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    kb1 = telebot.types.InlineKeyboardButton(text="  Да  ", callback_data="Да")
    kb2 = telebot.types.InlineKeyboardButton(text="  Нет  ", callback_data="Нет")
    keyboard.add(kb1, kb2)
    msg = bot.send_message(message.chat.id, "Расположение торговых залов на разных уровнях высоты?", reply_markup=keyboard)
    global msg_id;
    msg_id = msg.message_id;

def  get_second_floor(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    kb1 = telebot.types.InlineKeyboardButton(text="  Да  ", callback_data="Да ")
    kb2 = telebot.types.InlineKeyboardButton(text="  Нет  ", callback_data="Нет ")
    keyboard.add(kb1, kb2)
    msg = bot.send_message(message.chat.id, "Расположение торгового зала на 2 этаже?", reply_markup=keyboard)
    global msg_id;
    msg_id = msg.message_id;

def get_rent(message):
    global rent;
    rent = message.text;
    bot.send_message(message.chat.id, 'Приложите фото');
    bot.register_next_step_handler(message, get_photo);

def get_photo(message):
    global rent;
    rent = message.text;
    bot.send_message(message.chat.id, 'Напишите краткий комментарий к заявке');
    bot.register_next_step_handler(message, get_comment);

def get_comment(message):
    global rent;
    rent = message.text;
    bot.send_message(message.chat.id, 'Отправлю вашу заявку на рассмотрение!');
    bot.send_message(message.chat.id, 'Приятного дня!');
    add(message);


def  get_question(message):
    global error_in_input;
    keyboard = telebot.types.InlineKeyboardMarkup()
    kb1 = telebot.types.InlineKeyboardButton(text="  Да  ", callback_data="Да  ")
    kb2 = telebot.types.InlineKeyboardButton(text="  Нет  ", callback_data="Нет  ")
    keyboard.add(kb1, kb2)
    error_in_input = 0;
    msg = bot.send_message(message.chat.id, "Я решил ваш вопрос?", reply_markup=keyboard)
    global msg_id;
    msg_id = msg.message_id;
    #bot.send_sticker(message.chat.id, 'CAADAgADZgkAAnlc4gmfCor5YbYYRAI')



@bot.message_handler(content_types=['text', 'photo'])

def start(message):
    global error_in_input;
    if message.text == '/reg':
        bot.send_message(message.chat.id, "Как вас зовут? Напишите ФИО");


        error_in_input == 0;

        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name

    elif error_in_input == 1:
        get_count_room(message);
    elif error_in_input == 2:
        bot.send_message(message.chat.id, "Напишите количество парквочных мест");
        bot.register_next_step_handler(message, get_parking);

    else:
        bot.send_message(message.chat.id, ' Привет! Я бот-помощник по открытию нового магазина!');
        bot.send_message(message.chat.id, ' Давайте заполним заявку на открытие магазина. Напишите /reg');

def add(message):
    from init_add import Shop
    #shop = Shop(name="Hello World!", tel=2)
    #shop = Shop(address="addr")

    init_add.add(shop, session);
    bot.send_message(message.chat.id, ' Заявка отправлена в БД ');
    get_question(message);


session = init_add.init();



bot.polling(none_stop=True)
