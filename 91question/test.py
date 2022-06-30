from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.keys import Keys
from time import sleep
import os
import random
import numpy

result1 = True
result2 = True
result3 = True
result4 = True
result5 = True
browser = webdriver.Chrome()
url = "https://answer.91question.com/91/27c6cde183c14131ba15a98d377eb918?test=1"
browser.get(url)
sleep(1)
while result4:
	radios4 = browser.find_elements(By.CSS_SELECTOR,("input[type='radio']"))
	if radios4:
		radio4 = random.choice(radios4)
		radio4.click()
		sleep(1)
		tags = browser.find_elements(By.CSS_SELECTOR,("input[type='search']"))
		tags[0].click()
		years = browser.find_elements(By.CLASS_NAME,"ant-select-item-option-content")
		year = random.choice(years[:5])
		sleep(1)
		year.click()
		tags[1].click()
		months = browser.find_elements(By.CLASS_NAME,"ant-select-item-option-content")
		month = random.choice(months[-5:-2])
		sleep(1)
		month.click()
		next=browser.find_element(By.CSS_SELECTOR,"a[role=\"button\"]")
		next.click()
		sleep(3)
		browser.switch_to.window(browser.window_handles[0])
	else:
		result4 = False

while result5 :
		#print(f"browser text = {browser.page_source}")
		browser.maximize_window()
		provinces1= browser.find_element(By.ID,"rc_select_2")
		provinces1.click()

		#print(f"browser text = {browser.page_source}")
		provinces2 =browser.find_elements(By.CLASS_NAME,"ant-select-item-option-content")
		#provinces2 = browser.find_elements(By.XPATH,"/html/body/div[2]/div/div/div/div[2]/div[1]/div/div/div")
		#print(provinces2)
		#break
		#for i in provinces2:
		#	print(i.get_attribute('textContent'))
		#	print(i)
		#break

		#province=random.choice(provinces2[:8])
		province=provinces2[0]
		sleep(2)
		province.click()
		#ul = driver.find_element_by_css_selector("div#select2_container > ul")
		citys1 = browser.find_element(By.ID,"rc_select_3")

		citys1.click()
		#print(f"browser text = {browser.page_source}")
		#break

		citys2 = browser.find_elements(By.XPATH,"/html/body/div[3]/div/div/div/div[2]/div[1]/div/div/div")
		#citys2 = browser.find_elements(By.CLASS_NAME,"ant-select-item-option-content")
		for i in citys2:
			print(i.get_attribute('textContent'))
			#print(i.get_attribute('innerHTML'))
			#print(browser.execute_script("return arguments[0].innerHTML",i))
			#print(browser.execute_script("return arguments[0].textContent",i))
			#browser.execute_script("arguments[0].text",i)
			#print(i.get_attribute("value"))
			print(i)
		break		
		#print(len(citys2))
		#city = random.choice(citys2)
		#sleep(2)
		#city.click()
		break
	#tags = browser.find_elements(By.CSS_SELECTOR,("input[type='search']"))
