import requests
import time

from Models.dolphin import Dolphin
from Models.twitter import Twitter

# продвижение по аккаунту твиттера
# готовый скрипт, запускай да и все!

def request(secret_key, method, datas):

    url = "http://checks.wordok.by/twitter/api.php?method=" + method + "&secret_key=" + str(self.secret_key)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'}

    response = requests.request("POST", url, headers=headers, data=datas)

    print(method, "--> send", datas)
    print("response -->", response.text)

class Callbacks:
    def set_secret_key(self, secret_key):
        self.secret_key = secret_key

    def result_followers(self, user_id, result):
        request(self.secret_key, "result_followers", {'user_id': str(user_id), 'result': ",".join(result)})


    def result_follow_and_scan_count(self, user_id, result):
        request(self.secret_key, "result_follow_and_scan_count", {'user_id': user_id,
                   'login': result[0],
                   'followers': result[1],
                   'following': result[2],
                   'follow': result[3],
                   'ban': result[4]})

    def result_scan_my_followers(self, user_id, result):
        request(self.secret_key, "result_scan_my_followers", {'user_id': str(user_id), 'result': ",".join(result)})

    def result_unfollow(self, user_id, login):
        request(self.secret_key, "result_unfollow", {'user_id': str(user_id), 'login': login})

    def result_my_followers(self, user_id, profile, followers, following):
        request(self.secret_key, "result_my_followers", {'user_id': str(user_id), 'login': str(profile), 'followers': str(followers), 'following': str(following)})

class ZhFermaTwitter:
    def __init__(self, secret_key, chrome_driver):
        self.secret_key = secret_key
        self.chrome_driver = chrome_driver
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'}
        self.dolphin = None
        self.step = 0
        self.max_steps = 1000

        self.callbacks = Callbacks()
        self.callbacks.set_secret_key(self.secret_key)

    def start(self):

        while True:

            # каждые 1 секунд получаем задачу
            time.sleep(1)

            response = requests.request("GET", "http://checks.wordok.by/twitter/router.php?secret_key=" + str(self.secret_key), headers=self.headers)

            if response.text == "secret key not found!":
                print(response.text)
                break

            if response.text == "no secret key.":
                print(response.text)
                break

            for j in response.json():
                type = j["type"]
                user = j["user"]
                data = j["data"]

                # подключаемся к браузеру
                try:
                    if self.dolphin is None:
                        self.dolphin = Dolphin(user, self.chrome_driver)
                        self.dolphin.connect()
                        time.sleep(3)
                except Exception as e:
                    print("Error dolphin init!")
                    print(e)
                    break

                # ждем 4 секунд, после того как запустили
                time.sleep(4)

                if self.dolphin.isBrowserAlive() == False:
                    print("Error connect dolphin!")
                    time.sleep(5)
                    break

                # подключаем модель твитера
                twitter = Twitter(self.dolphin.get_driver(), self.callbacks)

                if type == "GET_FOLLOWERS":
                    # читаем фоловеров
                    twitter.get_followers(data["login"], user["id"])

                if type == "FOLLOW_AND_SCAN_COUNT":
                    # проверяем пользователя, и если что подписываемся
                    result = twitter.follow_and_scan_count(data["login"], user["id"])
                    # если мы в бане при подписке, значит отменим процесс.
                    if result == True:
                        print("ACCOUNT IS BAN!")
                        break

                if type == "SCAN_MY_FOLLOW":
                    # читаем фоловеров
                    twitter.scan_my_followers(user["id"])

                if type == "UNFOLLOW":
                    # отписываемся
                    twitter.go_unfollow(data["login"], user["id"])

                if type == "GET_MY_FOLLOWERS":
                    # получаем наших подписчиков
                    twitter.get_my_followers(data["login"], user["id"])


            # остановим задачу
            if self.dolphin is not None:
                self.dolphin.dolphin_stop()
                self.dolphin = None
                time.sleep(4)

            print("i don't sleep :)", self.step)

            self.step = self.step + 1
            if self.step > self.max_steps:
                break