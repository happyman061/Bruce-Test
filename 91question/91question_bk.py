#coding = utf-8


from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import numpy



def get_url():	
	driver = webdriver.Chrome()
	driver.maximize_window()
	while True:	
		url = "https://answer.91question.com/91/27c6cde183c14131ba15a98d377eb918?test=1"
		driver.get(url)
		sleep(1)
		if driver.find_elements(By.CLASS_NAME,"ant-radio-input"):
			return driver
			break


def next_page(driver):	
	if driver.find_elements(By.CSS_SELECTOR,"a[role=\"button\"]"):
		nextpage=driver.find_element(By.CSS_SELECTOR,"a[role=\"button\"]")
		nextpage.click()
		#sleep(1)
		driver.switch_to.window(driver.window_handles[0])
		#sleep(1)
		return 0
	else:
		return 1



def single_radio(diver):
	if driver.find_elements(By.CLASS_NAME,"ant-radio-input"):
		radios1 = driver.find_elements(By.CLASS_NAME,"ant-radio-input")
		radios2 = driver.find_elements(By.CSS_SELECTOR,("input[disabled]"))
		radios = list(set(radios1)-set(radios2))
		radio = random.choice(radios)
		radio.click()



def list_box(driver,id,xpath1,xpath2):
	if driver.find_elements(By.CLASS_NAME,"ant-select-selector"):
		if driver.find_elements(By.ID,id):
			listbox = driver.find_element(By.ID,id)
			listbox.click()
			if len(driver.find_elements(By.XPATH,xpath1)) > 8:
				m=random.randint(0,20)
				for i in range(m):
					drag = driver.find_element(By.XPATH,xpath2)
					ActionChains(driver).drag_and_drop_by_offset(drag,0,10).perform()
					#driver.implicitly_wait(5)
				elements = driver.find_elements(By.XPATH,xpath1)
				element = random.choice(elements[1:-2])
				sleep(1)
				element.click()	
			else:
				elements = driver.find_elements(By.XPATH,xpath1)
				element = random.choice(elements)
				sleep(1)
				element.click()	

def list_boxs(driver,id1,xpath1,xpath2,id2,xpath3,xpath4):
		list_box(driver,id1,xpath1,xpath2)
		#sleep(1)
		list_box(driver,id2,xpath3,xpath4)
		#sleep(1)

def dropdown_radio(driver,classname):
	if driver.find_elements(By.CLASS_NAME,classname):
		options = Select(driver.find_element(By.TAG_NAME,"select"))
		number = random.randint(1,len(options.options)-1)
		options.select_by_index(number)	
	#sleep(1)		

def matrix_radio(driver):
	radios1 = driver.find_elements(By.CLASS_NAME,"ant-radio-input")
	radios1_disable = driver.find_elements(By.CSS_SELECTOR,("input[disabled]"))
	row = len(driver.find_elements(By.TAG_NAME,"li"))-1
	column = int(len(radios1)/row)
	list1 = numpy.array(radios1).reshape(row,column)
	if radios1_disable:
		for i in range(row):
			list2=[]
			for j in range(column):
				for radio_disable in radios1_disable:
					if list1[i][j] != radio_disable:
						list2.append(list1[i][j])
			radio = random.choice(list2)
			radio.click()
	else:
		for i in range(row):
			radio = random.choice(list1[i])
			radio.click()

def ant_input(driver):
	if driver.find_elements(By.CLASS_NAME,"ant-input"):
		for i in driver.find_elements(By.CLASS_NAME,"ant-input"):
			i.send_keys("Bruce test!")

