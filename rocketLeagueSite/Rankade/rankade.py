import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import json
import sys

print('*'*30 + "path" + '*'*30)

class Rankade:

    def __init__(self, username, password, env='prod'):
        self.rankade = 'https://rankade.com'
        self.dashboard = self.rankade + '/#/group/WkMK9GYyb2o/DlLprOnOKM7'
        self.signin = self.rankade + '/signin/'
        self.save_button_xpath = '//*[@id="matchModal"]/div/div/div[3]/a[1]'
        self.user_drop_down_xpath = {1: '//*[@id="matchData"]/div[4]/div[1]/div[1]/div[1]/div/div[1]/div',
                                     2 : '//*[@id="matchData"]/div[4]/div[1]/div[1]/div[1]/div/div[2]/div',
                                     3 : '//*[@id="matchData"]/div[4]/div[1]/div[1]/div[2]/div/div[1]/div',
                                     4 : '//*[@id="matchData"]/div[4]/div[1]/div[1]/div[2]/div/div[2]/div'}

        self.save = True if env == 'prod' else False

        if env == 'prod':
            # options = Options()
            # options.add_argument("--headless")
            # self.driver = webdriver.Chrome(options=options)

            chrome_options = Options()
            chrome_options.binary_location = os.environ["GOOGLE_CHROME_BIN"]
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument('--no-sandbox')
            self.driver = webdriver.Chrome(executable_path=os.environ["CHROMEDRIVER_PATH"], chrome_options=chrome_options)

        else:
            self.driver = webdriver.Chrome()


        self.login(username, password)
        self.users = self.load_users('imageClassifierSite/Rankade/users.json')
        print(self.users)

    def login(self, username, password):
        self.driver.get(self.signin)

        self.driver.find_element_by_class_name('sign-button')

        _username = self.driver.find_element_by_name('email')
        _username.send_keys(username)

        _password = self.driver.find_element_by_name('password')
        _password.send_keys(password)
        time.sleep(2)
        _password.submit()

        self.driver.get(self.dashboard)

        self.clearPopUps()

    def add_matches(self, players, scores):
        try:
            add_match = self.driver.find_element_by_xpath('//*[@id="teamRankWidget"]/div[1]/a[1]')
            time.sleep(2)
            add_match.click()
        except:
            print("Unable to click add match button")
            sys.exit()

        for score in scores:
            time.sleep(2)
            self.add_match(players, score)

    def add_match(self, users, score):

        for i in range(0, len(users)):
            user = self.users[users[i]]
            print('adding user: {0}, at position: {1}'.format(user, i + 1))
            self.select_user(user, i + 1)

        self.add_score(score[0], score[1], self.save)

    def add_score(self, home_score, away_score, save=True):
        self.driver.find_element_by_name('f0_points').send_keys(home_score)
        self.driver.find_element_by_name('f1_points').send_keys(away_score)

        if save:
            self.save_score()

    def save_score(self):
        self.driver.find_element_by_xpath(self.save_button_xpath).click()

    def clearPopUps(self):
        closed = False
        try:
            time.sleep(5)
            self.driver.find_element_by_xpath('//*[@id="goProGroupModal"]/div/div/div[1]/button').click()
            closed = True
        except:
            closed = False

        if not closed:
            try:
                time.sleep(5)
                self.driver.find_element_by_xpath('//*[@id="goProGroupModal"]/div/div/div[3]/button').click()
                closed = True
            except:
                closed = False

        if not closed:
            try:
                alert = self.driver.switch_to.alert()
                alert.accept()
            except:
                closed = False

    def click_user(self, dropdown, user_id):
        try:
            elements = dropdown.find_elements_by_tag_name('li')
            actions = ActionChains(self.driver)

            for option in elements:
                if option.get_attribute('data-user-id') == user_id:
                    option.click()
                else:
                    actions.send_keys(Keys.ARROW_DOWN)
                    actions.perform()
        except:
            return 0

    def select_user(self, user_id, user_spot):
        print("Finding dropdown")
        try:
            dropdown = self.driver.find_element_by_xpath(self.user_drop_down_xpath[user_spot])
        except:
            print("Could not click dropdown: user_id = {0}".format(user_id))
            print("Could not find dropdown")
            sys.exit()

        try:
            print("Clicking dropdown")
            time.sleep(1)
            dropdown.click()

            self.click_user(dropdown, user_id)
        except:
            print("Could not click dropdown: {0}".format(user_id))
            sys.exit()

    def load_users(self, users_file):
        with open(users_file) as f:
            d = json.load(f)
            return d

    def close(self):
        self.driver.quit()

def read_matches(filename='match.txt'):
    _list = list()
    with open(filename, 'r') as f:
        for line in f.readlines():
            _list.append(read_match(line.replace('\n', '')))
    return _list

def read_match(fline):

    line = fline.split('=')

    players = list()
    for player in line[0].split(','):
        players.append(player.strip().replace('@', ''))

    print(players)

    scores = list()
    for score in line[1].split(','):
        ss = score.split('-')
        if len(ss) == 2:
            scores.append((ss[0].strip(), ss[1].strip()))
    print(scores)

    return players, scores

def record_matches(r, match_list):
    for players, scores in match_list:
        try:
            r.add_matches(players, scores)
            print("SUCCESSFULLY ADDED MATCHES!")
        except:
            print("FAILED TO ADD MATCHES")