#!/usr/bin/env python3
import os
import ssl
from datetime import datetime
import wget
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import gu2_int_monitoring_config

################################################################################
#####################  WARNING!!! SPAGHETTI CODE BELOW!!!  #####################
################################################################################

options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
ssl._create_default_https_context = ssl._create_unverified_context

try:
    os.remove('css.css')
except FileNotFoundError:
    pass
links = gu2_int_monitoring_config.zabbix_ptk_styles[1:]
links.append(gu2_int_monitoring_config.zabbix_new_style)
files = [link.split('/')[-1] for link in links]
for file in files:
    try:
        os.remove('styles/' + file)
    except FileNotFoundError:
        pass

HTML_FILE = 'monitoring.html'
CSS_FILE = wget.download(gu2_int_monitoring_config.zabbix_ptk_styles[0])
SLEEP_PERIOD = 3

# Basic HTML/CSS
HTML_HEADER = """<!doctype html><html lang="en"><head>  <meta charset="utf-8">
  <title>Monitoring INT</title>
  <meta name="description" content="Monitoring INT">
  <meta name="author" content="pjasinski@bluesoft.com">
  <meta http-equiv="refresh" content="30"/>
  <link rel="stylesheet" href="css.css">
  <link rel="stylesheet" href="styles/main.css">
  <link rel="stylesheet" href="styles/dark-theme.css">
</head><body><h1>Monitoring INT {}</h1><div class="wrapper">""".format(datetime.now())
CUSTOM_CSS = """.information {background: #D6F6FF !important;}
.warning {background: #FFF6A5 !important;}
.average {background: #FFB689 !important;}
.high {background: #FF9999 !important;}
.disaster {background: #FF3838 !important;}
body {margin: 40px;}
.wrapper {display: grid;grid-template-columns: 50% 50%;grid-gap: 10px;}
.box {border-radius: 5px;padding: 20px;}"""
open(HTML_FILE, 'w').write(HTML_HEADER)
open(CSS_FILE, 'a').write(CUSTOM_CSS)
urls = gu2_int_monitoring_config.zabbix_ptk_styles[1:]
# urls.append(gu2_int_monitoring_config.zabbix_new_style)
for url in urls:
    wget.download(url, out='styles')

# Zabbix PTK
url = gu2_int_monitoring_config.zabbix_ptk_url
open(HTML_FILE, 'a').write("""<div class="box"><h2>Zabbix PTK</h2><h3><a href="{}">{}</a></h3>""".format(url, url))
driver.get(url)
element = driver.find_element_by_id('name')
element.send_keys(gu2_int_monitoring_config.zabbix_ptk_username)
element = driver.find_element_by_id('password')
element.send_keys(gu2_int_monitoring_config.zabbix_ptk_password)
driver.find_element_by_id('enter').click()
sleep(SLEEP_PERIOD)
last_issues = driver.find_element_by_id('hat_lastiss')
zabbix_ptk_content = last_issues.get_attribute('innerHTML')
open(HTML_FILE, 'a').write(zabbix_ptk_content + '</div>')

# Zabbix EAI TP
url = gu2_int_monitoring_config.zabbix_eai_tp_url
open(HTML_FILE, 'a').write("""<div class="box"><h2>Zabbix EAI TP</h2><h3><a href="{}">{}</a></h3>""".format(url, url))
driver.get(url)
sleep(SLEEP_PERIOD)
last_issues = driver.find_element_by_id('hat_lastiss')
zabbix_eai_tp_content = last_issues.get_attribute('innerHTML')
open(HTML_FILE, 'a').write(zabbix_eai_tp_content + '</div>')

# Zabbix OM TP
url = gu2_int_monitoring_config.zabbix_om_tp_url
open(HTML_FILE, 'a').write("""<div class="box"><h2>Zabbix OM TP</h2><h3><a href="{}">{}</a></h3>""".format(url, url))
driver.get(url)
element = driver.find_element_by_id('name')
element.send_keys(gu2_int_monitoring_config.zabbix_om_tp_username)
element = driver.find_element_by_id('password')
element.send_keys(gu2_int_monitoring_config.zabbix_om_tp_password)
driver.find_element_by_id('enter').click()
sleep(SLEEP_PERIOD)
last_issues = driver.find_element_by_id('hat_lastiss')
zabbix_om_tp_content = last_issues.get_attribute('innerHTML')
open(HTML_FILE, 'a').write(zabbix_om_tp_content + '</div>')

# Zabbix OV TP
url = gu2_int_monitoring_config.zabbix_ov_tp_url
open(HTML_FILE, 'a').write("""<div class="box"><h2>Zabbix OV TP</h2><h3><a href="{}">{}</a></h3>""".format(url, url))
driver.get(url)
element = driver.find_element_by_id('name')
element.send_keys(gu2_int_monitoring_config.zabbix_ov_tp_username)
element = driver.find_element_by_id('password')
element.send_keys(gu2_int_monitoring_config.zabbix_ov_tp_password)
driver.find_element_by_id('enter').click()
sleep(SLEEP_PERIOD)
last_issues = driver.find_element_by_id('lastiss')
zabbix_ov_tp_content = last_issues.get_attribute('innerHTML')
open(HTML_FILE, 'a').write(zabbix_ov_tp_content + '</div>')

# Zabbix NOWY
url = gu2_int_monitoring_config.zabbix_new_url
open(HTML_FILE, 'a').write("""<div class="box"><h2>Zabbix NOWY</h2><h3><a href="{}">{}</a></h3>""".format(url, url))
driver.get(url)
element = driver.find_element_by_id('name')
element.send_keys(gu2_int_monitoring_config.zabbix_new_username)
element = driver.find_element_by_id('password')
element.send_keys(gu2_int_monitoring_config.zabbix_new_password)
driver.find_element_by_id('enter').click()
sleep(SLEEP_PERIOD)
problems = driver.find_element_by_class_name('list-table')
zabbix_new_content = problems.get_attribute('innerHTML')
open(HTML_FILE, 'a').write('<table>' + zabbix_new_content + '</table></div>')

# Basic HTML
HTML_FOOTER = """</div></body></html>"""
open(HTML_FILE, 'a').write(HTML_FOOTER)

driver.close()
