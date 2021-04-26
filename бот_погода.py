import vk_api
import time
import json
import requests

token1 = "a0ee4c846b3ff045fb7c4fa94244e402aff417bf07f6f4729db6398842d9e9f0af0dcf85e657e711d6019"
vk = vk_api.VkApi(token=token1)
vk._auth_token()


def get_button(label, color, payload=""):
    return {
        "action": {
            "type": "text",
            'payload': json.dumps(payload),
            "label": label
        },
        "color": color
    }


# приветственная клавиатура
keyboard_hello = {
    "one_time": True,
    "buttons": [[get_button(label="попробовать бота", color="positive")],
                [get_button(label="не пробовать", color="negative")]]
}

keyboard_hello = json.dumps(keyboard_hello, ensure_ascii=False).encode('utf-8')
keyboard_hello = str(keyboard_hello.decode('utf-8'))
# клавиатура не понял
keyboard_start = {
    "one_time": True,
    "buttons": [[get_button(label="привет", color="positive")]]
}

keyboard_start = json.dumps(keyboard_start, ensure_ascii=False).encode('utf-8')
keyboard_start = str(keyboard_start.decode('utf-8'))


while True:
    messages = vk.method("messages.getConversations", {"offset": 0, "count": 20})

    if messages["count"] >= 1:
        id = messages["items"][0]["last_message"]["from_id"]

        body = messages["items"][0]["last_message"]["text"].lower()
        if id != "204216101":
            if body == "начать" or body == "привет" or body == "Привет" or body == "Начать":
                vk.method("messages.send", {"peer_id": id,
                                            "attachment": "photo302808715_456239234",
                                            "message": "Приветствую тебя! Что ты хочешь сделать?",
                                            "keyboard": keyboard_hello})
            elif body == 'испытать бота':
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Испытывай его!!!",
                                            'keyboard': keyboard_start})
            elif body == 'не пробовать':
                vk.method("messages.send", {"peer_id": id,
                                            "message": "Тогда что ты тут делаешь?",
                                            'keyboard': keyboard_start})
            elif "погода" in body.lower():
                if body.lower() == "погода":
                    vk.method('messages.send', {'user_id': id,
                                                'message': "Пожалуйста, напиши ещё и город(в 1-м сообщении)"})
                else:
                    city = body.lower().replace("погода ", "")
                    apiKey = "34dee3a9ad750d39dfc67882b22c42f5"
                    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&type=like&" + "DE&appid=" + \
                          apiKey
                    response = requests.get(url)
                    pogoda_data = response.json()
                    if "message" in pogoda_data:
                        if pogoda_data["message"] == "city not found":
                            vk.method('messages.send', {'user_id': id,
                                                        'message': "Извини, но такой город не найден((( просьба "
                                                                   "проверить прописание вашего города"})
                    else:
                        obsheye = ""
                        pogoda_json_request = pogoda_data["weather"][0]
                        if pogoda_json_request["main"] == "Rain":
                            obsheye = "идёи дождь"
                        elif pogoda_json_request["main"] == "Clouds":
                            obsheye = "облачно"
                        elif pogoda_json_request["main"] == "Clear":
                            obsheye = "солнечно"
                        elif pogoda_json_request["main"] == "Thunderstorm":
                            obsheye = "шторм"
                        main = pogoda_data["main"]
                        # температура
                        temp1 = main["temp"]
                        temp2 = 273.15
                        temp = round(temp1-temp2)
                        temp_ans = ", температура - " + str(temp) + "°,"
                        # ветер
                        wind = pogoda_data["wind"]
                        wind_speed = wind["speed"]
                        if "deg" in wind:
                            wind_deg = wind["deg"]
                            mmm = " м/с, направление ветра: "

                            if wind_deg < 23:
                                napr = "северное"
                            elif wind_deg < 68:
                                napr = "северо-восточное"
                            elif wind_deg < 113:
                                napr = "восточное"
                            elif wind_deg < 158:
                                napr = "юго-восточное"
                            elif wind_deg < 203:
                                napr = "южное"
                            elif wind_deg < 248:
                                napr = "юго-западное"
                            elif wind_deg < 293:
                                napr = "западное"
                            elif wind_deg < 338:
                                napr = "cеверо-западное"
                            else:
                                napr = "северное"
                            wind_mess = "скорость ветра -" + str(wind_speed) + ", направление - " + napr
                            humidity = main["humidity"]
                            otvet_vlaznost = ", влажность воздуха -" + str(humidity)
                            answer = obsheye + temp_ans + wind_mess + otvet_vlaznost
                            vk.method("messages.send", {"user_id": id,
                                                        "message": answer,
                                                        "keyboard": keyboard_start})
                        else:
                            wind_mess = "скорость ветра -" + str(wind_speed)
                            humidity = main["humidity"]
                            otvet_vlaznost = ", влажность воздуха -" + str(humidity)
                            answer = obsheye + temp_ans + wind_mess + otvet_vlaznost
                            vk.method("messages.send", {"user_id": id,
                                                        "message": answer,
                                                        "keyboard": keyboard_start})

            else:
                vk.method("messages.send", {"peer_id": id, "message": "Извини, но я не знаю как ответить... "
                                                                      "Напиши 'привет', может поможет...",
                                            'keyboard': keyboard_start})
