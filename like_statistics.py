import vk_api
import json
from vk_api.longpoll import VkLongPoll, VkEventType
import requests
import random

kalk_mode = False
random_id = random.randint(1, 1000000)


def write_msg(user_id, message):
    global random_id
    r_id = random.randint(1, 1000000)
    while r_id == random_id:
        r_id = random.randint(1, 1000000)
    random_id = r_id
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": random_id})


token = "cfd06f1308c729bb30731feb2d509fb532db16684c1f70f46f8fe4b86fb505ccd98ee4bb0258a9c3eff80"
access_token = '7f5fd4918b0c688c6d54c60a008b1bc775ca469cb5549b502a9aa3e570b36997357e5eb3462e6b009ecba'
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


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


def kalk(event, request):
    try:
        otv = eval(request)
        write_msg(event.user_id, otv)
    except Exception as e:
        write_msg(event.user_id, e)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            request = event.text.lower()
            if request == 'калькулятор' or request == 'выйти':
                kalk_mode = not kalk_mode
                if kalk_mode:
                    write_msg(event.user_id, 'Режим калькулятор запущен.')
                    write_msg(event.user_id,
                              "Введите выражение. Используйте знаки из допустимого списка: +, -, *, "
                              "/, **, (, ), %, //.")
                else:
                    write_msg(event.user_id, 'Режим калькулятор остановлен.')
            elif kalk_mode:
                kalk(event, request)
            elif request == "начать":
                write_msg(event.user_id, "Хай")
            elif request == "статистика":
                write_msg(event.user_id, "{}".format(str(like_statistics(event.user_id))))
            elif request == "привет":
                write_msg(event.user_id, "Хай")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, "Не поняла вашего ответа...")