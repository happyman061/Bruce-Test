#coding = utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import numpy
import pyautogui
import tkinter as tk




#获取网页
def get_url(url):
	driver = webdriver.Chrome()
	driver.maximize_window()
	while True:	
		driver.get(url)
		sleep(1)
		if driver.find_elements(By.CLASS_NAME,"ant-radio-input"):
			return driver
			break

#翻页、中断、报错
def next_page(driver):
	#print("翻页、中断、报错")
	if driver.find_element(By.CLASS_NAME,"survey-title").text == "结束页" and driver.find_elements(By.XPATH,"//*[contains(text(),'遗憾')]"):
		driver.quit()
		return 1
	elif driver.find_element(By.CLASS_NAME,"survey-title").text == "结束页":
		driver.quit()
		return 2
	elif driver.find_elements(By.CSS_SELECTOR,"a[role=\"button\"]"):
		nextpage=driver.find_element(By.CSS_SELECTOR,"a[role=\"button\"]")
		try:
			nextpage.click()
		except:
			sleep(1)
			nextpage.click()
			driver.switch_to.window(driver.window_handles[0])
			return 0
		else:
			driver.switch_to.window(driver.window_handles[0])
			return 0
	else:
		return 3


def list_boxs(driver):
	if driver.find_elements(By.CLASS_NAME,"age") or driver.find_elements(By.CLASS_NAME,"city"): #S1-S2
		boxs = driver.find_elements(By.CLASS_NAME,"ant-select-selector")
		for box in boxs:
			if box.is_displayed():
				pass
			else:
				boxs.remove(box)
		num = len(boxs)
		for i in range(num):
			box = boxs[i].find_element(By.CLASS_NAME,"ant-select-selection-search-input")
			box.click()
			box_list = driver.find_elements(By.CLASS_NAME,"ant-select-dropdown")[-1]
			if len(box_list.find_element(By.CLASS_NAME,"rc-virtual-list-holder-inner").find_elements(By.CLASS_NAME,"ant-select-item-option-content")) > 8: 
				m = random.randrange(20)
				for i in range(m):
					drag = box_list.find_element(By.CLASS_NAME,"rc-virtual-list-scrollbar").find_element(By.CLASS_NAME,"rc-virtual-list-scrollbar-thumb")
					ActionChains(driver).drag_and_drop_by_offset(drag,0,10).perform()
				options = box_list.find_element(By.CLASS_NAME,"rc-virtual-list-holder-inner").find_elements(By.CLASS_NAME,"ant-select-item-option-content")
				option = random.choice(options[1:-2])
				option.click()
			else:				
				options = box_list.find_element(By.CLASS_NAME,"rc-virtual-list-holder-inner").find_elements(By.CLASS_NAME,"ant-select-item-option-content")
				option = random.choice(options)
				option.click()

#下拉单选
def dropdown_radio(driver):
	if driver.find_elements(By.CLASS_NAME,"dropdown-radio"):#A2
		print("下拉单选")
		options = Select(driver.find_element(By.TAG_NAME,"select"))
		number = random.randint(1,len(options.options)-1)
		options.select_by_index(number)	

