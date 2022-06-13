"""
tq_show_v2.0 - 


Author:
Date:2022/6/6
"""
import serial    # 串口库
from tkinter import *
from tkinter import ttk
import threading    # 多线程库
import numpy
import socket
import time


flag = 0

def connect_khd():
	global flag
	try:
		host = fwq_ip_entry.get()
		port = 9000
		s.connect((host, port))
	except Exception as e:
		print(e)
		if flag == 0:
			fwq_connect_show_lab.config(text='未连接服务器')
	else:
		fwq_connect_show_lab.config(text='已连接服务器')
		flag = 1



def read_ser(ser):
	global tqd_ls, xh, tq_sx, tq_xx, xh_ls
	while True:
		try:
			strs = s.recv(1024).decode('gbk')
			if strs == 'clear':
				clear_data()
			xh, tqd, tq_sx, tq_xx= strs_to_data(strs)
			tq_sx_lab2.config(text=str(tq_sx))
			tq_xx_lab2.config(text=str(tq_xx))
			tqd_ls.append(tqd)
			xh_ls.append(xh)
			if len(tqd_ls) == 33:
				clear_data()
				tqd_ls.append(tqd)
			tq_labs1[xh].config(text=str(tqd))
			tqd_avg(tqd_ls)
			change_bg_color(tqd)
			if len(tqd_ls) > 1:
				canvas.create_line(xh_ls[-2]*10, tqd_ls[-2]*4, xh_ls[-1]*10, tqd_ls[-1]*4)
		except Exception as e:
			print(e)
		time.sleep((0.05))


def strs_to_data(strs):
	try:
		data = strs.split()
		xh = int(data[0])
		tqd = float(data[1])
		tq_sx = float(data[2])
		tq_xx = float(data[3])
	except Exception as e:
		print(e)
	else:
		return xh, tqd, tq_sx, tq_xx


def tqd_avg(tqd_ls):
	if len(tqd_ls) < 9:
		tq_avg1 = round((sum(tqd_ls) / len(tqd_ls)), 2)
		tq_labs2[0].config(text=str(tq_avg1))
		if tq_avg1 > tq_sx or tq_avg1 < tq_xx:
			tq_labs2[0].config(bg='Red')
	if 9 <= len(tqd_ls) < 17:
		tq_avg2 = round((sum(tqd_ls[8:]) / len(tqd_ls[8:])), 2)
		tq_labs2[1].config(text=str(tq_avg2))
		if tq_avg2 > tq_sx or tq_avg2 < tq_xx:
			tq_labs2[1].config(bg='Red')
	if 17 <= len(tqd_ls) < 25:
		tq_avg3 = round((sum(tqd_ls[16:]) / len(tqd_ls[16:])), 2)
		tq_labs2[2].config(text=str(tq_avg3))
		if tq_avg3 > tq_sx or tq_avg3 < tq_xx:
			tq_labs2[2].config(bg='Red')
	if 25 <= len(tqd_ls) < 33:
		tq_avg4 = round((sum(tqd_ls[24:]) / len(tqd_ls[24:])), 2)
		tq_labs2[3].config(text=str(tq_avg4))
		if tq_avg4 > tq_sx or tq_avg4 < tq_xx:
			tq_labs2[3].config(bg='Red')
	tq_avg5 = round((sum(tqd_ls) / len(tqd_ls)), 2)
	tq_byxs1 = tq_byxs(tqd_ls)
	tq_min = min(tqd_ls)
	tq_max = max(tqd_ls)
	tq_labs3[0].config(text=str(tq_avg5))
	tq_labs3[1].config(text=str(tq_byxs1))
	tq_labs3[2].config(text=str(tq_min))
	tq_labs3[3].config(text=str(tq_max))
	if tq_avg5 > tq_sx or tq_avg5 < tq_xx:
		tq_labs3[0].config(bg='Red')
	else:
		tq_labs3[0].config(bg='LightGrey')
	if tq_max > tq_sx or tq_max < tq_xx:
		tq_labs3[3].config(bg='Red')
	else:
		tq_labs3[3].config(bg='LightGrey')
	if tq_min > tq_sx or tq_min < tq_xx:
		tq_labs3[2].config(bg='Red')
	else:
		tq_labs3[2].config(bg='LightGrey')


def tq_byxs(tqd_ls):
	mean = numpy.mean(tqd_ls)  # 计算平均值
	std = numpy.std(tqd_ls, ddof=0)  # 计算标准差
	cv = round((std / mean) * 100, 2)
	return cv


def clear_data():
	global tqd_ls, xh
	tqd_ls = []
	xh = 0
	for a in tq_labs1:
		a.config(text='')
		a.config(bg='LightGrey')
	for b in tq_labs2:
		b.config(text='')
		b.config(bg='LightGrey')
	for d in tq_labs3:
		d.config(text='')
		d.config(bg='LightGrey')


def change_bg_color(tqd):
	try:
		if tqd > tq_sx or tqd < tq_xx:
			tq_labs1[xh].config(bg='Red')
	except Exception as e:
		print(e)


