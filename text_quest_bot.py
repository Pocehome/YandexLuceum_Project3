import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id


def write_msg(user_id, message, keyboard):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": get_random_id(),
                                'keyboard': keyboard})


def create_quest_keyboard(*args):
    keyboard = vk_api.keyboard.VkKeyboard(one_time=True)
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

    # elif stage == 3:
    #     # write_msg(event.user_id, 'Вы оказываетесь в пещере.', create_empty_keyboard())
    #     # write_msg(event.user_id, 'Посередине находится озеро и на его дне вы видите ключ.', create_empty_keyboard())
    #     write_msg(event.user_id, 'Также на другом его берегу вы замечаете дверь.',
    #               create_quest_keyboard('Нырнуть за ключом', 'Попробовать открыть дверь'))

    # elif stage == 4:
    #     # write_msg(event.user_id, 'Вы оказываетесь в пещере.', create_empty_keyboard())
    #     # write_msg(event.user_id, 'Посередине находится озеро и на его дне вы видите ключ.', create_empty_keyboard())
    #     write_msg(event.user_id, 'Также на другом его берегу вы замечаете дверь.',
    #               create_quest_keyboard('Нырнуть за ключом', 'Попробовать открыть дверь'))

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


token = "cfd06f1308c729bb30731feb2d509fb532db16684c1f70f46f8fe4b86fb505ccd98ee4bb0258a9c3eff80"
quest_mode = False
quest_stage = 0
answer_continue = False
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text.lower()
            if request in ['квест', 'quest', 'текстовый квест']:  # текстовый квест
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

                # elif request == 'пойти в дверь №3' and quest_stage == 0:
                #     quest_stage = 3
                #     quest(event.user_id, quest_stage)
                # elif request == 'пойти в дверь №4' and quest_stage == 0:
                #     quest_stage = 4
                #     quest(event.user_id, quest_stage)

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

            elif request == "привет":
                write_msg(event.user_id, "Хай", create_empty_keyboard())
            elif request == "пока":
                write_msg(event.user_id, "Пока((", create_empty_keyboard())
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...", create_empty_keyboard())
