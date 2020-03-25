from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class Insta_bot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        sleep(3)
        username_field = driver.find_element_by_xpath("//input[@name='username']")
        username_field.clear()
        username_field.send_keys(self.username)
        password_field = driver.find_element_by_xpath("//input[@name='password']")
        password_field.clear()
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)
        sleep(5)
        not_now = driver.find_element_by_xpath("//div[@class='mt3GC']/button[2]")
        not_now.click()
        sleep(3)
    def like_photo(self, hashtag):

        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")

        for i in range(1, 3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)

        hrefs = driver.find_elements_by_tag_name("a")
        pic_hrefs = [elem.get_attribute('href') for elem in hrefs]
        pic_hrefs = [href for href in pic_hrefs if hashtag in href]
        print(hashtag + " photos: " + str(len(pic_hrefs)))

        for pic_href in pic_hrefs:
            driver.get(pic_href)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                driver.find_element_by_link_text("Like").click()
                sleep(18)
            except Exception as e:
                sleep(2)

    def unfollow(self):
        driver = self.driver
        account = driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(self.username))
        account.click()
        sleep(3)
        driver.find_element_by_xpath("//a[contains(@href, '/following')]").click()
        sleep(3)
        following = self._get_names()
        sleep(2)
        driver.find_element_by_xpath("//a[contains(@href, '/followers')]").click()
        followers = self._get_names()
        sleep(1)
        print(following)
        print(followers)
        not_following_back = [user for user in following if user not in followers]
        whitelist = ["nhl", "fullsend", "hockeybenders", "privacyinternational", "upstatenymemes", "shopfullsend", "avaroe",
                     "influencragency", "nelkboys", "usphlhockey","torproject","lakegeorgecamp","iihfhockey","nhlbruins",
                     "usahockeyntdp", "bardown", "spittinchiclets","pavelbarbertraining","heybarber","odrheaven","iihfworldjuniors",
                     "bauer.sticks","usahockey","hockeyplayersclub", "on.the.bench","alek__17__04", "ave.valderrana"]
        not_following_back2 = [user for user in not_following_back if user not in whitelist]
        for user in not_following_back2:
            self._unfollow(user)
            sleep(1)

    def _get_names(self):
        driver = self.driver
        scroll_box = driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = driver.execute_script("""
                    arguments[0].scrollTo(0, arguments[0].scrollHeight);
                    return arguments[0].scrollHeight;
                    """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        #close the window
        driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        return names

    def _unfollow(self, username):
        driver = self.driver
        driver.get("https://www.instagram.com/" + username + "/")
        sleep(2)
        driver.find_element_by_xpath("//button[contains(text(), 'Following')]").click()
        sleep(2)
        driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()

bot = Insta_bot("quirk_hockey6", "poppk456")
bot.login()
bot.unfollow()

hashtags = ["hockey","newyork", "lakegeorge", "adventure", "explore", "glensfalls", "guitar", "piano", "music", "cliftonpark", "earth",
            "programming", "track", "connecticut", "covid-19", "queensbury", "wisdom", "maine", "rink", "cybersecurity","dog"]
[bot.like_photo(tag) for tag in hashtags]
