#coding = utf-8


import tkinter as tk
from tkinter import ttk

def gui_interface():
	global list1
	list1=[]
	root=tk.Tk()
	root.title(u"永钥科技")
	root.geometry("800x600")
	#root.resizable(width=False,height=False)
	fm1=tk.Frame(root)
	content=u"永钥科技自动化测试工具V1.0"
	title_label=tk.Label(fm1,font=("黑体",20),height=4,text=content)
	title_label.pack()
	fm1.pack(side="top",fill="x")
	fm2=tk.Frame(root)
	fm2_left=tk.Frame(fm2)
	fm2_right=tk.Frame(fm2)
	url_label=tk.Label(fm2_left,text=u"测试URL：",font=("宋体",15),anchor="w",justify="left",width=20)
	url_label.pack(side="left")
	url_entry=tk.Entry(fm2_right,bd=4,width=80,justify="left")
	url_entry.pack(side="left")
	fm2_left.pack(side="left")
	fm2_right.pack(side="left")
	fm2.pack(side="top",fill="x")
	fm3=tk.Frame(root)
	fm3_left=tk.Frame(fm3)
	fm3_right=tk.Frame(fm3)
	num_label=tk.Label(fm3_left,text=u"循环次数：",font=("宋体",15),anchor="w",justify="left",width=20)
	num_label.pack(side="left")
	num_entry=tk.Entry(fm3_right,bd=4,width=80,justify="left")
	num_entry.pack(side="left")
	fm3_left.pack(side="left")
	fm3_right.pack(side="left")
	fm3.pack(side="top",fill="x")
	fm4=tk.Frame(root)
	fm4_left=tk.Frame(fm4)
	fm4_right=tk.Frame(fm4)
	start_button=tk.Button(fm4_left,text=u"开始",font=("宋体",15),width=10,bg="lightblue",command=lambda:button_start_click_handler(url_entry,num_entry))
	start_button.pack(side="right")
	stop_button=tk.Button(fm4_right,text=u"中断",font=("宋体",15),width=10,bg="lightblue",command=button_stop_click_handler)
	stop_button.pack(side="left")
	fm4_left.pack(side="left")
	fm4_right.pack(side="right")
	fm4.pack(side="top")
	sep=ttk.Separator(root,orient="horizontal")
	sep.pack(fill=tk.X)
	fm9=tk.Frame(root)
	bottom_label=tk.Label(fm9,font=("黑体",20),height=3,text=u"测试反馈")
	bottom_label.pack()
	fm9.pack(side="top",fill="x")


	fm5=tk.Frame(root)
	fm5_left=tk.Frame(fm5)
	fm5_right=tk.Frame(fm5)
	progress_label=tk.Label(fm5_left,text=u"进度：",font=("宋体",15),anchor="w",justify="left",width=20)
	progress_label.pack(side="left")
	progress_show=tk.Label(fm5_right,width=20,anchor="w",font=("宋体",15),justify="left")
	progress_show.pack(side="left")
	fm5_left.pack(side="left")
	fm5_right.pack(side="left")
	fm5.pack(side="top",fill="x")


	fm6=tk.Frame(root)
	fm6_left=tk.Frame(fm6)
	fm6_right=tk.Frame(fm6)
	sucess_label=tk.Label(fm6_left,text=u"成功样本：",font=("宋体",15),anchor="w",justify="left",width=20)
	sucess_label.pack(side="left")
	sucess_show=tk.Label(fm6_right,width=20,anchor="w",text=u"",font=("宋体",15),justify="left")
	sucess_show.pack(side="left")
	fm6_left.pack(side="left")
	fm6_right.pack(side="left")
	fm6.pack(side="top",fill="x")


	fm7=tk.Frame(root)
	fm7_left=tk.Frame(fm7)
	fm7_right=tk.Frame(fm7)
	stop_label=tk.Label(fm7_left,text=u"终止样本：",font=("宋体",15),anchor="w",justify="left",width=20)
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
	err_label=tk.Label(fm8_left,text=u"异常样本：",font=("宋体",15),anchor="w",justify="left",width=20)
	err_label.pack(side="left")
	err_show=tk.Label(fm8_middle,width=20,anchor="w",font=("宋体",15),justify="left")
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
	time_label=tk.Label(fm11_left,text=u"总时间（分钟）：",font=("宋体",15),anchor="w",justify="left",width=20)
	time_label.pack(side="left")
	time_show=tk.Label(fm11_right,width=20,anchor="w",font=("宋体",15),justify="left")
	time_show.pack(side="left")
	fm11_left.pack(side="left")
	fm11_right.pack(side="left")
	fm11.pack(side="top",fill="x")

	fm12=tk.Frame(root)
	fm12_left=tk.Frame(fm12)
	fm12_right=tk.Frame(fm12)
	avetime_label=tk.Label(fm12_left,text=u"平均时间（分钟/次）：",font=("宋体",15),anchor="w",justify="left",width=20)
	avetime_label.pack(side="left")
	avetime_show=tk.Label(fm12_right,width=20,anchor="w",font=("宋体",15),justify="left")
	avetime_show.pack(side="left")
	fm12_left.pack(side="left")
	fm12_right.pack(side="left")
	fm12.pack(side="top",fill="x")


	fm10=tk.Frame(root)
	refresh_button=tk.Button(fm10,text=u"刷新页面重新开始",font=("宋体",15),bg="lightblue",command=button_refresh_click_handler())
	refresh_button.pack(side="right")
	fm10.pack(side="bottom",fill="x")
	print(list1)
	#sucess_show['text']=url
	#stop_show['text']=cycs
	root.mainloop()




def button_start_click_handler(url_entry,num_entry):
	print("test1")
	url=str(url_entry.get())
	cycs=str(num_entry.get())
	list1.append(url)
	list1.append(cycs)
	


def button_stop_click_handler():
	print("test2")
	print(list1)

def button_err_click_handler():
	pass

def button_refresh_click_handler():
	pass

if __name__ == '__main__':
	gui_interface()