def matrix_radio(driver):
	#矩阵单选（含禁用，上下左右唯一）
	if  driver.find_elements(By.CLASS_NAME,"matrix_wrapper__2c6Kh") and driver.find_elements(By.CLASS_NAME,"matrix_openContainer__1xqzZ"): #A31-A32-A36-A37-A38-A56a-A56b
		print("矩阵单选(含渐显)")
		old_row = "None"
		while True:
			rows = driver.find_elements(By.TAG_NAME,"li")
			row = rows[-1]
			if row == old_row:
				break
			else:
				while True:
					option = random.choice(row.find_elements(By.CLASS_NAME,"ant-radio-input"))
					if option.is_enabled:
						option.click()
						break
				old_row = row 
		row_all = len(driver.find_elements(By.TAG_NAME,"li"))
		row_disable = len(driver.find_elements(By.CLASS_NAME,"matrix_titleRow__3Ab16"))
		radios = driver.find_elements(By.CLASS_NAME,"ant-radio-input")
		ges = driver.find_elements(By.CLASS_NAME,"matrix_openContainer__1xqzZ")
		radios_disable = driver.find_elements(By.CSS_SELECTOR,("input[disabled]"))
		row = int(row_all - row_disable)
		column = int(len(ges)/row)
		if len(radios) == len(ges):
			list1 = numpy.array(radios).reshape(row,column)
		else:
			list1 = numpy.array(ges).reshape(row,column)
			for i in range(row):
				for j in range(column):
					if list1[i][j].find_elements(By.CLASS_NAME,"ant-radio-input"):
						list1[i][j] = list1[i][j].find_element(By.CLASS_NAME,"ant-radio-input")
					else:
						list1[i][j] = False
		while True:
			row_index = random.randrange(row-1)
			column_index = random.randrange(column)
			if (list1[row_index][column_index] not in radios_disable) and (list1[row_index+1][column_index] not in radios_disable) and (list1[row_index][column_index] != False) and (list1[row_index+1][column_index] != False):
				list1[row_index][column_index].click()
				list1[row_index+1][column_index].click()
				break
		sleep(1)
		if (list1[row_index][column_index].is_selected()) and (list1[row_index+1][column_index].is_selected()) and not (driver.find_elements(By.XPATH,"//*[contains(text(),'最重要')]")):
			if radios_disable:
				for i in range(row):
					list2=[]
					for j in range(column):
						for radio_disable in radios_disable:
							if list1[i][j] != radio_disable:
								list2.append(list1[i][j])
					radio = random.choice(list2)
					radio.click()
			else:
				for i in range(row):
					radio = random.choice(list1[i])
					radio.click()

		elif (driver.find_elements(By.XPATH,"//*[contains(text(),'最重要')]")) and (driver.find_elements(By.XPATH,"//*[contains(text(),'以上均无')]")):
			list2 = list(range(column))
			if row > column:
				rows = random.sample(range(row),column)
			else:
				rows = range(row)
			old_j =0
			for i in rows:
				while True:
					j = random.choice(list2)
					if ((old_j < j) or ((old_j ==j) and (j == list2[-1])))  and (list1[i][j]):
						list1[i][j].click()
						old_j=j 
						break	
		else:
			list2 = list(range(column))
			if row > column:
				rows = random.sample(range(row),column)
			else:
				rows = range(row)
			try:
				for i in rows:	
					for j in list2:
						list3=list2
						if list1[i][j]:
							pass
						else:
							list3.remove(j)
					k = random.choice(list3)
					list1[i][k].click()
					list2.remove(k)
			except:
				pass

def ant_input(driver):
	#输入文本
	if driver.find_elements(By.CLASS_NAME,"questionContent_wrapper__1CciB") and driver.find_elements(By.CLASS_NAME,"ant-input") and driver.find_elements(By.CLASS_NAME,"matrix_wrapper__2c6Kh") and driver.find_elements(By.XPATH,"//*[contains(text(),'请填写')]") and driver.find_elements(By.CLASS_NAME,"matrix_titleRow__3Ab16"):
		rows_all = driver.find_elements(By.TAG_NAME,"li")
		rows_disable =  driver.find_elements(By.CLASS_NAME,"matrix_titleRow__3Ab16")
		rows = list(set(rows_all) -set(rows_disable))
		columns = rows_disable[-1].find_elements(By.XPATH,"//*[contains(text(),'请填写')]")
		options = driver.find_elements(By.CLASS_NAME,"ant-input")
		if len(options) == int(len(rows)*len(columns)):
			list1= numpy.array(options).reshape(len(rows),len(columns))
		for i in range(len(columns)):
			if columns[i].text == "请填写2（数字1~10）":
				index_10 = i 
			elif columns[i].text == "请填写3（整数1~100）":
				index_100 = i 
		for i in range(len(rows)):
			for j in range(len(columns)):
				if list1[i][j].get_attribute('value'):
					pass
				elif j == index_10:
					list1[i][j].send_keys(random.randint(1,10))
				elif j == index_100:
					list1[i][j].send_keys(random.randint(1,100))
				else:
					list1[i][j].send_keys("Bruce test!")
	elif driver.find_elements(By.CLASS_NAME,"base-input") and driver.find_elements(By.CLASS_NAME,"option-text") and driver.find_elements(By.CLASS_NAME,"q-content-option") and driver.find_elements(By.CLASS_NAME,"ant-input.option-input"):
		options = driver.find_elements(By.CLASS_NAME,"q-content-option")
		for option in options:
			if option.find_element(By.CLASS_NAME,"ant-input.option-input").get_attribute('value'):
	 			pass
			elif option.find_element(By.CLASS_NAME,"option-text").text == "请填写2（数字1~10）":
				option.find_element(By.CLASS_NAME,"ant-input.option-input").send_keys(random.randint(1,10))
			elif option.find_element(By.CLASS_NAME,"option-text").text == "请填写3（整数1~100）":
				option.find_element(By.CLASS_NAME,"ant-input.option-input").send_keys(random.randint(1,100))
			else:
				option.find_element(By.CLASS_NAME,"ant-input.option-input").send_keys("Bruce test!")
	elif driver.find_elements(By.CLASS_NAME,"ant-input"):
		for i in driver.find_elements(By.CLASS_NAME,"ant-input"):
			i.send_keys("Bruce test!")

