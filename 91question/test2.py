from selenium import webdriver
from time import sleep

def get_url(url):
	driver = webdriver.Chrome()
	driver.get(url)

if __name__ == '__main__':
	url = str(input("url:"))
	get_url(url)
	sleep(1)