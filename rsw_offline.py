#!/usr/bin/python

from selenium import webdriver
from urlparse import urlparse
import argparse


RESET_URLS = ['http://rswi' + x + y + '-slb.centertel.pl:7001/nbuk/jsp/admin/reset.jspx'
              for x in ['pok', 'pos', 'map', 'nbuk'] for y in ['1', '2', '3', '4']]

TEST_URLS = ['http://rswi' + x + y + '-slb.centertel.pl:7001/nbuk/optiSearch.do?msisdn=500000000'
             for x in ['pok', 'pos', 'map', 'nbuk'] for y in ['1', '2', '3', '4']]


def login(driver):
    login_url = 'https://voptisso-vip.centertel.pl/webSSO/auth/simple/login.do'
    login_data = {'username': '', 'password': '', 'domain': 'OTSA'} # fill in the data
    driver.get(login_url)
    element = driver.find_element_by_id("username")
    element.send_keys(login_data['username'])
    element = driver.find_element_by_id("password")
    element.send_keys(login_data['password'])
    driver.find_element_by_id('bt-submit').click()


def logout(driver):
    logout_url = 'https://voptisso-vip.centertel.pl/webSSO/auth/index.do'
    driver.get(logout_url)
    driver.find_element_by_id('logout-button').click()


def set_all_offline(driver):
    for url in RESET_URLS:
        driver.get(url)
        driver.execute_script("document.getElementById('reportForm:j_id72').click()")


def set_all_online(driver):
    for url in RESET_URLS:
        driver.get(url)
        driver.execute_script("document.getElementById('reportForm:j_id81').click()")


def print_status(driver):
    for url in TEST_URLS:
        server = urlparse(url).netloc
        driver.get(url)
        if 'w trybie Offline' in driver.page_source:
            print server + " OFFLINE"
        else:
            print server + " ONLINE"


def main():
    parser = argparse.ArgumentParser(description='Turn all EAI services offline or online in RSW/nBuk')
    parser.add_argument('mode', type=str, choices=['online', 'offline'], help='choose mode for all services')
    args = parser.parse_args()

    browser = webdriver.Firefox()
    login(browser)
    if args.mode == 'online':
        set_all_online(browser)
    elif args.mode == 'offline':
        set_all_offline(browser)
    print_status(browser)
    logout(browser)
    browser.close()


if __name__ == '__main__':
    main()

