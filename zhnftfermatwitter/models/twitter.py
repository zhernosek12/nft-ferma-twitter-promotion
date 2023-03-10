from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class Twitter:
    def __init__(self, driver, callbacks):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)

        self.xpath_follow = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[1]/div/div/span/span'

        self.callbacks = callbacks

    def check_auth(self):

        if "twitter.com" not in self.driver.current_url:
            self.driver.get("https://twitter.com/")
            time.sleep(2)

        try:
            self.driver.find_element(By.XPATH, "//a[@href='/compose/tweet']").text
        except:
            input("auth twitter, and press enter to continue...")

    def follow(self, url):
        print("go follow --> ")
        try:
            if url is not None:
                self.driver.get(url)

            time.sleep(1.5)

            follow = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Follow"]')))
            self.driver.execute_script("arguments[0].click();", follow)

            print("click follow")

            # проверим, лимит не превышен?

            time.sleep(1.5)

            try:
                # найти все span элементы, и проверить текст
                spans = self.driver.find_elements(By.TAG_NAME, "span")
                if spans:
                    for s in spans:
                        if s and s.text:
                            if "You are unable to follow more people at this time." in str(s.text):
                                return "UNABLE_FOOLOW"
                                break
            except:
                pass

            return "OK"

        except Exception as ex:
            print("Follow error:")
            print(ex)

            time.sleep(2)

            return "FAIL"

    def unfollow(self, url):
        try:
            self.driver.get(url)

            time.sleep(1)

            unfollow = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Following"]')))
            self.driver.execute_script("arguments[0].click();", unfollow)

            time.sleep(1)

            unfollow2 = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Unfollow"]')))
            self.driver.execute_script("arguments[0].click();", unfollow2)

            time.sleep(1)

        except Exception as ex:
            print("Unfollow error:")
            print(ex)
            time.sleep(1)

    def retweet(self, url):
        try:
            self.driver.get(url)

            time.sleep(2)

            retweet = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Retweet"]')))
            self.driver.execute_script("arguments[0].click();", retweet)

            time.sleep(2)

            retweet = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Retweet"]')))
            self.driver.execute_script("arguments[0].click();", retweet)

        except Exception as ex:
            print("Retweet error:", ex)
            time.sleep(1)

        # Like
        self.like()

    def like(self):
        try:
            time.sleep(1)

            like = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Like"]')))
            self.driver.execute_script("arguments[0].click();", like)

        except Exception as ex:
            print("Like error:", ex)
            time.sleep(1)

    # сканирование подписчиков
    def get_followers(self, profile, user_id):

        print("task --> get_followers @", profile)
        print("owner -->", user_id)
        print()

        follower_list = []
        step = 0
        max_steps = 15

        # открываем всех подписчиков
        self.driver.get("https://twitter.com/"+profile+"/followers")
        time.sleep(2)

        # Code to goto End of the Page
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(2)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            usernames = self.driver.find_elements(By.CLASS_NAME, "css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")
            for a in usernames:
                try:
                    text = a.text
                    if text and text[:1] == "@":
                        username = text[1:]
                        if username not in follower_list:
                            print(username, "add.")
                            follower_list.append(username)
                except:
                    pass

            step = step + 1
            if step >= max_steps:
                break

        self.callbacks.result_followers(user_id, follower_list)

    # сканирование подписчиков
    def follow_and_scan_count(self, profile, user_id):

        print("task --> follow_and_scan_count @", profile)
        print("owner -->", user_id)
        print()

        # открываем всех подписчиков
        self.driver.get("https://twitter.com/"+profile)
        time.sleep(2)

        followers = -2
        following = -2
        follow = False
        ban = False

        # parse
        try:
            followers_datas = self.driver.find_elements(By.CSS_SELECTOR, ".css-901oao.css-16my406.r-18jsvk2.r-poiln3.r-1b43r93.r-b88u0q.r-1cwl3u0.r-bcqeeo.r-qvutc0 .css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")

            following = self.parse_follow_text(followers_datas[0].text)
            followers = self.parse_follow_text(followers_datas[1].text)

            if following == 0:
                following = 1

            if followers == 0:
                followers = 1

            print("following", following, "followers", followers)

        except Exception as e:
            time.sleep(1)
            print("err", e)
            pass

        time.sleep(1)

        # условия подписываемся или нет?
        if following > 0 and following > 0:
            calc = following / followers

            # если не менее 20% он сам подписан, то скорее всего это бот
            if calc > 0.8 and calc < 2.2:
                # None --> мы находимся на этой странаице
                status_follow = self.follow(None)

                if status_follow == "OK" or status_follow == "FAIL":
                    follow = True
                else:
                    ban = True

        time.sleep(1)

        self.callbacks.result_follow_and_scan_count(user_id, [profile, followers, following, follow, ban])

        return ban

    #
    def parse_follow_text(self, text):

        text = text.replace(",", "")
        text = text.replace(" ", "")
        #text = text.replace(".", "")
        count = -1

        if text[-1:] == "K":
            count = text[:-1]
            count = float(count)
            count = count * 1000
        elif text[-1:] == "M":
            count = text[:-1]
            count = float(count)
            count = count * 1000000
        else:
            count = float(text)

        return count

    #
    def scan_my_followers(self, user_id):

        print("task --> scan_my_followers")
        print("owner -->", user_id)
        print()

        follower_list = []
        step = 0
        max_steps = 100

        # открываем всех подписчиков
        self.driver.get("https://twitter.com/followers")
        time.sleep(2)

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            usernames = self.driver.find_elements(By.CLASS_NAME, "css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")

            for a in usernames:
                try:
                    text = a.text
                    if text and text[:1] == "@":
                        username = text[1:]
                        if username not in follower_list:
                            print(username, "add.")
                            follower_list.append(username)
                except:
                    pass

            step = step + 1
            if step >= max_steps:
                break

        self.callbacks.result_scan_my_followers(user_id, follower_list)

    def go_unfollow(self, profile, user_id):

        print("task --> go_unfollow @", profile, user_id)
        print()

        # открываем всех подписчиков
        self.unfollow("https://twitter.com/" + profile)

        time.sleep(1)

        self.callbacks.result_unfollow(user_id, profile)

    def get_my_followers(self, profile, user_id):

        print("task --> scan my followers @", profile)
        print("owner -->", user_id)
        print()

        # открываем всех подписчиков
        self.driver.get("https://twitter.com/"+profile)
        time.sleep(2)

        followers = -2
        following = -2

        # parse
        try:
            followers_datas = self.driver.find_elements(By.CLASS_NAME, ".css-901oao.css-16my406.r-18jsvk2.r-poiln3.r-1b43r93.r-b88u0q.r-1cwl3u0.r-bcqeeo.r-qvutc0 .css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0")

            following = self.parse_follow_text(followers_datas[0].text)
            followers = self.parse_follow_text(followers_datas[1].text)

            if following == 0:
                following = 1

            if followers == 0:
                followers = 1

            print("following", following, "followers", followers)

        except Exception as e:
            time.sleep(1)
            print("err", e)
            pass

        time.sleep(1)

        self.callbacks.result_my_followers(user_id, profile, followers, following)