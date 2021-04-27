import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import requests
from wikipedia import wikipedia

from aut_reg_sl import aut_reg_sl

token = "cfd06f1308c729bb30731feb2d509fb532db16684c1f70f46f8fe4b86fb505ccd98ee4bb0258a9c3eff80"
access_token = '7f5fd4918b0c688c6d54c60a008b1bc775ca469cb5549b502a9aa3e570b36997357e5eb3462e6b009ecba'
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message, keyboard):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": get_random_id(),
                                'keyboard': keyboard})


def create_help_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)

    keyboard.add_button("Калькулятор", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Погода", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Текстовый квест", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("Wiki", color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Регион регистрации автомобиля", color=VkKeyboardColor.PRIMARY)

    return keyboard.get_keyboard()


def create_quest_keyboard(*args):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    if len(args) <= 2:
        for i, el in enumerate(args):
            if i != 0:
                keyboard.add_line()
            keyboard.add_button(el, color=VkKeyboardColor.PRIMARY)
    elif 2 < len(args) <= 4:
        for i, el in enumerate(args):
            if i % 2 == 0 and i != 0:
                keyboard.add_line()
            keyboard.add_button(el, color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()


def create_answer_keyboard(green, red):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)

    keyboard.add_button(green, color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(red, color=VkKeyboardColor.NEGATIVE)

    return keyboard.get_keyboard()


def create_empty_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard.get_empty_keyboard()

    return keyboard


def kalk(us_id, request):
    try:
        otv = eval(request)
        write_msg(us_id, otv, create_empty_keyboard())
    except Exception:
        write_msg(us_id, 'Ошибка в вводе запроса.', create_empty_keyboard())


def find_aut_reg(us_id, reg_num):
    try:
        reg_num = int(reg_num)
        region = aut_reg_sl[reg_num]
        write_msg(us_id, region, create_empty_keyboard())
    except ValueError:
        write_msg(us_id, 'Ошибка в вводе запроса. Используйте только цифры.', create_empty_keyboard())
    except KeyError:
        write_msg(us_id, 'Такого региона нет в нашей базе данных.', create_empty_keyboard())


def like_statistics(user_id):
    owner_id = '-204097194'
    posts_jason = requests.get('https://api.vk.com/method/wall.get',
                               params={'access_token': access_token,
                                       'v': '5.130',
                                       'owner_id': owner_id
                                       })
    posts_list = posts_jason.json()['response']['items']
    posts_id = []
    count_likes = 0
    for i in range(len(posts_list)):
        posts_id.append(int(posts_jason.json()['response']['items'][i]['id']))
    for post in posts_id:
        try:
            post_maybe_like = requests.get('https://api.vk.com/method/likes.isLiked',
                                           params={'user_id': user_id,
                                                   'type': 'post',
                                                   'owner_id': owner_id,
                                                   'item_id': post,
                                                   'access_token': access_token,
                                                   'v': '5.130'
                                                   })
            result_post_maybe_like = post_maybe_like.json()
            result_post_maybe_like = result_post_maybe_like['response']["liked"]
            if result_post_maybe_like == 1:
                count_likes += 1
        except:
            continue
    return count_likes


def quest(us_id, stage):
    if stage == 0:
        write_msg(us_id, 'Вы просыпаетесь в холодной каменной комнате.', create_empty_keyboard())
        write_msg(us_id, 'Она хорошо освещена, но источника света нигде не видно.',
                  create_empty_keyboard())
        write_msg(us_id, 'Также вы видите две двери.',
                  create_quest_keyboard('Пойти в дверь №1', 'Пойти в дверь №2'))

    elif stage == 1:
        write_msg(us_id, 'Вы оказываетесь в новой комнате.', create_empty_keyboard())
        write_msg(us_id, 'Посередине неё стоит стол а на нём бутылочка с зелёной жидкостью.',
                  create_empty_keyboard())
        write_msg(us_id, 'На пузырьке этикетка с надписью: "Выпей меня".', create_empty_keyboard())
        write_msg(us_id, 'Также в комнате вы замечаете небольшую дверцу у самого пола.',
                  create_quest_keyboard('Выпить из пузырька', 'Попробовать протиснуться в дверцу'))

    elif stage == 2:
        write_msg(us_id, 'Вы оказываетесь в пещере.', create_empty_keyboard())
        write_msg(us_id, 'Посередине находится озеро и на его дне вы видите ключ.', create_empty_keyboard())
        write_msg(us_id, 'Также на другом его берегу вы замечаете дверь.',
                  create_quest_keyboard('Нырнуть за ключом', 'Попробовать открыть дверь'))

    elif stage == 5:
        write_msg(us_id, 'Вы выпиваете из пузырька и замечаете, как вокруг вас всё начинает расти.',
                  create_empty_keyboard())
        write_msg(us_id, 'Затем вы понимаете, что это не всё выросло, а вы уменьшились.',
                  create_empty_keyboard())
        write_msg(us_id, 'Теперь вы запросто можете пройти в дверь, что вы и делаете.',
                  create_empty_keyboard())
        write_msg(us_id, 'Поздравляем, вы на свободе!!!',
                  create_answer_keyboard('Начать с начала', 'Закончить'))

    elif stage == 6:
        write_msg(us_id, 'Вы просовываете в дверь голову и видите за ней солнце. Похоже, что это выход.',
                  create_empty_keyboard())
        write_msg(us_id, 'Пролезая дальше вы высовываетесь до пояса, но понимаете, что вы застряли.',
                  create_empty_keyboard())
        write_msg(us_id, 'Влезть назад у вас не получается тоже. Видимо вы обречены лежать в таком положении '
                         'пока не станете тоньше.', create_empty_keyboard())
        write_msg(us_id, '...', create_empty_keyboard())
        write_msg(us_id, 'Спустя неделю вынужденной голодовки вы, наконец, смогли вылезти. Вам ещё повезло, что'
                         ' за это время несколько раз шёл дождь, что не дало вам умереть от жажды.',
                  create_empty_keyboard())
        write_msg(us_id, 'Поздравляем, вы на свободе!', create_answer_keyboard('Начать с начала', 'Закончить'))

    elif stage == 7:
        write_msg(us_id, 'Вы ныряете за ключом на самое дно озера.', create_empty_keyboard())
        write_msg(us_id, 'Как только вы подплываете к ключу, на дне открывается люк и вас засасывает в него '
                         'потоком воды.', create_empty_keyboard())
        write_msg(us_id, 'Вы оказываетесь в новой пещере полностью заполненной водой и замечаете, как к вам '
                         'подплавает русалка.', create_empty_keyboard())
        write_msg(us_id, 'Она касается вас своим хвостом и вы понимаете, что больше не задыхаетесь.'
                         'Теперь у вас есть жабры, хвост и новая подруга с которой вы и остаётесь здесь.',
                  create_empty_keyboard())
        write_msg(us_id, 'Поздравляем, вы теперь русалка!!!',
                  create_answer_keyboard('Начать с начала', 'Закончить'))

    elif stage == 8:
        write_msg(us_id, 'Вы подходите к двери, толкаете её, и она открывается.', create_empty_keyboard())
        write_msg(us_id, 'За ней вы видите озарённую ярким солнцем полянкую Похоже, вы выбрались!.',
                  create_empty_keyboard())
        write_msg(us_id, 'Это было даже слишком легко.', create_empty_keyboard())
        write_msg(us_id, 'Поздравляем, вы на свободе!!!',
                  create_answer_keyboard('Начать с начала', 'Закончить'))


def weather(us_id, request):
    city = request
    api_key = "34dee3a9ad750d39dfc67882b22c42f5"
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&type=like&" + "DE&appid=" + api_key
    response = requests.get(url)
    weather_data = response.json()
    if "message" in weather_data:
        if weather_data["message"] == "city not found":
            write_msg(us_id, "Извините, но такой город не найден. Просьба проверить прописание вашего города.",
                      create_empty_keyboard())
    else:
        general = ""
        weather_json_request = weather_data["weather"][0]

        # общее представление о погоде
        if weather_json_request["main"] == "Rain":
            general = "Идёт дождь"
        elif weather_json_request["main"] == "Clouds":
            general = "Облачно"
        elif weather_json_request["main"] == "Clear":
            general = "Солнечно"
        elif weather_json_request["main"] == "Thunderstorm":
            general = "Гроза"

        main_data = weather_data["main"]

        # температура
        kelvin_temp = main_data["temp"]
        delta = 273.15
        celsius_temp = round(kelvin_temp - delta)
        temp_answer = ", температура: " + str(celsius_temp) + "°, "

        # ветер
        wind = weather_data["wind"]
        wind_speed = wind["speed"]
        if "deg" in wind:
            wind_deg = wind["deg"]

            if wind_deg < 23:
                direction = "северное"
            elif wind_deg < 68:
                direction = "северо-восточное"
            elif wind_deg < 113:
                direction = "восточное"
            elif wind_deg < 158:
                direction = "юго-восточное"
            elif wind_deg < 203:
                direction = "южное"
            elif wind_deg < 248:
                direction = "юго-западное"
            elif wind_deg < 293:
                direction = "западное"
            elif wind_deg < 338:
                direction = "cеверо-западное"
            else:
                direction = "северное"

            wind_mess = "скорость ветра: " + str(wind_speed) + " м/с, направление: " + direction

            # влажность
            humidity = main_data["humidity"]
            answer_humidity = ", влажность воздуха: " + str(humidity) + "%"

            # формирование итогового ответа
            answer = general + temp_answer + wind_mess + answer_humidity + '.'
            write_msg(us_id, answer, create_empty_keyboard())

        else:
            wind_mess = "скорость ветра: " + str(wind_speed) + "м/с"
            humidity = main_data["humidity"]
            answer_humidity = ", влажность воздуха: " + str(humidity) + "%"
            answer = general + temp_answer + wind_mess + answer_humidity + '.'
            write_msg(us_id, answer, create_empty_keyboard())
            write_msg(us_id, "Введите название города, погоду в котором вы хотите узнать.", create_empty_keyboard())


def wiki_response(request_text):
    try:
        txt = str(wikipedia.page(request_text).content[:1000])
    except Exception:
        txt = 'По данному запросу ничего не найдено.'
    return txt


def wiki_search(us_id, request):
    write_msg(us_id, f"{wiki_response(request)}\n\n{'О чём мне спросить у Википедии?'}", create_empty_keyboard())


def main():
    kalk_mode = False
    aut_reg_mode = False
    quest_mode = False
    weather_mode = False
    wiki_mode = False
    quest_stage = 0
    answer_quest_continue = False
    wikipedia.set_lang('ru')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text.lower()

                if request in ['stop', 'стоп']:  # остановить все режимы
                    kalk_mode = False
                    aut_reg_mode = False
                    quest_mode = False
                    weather_mode = False
                    wiki_mode = False
                    write_msg(event.user_id, 'Все режимы остановленны.', create_empty_keyboard())

                elif request in ["что ты можешь", 'помощь', 'help']:
                    write_msg(event.user_id, "Вот, что я могу:", create_help_keyboard())

                elif request in ['калькулятор', 'kalk'] and not wiki_mode:  # Калькулятор
                    kalk_mode = not kalk_mode
                    if kalk_mode:

                        aut_reg_mode = False
                        quest_mode = False
                        weather_mode = False
                        wiki_mode = False

                        write_msg(event.user_id, 'Режим калькулятор запущен.', create_empty_keyboard())
                        write_msg(event.user_id,
                                  "Введите выражение. Используйте знаки из допустимого списка: "
                                  "+, -, *, /, **, (, ), %, //. Для остановки режима введите 'stop', 'стоп' "
                                  "или слово, использованное для старта.",
                                  create_empty_keyboard())
                    else:
                        write_msg(event.user_id, 'Режим калькулятор остановлен.', create_empty_keyboard())

                elif request in ['регион', 'aut_reg', 'номер'] and not wiki_mode:  # Регион регистрации автомобиля
                    aut_reg_mode = not aut_reg_mode
                    if aut_reg_mode:

                        kalk_mode = False
                        quest_mode = False
                        weather_mode = False
                        wiki_mode = False

                        write_msg(event.user_id,
                                  "Режим поиска региона регистрации автомобиля запущен. "
                                  "Для остановки режима введите 'stop', 'стоп' или слово, использованное для старта.",
                                  create_empty_keyboard())
                        write_msg(event.user_id, "Введите номер региона. Исспользуйте только цифры.",
                                  create_empty_keyboard())
                    else:
                        write_msg(event.user_id, 'Режим поиска региона регистрации автомобиля остановлен.',
                                  create_empty_keyboard())

                elif request in ['квест', 'quest', 'текстовый квест'] and not wiki_mode:  # текстовый квест
                    quest_mode = not quest_mode
                    if quest_mode:

                        kalk_mode = False
                        aut_reg_mode = False
                        weather_mode = False
                        wiki_mode = False

                        write_msg(event.user_id, "Режим текстового квеста запущен. Для остановки режима введите "
                                                 "'stop', 'стоп' или слово, использованное для старта.",
                                  create_empty_keyboard())

                        if quest_stage != 0:
                            write_msg(event.user_id, 'Хотите продолжить с момента, на котором остановились?',
                                      create_answer_keyboard('Да', 'Нет'))
                            answer_quest_continue = True
                            continue

                        quest(event.user_id, quest_stage)
                    else:
                        write_msg(event.user_id, 'Режим текстового квеста остановлен.', create_empty_keyboard())

                elif request in ['погода', 'weather'] and not wiki_mode:  # погода
                    weather_mode = not weather_mode
                    if weather_mode:

                        kalk_mode = False
                        aut_reg_mode = False
                        quest_mode = False
                        wiki_mode = False

                        write_msg(event.user_id,
                                  "Режим погода запущен. "
                                  "Для остановки режима введите 'stop', 'стоп' или слово, использованное для старта.",
                                  create_empty_keyboard())
                        write_msg(event.user_id, "Введите название города, погоду в котором вы хотите узнать.",
                                  create_empty_keyboard())
                    else:
                        write_msg(event.user_id, 'Режим погода остановлен.', create_empty_keyboard())

                elif request == 'wiki' or request == 'поиск':  # поиск в wikipedia
                    wiki_mode = not wiki_mode
                    if wiki_mode:

                        kalk_mode = False
                        aut_reg_mode = False
                        quest_mode = False
                        weather_mode = False

                        write_msg(event.user_id,
                                  "Режим wikipedia запущен. "
                                  "Для остановки режима введите 'stop', 'стоп' или слово, использованное для старта.",
                                  create_empty_keyboard())
                        write_msg(event.user_id, "Введите ваш запрос:",
                                  create_empty_keyboard())
                    else:
                        write_msg(event.user_id, 'Режим wikipedia остановлен.', create_empty_keyboard())

                elif kalk_mode:
                    kalk(event.user_id, request)

                elif aut_reg_mode:
                    find_aut_reg(event.user_id, request)

                elif quest_mode:
                    if answer_quest_continue is True:
                        answer_quest_continue = False
                        if request == 'да':
                            quest(event.user_id, quest_stage)
                        elif request == 'нет':
                            quest_stage = 0
                            quest(event.user_id, quest_stage)

                    elif request == 'пойти в дверь №1' and quest_stage == 0:
                        quest_stage = 1
                        quest(event.user_id, quest_stage)

                    elif request == 'пойти в дверь №2' and quest_stage == 0:
                        quest_stage = 2
                        quest(event.user_id, quest_stage)

                    elif request == 'выпить из пузырька' and quest_stage == 1:
                        quest_stage = 5
                        quest(event.user_id, quest_stage)

                    elif request == 'попробовать протиснуться в дверцу' and quest_stage == 1:
                        quest_stage = 6
                        quest(event.user_id, quest_stage)

                    elif request == 'нырнуть за ключом' and quest_stage == 2:
                        quest_stage = 7
                        quest(event.user_id, quest_stage)

                    elif request == 'попробовать открыть дверь' and quest_stage == 2:
                        quest_stage = 8
                        quest(event.user_id, quest_stage)

                    elif request == 'начать с начала':
                        quest_stage = 0
                        quest(event.user_id, quest_stage)

                    elif request == 'закончить':
                        quest_stage = 0
                        quest_mode = False
                        write_msg(event.user_id, 'Режим текстового квеста остановлен.', create_empty_keyboard())

                elif weather_mode:
                    weather(event.user_id, request)

                elif wiki_mode:
                    wiki_search(event.user_id, request)

                # общение с пользователем
                elif request == "статистика":
                    write_msg(event.user_id,
                              "Вы поставили нашим постам {} лайков".format(str(like_statistics(event.user_id))), create_empty_keyboard())
                elif request == "привет" or request == 'hello':
                    write_msg(event.user_id, "Здравствуйте.", create_empty_keyboard())

                elif request == "пока" or request == 'goodbye':
                    write_msg(event.user_id, "До свидания.", create_empty_keyboard())

                else:
                    write_msg(event.user_id, "Не понимаю вашего ответа... Если нужна помощь введите 'help' "
                                             "или 'помощь'.", create_quest_keyboard('Help'))


if __name__ == '__main__':
    main()