def radio_page(driver):
	#多页单选（含禁用）
	if driver.find_elements(By.CLASS_NAME,"matrix-radio") and driver.find_elements(By.CLASS_NAME,"q-matrix-content"): #A34-A34a	
		print(r"多页单选（含禁用）")	
		pages = driver.find_elements(By.CSS_SELECTOR,("div[data-index]"))
		for page in pages:
			radios_all = page.find_elements(By.CLASS_NAME,"ant-radio-input")
			radios_disable = page.find_elements(By.CSS_SELECTOR,("input[disabled]"))
			radios = list(set(radios_all)-set(radios_disable))
			radio = random.choice(radios)
			radio.click()
			if driver.find_elements(By.CLASS_NAME,"ant-radio.ant-radio-checked") and driver.find_elements(By.CLASS_NAME,"anticon.anticon-right"):
				driver.find_element(By.CLASS_NAME,"anticon.anticon-right").click()
			driver.forward()
			driver.switch_to.window(driver.window_handles[0])
			sleep(1)
	elif driver.find_elements(By.CLASS_NAME,"age") or driver.find_elements(By.CLASS_NAME,"base-radio"):#S1-A1-A12-A13
			#单选
			print("单选")
			radios1 = driver.find_elements(By.CLASS_NAME,"ant-radio-input")
			radios2 = driver.find_elements(By.CSS_SELECTOR,("input[disabled]"))
			radios = list(set(radios1)-set(radios2))
			radio = random.choice(radios)
			radio.click()

def maxdiff_row(driver):
#左右单选
	if driver.find_elements(By.CLASS_NAME,"maxdiff-row"):#A33
		print("左右单选")
		radios = list(driver.find_elements(By.CLASS_NAME,"ant-radio-input"))
		row=int(len(radios)/2)
		list1 = numpy.array(radios).reshape(row,2)
		list2 = list(range(row))
		i=random.choice(list2)
		list1[i][0].click()
		list2.remove(i)
		j=random.choice(list2)		
		list1[j][1].click()

