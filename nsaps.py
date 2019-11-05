#!/usr/bin/python3

"""
Spyder Editor

This is a script file for gathering nsaps fairs
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests, bs4, csv, os, csv

csvinfilename='nsaps_in.csv'
csvoutfilename='nsaps_out.csv'
nsaps_url='https://secure.onr.navy.mil/nsap/view_science_fair.aspx'
fair_field='ctl00_ContentPlaceHolder1_DD3'
ids=[]
data = csv.reader(open(csvinfilename, 'rt'))
for row in data:
	ids.append(str(row[0]))

print(ids)

browser=webdriver.Firefox()
browser.get('https://secure.onr.navy.mil/nsap/view_science_fair.aspx')

judge_list={}
judges_x='//*[@id="ctl00_ContentPlaceHolder1_FairData"]/table[3]/tbody/tr/td[1]/p'
presenters_x='//*[@id="ctl00_ContentPlaceHolder1_FairData"]/table[3]/tbody/tr/td[2]/p'

for id in ids:
	xpath="//select[@id='"+fair_field+"']/option[@value='"+id+"']"
	try:	
		option=browser.find_element_by_xpath(xpath).click()
	except:
		continue
	try:
		waiter=WebDriverWait(browser, 7).until(EC.text_to_be_present_in_element((By.XPATH,'//*[@id="ctl00_ContentPlaceHolder1_FairData"]/p[1]/b'), id))
	except: continue
	
	judges=browser.find_element_by_xpath(judges_x).get_attribute('innerHTML')
	presenters=browser.find_element_by_xpath(presenters_x).get_attribute('innerHTML')

	out=judges[18:].replace('\n','').replace('<br>',' ').replace('  ','')+' '+presenters[22:].replace('\n','').replace('<br>',' ').replace('  ','')

	judge_list[id]=out

headers=['fair id', 'judges/presenters']
csvOut=open(csvoutfilename, 'w', newline='')
csvWriter=csv.writer(csvOut)
csvWriter.writerow(headers)

for fair in judge_list:
	row=[fair, judge_list[fair]]
	csvWriter.writerow(row)

csvOut.close()