def matrix_card(driver):
	radios = list(driver.find_elements(By.CLASS_NAME,"ant-radio-input"))
	radios_disable = driver.find_elements(By.CSS_SELECTOR,("input[disabled]"))
	row = len(driver.find_elements(By.CSS_SELECTOR,("div[data-index]")))
	column = int(len(radios)/row)
	list1 = numpy.array(radios).reshape(row,column)
	if radios_disable:
		for i in range(row):
			list2=[]
			for j in range(column):
				for radio_disable in radios_disable:
					if list1[i][j] != radio_disable:
						list2.append(list1[i][j])
			radio = random.choice(list2)
			radio.click()
			if driver.find_elements(By.CLASS_NAME,"ant-radio.ant-radio-checked") and driver.find_elements(By.CLASS_NAME,"anticon.anticon-right"):
				driver.find_element(By.CLASS_NAME,"anticon.anticon-right").click()
			driver.forward()
			driver.switch_to.window(driver.window_handles[0])
			sleep(1)			
	else:
		for i in range(row):
			radio = random.choice(list1[i])
			radio.click()
			if driver.find_elements(By.CLASS_NAME,"ant-radio.ant-radio-checked") and driver.find_elements(By.CLASS_NAME,"anticon.anticon-right"):
				driver.find_element(By.CLASS_NAME,"anticon.anticon-right").click()
			driver.forward()
			driver.switch_to.window(driver.window_handles[0])
			sleep(1)

def maxdiff_row(driver):
	if driver.find_elements(By.CLASS_NAME,"maxdiff-row"):
		radios = list(driver.find_elements(By.CLASS_NAME,"ant-radio-input"))
		row=int(len(radios)/2)
		list1 = numpy.array(radios).reshape(row,2)
		list2 = list(range(row))
		i=random.choice(list2)
		list1[i][0].click()
		list2.remove(i)
		j=random.choice(list2)		
		list1[j][1].click()



if __name__ == '__main__':
	stopnum = 0
	driver = get_url()
	while True:
		sleep(1)
		if driver.find_elements(By.CLASS_NAME,"matrix-radio"):
			matrix_card(driver)
		elif driver.find_elements(By.CLASS_NAME,"matrix_wrapper__2c6Kh"):
			matrix_radio(driver)
		else:
			single_radio(driver)
		ant_input(driver)
		maxdiff_row(driver)
		list_boxs(driver,"rc_select_0","/html/body/div[2]/div/div/div/div[2]/div[1]/div/div/div","/html/body/div[2]/div/div/div/div[2]/div[2]/div","rc_select_1","/html/body/div[3]/div/div/div/div[2]/div[1]/div/div/div","/html/body/div[3]/div/div/div/div[2]/div[2]/div")
		list_boxs(driver,"rc_select_2","/html/body/div[2]/div/div/div/div[2]/div[1]/div/div/div","/html/body/div[2]/div/div/div/div[2]/div[2]/div","rc_select_3","/html/body/div[3]/div/div/div/div[2]/div[1]/div/div/div","/html/body/div[3]/div/div/div/div[2]/div[2]/div")
		dropdown_radio(driver,"dropdown-radio")


		if driver.find_elements(By.CSS_SELECTOR,("div[data-rbd-drag-handle-draggable-id]")):
			sources = driver.find_elements(By.CSS_SELECTOR,("div[data-rbd-draggable-id]"))
			#targets = driver.find_elements(By.XPATH,"/html/body/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div[3]/div")
			#print(sources,type(sources),len(sources))
			#print(targets,type(targets),len(targets))
			#for i in range(5):
			#	print(sources[i].text)
			#	print(targets[i].text)
			#	print(targets[i]
			target = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div[3]/div[1]")
			print(target.location,target.size)
			source = sources[0]
			#source = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div[1]/div[1]")
			print(source.location,source.text,source.size)
			#for i in range(20):
			#driver.switch_to.frame('iframeResult')
			ActionChains(driver).drag_and_drop_by_offset(source,10,250).perform()
			#action = ActionChains(driver)
			#action.move_to_element(source).perform()
			#print("1：",source.location)
			#action.click_and_hold().perform()
			#action.move_to_element(target).perform()
			#print("2:",source.location)
			#action.release().perform()
			#print("3:",source.location)

			#driver.implicitly_wait(5)
			sleep(1)
			break


		n = next_page(driver)
		print("it is OK!")	
		if n == 1 :
			stopnum += 1
			print(stopnum)
			driver.quit()
			break