'''
	if tags:
		tags[0].click()
		shens = browser.find_elements(By.CLASS_NAME,"ant-select-item-option-content")
		#shen = random.choice(shens[:8])
		
		sleep(1)
		shen.click()
		sleep(1)
		tags[1].click()
		sleep(1)
		#print(f"browser text = {browser.page_source}")
		shis = browser.find_elements(By.CLASS_NAME,"ant-select-item-option-content")
		print(shis)
		#shis = browser.find_elements(By.CLASS_NAME,"ant-select-selection-search")
	
	
		#shi = random.choice(shis[-8:])
		#shi.click()
		#print(f"browser text = {browser.page_source}")
		break
'''
'''
while result1:
	radios1 = browser.find_elements(By.CSS_SELECTOR,("input[type='radio']"))
	if radios1:
		radio1 = random.choice(radios1)
		if radio1.is_selected():
			pass
		else:
			radio1.click()
			sleep(1)
			if browser.find_elements(By.CLASS_NAME,"ant-input"):
				browser.find_element(By.CLASS_NAME,"ant-input").send_keys("this is bruce test!")
			sleep(1)

		next=browser.find_element(By.CSS_SELECTOR,"a[role=\"button\"]")
		next.click()
		sleep(3)
		browser.switch_to.window(browser.window_handles[0])
	else:
		result1 = False

print('-----------------')

while result2:
	select = browser.find_elements(By.CLASS_NAME,"dropdown-radio")
	if select:
		select = browser.find_element(By.CLASS_NAME,"dropdown-radio")
		tags =select.find_elements(By.TAG_NAME,"option")
		tag = random.choice(tags)
		tag.click()
		sleep(1)
		next=browser.find_element(By.CSS_SELECTOR,"a[role=\"button\"]")
		next.click()
		sleep(3)
		browser.switch_to.window(browser.window_handles[0])
	else:
		result2 = False

print('-----------------')

while result3:
	radios2 = browser.find_elements(By.CSS_SELECTOR,("input[type='radio']"))
	if radios2:
		num = int(len(radios2)/5)
		list2 = numpy.array(radios2).reshape(num,5)
		print(list2)
		for i in range(0,num):
			print('11111')
			print(list2[i])
			print('2222222')
			radio2 = random.choice(list2[i])
			radio2.click()
			sleep(1)

			if browser.find_elements(By.CLASS_NAME,"ant-input"):
				browser.find_element(By.CLASS_NAME,"ant-input").send_keys("bruce test!")
				sleep(1)

			if browser.find_elements(By.CSS_SELECTOR,"a[data-icon=\"right\"]"):
				print(browser.find_element(By.CSS_SELECTOR,"a[data-icon=\"right\"]"))
				browser.find_element(By.CSS_SELECTOR,"a[data-icon=\"right\"]").click()
				sleep(1)
				browser.switch_to.window(browser.window_handles[0])
		next=browser.find_element(By.CSS_SELECTOR,"a[role=\"button\"]")
		next.click()
		sleep(3)
		browser.switch_to.window(browser.window_handles[0])
	else:
		result3 = False

'''

'''
if browser.find_element(By.CLASS_NAME,"survey-title"):
	sleep(3)
	browser.quit()
#browser.forward()
#print(f"browser text = {browser.page_source}")
#browser.quit()




#root > div > div.ant-spin-nested-loading > div > div > div.question-content > div > div:nth-child(2) > div > div > div > div:nth-child(2) > div > label > span > input
#root > div > div.ant-spin-nested-loading > div > div > div.question-content > div > div:nth-child(2) > div > div > div > div:nth-child(2) > div > label > span > 

'''
		n = next_page(driver)
		sleep(1)
		list_box(driver,"rc_select_2","/html/body/div[2]/div/div/div/div[2]/div[1]/div/div/div","/html/body/div[2]/div/div/div/div[2]/div[2]/div")
		sleep(1)
		list_box(driver,"rc_select_3","/html/body/div[3]/div/div/div/div[2]/div[1]/div/div/div","/html/body/div[3]/div/div/div/div[2]/div[2]/div")
		sleep(1)
		n = next_page(driver)
		sleep(1)
		single_radio(driver,"ant-radio-input")
		n = next_page(driver)
		sleep(1)
		single_radio(driver,"ant-radio-input")
		n = next_page(driver)
		sleep(1)
		single_radio(driver,"ant-radio-input")
		n = next_page(driver)
		sleep(1)
		dropdown_radio(driver,"dropdown-radio")
		n = next_page(driver)
		sleep(1)		

'''




'''
	driver.implicitly_wait(20)
	print("It is OK!")
	next_page(driver)
	driver.quit()

	print("it is OK!")
'''


			print(row_ele,len(row_ele))
			print(row_ele[1])
			print(row_ele[1].text)
			print(row_ele[1].get_attribute('textContent'))
			print(row_ele[1].get_attribute('innerHTML'))
			print(driver.execute_script("return arguments[0].innerHTML",row_ele[1]))
			print(driver.execute_script("return arguments[0].textContent",row_ele[1]))
			print(driver.execute_script("arguments[0].text",row_ele[1]))
			print(row_ele[1].get_attribute("value"))
'''

			
				
'''
		if  driver.find_elements(By.ID,"1466639249002909710"):
			print("new")
			rows = driver.find_elements(By.CLASS_NAME,"ant-table-row.ant-table-row-level-0")
			rows_disable = driver.find_elements(By.CLASS_NAME,"ant-table-row.ant-table-row-level-0.custom-head")
			rest_rows = list(set(rows)-set(rows_disable))
			print(rows,len(rows))
			print(rows_disable,len(rows_disable))
			print(rest_rows,len(rest_rows))

			break

'''
			



'''
			print(options_all1,len(options_all1))
			print(options_disable1,len(options_disable1))
			print(options1,len(options1))
			print(option1)
			print("-----------------")
			print(options_all2,len(options_all2))
			print(options_disable1,len(options_disable1))
			print(options2,len(options2))
			print(num,maxnum)
			print("======================")	
'''



