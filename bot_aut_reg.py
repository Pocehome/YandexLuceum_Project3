import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from aut_reg_sl import aut_reg_sl


def write_msg(user_id, message, keyboard):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": get_random_id(),
                                'keyboard': keyboard})


def create_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard(one_time=False)

    keyboard.add_button("9", color=VkKeyboardColor.POSITIVE)
    keyboard.add_button("8", color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()  # Обозначает добавление новой строки
    keyboard.add_button("7", color=VkKeyboardColor.PRIMARY)
    keyboard.add_button("/", color=VkKeyboardColor.SECONDARY)

    return keyboard.get_keyboard()


def create_empty_keyboard():
    keyboard = vk_api.keyboard.VkKeyboard.get_empty_keyboard()
    return keyboard


def find_aut_reg(reg_num):
    try:
        reg_num = int(reg_num)
        region = aut_reg_sl[reg_num]
        write_msg(event.user_id, region, create_empty_keyboard())
    except ValueError:
        write_msg(event.user_id, 'Ошибка в вводе запроса. Используйте только цифры.', create_empty_keyboard())
    except KeyError:
        write_msg(event.user_id, 'Такого региона нет в нашей базе данных.', create_empty_keyboard())


token = "cfd06f1308c729bb30731feb2d509fb532db16684c1f70f46f8fe4b86fb505ccd98ee4bb0258a9c3eff80"
aut_reg_mode = False
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text.lower()
            if request == "Регион регистрации автомобиля" or request == 'aut_reg':
                aut_reg_mode = not aut_reg_mode
                if aut_reg_mode:
                    write_msg(event.user_id, 'Режим поиска региона регистрации автомобиля запущен.',
                              create_empty_keyboard())
                    write_msg(event.user_id, "Введите номер региона. Исспользуйте только цифры.",
                              create_empty_keyboard())
                else:
                    write_msg(event.user_id, 'Режим поиска региона регистрации автомобиля остановлен.',
                              create_empty_keyboard())
            elif aut_reg_mode:
                find_aut_reg(request)
