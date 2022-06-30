#coding = utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import time
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
import numpy
import pyautogui
import tkinter as tk
from tkinter import ttk
import os 
import sys


#获取网页
def get_url(url):
	#options=webdriver.ChromeOptions()
	#options.add_argument('--headless')
	#driver = webdriver.Chrome(options=options)
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

def auto_test(url,runs):
	breaknum = 0
	finnum = 0
	errnum = 0
	for run in range(runs):
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
	list1=[finnum,breaknum,errnum]
	return list1

def gui_interface():
#图形界面
	global list1
	list1=[]
	root=tk.Tk()
	root.title(u"永钥科技")
	root.geometry("800x600")
	root.resizable(width=False,height=False)
	fm1=tk.Frame(root)
	content=u"永钥科技自动化测试工具V1.0"
	title_label=tk.Label(fm1,font=("黑体",20),height=4,text=content)
	title_label.pack()
	fm1.pack(side="top",fill="x")
	fm2=tk.Frame(root)
	fm2_left=tk.Frame(fm2)
	fm2_right=tk.Frame(fm2)
	url_label=tk.Label(fm2_left,text=u"测试URL：",padx=20,font=("宋体",15),anchor="w",justify="left",width=10)
	url_label.pack(side="left")
	url_entry=tk.Entry(fm2_right,bd=4,width=80,justify="left")
	url_entry.pack(side="left")
	fm2_left.pack(side="left")
	fm2_right.pack(side="left")
	fm2.pack(side="top",fill="x")
	fm3=tk.Frame(root)
	fm3_left=tk.Frame(fm3)
	fm3_right=tk.Frame(fm3)
	num_label=tk.Label(fm3_left,text=u"循环次数：",padx=20,font=("宋体",15),anchor="w",justify="left",width=10)
	num_label.pack(side="left")
	num_entry=tk.Entry(fm3_right,bd=4,width=80,justify="left")
	num_entry.pack(side="left")
	fm3_left.pack(side="left")
	fm3_right.pack(side="left")
	fm3.pack(side="top",fill="x")
	fm4=tk.Frame(root)
	fm4_left=tk.Frame(fm4)
	fm4_right=tk.Frame(fm4)
	start_button=tk.Button(fm4_left,text=u"开始",font=("宋体",15),width=10,bg="lightblue",command=lambda:button_start_click_handler(url_entry,num_entry,sucess_show,stop_show,err_show,time_show,avetime_show))
	start_button.pack(side="right")
	stop_button=tk.Button(fm4_right,text=u"中断",font=("宋体",15),width=10,bg="lightblue",command=button_stop_click_handler)
	stop_button.pack(side="left")
	fm4_left.pack(side="left")
	fm4_right.pack(side="right")
	fm4.pack(side="top",ipady=10)
	sep=ttk.Separator(root,orient="horizontal")
	sep.pack(fill=tk.X)
	fm9=tk.Frame(root)
	bottom_label=tk.Label(fm9,font=("黑体",20),height=3,text=u"测试反馈")
	bottom_label.pack()
	fm9.pack(side="top",fill="x")
	fm5=tk.Frame(root)
	fm5_left=tk.Frame(fm5)
	fm5_right=tk.Frame(fm5)
	progress_label=tk.Label(fm5_left,text=u"进度：",padx=20,font=("宋体",15),anchor="w",justify="left",width=10)
	progress_label.pack(side="left")
	progress_show=tk.Label(fm5_right,width=20,anchor="w",text=u"",font=("宋体",15),justify="left")
	progress_show.pack(side="left")
	fm5_left.pack(side="left")
	fm5_right.pack(side="left")
	fm5.pack(side="top",fill="x")


	fm6=tk.Frame(root)
	fm6_left=tk.Frame(fm6)
	fm6_right=tk.Frame(fm6)
	sucess_label=tk.Label(fm6_left,text=u"成功样本：",padx=20,font=("宋体",15),anchor="w",justify="left",width=10)
	sucess_label.pack(side="left")
	sucess_show=tk.Label(fm6_right,width=20,anchor="w",text=u"",font=("宋体",15),justify="left")
	sucess_show.pack(side="left")
	fm6_left.pack(side="left")
	fm6_right.pack(side="left")
	fm6.pack(side="top",fill="x")


	fm7=tk.Frame(root)
	fm7_left=tk.Frame(fm7)
	fm7_right=tk.Frame(fm7)
	stop_label=tk.Label(fm7_left,text=u"终止样本：",padx=20,font=("宋体",15),anchor="w",justify="left",width=10)
	stop_label.pack(side="left")
	stop_show=tk.Label(fm7_right,width=20,anchor="w",text=u"",font=("宋体",15),justify="left")
	stop_show.pack(side="left")
	fm7_left.pack(side="left")
	fm7_right.pack(side="left")
	fm7.pack(side="top",fill="x")



	fm8=tk.Frame(root)
	fm8_left=tk.Frame(fm8)
	fm8_middle=tk.Frame(fm8)
	fm8_right=tk.Frame(fm8)
	err_label=tk.Label(fm8_left,text=u"异常样本：",padx=20,font=("宋体",15),anchor="w",justify="left",width=10)
	err_label.pack(side="left")
	err_show=tk.Label(fm8_middle,width=20,anchor="w",text=u"",font=("宋体",15),justify="left")
	err_show.pack(side="left")
	err_detail=tk.Button(fm8_right,text=u"点击下载异常ID",font=("宋体",15),bg="lightblue",command=button_err_click_handler())
	err_detail.pack(side="left",anchor="w")
	fm8_left.pack(side="left")
	fm8_middle.pack(side="left")
	fm8_right.pack(side="left")
	fm8.pack(side="top",fill="x")

	fm11=tk.Frame(root)
	fm11_left=tk.Frame(fm11)
	fm11_right=tk.Frame(fm11)
	time_label=tk.Label(fm11_left,text=u"总时间（分钟）：",padx=20,font=("宋体",15),anchor="w",justify="left",width=20)
	time_label.pack(side="left")
	time_show=tk.Label(fm11_right,width=20,anchor="w",text=u"",font=("宋体",15),justify="left")
	time_show.pack(side="left")
	fm11_left.pack(side="left")
	fm11_right.pack(side="left")
	fm11.pack(side="top",fill="x")

	fm12=tk.Frame(root)
	fm12_left=tk.Frame(fm12)
	fm12_right=tk.Frame(fm12)
	avetime_label=tk.Label(fm12_left,text=u"平均时间（分钟/次）：",padx=20,font=("宋体",15),anchor="w",justify="left",width=20)
	avetime_label.pack(side="left")
	avetime_show=tk.Label(fm12_right,width=20,anchor="w",text=u"",font=("宋体",15),justify="left")
	avetime_show.pack(side="left")
	fm12_left.pack(side="left")
	fm12_right.pack(side="left")
	fm12.pack(side="top",fill="x")


	fm10=tk.Frame(root)
	refresh_button=tk.Button(fm10,text=u"刷新页面重新开始",font=("宋体",15),bg="lightblue",command=button_refresh_click_handler())
	refresh_button.pack(side="right")
	fm10.pack(side="bottom",fill="x",pady=10,padx=10)
	root.mainloop()




def button_start_click_handler(url_entry,num_entry,sucess_show,stop_show,err_show,time_show,avetime_show):
	url=url_entry.get()
	runs=int(num_entry.get())
	start=time.time()
	list1=auto_test(url,runs)
	end=time.time()
	sucess_show['text']=list1[0]
	stop_show['text']=list1[1]
	err_show['text']=list1[2]
	ttl_time=(end-start)/60
	ave_time=ttl_time/runs
	time_show['text']=ttl_time
	avetime_show['text']=ave_time

	
	#url_entry.delete(0,tk.END)
	#num_entry.delete(0,tk.END)

	


def button_stop_click_handler():
	sys.exit(1)

def button_err_click_handler():
	pass

def button_refresh_click_handler():
	pass


if __name__ == '__main__':
	print(r"https://answer.91question.com/91/27c6cde183c14131ba15a98d377eb918?test=1")
	gui_interface()

		
