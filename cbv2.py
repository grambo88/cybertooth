from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from time import sleep
import itertools
import sys
import csv, re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from tabulate import tabulate
import pandas as pd 


class Webdriver:

    def __init__(self):
        self.generateBroswer()
        # sleep(1)
        # self.table_scrape()
        # sleep(1)
        pd.set_option('display.max_rows', None, 'display.max_columns', None)


    def generateBroswer(self): # sets all driver options and creates the instance
        print('*** STARTING  : generateBrowser() method ***')
        chrome_options = webdriver.ChromeOptions()
        # prefs = {"profile.default_content_setting_values.notifications": 2}
        # chrome_options.add_experimental_option("prefs", prefs)
        # chrome_options.add_experimental_option("detach", True)
        # chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=chrome_options)
        url_base = "https://entries.horseracingnation.com/entries-results/belmont-park/"
        url_date = "2022-05-15"
        url = url_base+url_date
        self.driver.get(url)
        sleep(1)
        # print('*** Removing Pop-up ***')
        self.driver.refresh()
        sleep(1)
        # self.driver.switchTo().parentFrame()
        print('*** COMPLETED : generateBrowser() method ***')
        sleep(1)
        # WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframeCssSelector")))

    def master(self): # 'join' is not defined

        filename = 'extra/Belmont-Dates-2022.csv'
        with open(filename, 'r') as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                print(row)
                url_base = "https://entries.horseracingnation.com/entries-results/belmont-park/"
                # url = ' '.join(url_base, row)
                url_date = ' '.join(row)
                print(url_base + url_date)
                url_full = url_base + url_date
                self.driver.get(url_full)
                sleep(5)
                self.table_scrape()
                sleep(5)
                print('got to here')



    def next_page(self):
        # url_base_2 = "2022-05-14"
        self.driver.get("https://entries.horseracingnation.com/entries-results/belmont-park/2022-05-14")
        self.get_num_tables()


    def get_num_tables(self): # returns 27 (num of tables on page)
        num_tables = self.driver.find_elements_by_tag_name('table')
        table_count = len(num_tables)

        return table_count


    def get_payouts(self): # returns payouts table
        web_pay_df = pd.read_html(self.driver.find_element_by_xpath("//table[@class='table table-hrn table-payouts']").get_attribute('outerHTML'))[0]
        web_pay_df.to_csv('data/payouts.csv')

        return web_pay_df


    def get_entries(self): # returns entries table
        web_entries_df = pd.read_html(self.driver.find_element_by_xpath("//table[@class='table table-sm table-hrn table-entries']").get_attribute('outerHTML'))[0]
        web_entries_df.to_csv('data/entries.csv')

        return web_entries_df


    def get_exotics(self): # returns exotics table
        web_exotics_df = pd.read_html(self.driver.find_element_by_xpath("//table[@class='table table-hrn table-exotic-payouts']").get_attribute('outerHTML'))[0]
        web_exotics_df.to_csv('data/exotics.csv')

        return web_exotics_df


    def get_scratched(self): # returns scratched class
        scratched = self.driver.find_elements_by_xpath("//*[@class='scratched']")
        for s in scratched: # only prints one line now, needs to print all scratchers

            return s.text


    def get_race_count(self): # returns race count
        num_tables = self.driver.find_elements_by_tag_name('table')
        race_count = len(num_tables) / 3

        return int(race_count)


    def get_headers(self): # returns 'PP Horse / Sire Trainer / Jockey ML'
        col_headers = self.driver.find_element_by_tag_name('thead')
        
        return col_headers.text 


    def num_of_races(self):
        data_sets = self.driver.find_elements_by_class_name('my-5')
        x = len(data_sets)

        return x


    def get_race_info(self):

        r_header = self.driver.find_elements_by_xpath("//*[@class='race-header']")
        dist = self.driver.find_elements_by_xpath("//*[@class='col-lg-auto flex-grow-1 race-distance']")
        purse = self.driver.find_elements_by_xpath("//*[@class='col-lg-auto race-purse']")
        path = 'data/race_info.csv'
        sys.stdout = open(path, 'a') # maybe use writerow feature?
        for (a, b, c) in zip(r_header, dist, purse):
             print (a.text + ',', b.text + ',', c.text)


    def new_purse(self):
        purse = self.driver.find_elements_by_xpath("//*[@class='col-lg-auto race-purse']")
        comma = ','
        for i in purse:
            for x in i.text:
                x.replace(',', '')
        print(i)
        


    def new_process(self):

        # col-lg-auto race-purse

        data_sets = self.driver.find_elements_by_class_name('my-5')
        r_info = self.driver.find_elements_by_xpath("//*[@class='col-lg-auto flex-grow-1 race-distance']")
        time = self.driver.find_elements_by_class_name('race-time')

        dist = None
        # post = []
        new_list = []

        for dist in r_info:
            print(dist.text)
            dist = dist.text

        y = 0

        # for dist in r_info:
        #     # print(dist.text)
        #     y = y + 1
        #     for post in time:

        #         # dist = [dist]   ---------->>>>>
        #         print(dist, post)

        for post in time:
            # print(post.text) # keep 
            post = [post.text]
            post.append(dist)
            print(post)




        print('dist object is type: ')

        print(type(dist))

        print('post object is type: ')

        print(type(post))

        print("END")

        # for i in dist & post:
        #     new_list = dist[i] + post[i]
        #     print(new_list)

        # for i in range(len(dist)):
        #     dist[i].extend(post[i])

        # return dist

       # return new_list

        # for _ in range(0,len(data_sets)):


        #     constructed_race = [dist.text]
        #     constructed_race.append(post.text)

        #     print(constructed_race)

        # print(len(data_sets))

        # # for x in range(0,len(data_sets)):
        # rows = self.driver.find_elements_by_xpath("//*[@class='row']")
        # test = self.driver.find_elements_by_xpath("//*[@class='col-lg-auto flex-grow-1 race-distance']")
        # purse = self.driver.find_elements_by_xpath("//*[@class='col-lg-auto race-purse']")


        # c = 0
        # for x in data_sets: # returns num of races 
        #    c = c + 1
        #    print('data: ', c)


    def regroup_data(self):

            file = open('data/horse_stats.csv', 'r')
            reader = csv.reader(file)
            new_list = open('data/stuff.csv', 'w')
            writer = csv.writer(new_list)
            lists_from_csv = []

            for row in reader:
                lists_from_csv.append(row)
            writer.writerows(lists_from_csv)
            # print(lists_from_csv)
            # return lists_from_csv
            for x in lists_from_csv:
                print(x)


    def table_scrape(self):

        print('*** STARTING  : table_scrape() method ***')

        num_tables = self.driver.find_elements_by_tag_name('table')
        race_count = len(num_tables) / 3

        # for x in range(1, int(int(race_count)+1)):
        #     print('Race: ', x)

        tables = self.driver.find_elements_by_xpath("//table[@class='table table-sm table-hrn table-entries']")

        scratched = self.driver.find_elements_by_xpath("//*[@class='scratched']")
        # print('\n')
        # print(scratched)
        # for s in scratched:
        #     print(s.text)

        col_headers = self.driver.find_element_by_tag_name('thead')
        # print(col_headers.text) # prints 'PP Horse / Sire Trainer / Jockey ML'

        n = 0

        for race in tables:

            n = n+1            
            for entry in race.find_elements_by_tag_name('tr'):

                if entry not in scratched:
                    # print('got here')

                    horse_stats = []
                    for stat in entry.find_elements_by_tag_name('td'):
                        horse_stats.append(stat.text)

                    if horse_stats == []:
                        pass

                    else:
                        addRaceNum = 'Race:' + str(n)
                        horse_stats.insert(0, addRaceNum) # need to add Track and Date, hash value?
                        path = 'data/horse_stats.csv'
                        sys.stdout = open(path, 'a')
                        print(horse_stats) # , newline=""

        # print(horse_stats.text)







