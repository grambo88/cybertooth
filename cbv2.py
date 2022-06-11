from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from time import sleep
import itertools
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
        sleep(1)
        # self.table_scrape()
        sleep(1)
        pd.set_option('display.max_rows', None, 'display.max_columns', None)



    def generateBroswer(self): # sets all driver options and creates the instance
        print('*** STARTING  : generateBrowser() method ***')
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=chrome_options)
        url = "https://entries.horseracingnation.com/entries-results/belmont-park/2022-05-15"
        self.driver.get(url)
        sleep(5)
        self.driver.refresh()
        sleep(2)
        print('*** COMPLETED : generateBrowser() method ***')
        # WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframeCssSelector")))



    def get_num_tables(self): # returns 27 (num of tables on page)
        num_tables = self.driver.find_elements_by_tag_name('table')
        table_count = len(num_tables)

        return table_count


    def get_payouts(self): # returns payouts table
        web_pay_df = pd.read_html(self.driver.find_element_by_xpath("//table[@class='table table-hrn table-payouts']").get_attribute('outerHTML'))[0]
        web_pay_df.to_csv('_data_files/payouts.csv')

        return web_pay_df


    def get_entries(self): # returns entries table
        web_entries_df = pd.read_html(self.driver.find_element_by_xpath("//table[@class='table table-sm table-hrn table-entries']").get_attribute('outerHTML'))[0]
        web_entries_df.to_csv('_data_files/entries.csv')

        return web_entries_df


    def get_exotics(self): # returns exotics table
        web_exotics_df = pd.read_html(self.driver.find_element_by_xpath("//table[@class='table table-hrn table-exotic-payouts']").get_attribute('outerHTML'))[0]
        web_exotics_df.to_csv('_data_files/exotics.csv')

        return web_exotics_df


    def get_num_races(self): # returns number of races
        num_tables = self.driver.find_elements_by_tag_name('table')
        race_count = len(num_tables) / 3
        # print(race_count)

        return int(race_count)


    def get_scratched(self): # returns scratched class
        scratched = self.driver.find_elements_by_xpath("//*[@class='scratched']")
        # print('\n')
        # print(scratched)
        for s in scratched:
            # print(s.text)

            return s.text


    def get_race_count(self): # returns race count
        num_tables = self.driver.find_elements_by_tag_name('table')
        race_count = len(num_tables) / 3

        return race_count


    def get_headers(self): # returns 'PP Horse / Sire Trainer / Jockey ML'
        col_headers = self.driver.find_element_by_tag_name('thead')
        
        return col_headers.text 


    def show_races(self):
        pass


    def new_process(self):

        # col-lg-auto race-purse
        data_sets = self.driver.find_elements_by_class_name('my-5')

        for x in range(0,len(data_sets)):
            purse = self.driver.find_elements_by_xpath("//*[@class='row']")
            for y in purse:
                # print(y.text)

                fullstring = 'Belmont Park Race'

            
                if fullstring != None and y.text == fullstring:

                    print('found race')
                    print(y.text)
                else:
                    print('found junk')
                    print(y.text)
                # print('Found ' + len())



        race_info_df = data_sets[5]

        # purse = self.driver.find_elements_by_xpath("//*[@class='row']")

        # purse = data_sets.find_element_by_class_name('col-lg-auto race-purse')
        

        # for x in purse:
        #     print(x.text)

        # race_info_df = pd.read_html(self.driver.find_element_by_xpath())
        # race_info_df.to_csv('_data_files/race_info_df.csv')

        print(race_info_df) # returns web element

        c = 0
        for x in data_sets: # returns num of races 
           c = c + 1
           print('data: ', c)
           # print(len(c))

    def regroup_data(self):

            file = open('_data_files/horse_stats1.csv', 'r')
            reader = csv.reader(file)
            new_list = open('_data_files/stuff.csv', 'w')
            writer = csv.writer(new_list)
            lists_from_csv = []
            # for x in range(0,4):

            for row in reader:
                lists_from_csv.append(row)
            writer.writerows(lists_from_csv)
            # print(lists_from_csv)
            # return lists_from_csv
            for x in lists_from_csv:
                print(x)

            # with open('_data_files/stuff.csv') as f:
            #     for line1,line2 in itertools.zip_longest(*[f]*2):
            #         print(line1,line2)


                # for row[2] in reader:
                #     print("dont know")




    def table_scrape(self):

        print('*** STARTING  : table_scrape() method ***')

        num_tables = self.driver.find_elements_by_tag_name('table')
        race_count = len(num_tables) / 3

        for x in range(1, int(int(race_count)+1)):
            print('Race: ', x)

        tables = self.driver.find_elements_by_xpath("//table[@class='table table-sm table-hrn table-entries']")
        print('################################')
        print('there are ', len(tables), ' entries_tables')
        print('################################')

        scratched = self.driver.find_elements_by_xpath("//*[@class='scratched']")
        print('\n')
        print(scratched)
        for s in scratched:
            print(s.text)

        # print('\n')

        col_headers = self.driver.find_element_by_tag_name('thead')
        print(col_headers.text) # prints 'PP Horse / Sire Trainer / Jockey ML'

        n = 0

        for race in tables:

            n = n+1
            # print('Race: ', n)

            # col_headers = self.driver.find_element_by_tag_name('thead')
            # print(col_headers.text) # prints 'PP Horse / Sire Trainer / Jockey ML'
            
            for entry in race.find_elements_by_tag_name('tr'):
                
                if entry not in scratched:
                    horse_stats = []
                    for stat in entry.find_elements_by_tag_name('td'):
                        horse_stats.append(stat.text)

                    if horse_stats == []:
                        pass
                        # print('first')
                    else:
                        addRaceNum = 'Race:' + str(n)
                        horse_stats.insert(0, addRaceNum) # need to add Track and Date, hash value?

                        # ('_data_files/horse_stats.csv')
                        print(horse_stats)
                        with open('_data_files/horse_stats1.csv', 'a', newline="") as entrie_csv:
                            writer = csv.writer(entrie_csv)
                            writer.writerow(horse_stats) # this works but splits each into 3 rows
                            


            # print('################################')

        sleep(1)


        print('*** COMPLETED : table_scrape() method ***')