def drag_drop(driver):
#拖拽
	#拖拽——一对一
	if driver.find_elements(By.CSS_SELECTOR,("div[data-rbd-draggable-id]")) and driver.find_elements(By.CLASS_NAME,"ant-checkbox"):#A-36b
		print("拖拽——一对一")
		sources = list(driver.find_elements(By.CLASS_NAME,"ant-checkbox"))
		targets = []
		bkgs = driver.find_elements(By.XPATH,"//div//div[starts-with(@style,'background')]")
		for bkg in bkgs:
			if bkg.find_elements(By.XPATH,"div[starts-with(@style,'margin')]"):
				targets.append(bkg.find_element(By.XPATH,"div[starts-with(@style,'background')]"))
		for source in sources:
			target = random.choice(targets)
			pyautogui.moveTo(source.location['x']+20,source.location['y']+110)
			pyautogui.dragTo(target.location['x']+20,target.location['y']+155,duration=1)
			targets.remove(target)
		sleep(1)
	elif driver.find_elements(By.CSS_SELECTOR,("div[data-rbd-draggable-id]")):#A35-A35a-A54-A54a
		print("拖拽——一对多、多对多")
		sources = driver.find_elements(By.CSS_SELECTOR,("div[data-rbd-draggable-id]"))
		all_targets = driver.find_elements(By.XPATH,"//div[starts-with(@style,'display')]//div[starts-with(@style,'background')]")
		for source in sources:
			target = random.choice(all_targets)
			pyautogui.moveTo(source.location['x']+20,source.location['y']+125)
			pyautogui.dragTo(target.location['x']+20,target.location['y']+155,duration=1)
		sleep(1)
		sources_after =  driver.find_elements(By.CSS_SELECTOR,("div[data-rbd-draggable-id]"))
		if len(sources_after) > len(sources):
			maxnum = len(all_targets)
			result = True
			while result:
				for source in sources:
					targets	= random.sample(all_targets,random.randint(1,maxnum))
					for target in targets:
						pyautogui.moveTo(source.location['x']+20,source.location['y']+125)
						pyautogui.dragTo(target.location['x']+20,target.location['y']+155,duration=1)
					sleep(1)
				list2 = []
				for target in all_targets:
					if target.find_elements(By.CSS_SELECTOR,("div[data-rbd-draggable-id]")):
						list2.append("True")
					else:
						list2.append("False")
				if "False" in list2:
					result = True
				else:
					result = False

#下拉单选一对一
def matrix_select(driver):
	if driver.find_elements(By.CLASS_NAME,"matrixSelect_wrapper__2jcBe"):#A36a
		print("下拉单选一对一")
		columns = driver.find_elements(By.CLASS_NAME,"ant-select-selector")
		for column in columns:
			column.click()
			sleep(1)
			options = driver.find_elements(By.CLASS_NAME,"ant-select-item.ant-select-item-option")[-5:]
			options_disable =driver.find_elements(By.CLASS_NAME,"ant-select-item.ant-select-item-option.ant-select-item-option-disabled") 
			list1 = list(set(options)-set(options_disable))
			option = random.choice(list1)
			option.click()

