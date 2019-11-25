#!/usr/bin/python3
import logging
import pytesseract 
import time 
import re 
import os
import sys
import pandas as pd
from PIL import Image 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from googlesearch import search
   
# '''Function to validate the input file'''   
current_path = os.getcwd()

def readPath():
	file_name = input("Enter the input xlsx file name: ")
	file_path =  current_path + '/' + file_name
	if (os.path.exists(file_path)):
		return file_path
	else:
		print("File entered is invalid/not exist in current folder")
		logging.info("File entered is invalid/not exist in current folder")
		sys.exit()
   
# '''E-mail ID extractor'''
def extract_emails(file_name): 
	print("Email Extraction started")
	logging.info("Email Extraction started")
	dframe = pd.read_excel(file_name, sheet_name = "Sheet1",header = None)
	domain_list = list(dframe[0].astype("str"))
   
	#'''launch the Web Browser'''
	driver = webdriver.Chrome()
	#driver = webdriver.Firefox() For firefox users   
	driver.maximize_window()
   
	total_emails = set()
	for url in domain_list:
		start = time.time()
   
		email = set()
		ocr_file = current_path + "/" +  "out_text.txt"
		screen_shot1 = current_path + "/" +"1.png"   
   		
		# File is opened in 'a+' mode to avoid open twice for write and read write
		f = open(ocr_file, "a+") 
   		
		# some domain names may not start with 'www'
		try:
			url = (url.split('www.')[1]).split('/')[0]
		except:
			url = (url.split('//')[1]).split('/')[0]
   		
		print("URL:",url)
		logging.info("URL:{a}".format(a = url))
   		
		#creating the search URL and sending the request 
		search_link = "https://www.google.com/search?q=emails+" + url + '"' + "&num=28"
		driver.get(search_link)
   
		# zoom the screen so that OCR is applied effectively
		size = "document.body.style.zoom='139%'"
		driver.execute_script(size)
		time.sleep(2)
   
		#getting the element of the body to take a screenshot
		el = driver.find_element_by_tag_name('body')
		el.screenshot(screen_shot1)

		#applying OCR on the screenshot image
		text = str(((pytesseract.image_to_string(Image.open(screen_shot1))))) 
		text = text.replace('-\n', '')	 
		f.write(text) 
   		
		#extracting the e-mail ID's and updating them in temporary storage to print and the permanent storage to update the sheet
		f.seek(0, 0)
		text  = f.read()
		email.update(re.findall(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)", text, re.I))
		total_emails.update(email)
		for i in email:
			print(i)
		logging.info("Emails for the link: {a} ==>  {b}".format(a = url, b = email ))
   
		f.close() 
		os.remove(ocr_file)
		end = time.time()
		print("Time taken to get mails in %s ==>  %s" %(url, round((end - start),2)))
		logging.info("Time taken to get mails in {a} ==>  {b}".format(a = url, b = round((end - start),2)))
	driver.close()
	os.remove(screen_shot1)
   	
	writer = pd.ExcelWriter(file_name, engine="openpyxl", mode = 'a')
	df = pd.DataFrame(total_emails)
	df.to_excel(writer,"Sheet2",index = False)
	writer.save()
	writer.close()   
   
	#Driver function
def main():
	file_name = readPath()
	log_file_name = (file_name.split('/')[-1]) + "_mail_extractor.log"
	logging.basicConfig(filename = log_file_name, format = '%(asctime)s %(message)s', filemode='w') 
	logger=logging.getLogger() 
	logger.setLevel(logging.INFO)
	extract_emails(file_name)
   
if __name__== "__main__":
	main()

