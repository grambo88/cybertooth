from cbv2 import Webdriver
from time import sleep
import csv


browser = Webdriver()

print('Starting tests:')

functs = [browser.regroup_data(), browser.get_num_tables(), 
           browser.get_payouts(), browser.get_entries(), browser.get_exotics(), 
           browser.get_scratched(), browser.get_race_count(), browser.get_headers()]

def test(self):
	for i in functs:

		i 


print('Tests complete!')

