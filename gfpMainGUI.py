#!/usr/bin/python
import os.path
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
#from PIL import Image, ImageTk
from dbfunctions import *
import datetime

class GFPTime(tk.Tk):
	def __init__(self,*args,**kwargs):
		
		tk.Tk.__init__(self,*args,**kwargs)
		
		tk.Tk.wm_title(self,"GFP Employee Timecard System")
		tk.Tk.wm_geometry(self,"800x480+0+0")

		container =tk.Frame(self)
		container.pack(side='top',fill='both',expand= True)
		
		container.grid_rowconfigure(0,weight=1)
		container.grid_columnconfigure(0,weight=1)

		self.frames = {}
		
		for F in (MainMenu,RecEmp,RecordTime,EditEmployeeList):
			
			frame = F(container,self)
			
			self.frames[F] = frame
			frame.grid(row=0,column=0,stick='nsew')
			
		self.show_frame(MainMenu)

	def show_frame(self,cont):
		frame = self.frames[cont]
		frame.tkraise()

	def empcbxlist(self, widget_name, criteria):
		db = TimeCardDB()
		cbvalue = db.listActiveEmployees()
		db.dbclose()

		ob = self.frames.get(RecEmp)
		cdatetime = getdatetime(self)
		# dateLb.configure(text=cddt.get())
		# timeLB.configure(text=ctdt.get())
		widget = getattr(ob,'cbxemp')
		widget[criteria] = cbvalue

		widget = getattr(ob,'cbxyear')
		widget.configure(values = [str(int(cdatetime[2].get())-1), cdatetime[2].get(), str(int(cdatetime[2].get())+1)])
		widget.set(cdatetime[2].get())
		
		widget = getattr(ob,'cbxmonth')
		widget.set(cdatetime[0].get())
		
		widget = getattr(ob,'cbxday')
		if cdatetime[0].get() == 'Jan' or cdatetime[0].get() == 'Mar' or cdatetime[0].get() == 'May' or cdatetime[0].get() == 'Jul' or cdatetime[0].get() == 'Aug' or cdatetime[0].get() == 'Oct' or cdatetime[0].get() == 'Dec':
			widdate = getattr(ob,'oddday')
		elif cdatetime[0].get() == 'Feb':
			if cdatetime[2].get() % 4 == 0:
				widdate = getattr(ob,'leapday')
			else:
				widdate = getattr(ob,'febday')
		else:
			widdate = getattr(ob,'evenday')
		widget.configure(values = widdate)
		widget.set(cdatetime[1].get())

	def setuprecordemp(self):
		# getting the widgets needed to be changed
		ob = self.frames.get(RecordTime)
		nameLb = getattr(ob,'nameLb')
		dateLb = getattr(ob,'dateLb')

		lowbtn = getattr(ob,'lowbtn')
		holbtn = getattr(ob,'holbtn')
		offbtn = getattr(ob,'offbtn')
		cbxvac = getattr(ob,'cbxvac')
		cbxtentatt = getattr(ob,'cbxtentatt')
		cbxot = getattr(ob,'cbxot')
		cbxinhr1 = getattr(ob,'cbxinhr1')
		cbxinhr2 = getattr(ob,'cbxinhr2')
		cbxinhr3 = getattr(ob,'cbxinhr3')
		cbxouthr1 = getattr(ob,'cbxouthr1')
		cbxouthr2 = getattr(ob,'cbxouthr2')
		cbxouthr3 = getattr(ob,'cbxouthr3')
		cbxinmin1 = getattr(ob,'cbxinmin1')
		cbxinmin2 = getattr(ob,'cbxinmin2')
		cbxinmin3 = getattr(ob,'cbxinmin3')
		cbxoutmin1 = getattr(ob,'cbxoutmin1')
		cbxoutmin2 = getattr(ob,'cbxoutmin2')
		cbxoutmin3 = getattr(ob,'cbxoutmin3')

		ob = self.frames.get(RecEmp)
		nameLb.configure(text = getattr(ob,'cbxemp').get())
		dateLb.configure(text = getattr(ob,'cbxmonth').get()+'  '+getattr(ob,'cbxday').get()+', '+getattr(ob,'cbxyear').get())
		
		name = getattr(ob,'cbxemp').get().split()
		name = name[1]+'_'+name[2]+'_'+name[0]
		
		
		month = getattr(ob,'cbxmonth').get().split()
		month = month[0]
		print(month)
		date = getattr(ob,'cbxyear').get()+'-'+month+'-'+getattr(ob,'cbxday').get()

		db = TimeCardDB()
		records = db.pullTimeRecord(name,date)

		db.dbclose()

###
class MainMenu(tk.Frame):
	
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		#tk.Frame.configure(self,background='red')
		font9 = "-family {Minion Pro} -size 14 -weight bold"
		self.controller = controller

		recordBn = tk.Button(self,command=lambda: [self.controller.show_frame(RecEmp), self.controller.empcbxlist('cbxemp','values')])
		recordBn.place(relx=0.269, rely=0.646, height=50, width=180)
		recordBn.configure(activebackground="#ececec")
		recordBn.configure(activeforeground="#000000")
		recordBn.configure(background="#d9d9d9")
		recordBn.configure(disabledforeground="#a3a3a3")
		recordBn.configure(font=font9)
		recordBn.configure(foreground="#000000")
		recordBn.configure(highlightbackground="#d9d9d9")
		recordBn.configure(highlightcolor="black")
		recordBn.configure(pady="0")
		recordBn.configure(text='''Record Time''')

		editBn = tk.Button(self,command=lambda: self.controller.show_frame(EditEmployeeList))
		editBn.place(relx=0.506, rely=0.646, height=50, width=180)
		editBn.configure(activebackground="#ececec")
		editBn.configure(activeforeground="#000000")
		editBn.configure(background="#d9d9d9")
		editBn.configure(disabledforeground="#a3a3a3")
		editBn.configure(font=font9)
		editBn.configure(foreground="#000000")
		editBn.configure(highlightbackground="#d9d9d9")
		editBn.configure(highlightcolor="black")
		editBn.configure(pady="0")
		editBn.configure(text='''Edit Employee''')
		
		reportBn = tk.Button(self)
		reportBn.place(relx=0.269, rely=0.771, height=50, width=180)
		reportBn.configure(activebackground="#ececec")
		reportBn.configure(activeforeground="#000000")
		reportBn.configure(background="#d9d9d9")
		reportBn.configure(disabledforeground="#a3a3a3")
		reportBn.configure(foreground="#000000")
		reportBn.configure(font=font9)
		reportBn.configure(highlightbackground="#d9d9d9")
		reportBn.configure(highlightcolor="black")
		reportBn.configure(pady="0")
		reportBn.configure(text='''Reports''')

		exitBn = tk.Button(self,command=lambda:app.destroy())
		exitBn.place(relx=0.506, rely=0.771, height=50, width=180)
		exitBn.configure(activebackground="#ececec")
		exitBn.configure(activeforeground="#000000")
		exitBn.configure(background="#d9d9d9")
		exitBn.configure(disabledforeground="#a3a3a3")
		exitBn.configure(font=font9)
		exitBn.configure(foreground="#000000")
		exitBn.configure(highlightbackground="#d9d9d9")
		exitBn.configure(highlightcolor="black")
		exitBn.configure(pady="0")
		exitBn.configure(text='''Exit''')

		#imgLb = tk.Label(self)
		#imgLb.place(relx=0.0, rely=0.042, height=185, width=800)
		#imgLb.configure(background="red")
		#_img0 = tk.PhotoImage(file="New_Logo_2014_white_outline small.png")
		#imgLb.configure(image=_img0)
		#imgLb.image = _img0


