import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

from wikipedia import wikipedia

token = "cfd06f1308c729bb30731feb2d509fb532db16684c1f70f46f8fe4b86fb505ccd98ee4bb0258a9c3eff80"
vk_session = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk_session, group_id="204216101")
vk = vk_session.get_api()

wikipedia.set_lang('ru')


def wiki_response(request_text):
    return str(wikipedia.page(request_text).content[:1000])


def help():
    return f"О чём мне спросить у Википедии?"


def main():
    flag_wiki, flag_help = False, True
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and flag_help:
            flag_wiki = not flag_wiki
            flag_help = not flag_help
            vk.messages.send(user_id=event.obj.massage['from_id'],
                             message=help(),
                             random_id=random.randint(0, 2 ** 64))

        elif event.type == VkBotEventType.MESSAGE_NEW and flag_wiki:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=f"{wiki_response(event.obj.message['from_id'])}\n\n{help()}",
                             random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()