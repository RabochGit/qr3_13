import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State


state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot("6610080826:AAE21udGfNjihGKmyTrumNvIYjF6SVHEpKc",
                      state_storage=state_storage, parse_mode='Markdown')


class PollState(StatesGroup):
    name = State()
    age = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "👨‍🦰 Об Авторе бота"  # Можно менять текст
text_button_1 = "🔗 Ссылки на автора"  # Можно менять текст


menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)
menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        'Привет! Данный бот тестовый. Пока можно ознакомиться с автором, нажав на кнопку "Об Авторе бота"',  # Можно менять текст
        reply_markup=menu_keyboard)

@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id, 'Итак... Меня зовут Артем. Я из Москвы и мне 17 лет. Учусь в 11 инженерном классе. Сдаю на ЕГЭ: обществознание (привет Насте Маловой), Информатику (Викусь хай👋), Русский ("Грамотным быть модно" - Саня легенда), а также профильную матешу (Турик🤓). В Умскуле (мой любимый мендвежонок💕) я с 2022 года. Пришел в феврале к Алине Максимовой на подготовку к ОГЭ по Английскому и до сих пор не хочу расставаться, так как вы самая лучшая онлайн школа с образовательной лицензией (хех🤣🤣🤣) \n \nТак... Что это я все об учебе и об учебе... Давай отвлечемся от нее хоть на пару минут... Неужели за 1.5 месяца она тебе не наскучила? Если нет, то поздравляю тебя со сломанной психикой😁 А я пожалуй продолжу свой рассказ о себе. \n \nЯ волонтер. Увлекаюсь волонтерской деятельностью уже более 3х лет (с 2020 года). Для меня волонтерство - уже как моя вторая жизнь. Ведь я действительно этим живу😍😍😍 Я являюсь волонтером такого известного проекта как Лига Будущего. Состою в ней уже более года. До этого являлся волонтером ВЦ "Мосволонтер". В моей волонтерской деятельности было очень много разнообразных мероприятияй, перечислю некоторые: "Кубок губернатора. Лига помосковья", "Чемпионат России по триатлону от IronStar", "Велогонка/Велофестиваль LaStrada", "Форум "Путешествуй!" на ВДНХ", "ЗаБег РФ". Если тебе будет интересно, забегай в мой канал по ссылке, которую я расположу в кнопке "Ссылки на автора". Буду очень рад тебя видеть😁 \n \nТак... Со мной познакомились... А тебя как зовут? Очень бы хотел с тобой познакомиться, расскажешь о себе? Как зовут? Чем увлекаешься?')
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id, 'Ого! Не думал, что ты и вправду напишешь о себе. Кстати говоря, красивое имя😍 А сколько тебе говоришь лет?')
    bot.set_state(message.from_user.id, PollState.age, message.chat.id)


@bot.message_handler(state=PollState.age)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['age'] = message.text
    bot.send_message(message.chat.id, 'У тебя самый классный возраст🔥🔥🔥', reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, "Я рад, что я смог тебя заинтересовать таким маленьким своим первым ботом. Если захочешь подружиться, то оставляю свои links тут😉 \n \n*ВК* - vk.com/temamosvol \n \n*TG* - @temamosvol \n\n*Мой тгк* - https://t.me/+OHle3JRUFNM0NGNi \n \nДо новых встреч!💕💕💕", reply_markup=menu_keyboard)  # Можно менять текст


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()