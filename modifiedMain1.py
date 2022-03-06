from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from time import sleep
import itertools
from defs import MindYa, Business
import csv, re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from tabulate import tabulate


class Webdriver:

    def __init__(self):
        self.genrateBroswer()
        sleep(3)
        self.acctLogin()
        sleep(1)

    def genrateBroswer(self): # sets all driver options and creates the instance is created
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver", options=chrome_options)
        url = "https://www.offtrackbetting.com/"
        self.driver.get(url)
        sleep(1)

    def acctLogin(self): # logs into page via supplied creds
        account_number_input = self.driver.find_element_by_xpath('//*[@id="accountNumber"]')
        pin_input = self.driver.find_element_by_xpath('//*[@id="pin"]')
        log_in_btn = self.driver.find_element_by_xpath('//*[@id="loginButton"]')
        account_number_input.send_keys(MindYa)
        pin_input.send_keys(Business)
        log_in_btn.click()
        sleep(10)
        iframe = self.driver.find_element_by_xpath('//*[@id="ticket"]')
        self.driver.switch_to.frame(iframe)


    def start_process(self):
        # meets = self.get_list_meets()
        track = self.driver.find_element_by_xpath('//*[@id="selectCurrentTrack"]') # not needed?
        # count = 0
        # print(meets)
        x = 'Auteuil FR'
        # for x in meets:
        sleep(1)
        drop = Select(track)
        drop.select_by_visible_text(x)
        sleep(1)
        global count
        count = 1
        try:
            for i in range(count, 25): # break this down into small pieces 
                print('\n')
                print("Starting iteration: ", count)
                sleep(1)
                race_panel = self.driver.find_element_by_xpath('//*[@id="panel_R' + str(count) + '"]')
                race_panel.click()
                print(f'Track: {x}; Race: {count};', ' write_info Function')
                sleep(1)
                self.write_info()
                sleep(1)
                print('Completed write_info Function')
                sleep(1)
                count = count + 1

        except:
            None

        sleep(1)
        self.remove_scratched()
        sleep(1)
        self.clean_data()
        sleep(1)

        print('*** start_process() finished ***')


    def write_info(self):
        with open("wp_output.csv", "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(self.get_info_tab())
            writer.writerow(' ')
            f.close()
            sleep(2)
            self.get_results_tab()
            sleep(2)


    def clean_data(self):
        with open("wp_output_clean.csv", 'r+') as f:
            text = f.read()
            text = re.sub('"', '', text)
            f.seek(0)
            f.write(text)
            f.write(' ')
            f.truncate()
            f.close()


    def remove_scratched(self):
        with open('wp_output.csv', 'rt') as inp, open('wp_output_clean.csv', 'wt') as out:
            writer = csv.writer(out)
            for row in csv.reader(inp):
                try:
                    if row[3] != "-":
                        writer.writerow(row)
                    if row[3] == '-':
                        pass
                    else:
                        pass
                except:
                    writer.writerow(' ')
                    print(' ')

    def get_results_tab(self):
        try:
            race_results = self.driver.find_element_by_xpath('//*[@id="panel_detailTabResults"]')
            race_results.click()
            sleep(1)
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'r' + str(count) + '_result'))) # was 'r1_result'
            table = self.driver.find_element_by_id('r' + str(count) + '_result')
            with open('race: ' + str(count) + '.csv', 'a') as results:
                writer = csv.writer(results)
                results.write(table.text)
                writer.writerow(' ')
                writer.writerow(' ')
                results.close()
                sleep(2)
            race_results = self.driver.find_element_by_xpath('//*[@id="panel_detailTabDetails"]')
            race_results.click()
        except:
            print('failed get_results_tab()')

    # def get_results_tab(self):
    #     try:
    #         race_results = self.driver.find_element_by_xpath('//*[@id="panel_detailTabResults"]')
    #         race_results.click()
    #         sleep(1)
    #         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'r' + str(count) + '_result'))) # was 'r1_result'
    #         table = self.driver.find_element_by_id('r' + str(count) + '_result')
    #         with open('new_file.csv', 'a') as results:
    #             writer = csv.writer(results)
    #             results.write(table.text)
    #             writer.writerow(' ')
    #             writer.writerow(' ')
    #             results.close()
    #             sleep(2)
    #         race_results = self.driver.find_element_by_xpath('//*[@id="panel_detailTabDetails"]')
    #         race_results.click()
    #     except:
    #         print('failed get_results_tab()')


    def get_info_tab(self):
        panel_1 = self.driver.find_element_by_xpath('//*[@id="panel1_canvas"]')
        panel_2 = self.driver.find_element_by_xpath('//*[@id="panel2_canvas"]')
        panel_1_rows = panel_1.find_elements_by_xpath('//div[contains(@class, "row")]')
        panel_2_rows = panel_2.find_elements_by_xpath('//div[contains(@class, "row")]')
        data = []
        panel_1_data = []
        panel_2_data = []
        for row in panel_1_rows:
            try:
                # race = ('Race ', str(count))
                no = row.find_element_by_xpath('div[1]/div[1]/div').text
                pp = row.find_element_by_xpath('div[1]/div[2]').text
                odds = row.find_element_by_xpath('div[1]/div[3]').text
                ml = row.find_element_by_xpath('div[1]/div[4]').text
                runner = row.find_element_by_xpath('div[1]/div[5]').text
                panel_1_data.append([count, no, pp, odds, ml, runner])
            except:
                None

        for row in panel_2_rows:
            try:
                breeding = row.find_element_by_xpath('div[1]').text
                trainer = row.find_element_by_xpath('div[2]').text
                jockey = row.find_element_by_xpath('div[3]').text
                panel_2_data.append([breeding, trainer, jockey])
            except:
                None

        for i in range(len(panel_1_data)):
            panel_1_data[i].extend(panel_2_data[i])

        return (panel_1_data)


    def get_list_meets(self): # returns list of available thoroughbred tracks
        try:
            element = self.driver.find_element_by_id('formSelectCurrentTrack').text
            track = self.driver.find_element_by_xpath('//*[@id="selectCurrentTrack"]')
            test_data = element.split('\n')

            def pred(c):
                c = c[0].lower()
                result = (pred.previous <= c)
                pred.previous = c
                return result

            pred.previous = 'a' # *** I dont know what this does? ***
            meets = list(itertools.takewhile(pred, test_data))

            # with 



            return meets 

        except:
            sleep(3)
            print('Exception occurred...')
            driver.quit()