def matrix_checkbox(driver):
	#矩阵多选——翻页
	if driver.find_elements(By.XPATH,"//div[starts-with(@class,'matrixCard')]") and driver.find_elements(By.CLASS_NAME,"slick-list") and driver.find_elements(By.CLASS_NAME,"matrix-checkbox") and driver.find_elements(By.CLASS_NAME,"slick-slide"):#A52
		print("矩阵多选——翻页")
		pages = driver.find_elements(By.CSS_SELECTOR,("div[data-index]"))
		for page in pages:
			options_all = page.find_elements(By.CLASS_NAME,"ant-checkbox-input")
			options_disable = page.find_elements(By.CSS_SELECTOR,("input[disabled]"))
			options = list(set(options_all)-set(options_disable))
			num = random.randint(1,len(options))
			for option in random.sample(options,num):
				option.click()
			if driver.find_elements(By.CLASS_NAME,"anticon.anticon-right"):
				driver.find_element(By.CLASS_NAME,"anticon.anticon-right").click()
			driver.forward()
			driver.switch_to.window(driver.window_handles[0])
			sleep(1)			
	elif  driver.find_elements(By.CLASS_NAME,"ant-table-row.ant-table-row-level-0") and driver.find_elements(By.CLASS_NAME,"ant-table.ant-table-bordered") and driver.find_elements(By.CLASS_NAME,"cell-div") and driver.find_elements(By.CLASS_NAME,"ant-table-container"): #A51-A51b-A53-A55
		print(r"矩阵多选——禁用、互斥、逐显")
		rows_all = driver.find_elements(By.CLASS_NAME,"ant-table-row.ant-table-row-level-0")
		rows_disable = driver.find_elements(By.CLASS_NAME,"ant-table-row.ant-table-row-level-0.custom-head")
		rows = list(set(rows_all)-set(rows_disable))
		for row in rows:
			if row.find_elements(By.CLASS_NAME,"ant-checkbox-input"):
				options_all = row.find_elements(By.CLASS_NAME,"ant-checkbox-input")
				options_disable = row.find_elements(By.CSS_SELECTOR,("input[disabled]"))
				options = list(set(options_all)-set(options_disable))
				option =random.choice(options)
				if option.is_selected():
					pass
				else:
					option.click()
				sleep(1)
				options_all2 = row.find_elements(By.CLASS_NAME,"ant-checkbox-input")
				options2 = list(set(options_all2) - set(options_disable))
				options2.remove(option)
				maxnum = len(options2)
				num = random.randint(0,maxnum)
				for option in random.sample(options2,num):
					if option.is_selected():
						pass
					else:					
						option.click()
				sleep(2)
		while True:
			rows_old = rows_all
			old_row = len(rows_all)
			rows_all = driver.find_elements(By.CLASS_NAME,"ant-table-row.ant-table-row-level-0")
			new_row = len(rows_all)	
			if new_row == old_row:
				break
			else:
				last_rows = list(set(rows_all) - set(rows_old))
				last_row = last_rows[-1]
				options_all = last_row.find_elements(By.CLASS_NAME,"ant-checkbox-input")
				options_disable = last_row.find_elements(By.CSS_SELECTOR,("input[disabled]"))
				options = list(set(options_all)-set(options_disable))
				option =random.choice(options)
				if option.is_selected():
					pass
				else:
					option.click()
				sleep(1)
				options_all2 = last_row.find_elements(By.CLASS_NAME,"ant-checkbox-input")
				options2 = list(set(options_all2) - set(options_disable))
				options2.remove(option)
				maxnum = len(options2)
				num = random.randint(0,maxnum)
				for option in random.sample(options2,num):
					if option.is_selected():
						pass
					else:					
						option.click()
				rows_old=rows_all
				sleep(2)
	elif driver.find_elements(By.CLASS_NAME,"base-checkbox") and driver.find_elements(By.CLASS_NAME,"ant-checkbox"):  #A4-A56
		print("多选互斥")
		maxnum = 4
		options1 = driver.find_elements(By.CLASS_NAME,"ant-checkbox-input")
		option1 = random.choice(options1)
		sleep(1)
		option1.click()
		options2 = driver.find_elements(By.CLASS_NAME,"ant-checkbox-input")
		options2.remove(option1)
		if options2:
			num = random.randrange(maxnum)
			options = random.sample(options2,num)
			for option in options:
				option.click()
		sleep(2)

def read_input():
	print(r"https://answer.91question.com/91/27c6cde183c14131ba15a98d377eb918?test=1")
	cycs = int(input("请输入需要循环的次数："))
	url = str(input("请输入需要测试的网址："))
	#url = "https://answer.91question.com/91/27c6cde183c14131ba15a98d377eb918?test=1"
	#cycs = int(1)
	return cycs,url

def show_title(driver):
	if driver.find_element(By.CLASS_NAME,"survey-title").text == "结束页":
		pass
	else:
		title1 = driver.find_element(By.CLASS_NAME,"q-title-code").text
		title2 = driver.find_element(By.CLASS_NAME,"QTitle_q_title_text__3cVtW").text
		print(f"现在操作题目：{title1}{title2}")



if __name__ == '__main__':
	breaknum = 0
	finnum = 0
	errnum = 0
	cycs,url = read_input()
	for cyc in range(cycs):
		result = 0
		driver = get_url(url)
		while True:
			sleep(1)
			show_title(driver)
			radio_page(driver)
			list_boxs(driver)
			dropdown_radio(driver)
			matrix_radio(driver)
			maxdiff_row(driver)		
			drag_drop(driver)
			matrix_select(driver)		
			matrix_checkbox(driver)
			ant_input(driver)
			result = next_page(driver)
			if result == 1:
				breaknum += 1
				break
			elif result == 2:
				finnum += 1
				break	
			elif result == 0:
				pass
			elif result == 3:
				errnum += 1
				break		
			else:
				errnum += 1
				break

print(f"总共的测试次数：{cycs}")
print(f"不符合要求中止的测试次数：{breaknum}")
print(f"正常完成的测试次数：{finnum}")
print(f"异常中断的测试次数：{errnum}")	

		

			


