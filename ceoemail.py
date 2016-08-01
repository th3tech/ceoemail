#!/usr/bin/env python

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.proxy import *
from HTMLParser import HTMLParser
from BeautifulSoup import BeautifulSoup as bs
from pyvirtualdisplay import Display

import time
import argparse

def ChangeProxy(ProxyHost ,ProxyPort):
    print "Define Firefox Profile " + ProxyHost + " : " + ProxyPort
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.http", ProxyHost )
    profile.set_preference("network.proxy.http_port", int(ProxyPort))
    profile.set_preference("general.useragent.override","Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0")
    profile.update_preferences()
    return webdriver.Firefox(firefox_profile=profile)

def FixProxy():
    print "Reset Firefox Profile"
    profile = webdriver.FirefoxProfile()
    profile.set_preference("network.proxy.type", 0)
    return webdriver.Firefox(firefox_profile=profile)

parser = argparse.ArgumentParser(description='Scrape ceoemail')
parser.add_argument('-p', '--proxy', type=str, required=True)
parser.add_argument('-t', '--port', type=str, required=True)
parser.add_argument('-l', '--loop', type=str, required=True)
parser.add_argument('-u', '--url', type=str, required=True)
args = parser.parse_args()
print "Args loaded"

display = Display(visible=0, size=(800, 600))
display.start()
print "Display started"
browser = ChangeProxy(args.proxy,args.port)
#browser = webdriver.Firefox()
browser.get(args.url)
html = browser.page_source.encode('ascii', 'xmlcharrefreplace')
exit = 0
while exit == 0:
        if "email addresses found" not in html:
                browser.implicitly_wait(10)
		print "Waiting..."
		html = browser.page_source.encode('ascii', 'xmlcharrefreplace')
	else:
		exit = 1
html = browser.page_source.encode('ascii', 'xmlcharrefreplace')
print html
counter = 0
elements = browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % 's.php?id=ceo')
for counter in range(counter, len(elements)):
	elements = browser.find_elements_by_xpath('//a[contains(@href, "%s")]' % 's.php?id=ceo')
	print elements[counter].get_attribute('href')
	if args.loop > counter: 
		elements[counter].click()
		source = browser.page_source.encode('ascii', 'xmlcharrefreplace')
		if "mailto" in source:
			print source
		else:
			print "Failed ",counter," Proxy: ",args.proxy," URL: ",elements[counter]
	else:
		print "Skipped ",counter
	browser.back()
	time.sleep(5)
browser.quit()