###
class RecEmp(tk.Frame):
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)

		font9 = "-family {Minion Pro} -size 14 -weight bold"

		def resetwidgets():
			self.cbxemp.set('')
			recempsubbtn.configure(state = 'disabled')

		recempsubbtn = tk.Button(self,command=lambda: [controller.show_frame(RecordTime),controller.setuprecordemp(),resetwidgets()])#,self.controller.empcbxlist('cbxemp','values')])
		recempsubbtn.place(relx=0.513, rely=0.688, height=40, width=130)
		recempsubbtn.configure(activebackground="#ececec")
		recempsubbtn.configure(state = 'disabled')
		recempsubbtn.configure(activeforeground="#000000")
		recempsubbtn.configure(background="#d9d9d9")
		recempsubbtn.configure(disabledforeground="#a3a3a3")
		recempsubbtn.configure(font=font9)
		recempsubbtn.configure(foreground="#000000")
		recempsubbtn.configure(highlightbackground="#d9d9d9")
		recempsubbtn.configure(highlightcolor="black")
		recempsubbtn.configure(pady="0")
		recempsubbtn.configure(text='''Submit''')
		
		def empchose(event):
			recempsubbtn.configure(state="normal")

		self.cbxemp = ttk.Combobox(self)
		self.cbxemp.place(relx=0.35, rely=0.208, relheight=0.083, relwidth=0.438)
		self.cbxemp.configure(font=font9)
		self.cbxemp.configure(state = 'readonly')
		self.cbxemp.configure(width=287)
		self.cbxemp.configure(takefocus="", height = 6)
		self.cbxemp.bind("<<ComboboxSelected>>", empchose)

		def monthchose(event):
			widget = self.cbxmonth.get()
			widget = widget.split()
			widget = widget[1]
			self.cbxday.set('')
			if widget == 'Jan' or widget == 'Mar' or widget == 'May' or widget == 'Jul' or widget == 'Aug' or widget == 'Oct' or widget == 'Dec':
				widday = self.oddday
			elif widget == 'Feb':
				if int(self.cbxyear.get()) % 4 == 0:
					widday = self.leapday
				else:
					widday = self.febday
			else:
				widday = self.evenday
			self.cbxday.configure(values = widday)

		self.cbxmonth = ttk.Combobox(self)
		self.cbxmonth.place(relx=0.488, rely=0.313, relheight=0.083, relwidth=0.1)
		self.cbxmonth.configure(font=font9,state = 'readonly')
		self.cbxmonth.configure(width=80)
		self.cbxmonth.configure(takefocus="", height = 6)
		monthval = ['01 Jan','02 Feb','03 Mar','04 Apr','05 May','06 Jun','07 Jul','08 Aug','09 Sep','10 Oct','11 Nov','12 Dec']
		self.cbxmonth.configure(values = monthval)
		self.cbxmonth.bind("<<ComboboxSelected>>", monthchose)

		def yearchose(event):
			widget = self.cbxmonth.get()
			self.cbxday.set('')
			if widget == 'Jan' or widget == 'Mar' or widget == 'May' or widget == 'Jul' or widget == 'Aug' or widget == 'Oct' or widget == 'Dec':
				widday = self.oddday
			elif widget == 'Feb':
				if int(self.cbxyear.get()) % 4 == 0:
					widday = self.leapday
				else:
					widday = self.febday
			else:
				widday = self.evenday
			self.cbxday.configure(values = widday)

		self.cbxyear = ttk.Combobox(self)
		self.cbxyear.place(relx=0.488, rely=0.521, relheight=0.083, relwidth=0.1)
		self.cbxyear.configure(font=font9,state = 'readonly')
		self.cbxyear.configure(takefocus="")
		self.cbxyear.bind("<<ComboboxSelected>>", yearchose)
		
		self.oddday = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20',
						'21','22','23','24','25','26','27','28','29','30','31']
		self.evenday = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20',
						'21','22','23','24','25','26','27','28','29','30']
		self.leapday = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20',
						'21','22','23','24','25','26','27','28','29']
		self.febday = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20',
						'21','22','23','24','25','26','27','28']

		self.cbxday = ttk.Combobox(self)
		self.cbxday.place(relx=0.488, rely=0.417, relheight=0.083, relwidth=0.1)
		self.cbxday.configure(font=font9,state = 'readonly')
		self.cbxday.configure(takefocus="", height = 6)

		recmmubtn = tk.Button(self,command=lambda: [controller.show_frame(MainMenu),resetwidgets()])
		recmmubtn.place(relx=0.325, rely=0.688, height=40, width=130)
		recmmubtn.configure(activebackground="#ececec")
		recmmubtn.configure(activeforeground="#000000")
		recmmubtn.configure(background="#d9d9d9")
		recmmubtn.configure(disabledforeground="#a3a3a3")
		recmmubtn.configure(font=font9)
		recmmubtn.configure(foreground="#000000")
		recmmubtn.configure(highlightbackground="#d9d9d9")
		recmmubtn.configure(highlightcolor="black")
		recmmubtn.configure(pady="0")
		recmmubtn.configure(text='''Main Menu''')

		Label1 = tk.Label(self)
		Label1.place(relx=0.213, rely=0.208, height=40, width=106)
		Label1.configure(background="#d9d9d9")
		Label1.configure(disabledforeground="#a3a3a3")
		Label1.configure(font=font9)
		Label1.configure(foreground="#000000")
		Label1.configure(text='''Employee:''')

		Label1_14 = tk.Label(self)
		Label1_14.place(relx=0.413, rely=0.417, height=38, width=56)
		Label1_14.configure(activebackground="#f9f9f9")
		Label1_14.configure(activeforeground="black")
		Label1_14.configure(background="#d9d9d9")
		Label1_14.configure(disabledforeground="#a3a3a3")
		Label1_14.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label1_14.configure(foreground="#000000")
		Label1_14.configure(highlightbackground="#d9d9d9")
		Label1_14.configure(highlightcolor="black")
		Label1_14.configure(text='''Day:''')
		Label1_14.configure(width=56)

		Label1_15 = tk.Label(self)
		Label1_15.place(relx=0.388, rely=0.313, height=38, width=76)
		Label1_15.configure(activebackground="#f9f9f9")
		Label1_15.configure(activeforeground="black")
		Label1_15.configure(background="#d9d9d9")
		Label1_15.configure(disabledforeground="#a3a3a3")
		Label1_15.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label1_15.configure(foreground="#000000")
		Label1_15.configure(highlightbackground="#d9d9d9")
		Label1_15.configure(highlightcolor="black")
		Label1_15.configure(text='''Month:''')
		Label1_15.configure(width=76)

		Label1_16 = tk.Label(self)
		Label1_16.place(relx=0.413, rely=0.521, height=38, width=56)
		Label1_16.configure(activebackground="#f9f9f9")
		Label1_16.configure(activeforeground="black")
		Label1_16.configure(background="#d9d9d9")
		Label1_16.configure(disabledforeground="#a3a3a3")
		Label1_16.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label1_16.configure(foreground="#000000")
		Label1_16.configure(highlightbackground="#d9d9d9")
		Label1_16.configure(highlightcolor="black")
		Label1_16.configure(text='''Year:''')
		Label1_16.configure(width=56)

