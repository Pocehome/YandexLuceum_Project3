import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id


def write_msg(user_id, message, keyboard):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": get_random_id(),
                                'keyboard': keyboard})


def create_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)
    # False Если клавиатура должна оставаться откртой после нажатия на кнопку
    # True если она должна закрваться

    keyboard.add_button("9", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("8", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()  # Обозначает добавление новой строки
    keyboard.add_button("7", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("/", color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()


def create_empty_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard.get_empty_keyboard()

    return keyboard


def kalk(event, request):
    try:
        otv = eval(request)
        write_msg(event.user_id, otv, create_empty_keyboard())
    except Exception:
        write_msg(event.user_id, 'Ошибка в вводе запроса.', create_empty_keyboard())


token = "cfd06f1308c729bb30731feb2d509fb532db16684c1f70f46f8fe4b86fb505ccd98ee4bb0258a9c3eff80"
kalk_mode = False
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text.lower()
            if request == 'калькулятор' or request == 'kalk':
                kalk_mode = not kalk_mode
                if kalk_mode:
                    write_msg(event.user_id, 'Режим калькулятор запущен.', create_empty_keyboard())
                    write_msg(event.user_id,
                              "Введите выражение. Используйте знаки из допустимого списка: +, -, *, "
                              "/, **, (, ), %, //.", create_empty_keyboard())
                else:
                    write_msg(event.user_id, 'Режим калькулятор остановлен.', create_empty_keyboard())
            elif kalk_mode:
                kalk(event, request)
            elif request == "привет":
                write_msg(event.user_id, "Хай", create_empty_keyboard())
            elif request == "пока":
                write_msg(event.user_id, "Пока((", create_empty_keyboard())
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...", create_empty_keyboard())
