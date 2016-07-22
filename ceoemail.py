#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup as bs
from pyvirtualdisplay import Display

import argparse

parser = argparse.ArgumentParser(description='Scrape Factual')
parser.add_argument('-p', '--proxy', type=str, required=True)
parser.add_argument('-u', '--url', type=str, required=True)
args = parser.parse_args()
print args.proxy 
print args.url

webdriver.DesiredCapabilities.FIREFOX['proxy']={
	"httpProxy":args.proxy,
	"ftpProxy":args.proxy,
	"sslProxy":args.proxy,
	"noProxy":None,
	"proxyType":"MANUAL",
	"autodetect":False
}

display = Display(visible=0, size=(800, 600))
display.start()
browser = webdriver.Firefox()
browser.get(args.url)
html = browser.page_source.encode('ascii', 'xmlcharrefreplace')
soup = bs(html)
links = browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % 's.php?id=ceo')
for link in links:
	print link.get_attribute('href')
	browser.implicitly_wait(30)
	link.click()
	source = browser.page_source.encode('ascii', 'xmlcharrefreplace')
	print source
	browser.get(args.url)
browser.quit()
