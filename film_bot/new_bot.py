import conf
from conf import TOKEN
import sqlite3
import flask
import csv
import telebot
import random
from telebot import types
import requests
import sqlite3

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)
bot = telebot.TeleBot(TOKEN, threaded = False)
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

gen_id = 0
gen_film_slogan = ''
pictures = ['Амели.jfif', "Достучаться до небес.jfif", "Интерстеллар.jfif", "Побег из Шоушенка.jfif", 'Бесславные ублюдки.jfif', 'Бэтмен темный рыцарь.jpg', 'Грань будущего.jfif', 'Достучаться до небес.jfif', 'Дурак.png', 'Дьявол носит Prada.jfif', 'Жизнь Пи.jfif', 'Интерстеллар.jfif', 'Искупление.jfif', 'Криминальное чтиво.jfif', 'Леон.jpg', 'Люди в черном.jfif', 'Матрица.jpg', 'Остров проклятых.jpg', 'Побег из Шоушенка.jfif', 'Список Шиндлера.jfif', 'Форест Гамп.jpg', 'Человек дождя.jfif', 'Шерлок Холмс.jfif', '12 друзей Оушена.jpg', '12 лет рабства.jpg', 'Ford против Ferrari.jfif']
gen_film_picture = ''
send_pic = False
send_slogan = False

@bot.message_handler(commands=["start", "help"])
def say_hello(message):
    bot.send_message(message.chat.id, "Привет! Я - бот, который присылает тебе слоганы или кадры из фильмов, а ты должен отгадать, из какого он фильма. Отправь команду /send_slogan или /send_picture")

@bot.message_handler(commands=["send_picture"])
def send(message):
    global gen_film_picture, send_pic, send_slogan
    send_pic = True
    send_slogan = False
    rand_pic = random.choice(pictures)
    photo = open(rand_pic, 'rb')
    ind = rand_pic.index('.')
    gen_film_picture = rand_pic[:ind]
    bot.send_photo(message.chat.id, photo)

@bot.message_handler(commands=["send_slogan"])
def send_sticker(message):
    global send_slogan, send_pic, gen_id, gen_film_slogan
    send_slogan = True
    send_pic = False
    con = sqlite3.connect('films.db')
    cur = con.cursor()
    import random
    con = sqlite3.connect('films.db')
    cur = con.cursor()
    tom_hanks_query = """
    SELECT slogans.film_id, film, send_slogan
    FROM slogans
        JOIN genres ON slogans.film_id = genres.film_id"""
    cur.execute(tom_hanks_query)
    data = cur.fetchall()
    dlina = 65
    rand_data = ''
    while dlina > 64:
        rand_data = random.choice(data)
        dlina = len(rand_data[1].encode('utf-8'))
    rand_slogan = rand_data[2]
    rand_id = rand_data[0]
    gen_id = rand_id
    rand_film = rand_data[1]
    gen_film_slogan = rand_film[:-6]
    bot.send_message(message.chat.id, rand_slogan)
    bot.send_message(message.chat.id, 'Если хочешь подсказку, пришли команду /send_clue')

@bot.message_handler(commands=["send_clue"])
def say_clue(message):
    global gen_id, gen_film_slogan
    new_names_id = []
    films_id = []
    con = sqlite3.connect('films.db')
    cur = con.cursor()
    slogans_query = """
    SELECT slogans.film_id, film, send_slogan
    FROM slogans"""
    cur.execute(slogans_query)
    slogans_data = cur.fetchall()
    genres_query = """
    SELECT genres.film_id, genre
    FROM genres
    """
    cur.execute(genres_query)
    genres_data = cur.fetchall()
    names = []
    new_data = []
    for d in slogans_data:
        new_data.append(d)
    for d in slogans_data:
        if len(d[1].encode('utf-8')) < 64:
            new_names_id.append(d[0])
    for d in genres_data:
        if d[0] == gen_id:
            genre = d[1]
    for d in genres_data:
        if genre == 'криминал':
            genre == 'боевик'
        if genre == 'ужасы':
            genre = 'фантастика'
        if genre == 'приключения':
            genre == 'боевик'
        if d[1] == genre and gen_id != d[0] and d[0] in new_names_id:
            films_id.append(d[0])
    ids = random.sample(films_id, 3)
    for i in ids:
        for d in new_data:
            if i == d[0]:
                names.append(d[1][:-6])
                break
    names.append(gen_film_slogan)
    for name in names:
        if ':' in name:
            ind = names.index(name)
            names[ind] = name.replace(':', '')
        if '—' in name:
            ind = names.index(name)
            names[ind] = name.replace(':', '')
    random.shuffle(names)
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text= names[0], callback_data= names[0])
    button2 = types.InlineKeyboardButton(text= names[1], callback_data= names[1])
    button3 = types.InlineKeyboardButton(text= names[2], callback_data= names[2])
    button4 = types.InlineKeyboardButton(text= names[3], callback_data= gen_film_slogan)
    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    keyboard.add(button4)
    bot.send_message(message.chat.id, "Выбери из этих вариантов", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global gen_film_slogan, send_slogan

    if call.message:         
        if call.data == gen_film_slogan:
            bot.send_message(call.message.chat.id, "Правильно!")
        else:
            bot.send_message(call.message.chat.id, "Нет, это " + gen_film_slogan)
        send_slogan = False
        bot.send_message(call.message.chat.id, "Отправь /send_slogan или /send_picture")

@bot.message_handler(content_types=['text'])
def answer(message):
    global gen_film_slogan, gen_film_picture
    global send_pic, send_slogan

    if send_slogan == True:
        if message.text != '/send_clue':
            if message.text in gen_film_slogan:
                bot.send_message(message.chat.id, "Правильно!")
            else:
                mes = "Нет, это " + gen_film_slogan
                bot.send_message(message.chat.id, mes)
            send_slogan = False
    if send_pic == True:
        if message.text == gen_film_picture:
            bot.send_message(message.chat.id, "Правильно!")
        else:
            mes = "Нет, это " + gen_film_picture
            bot.send_message(message.chat.id, mes)
        send_pic = False
    bot.send_message(message.chat.id, "Отправь /send_slogan или /send_picture")

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)