if __name__ == '__main__':
	window = Tk()
	window.title('透气度实时显示')
	#  screen_width = window.winfo_screenwidth()
	#  screen_height = window.winfo_screenheight()
	w, h = 1600, 900
	window.geometry('%dx%d' % (w, h))
	window.config(bg='White')

	tq_show_frame1 = Frame(window, bg='White')
	tq_show_frame1.place(x=10, y=10, width=1060, height=580)
	tq_show_frame2 = Frame(window, bg='White')
	tq_show_frame2.place(x=10, y=600, width=1060, height=70)
	tq_show_frame3 = Frame(window, bg='White')
	tq_show_frame3.place(x=50, y=680, width=1020, height=200)
	tq_show_frame4 = Frame(window, bg='White')
	tq_show_frame4.place(x=1080, y=420, width=510, height=450)
	tq_set_frame = Frame(window, bg='White')
	tq_set_frame.place(x=1100, y=10, width=490, height=180)
	fwq_show_frame = Frame(window, bg='White')
	fwq_show_frame.place(x=1100, y=250, width=490, height=150)

	tq_labs1 = []
	tq_labs2 = []
	tq_labs3 = []
	tqd_ls = []
	xh_ls = []
	xh = 0
	c = None
	tq_sx = 9999
	tq_xx = 0


	# 设置透气度显示区域标签
	n = 1
	for c in range(8):
		for r in range(8):
			if c % 2 != 0:
				lab1 = Label(tq_show_frame1, width=8, height=1, font='Helvetica 30 bold')
				tq_labs1.append(lab1)
			else:
				lab1 = Label(tq_show_frame1, width=3, height=1, font='Helvetica 20 bold', bg='White')
				lab1.config(text=str(n))
				n += 1
			lab1.grid(row=r, column=c, padx=2, pady=10)

	# 设置透气度平均值区域标签
	names1 = ['操边', '操中', '传中', '传边']
	name = 0
	for c in range(8):
		if c % 2 != 0:
			lab2 = Label(tq_show_frame2, width=8, height=1, font='Helvetica 30 bold')
			tq_labs2.append(lab2)
		else:
			lab2 = Label(tq_show_frame2, width=3, height=1, font='Helvetica 20 bold', bg='White')
			lab2.config(text=names1[name])
			name += 1
		lab2.grid(row=0, column=c, padx=2, pady=10)


	#  设置透气度总数据区域标签
	names2 = ['平均值', '变异系数', '最小值', '最大值']
	name2 = 0
	for r in range(2):
		for c in range(4):
			if c % 2 != 0:
				lab3 = Label(tq_show_frame3, width=8, height=1, font='Helvetica 30 bold')
				tq_labs3.append(lab3)
			else:
				lab3 = Label(tq_show_frame3, width=8, height=1, font='Helvetica 20 bold', bg='White')
				lab3.config(text=names2[name2])
				name2 += 1
			lab3.grid(row=r, column=c, padx=2, pady=15)

	#  设置清空数据按钮
	clear_B = Button(tq_show_frame3, text='清空数据',height=4, width=10, font='Helvetica 20 bold',
					 command=clear_data)
	clear_B.grid(row=0, rowspan=2, column=4, padx=50, pady=20)

	#  设置透气度上下限文本框和标签
	tq_sx_lab = Label(tq_set_frame, text='透气度上限值', width=18, height=2, font='BritannicBold 15')
	tq_xx_lab = Label(tq_set_frame, text='透气度下限值', width=18, height=2, font='BritannicBold 15')

	tq_sx_lab2 = Label(tq_set_frame, width=8, height=2, font='BritannicBold 15')
	tq_xx_lab2 = Label(tq_set_frame, width=8, height=2, font='BritannicBold 15')

	tq_sx_lab.grid(row=0, column=0, pady=5, padx=5)
	tq_sx_lab2.grid(row=0, column=1, pady=5, padx=5)

	tq_xx_lab.grid(row=1, column=0,pady=5, padx=5)
	tq_xx_lab2.grid(row=1, column=1, pady=5, padx=5)

	#  设置服务器ip和端口显示以及连接信息标签
	fwq_ip_lab = Label(fwq_show_frame, width=20, height=2, text='服务器ip', font='BritannicBold 12')
	fwq_ip_entry = Entry(fwq_show_frame, width=20, font='BritannicBold 12')
	fwq_connect_show_lab = Label(fwq_show_frame, width=42, height=2, font='BritannicBold 12')
	connect_button = Button(fwq_show_frame, width=10, height=6, text='连接', font='BritannicBold 12', command=connect_khd)

	fwq_ip_lab.grid(row=0, column=0, padx=5, pady=10)
	fwq_ip_entry.grid(row=0, column=1, padx=5, pady=10, ipady=7)
	fwq_connect_show_lab.grid(row=2, column=0, columnspan=2,pady=5)
	connect_button.grid(row=0, rowspan=3, column=2, pady =10, padx=5)

	# 建立画布
	canvas = Canvas(window, width=510, height=450)
	canvas.place(x=1080, y=420)





	with open('ip.txt') as f:
		ip = f.read()

	fwq_ip_entry.insert(0, ip)
	s = socket.socket()
	fwq_connect_show_lab.config(text='未连接服务器')

	t1 = threading.Thread(target=read_ser, args=(s,))
	t1.daemon = True
	t1.start()
	canvas.create_line(0, tq_sx, 330, tq_sx)
	canvas.create_line(0, tq_xx, 330, tq_xx)
	window.mainloop()