###	
class RecordTime(tk.Frame):
	
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		self.controller = controller
		self.cbxhrval = ['01','02','03','04','05','06','07','08','09','10','11','12']
		self.cbxminval = ['00','15','30','45']
		self.cbxapval = ['AM','PM']

		self.cbxinhr1 = ttk.Combobox(self)
		self.cbxinhr1.place(relx=0.113, rely=0.229, relheight=0.083, relwidth=0.1)
		self.cbxinhr1.configure(takefocus="", height = 6)
		self.cbxinhr1.configure(values = self.cbxhrval, state = 'disabled')
		self.cbxinhr1.configure(font="-family {Minion Pro} -size 14 -weight bold")
		
		self.cbxinmin1 = ttk.Combobox(self)
		self.cbxinmin1.place(relx=0.25, rely=0.229, relheight=0.083, relwidth=0.1)
		self.cbxinmin1.configure(takefocus="", height = 6)
		self.cbxinmin1.configure(values = self.cbxminval, state = 'disabled')
		self.cbxinmin1.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxinap1 = ttk.Combobox(self)
		self.cbxinap1.place(relx=0.375, rely=0.229, relheight=0.083, relwidth=0.1)
		self.cbxinap1.configure(takefocus="", height = 6)
		self.cbxinap1.configure(values = self.cbxapval, state = 'disabled')
		self.cbxinap1.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxouthr1 = ttk.Combobox(self)
		self.cbxouthr1.place(relx=0.5, rely=0.229, relheight=0.083, relwidth=0.1)
		self.cbxouthr1.configure(takefocus="", height=6)
		self.cbxouthr1.configure(values = self.cbxhrval,state = 'disabled')
		self.cbxouthr1.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxoutmin1 = ttk.Combobox(self)
		self.cbxoutmin1.place(relx=0.638, rely=0.229, relheight=0.083, relwidth=0.1)
		self.cbxoutmin1.configure(takefocus="", height=6)
		self.cbxoutmin1.configure(values = self.cbxminval,state = 'disabled')
		self.cbxoutmin1.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxoutap1 = ttk.Combobox(self)
		self.cbxoutap1.place(relx=0.763, rely=0.229, relheight=0.083, relwidth=0.1)
		self.cbxoutap1.configure(takefocus="", height=6)
		self.cbxoutap1.configure(values = self.cbxapval,state = 'disabled')
		self.cbxoutap1.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxinhr2 = ttk.Combobox(self)
		self.cbxinhr2.place(relx=0.113, rely=0.333, relheight=0.083, relwidth=0.1)
		self.cbxinhr2.configure(takefocus="", height=6)
		self.cbxinhr2.configure(values = self.cbxhrval,state = 'disabled')
		self.cbxinhr2.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxinmin2 = ttk.Combobox(self)
		self.cbxinmin2.place(relx=0.25, rely=0.333, relheight=0.083, relwidth=0.1)
		self.cbxinmin2.configure(takefocus="", height=6)
		self.cbxinmin2.configure(values = self.cbxminval,state = 'disabled')
		self.cbxinmin2.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxinap2 = ttk.Combobox(self)
		self.cbxinap2.place(relx=0.375, rely=0.333, relheight=0.083, relwidth=0.1)
		self.cbxinap2.configure(takefocus="", height=6)
		self.cbxinap2.configure(values = self.cbxapval,state = 'disabled')
		self.cbxinap2.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxouthr2 = ttk.Combobox(self)
		self.cbxouthr2.place(relx=0.5, rely=0.333, relheight=0.083, relwidth=0.1)
		self.cbxouthr2.configure(takefocus="", height=6)
		self.cbxouthr2.configure(values = self.cbxhrval,state = 'disabled')
		self.cbxouthr2.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxoutmin2 = ttk.Combobox(self)
		self.cbxoutmin2.place(relx=0.638, rely=0.333, relheight=0.083, relwidth=0.1)
		self.cbxoutmin2.configure(takefocus="", height=6)
		self.cbxoutmin2.configure(values = self.cbxminval,state = 'disabled')
		self.cbxoutmin2.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxoutap2 = ttk.Combobox(self)
		self.cbxoutap2.place(relx=0.763, rely=0.333, relheight=0.083, relwidth=0.1)
		self.cbxoutap2.configure(takefocus="", height=6)
		self.cbxoutap2.configure(values = self.cbxapval,state = 'disabled')
		self.cbxoutap2.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxinhr3 = ttk.Combobox(self)
		self.cbxinhr3.place(relx=0.113, rely=0.438, relheight=0.083, relwidth=0.1)
		self.cbxinhr3.configure(takefocus="", height=6)
		self.cbxinhr3.configure(values = self.cbxhrval,state = 'disabled')
		self.cbxinhr3.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxinmin3 = ttk.Combobox(self)
		self.cbxinmin3.place(relx=0.25, rely=0.438, relheight=0.083, relwidth=0.1)
		self.cbxinmin3.configure(takefocus="", height=6)
		self.cbxinmin3.configure(values = self.cbxminval,state = 'disabled')
		self.cbxinmin3.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxinap3 = ttk.Combobox(self)
		self.cbxinap3.place(relx=0.375, rely=0.438, relheight=0.083, relwidth=0.1)
		self.cbxinap3.configure(takefocus="", height=6)
		self.cbxinap3.configure(values = self.cbxapval,state = 'disabled')
		self.cbxinap3.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxoutap3 = ttk.Combobox(self)
		self.cbxoutap3.place(relx=0.763, rely=0.438, relheight=0.083, relwidth=0.1)
		self.cbxoutap3.configure(takefocus="", height=6)
		self.cbxoutap3.configure(values = self.cbxapval,state = 'disabled')
		self.cbxoutap3.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxoutmin3 = ttk.Combobox(self)
		self.cbxoutmin3.place(relx=0.638, rely=0.438, relheight=0.083, relwidth=0.1)
		self.cbxoutmin3.configure(takefocus="", height=6)
		self.cbxoutmin3.configure(values = self.cbxminval,state = 'disabled')
		self.cbxoutmin3.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxouthr3 = ttk.Combobox(self)
		self.cbxouthr3.place(relx=0.5, rely=0.438, relheight=0.083, relwidth=0.1)
		self.cbxouthr3.configure(takefocus="", height=6)
		self.cbxouthr3.configure(values = self.cbxhrval,state = 'disabled')
		self.cbxouthr3.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxot = ttk.Combobox(self)
		self.cbxot.place(relx=0.425, rely=0.583, relheight=0.083, relwidth=0.1)
		self.cbxot.configure(takefocus="", height=6)
		self.cbxot.configure(values = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'],state = 'readonly')
		self.cbxot.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxtent = ttk.Combobox(self)
		self.cbxtent.place(relx=0.188, rely=0.583, relheight=0.083, relwidth=0.1)
		self.cbxtent.configure(takefocus="", height=6)
		self.cbxtent.configure(values = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16'],state = 'readonly')
		self.cbxtent.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxtentatt = ttk.Combobox(self)
		self.cbxtentatt.place(relx=0.792, rely=0.583, relheight=0.083, relwidth=0.1)
		self.cbxtentatt.configure(takefocus="")
		self.cbxtentatt.configure(values = ['100','200'],state = 'readonly')
		self.cbxtentatt.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.cbxvac = ttk.Combobox(self)
		self.cbxvac.place(relx=0.463, rely=0.708, relheight=0.083, relwidth=0.1)
		self.cbxvac.configure(takefocus="", height=6,state = 'readonly')
		self.cbxvac.configure(values = ['1','2','3','4','5','6','7','8'])
		self.cbxvac.configure(font="-family {Minion Pro} -size 14 -weight bold")

		self.dateLb = tk.Label(self)
		self.dateLb.place(relx=0.213, rely=0.021, height=38, width=144)
		self.dateLb.configure(activebackground="#f9f9f9")
		self.dateLb.configure(activeforeground="black")
		self.dateLb.configure(disabledforeground="#a3a3a3")
		self.dateLb.configure(font="-family {Minion Pro} -size 14 -weight bold")
		self.dateLb.configure(foreground="#000000")
		self.dateLb.configure(highlightbackground="#d9d9d9")
		self.dateLb.configure(highlightcolor="black")
		self.dateLb.configure(text='''SHOW DATE''')

		Label3_9 = tk.Label(self)
		Label3_9.place(relx=0.225, rely=0.125, height=48, width=108)
		Label3_9.configure(activebackground="#f9f9f9")
		Label3_9.configure(activeforeground="black")
		Label3_9.configure(disabledforeground="#a3a3a3")
		Label3_9.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label3_9.configure(foreground="#000000")
		Label3_9.configure(highlightbackground="#d9d9d9")
		Label3_9.configure(highlightcolor="black")
		Label3_9.configure(text='''Time IN''')

		Label3_8 = tk.Label(self)
		Label3_8.place(relx=0.613, rely=0.146, height=38, width=120)
		Label3_8.configure(activebackground="#f9f9f9")
		Label3_8.configure(activeforeground="black")
		Label3_8.configure(disabledforeground="#a3a3a3")
		Label3_8.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label3_8.configure(foreground="#000000")
		Label3_8.configure(highlightbackground="#d9d9d9")
		Label3_8.configure(highlightcolor="black")
		Label3_8.configure(text='''Time OUT''')

		Label4 = tk.Label(self)
		Label4.place(relx=0.363, rely=0.583, height=38, width=45)
		Label4.configure(activebackground="#f9f9f9")
		Label4.configure(activeforeground="black")
		Label4.configure(disabledforeground="#a3a3a3")
		Label4.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label4.configure(foreground="#000000")
		Label4.configure(highlightbackground="#d9d9d9")
		Label4.configure(highlightcolor="black")
		Label4.configure(text='''OT:''')

		Label5 = tk.Label(self)
		Label5.place(relx=0.063, rely=0.583, height=38, width=99)
		Label5.configure(activebackground="#f9f9f9")
		Label5.configure(activeforeground="black")
		Label5.configure(disabledforeground="#a3a3a3")
		Label5.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label5.configure(foreground="#000000")
		Label5.configure(highlightbackground="#d9d9d9")
		Label5.configure(highlightcolor="black")
		Label5.configure(text='''Tent Hrs:''')

		Label6 = tk.Label(self)
		Label6.place(relx=0.575, rely=0.583, height=38, width=171)
		Label6.configure(activebackground="#f9f9f9")
		Label6.configure(activeforeground="black")
		Label6.configure(disabledforeground="#a3a3a3")
		Label6.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label6.configure(foreground="#000000")
		Label6.configure(highlightbackground="#d9d9d9")
		Label6.configure(highlightcolor="black")
		Label6.configure(text='''Tent Attendant:''')

		Label7 = tk.Label(self)
		Label7.place(relx=0.063, rely=0.708, height=38, width=101)
		Label7.configure(activebackground="#f9f9f9")
		Label7.configure(activeforeground="black")
		Label7.configure(disabledforeground="#a3a3a3")
		Label7.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label7.configure(foreground="#000000")
		Label7.configure(highlightbackground="#d9d9d9")
		Label7.configure(highlightcolor="black")
		Label7.configure(text='''Day OFF:''')

		self.offbtn = tk.Button(self)
		self.offbtn.place(relx=0.2, rely=0.708, height=40, width=60)
		self.offbtn.configure(activebackground="#ececec")
		self.offbtn.configure(activeforeground="#000000")
		self.offbtn.configure(disabledforeground="#a3a3a3")
		self.offbtn.configure(font="-family {Minion Pro} -size 14 -weight bold")
		self.offbtn.configure(foreground="#000000")
		self.offbtn.configure(highlightbackground="#d9d9d9")
		self.offbtn.configure(highlightcolor="black")
		self.offbtn.configure(pady="0")
		self.offbtn.configure(text='''NO''')

		Label8 = tk.Label(self)
		Label8.place(relx=0.325, rely=0.708, height=38, width=100)
		Label8.configure(activebackground="#f9f9f9")
		Label8.configure(activeforeground="black")
		Label8.configure(disabledforeground="#a3a3a3")
		Label8.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label8.configure(foreground="#000000")
		Label8.configure(highlightbackground="#d9d9d9")
		Label8.configure(highlightcolor="black")
		Label8.configure(text='''Vacation:''')

		Label9 = tk.Label(self)
		Label9.place(relx=0.625, rely=0.708, height=38, width=90)
		Label9.configure(activebackground="#f9f9f9")
		Label9.configure(activeforeground="black")
		Label9.configure(disabledforeground="#a3a3a3")
		Label9.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label9.configure(foreground="#000000")
		Label9.configure(highlightbackground="#d9d9d9")
		Label9.configure(highlightcolor="black")
		Label9.configure(text='''Holiday:''')

		self.holbtn = tk.Button(self)
		self.holbtn.place(relx=0.75, rely=0.708, height=40, width=60)
		self.holbtn.configure(activebackground="#ececec")
		self.holbtn.configure(activeforeground="#000000")
		self.holbtn.configure(disabledforeground="#a3a3a3")
		self.holbtn.configure(font="-family {Minion Pro} -size 14 -weight bold")
		self.holbtn.configure(foreground="#000000")
		self.holbtn.configure(highlightbackground="#d9d9d9")
		self.holbtn.configure(highlightcolor="black")
		self.holbtn.configure(pady="0")
		self.holbtn.configure(text='''NO''')

		Label10 = tk.Label(self)
		Label10.place(relx=0.063, rely=0.833, height=38, width=148)
		Label10.configure(activebackground="#f9f9f9")
		Label10.configure(activeforeground="black")
		Label10.configure(disabledforeground="#a3a3a3")
		Label10.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label10.configure(foreground="#000000")
		Label10.configure(highlightbackground="#d9d9d9")
		Label10.configure(highlightcolor="black")
		Label10.configure(text='''Low Earnings:''')

		self.lowbtn = tk.Button(self)
		self.lowbtn.place(relx=0.26, rely=0.833, height=40, width=60)
		self.lowbtn.configure(activebackground="#ececec")
		self.lowbtn.configure(activeforeground="#000000")
		self.lowbtn.configure(disabledforeground="#a3a3a3")
		self.lowbtn.configure(font="-family {Minion Pro} -size 14 -weight bold")
		self.lowbtn.configure(foreground="#000000")
		self.lowbtn.configure(highlightbackground="#d9d9d9")
		self.lowbtn.configure(highlightcolor="black")
		self.lowbtn.configure(pady="0")
		self.lowbtn.configure(text='''NO''')

		recsubbtn = tk.Button(self, command=lambda: [controller.show_frame(RecEmp)])
		recsubbtn.place(relx=0.825, rely=0.833, height=40, width=130)
		recsubbtn.configure(activebackground="#ececec")
		recsubbtn.configure(activeforeground="#000000")
		recsubbtn.configure(disabledforeground="#a3a3a3")
		recsubbtn.configure(font="-family {Minion Pro} -size 14 -weight bold")
		recsubbtn.configure(foreground="#000000")
		recsubbtn.configure(highlightbackground="#d9d9d9")
		recsubbtn.configure(highlightcolor="black")
		recsubbtn.configure(pady="0")
		recsubbtn.configure(text='''Submit''')

		Label11 = tk.Label(self)
		Label11.place(relx=0.225, rely=0.229, height=38, width=12)
		Label11.configure(activebackground="#f9f9f9")
		Label11.configure(activeforeground="black")
		Label11.configure(disabledforeground="#a3a3a3")
		Label11.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label11.configure(foreground="#000000")
		Label11.configure(highlightbackground="#d9d9d9")
		Label11.configure(highlightcolor="black")
		Label11.configure(text=''':''')

		Label11_9 = tk.Label(self)
		Label11_9.place(relx=0.225, rely=0.333, height=38, width=11)
		Label11_9.configure(activebackground="#f9f9f9")
		Label11_9.configure(activeforeground="black")
		Label11_9.configure(disabledforeground="#a3a3a3")
		Label11_9.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label11_9.configure(foreground="#000000")
		Label11_9.configure(highlightbackground="#d9d9d9")
		Label11_9.configure(highlightcolor="black")
		Label11_9.configure(text=''':''')

		Label11_10 = tk.Label(self)
		Label11_10.place(relx=0.225, rely=0.438, height=38, width=11)
		Label11_10.configure(activebackground="#f9f9f9")
		Label11_10.configure(activeforeground="black")
		Label11_10.configure(disabledforeground="#a3a3a3")
		Label11_10.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label11_10.configure(foreground="#000000")
		Label11_10.configure(highlightbackground="#d9d9d9")
		Label11_10.configure(highlightcolor="black")
		Label11_10.configure(text=''':''')

		Label11_11 = tk.Label(self)
		Label11_11.place(relx=0.613, rely=0.229, height=38, width=11)
		Label11_11.configure(activebackground="#f9f9f9")
		Label11_11.configure(activeforeground="black")
		Label11_11.configure(disabledforeground="#a3a3a3")
		Label11_11.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label11_11.configure(foreground="#000000")
		Label11_11.configure(highlightbackground="#d9d9d9")
		Label11_11.configure(highlightcolor="black")
		Label11_11.configure(text=''':''')

		Label11_7 = tk.Label(self)
		Label11_7.place(relx=0.613, rely=0.333, height=38, width=11)
		Label11_7.configure(activebackground="#f9f9f9")
		Label11_7.configure(activeforeground="black")
		Label11_7.configure(disabledforeground="#a3a3a3")
		Label11_7.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label11_7.configure(foreground="#000000")
		Label11_7.configure(highlightbackground="#d9d9d9")
		Label11_7.configure(highlightcolor="black")
		Label11_7.configure(text=''':''')

		Label11_8 = tk.Label(self)
		Label11_8.place(relx=0.613, rely=0.438, height=38, width=11)
		Label11_8.configure(activebackground="#f9f9f9")
		Label11_8.configure(activeforeground="black")
		Label11_8.configure(disabledforeground="#a3a3a3")
		Label11_8.configure(font="-family {Minion Pro} -size 14 -weight bold")
		Label11_8.configure(foreground="#000000")
		Label11_8.configure(highlightbackground="#d9d9d9")
		Label11_8.configure(highlightcolor="black")
		Label11_8.configure(text=''':''')

		TSeparator1_10 = ttk.Separator(self)
		TSeparator1_10.place(relx=0.488, rely=0.188, relheight=0.354)
		TSeparator1_10.configure(orient="vertical")

		self.nameLb = tk.Label(self)
		self.nameLb.place(relx=0.55, rely=0.021, height=38, width=200)
		self.nameLb.configure(activebackground="#f9f9f9")
		self.nameLb.configure(activeforeground="black")
		self.nameLb.configure(disabledforeground="#a3a3a3")
		self.nameLb.configure(font="-family {Minion Pro} -size 14 -weight bold")
		self.nameLb.configure(foreground="#000000")
		self.nameLb.configure(highlightbackground="#d9d9d9")
		self.nameLb.configure(highlightcolor="black")
		self.nameLb.configure(text='''SHOW NAME''')

		otpolbtn = tk.Button(self)
		otpolbtn.place(relx=0.488, rely=0.833, height=40, width=118)
		otpolbtn.configure(activebackground="#ececec")
		otpolbtn.configure(activeforeground="#000000")
		otpolbtn.configure(disabledforeground="#a3a3a3")
		otpolbtn.configure(font="-family {Minion Pro} -size 14 -weight bold")
		otpolbtn.configure(foreground="#000000")
		otpolbtn.configure(highlightbackground="#d9d9d9")
		otpolbtn.configure(highlightcolor="black")
		otpolbtn.configure(pady="0")
		otpolbtn.configure(text='''OT Policy''')
		
		recmainmenubtn = tk.Button(self, command=lambda: [controller.show_frame(MainMenu)])
		recmainmenubtn.place(relx=0.65, rely=0.833, height=40, width=128)
		recmainmenubtn.configure(activebackground="#ececec")
		recmainmenubtn.configure(activeforeground="#000000")
		recmainmenubtn.configure(disabledforeground="#a3a3a3")
		recmainmenubtn.configure(font="-family {Minion Pro} -size 14 -weight bold")
		recmainmenubtn.configure(foreground="#000000")
		recmainmenubtn.configure(highlightbackground="#d9d9d9")
		recmainmenubtn.configure(highlightcolor="black")
		recmainmenubtn.configure(pady="0")
		recmainmenubtn.configure(text='''Main Menu''')
		recmainmenubtn.configure(width=128)

###
class  EditEmployeeList(tk.Frame):
	
	def __init__(self,parent,controller):
		tk.Frame.__init__(self,parent)
		
		font14 = "-family {Minion Pro} -size 14 -weight bold"
		font16 = "-family {Minion Pro} -size 16 -weight bold"
		font21 = "-family {Times New Roman} -size 14"
		self.option_add("*TCombobox*Listbox*Font",font16)
		
		# subcategory is used to know which employee edit feature is being used in order to submit to the database the correct information
		# 0=reset (nothing can be submitted) 1= new employee 2= edit current employee 3= reinstate previous employee
		subcategory = tk.StringVar()
		subcategory.set('0')

		def newemp():
			empCx.configure(state = 'disabled')
			empCx.set('')
			firstEy.configure(state = 'normal')
			midEy.configure(state = 'normal')
			lastEy.configure(state = 'normal')
			firstEy.delete(0,'end')
			midEy.delete(0,'end')
			lastEy.delete(0,'end')
			tstr.set('NO')
			termBn.configure(text=tstr.get())
			subcategory.set('1')
			submitBn.configure(state = 'normal')
		
		newBn = tk.Button(self,command = lambda:newemp())
		newBn.place(relx=0.013, rely=0.021, height=40, width=130)
		newBn.configure(activebackground="#ececec")
		newBn.configure(activeforeground="#000000")
		newBn.configure(background="#d9d9d9")
		newBn.configure(disabledforeground="#a3a3a3")
		newBn.configure(font=font14)
		newBn.configure(foreground="#000000")
		newBn.configure(highlightbackground="#d9d9d9")
		newBn.configure(highlightcolor="black")
		newBn.configure(pady="0")
		newBn.configure(text='''New''')

		def editemp():
			db=TimeCardDB()
			cbvalue = db.listActiveEmployees()
			empCx.set('')
			empCx.configure(state = 'readonly')
			empCx.configure(values=cbvalue)
			firstEy.delete(0,'end')
			midEy.delete(0,'end')
			lastEy.delete(0,'end')
			firstEy.configure(state = 'disabled')
			midEy.configure(state = 'disabled')
			lastEy.configure(state = 'disabled')
			tstr.set('NO')
			termBn.configure(text=tstr.get())
			subcategory.set('2')
			submitBn.configure(state = 'disabled')
			db.dbclose()
			
		self.editBn = tk.Button(self, command = lambda:editemp())
		self.editBn.place(relx=0.013, rely=0.104, height=40, width=130)
		self.editBn.configure(activebackground="#ececec")
		self.editBn.configure(activeforeground="#000000")
		self.editBn.configure(background="#d9d9d9")
		self.editBn.configure(disabledforeground="#a3a3a3")
		self.editBn.configure(font=font14)
		self.editBn.configure(foreground="#000000")
		self.editBn.configure(highlightbackground="#d9d9d9")
		self.editBn.configure(highlightcolor="black")
		self.editBn.configure(pady="0")
		self.editBn.configure(text='''Edit''')

		def reinemp():
			db=TimeCardDB()
			cbvalue = db.listTermEmployees()
			empCx.set('')
			empCx.configure(state = 'readonly')
			empCx.configure(values=cbvalue)
			firstEy.delete(0,'end')
			midEy.delete(0,'end')
			lastEy.delete(0,'end')
			firstEy.configure(state = 'disabled')
			midEy.configure(state = 'disabled')
			lastEy.configure(state = 'disabled')
			tstr.set('YES')
			subcategory.set('3')
			termBn.configure(text=tstr.get())
			submitBn.configure(state = 'disabled')
			db.dbclose()
			
			
		reinBn = tk.Button(self, command = lambda:[reinemp()])
		reinBn.place(relx=0.013, rely=0.188, height=40, width=130)
		reinBn.configure(activebackground="#ececec")
		reinBn.configure(activeforeground="#000000")
		reinBn.configure(background="#d9d9d9")
		reinBn.configure(disabledforeground="#a3a3a3")
		reinBn.configure(font=font14)
		reinBn.configure(foreground="#000000")
		reinBn.configure(highlightbackground="#d9d9d9")
		reinBn.configure(highlightcolor="black")
		reinBn.configure(pady="0")
		reinBn.configure(text='''Reinstate''')
		
		def RecordReset():
			empCx.configure(state = 'disabled')
			empCx.set('')
			firstEy.delete(0,'end')
			midEy.delete(0,'end')
			lastEy.delete(0,'end')
			firstEy.configure(state = 'disabled')
			midEy.configure(state = 'disabled')
			lastEy.configure(state = 'disabled')
			tstr.set('NO')
			termBn.configure(text=tstr.get())
			termBn.configure(state = 'disabled')
			subcategory.set('0')
			submitBn.configure(state = 'disabled')
			

		mainBn = tk.Button(self,command=lambda: [controller.show_frame(MainMenu),RecordReset()])
		mainBn.place(relx=0.013, rely=0.333, height=40, width=130)
		mainBn.configure(activebackground="#ececec")
		mainBn.configure(activeforeground="#000000")
		mainBn.configure(background="#d9d9d9")
		mainBn.configure(disabledforeground="#a3a3a3")
		mainBn.configure(font=font14)
		mainBn.configure(foreground="#000000")
		mainBn.configure(highlightbackground="#d9d9d9")
		mainBn.configure(highlightcolor="black")
		mainBn.configure(pady="0")
		mainBn.configure(text='''Main Menu''')

		def submitemp():
			db = TimeCardDB()
			empCx.configure(state = 'disabled')
			if subcategory.get() == '1':
				db.newemployee(firstStrEy.get(),midStrEy.get(),lastStrEy.get())
			if subcategory.get() == '2':
				name = empCx.get()
				lNm,fNm,mNm = name.split()
				db.editEmployee(fNm, mNm, lNm, firstStrEy.get(), midStrEy.get(), lastStrEy.get(),tstr.get())
			if subcategory.get() == '3':
				name = empCx.get()
				lNm,fNm,mNm = name.split()
				db.editEmployee(fNm, mNm, lNm, firstStrEy.get(), midStrEy.get(), lastStrEy.get(),tstr.get())
			mStr = "First: {}\n Middle: {}\n Last: {} \n Terminated: {}"
			messagebox.showinfo("Submission", mStr.format(firstStrEy.get(),midStrEy.get(),lastStrEy.get(),tstr.get()))
			firstEy.delete(0,'end')
			midEy.delete(0,'end')
			lastEy.delete(0,'end')
			firstEy.configure(state = 'disabled')
			midEy.configure(state = 'disabled')
			lastEy.configure(state = 'disabled')
			tstr.set('NO')
			empCx.set('')
			termBn.configure(text=tstr.get())
			termBn.configure(state = 'disabled')
			submitBn.configure(state = 'disabled')
			subcategory.set('0')
			db.dbclose()
			
		submitBn = tk.Button(self, command = lambda: submitemp())
		submitBn.place(relx=0.775, rely=0.438, height=40, width=130)
		submitBn.configure(activebackground="#ececec")
		submitBn.configure(state = 'disabled')
		submitBn.configure(activeforeground="#000000")
		submitBn.configure(background="#d9d9d9")
		submitBn.configure(disabledforeground="#a3a3a3")
		submitBn.configure(font=font14)
		submitBn.configure(foreground="#000000")
		submitBn.configure(highlightbackground="#d9d9d9")
		submitBn.configure(highlightcolor="black")
		submitBn.configure(pady="0")
		submitBn.configure(text='''Submit''')

		tstr = tk.StringVar()
		tstr.set('NO')
		def termchange():
			if tstr.get() == 'NO':
				tstr.set('YES')
				termBn.configure(text=tstr.get())
			else:
				tstr.set('NO')
				termBn.configure(text=tstr.get())

		termBn = tk.Button(self, command = lambda:termchange())
		termBn.place(relx=0.5, rely=0.438, height=40, width=60 )
		termBn.configure(activebackground="#ececec")
		termBn.configure(state = 'disabled')
		termBn.configure(activeforeground="#000000")
		termBn.configure(background="#d9d9d9")
		termBn.configure(disabledforeground="#a3a3a3")
		termBn.configure(font=font14)
		termBn.configure(foreground="#000000")
		termBn.configure(highlightbackground="#d9d9d9")
		termBn.configure(highlightcolor="black")
		termBn.configure(pady="0")
		termBn.configure(text=tstr.get())

		def fillentries(event):
			name = empCx.get()
			lNm,fNm,mNm = name.split()
			firstStrEy.set(fNm)
			midStrEy.set(mNm)
			lastStrEy.set(lNm)
			firstEy.configure(state = 'normal')
			midEy.configure(state = 'normal')
			lastEy.configure(state = 'normal')
			termBn.configure(state = 'normal')
			submitBn.configure(state = 'normal')

		combostyle = ttk.Style()
		combostyle.theme_settings('default', {'TCombobox': { 
												'map': {
													'background': [("readonly","#d9d9d9"),
																	("disabled","#d9d9d9")],
													'fieldbackground': [("readonly","#f9f9f9"),
																	('disabled','#d9d9d9')],
													'selectbackground': [('readonly','#004cff'),
																	('disabled','#004cff')]}}})
		empCx = ttk.Combobox(self)
		empCx.configure(state = 'disabled')
		empCx.configure(font=font14)
		empCx.place(relx=0.5, rely=0.021, relheight=0.083, relwidth=0.438)
		empCx.bind("<<ComboboxSelected>>", fillentries)

		fnLl = tk.Label(self)
		fnLl.place(relx=0.340, rely=0.125, height=40, width=125)
		fnLl.configure(activebackground="#f9f9f9")
		fnLl.configure(activeforeground="black")
		fnLl.configure(background="#d9d9d9")
		fnLl.configure(disabledforeground="#a3a3a3")
		fnLl.configure(font=font14)
		fnLl.configure(foreground="#000000")
		fnLl.configure(highlightbackground="#d9d9d9")
		fnLl.configure(highlightcolor="black")
		fnLl.configure(text='''First Name:''')

		mi = tk.Label(self)
		mi.place(relx=0.308, rely=0.229, height=40, width=150)
		mi.configure(activebackground="#f9f9f9")
		mi.configure(activeforeground="black")
		mi.configure(background="#d9d9d9")
		mi.configure(disabledforeground="#a3a3a3")
		mi.configure(font=font14)
		mi.configure(foreground="#000000")
		mi.configure(highlightbackground="#d9d9d9")
		mi.configure(highlightcolor="black")
		mi.configure(text='''Middle Initial:''')

		lln = tk.Label(self)
		lln.place(relx=0.346, rely=0.333, height=40, width=119)
		lln.configure(activebackground="#f9f9f9")
		lln.configure(activeforeground="black")
		lln.configure(background="#d9d9d9")
		lln.configure(disabledforeground="#a3a3a3")
		lln.configure(font=font14)
		lln.configure(foreground="#000000")
		lln.configure(highlightbackground="#d9d9d9")
		lln.configure(highlightcolor="black")
		lln.configure(text='''Last Name:''')

		termLb = tk.Label(self)
		termLb.place(relx=0.349, rely=0.438, height=40, width=118)
		termLb.configure(background="#d9d9d9")
		termLb.configure(disabledforeground="#a3a3a3")
		termLb.configure(font=font14)
		termLb.configure(foreground="#000000")
		termLb.configure(text='''Terminate:''')

		chempLb = tk.Label(self)
		chempLb.place(relx=0.248, rely=0.021, height=38, width=200)
		chempLb.configure(background="#d9d9d9")
		chempLb.configure(disabledforeground="#a3a3a3")
		chempLb.configure(font=font14)
		chempLb.configure(foreground="#000000")
		chempLb.configure(text='''Choose Employee:''')
		
		firstStrEy = tk.StringVar()
		firstEy = tk.Entry(self)
		firstEy.place(relx=0.5, rely=0.125,height=40, relwidth=0.25)
		firstEy.configure(background="white")
		firstEy.configure(state = 'disabled')
		firstEy.configure(disabledforeground="#a3a3a3")
		firstEy.configure(font=font21)
		firstEy.configure(foreground="#000000")
		firstEy.configure(insertbackground="black")
		firstEy.configure(textvariable = firstStrEy)

		midStrEy = tk.StringVar()
		midEy = tk.Entry(self)
		midEy.place(relx=0.5, rely=0.229,height=40, relwidth=0.063)
		midEy.configure(background="white")
		midEy.configure(state = 'disabled')
		midEy.configure(disabledforeground="#a3a3a3")
		midEy.configure(font=font21)
		midEy.configure(foreground="#000000")
		midEy.configure(insertbackground="black")
		midEy.configure(textvariable = midStrEy)

		lastStrEy = tk.StringVar()
		lastEy = tk.Entry(self)
		lastEy.place(relx=0.5, rely=0.333,height=40, relwidth=0.25)
		lastEy.configure(background="white")
		lastEy.configure(state = 'disabled')
		lastEy.configure(disabledforeground="#a3a3a3")
		lastEy.configure(font=font21)
		lastEy.configure(foreground="#000000")
		lastEy.configure(insertbackground="black")
		lastEy.configure(textvariable = lastStrEy)

		TSeparator1 = ttk.Separator(self)
		TSeparator1.place(relx=0.0, rely=0.542, relwidth=0.995)	

###

def getdatetime(self):
	cmnt = tk.StringVar()
	cday = tk.StringVar()
	cyr = tk.StringVar()
	cthr = tk.StringVar()
	cmin = tk.StringVar()
	cap = tk.StringVar()
	currentDT = datetime.datetime.now()
	cmnt.set(currentDT.strftime("%B"))
	cday.set(currentDT.strftime("%d"))
	cyr.set(currentDT.strftime("%Y"))
	cthr.set(currentDT.strftime("%I"))
	cmin.set(currentDT.strftime("%M"))
	cap.set(currentDT.strftime("%p"))

	return cmnt, cday, cyr, cthr, cmin, cap

app = GFPTime()
#app.wm_geometry('800x480')
app.mainloop()
