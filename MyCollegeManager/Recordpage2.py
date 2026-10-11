import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview, Combobox

import pymysql

from printoutpage import my_cust_PDF


class Record2Class:
    def __init__(self,pwindow):
        self.window = Toplevel(pwindow)  # create window that is depends on pwindow(homepage)
        # ------------- settings ----------------------
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        w1 = w-50
        h1 = h-250

        self.window.minsize(w1,h1)
        self.window.geometry("%dx%d+%d+%d"%(w1,h1,5,160)) # w*h+x+y

        #----------------- WIDGETS -------------------------
        mycolor1 = '#C1C8E4'
        mycolor2 = '#5AB9EA'
        myfont1 = ('Cambria',14,'bold')
        self.window.config(background=mycolor1)

        self.headlbl = Label(self.window,text="Student Record",background=mycolor2,font=('Cambria',22,'bold'),relief='groove',borderwidth=3)

        self.v1 = StringVar()
        self.c1 = Combobox(self.window,textvariable=self.v1,font=myfont1,state='readonly')
        self.c1.bind("<<ComboboxSelected>>",lambda e: self.get_all_data())

        #----------- table --------------
        self.mytable1 = Treeview(self.window,columns=['c1','c2','c3','c4','c5','c6','c7','c8'],height=18)

        self.mytable1.heading('c1',text='Roll no')
        self.mytable1.heading('c2',text='Name')
        self.mytable1.heading('c3',text='Phone')
        self.mytable1.heading('c4',text='Gender')
        self.mytable1.heading('c5',text='DOB')
        self.mytable1.heading('c6',text='Address')
        self.mytable1.heading('c7',text='Department')
        self.mytable1.heading('c8',text='Course')
        self.mytable1['show']='headings'
        self.mytable1.column('c1',width=100,anchor='n')
        self.mytable1.column('c2',width=200,anchor='s')
        self.mytable1.column('c3',width=100,anchor='e')
        self.mytable1.column('c4',width=100,anchor='w')
        self.mytable1.column('c5',width=100,anchor='center')
        self.mytable1.column('c6',width=200,anchor='center')
        self.mytable1.column('c7',width=200,anchor='center')
        self.mytable1.column('c8',width=200,anchor='center')


        #------------------- buttons ---------------------
        self.b1 = Button(self.window,text="Print",font=myfont1,background=mycolor2,command=self.get_printout)

        #---------- placements --------------------------
        self.headlbl.place(x=0,y=0,width=w1,height=70)
        x1 = 150
        y1 = 100
        x_diff = 150
        y_diff = 50

        self.c1.place(x=x1,y=y1)
        y1+=y_diff
        self.mytable1.place(x=x1,y=y1)
        self.b1.place(x=int(w1/2)-100,y=h1-100,width=200,height=40)


        #----------- calling required functions ----------
        self.databaseConnection()
        self.get_all_department()
        self.window.mainloop()
    def get_printout(self):
        pdf = my_cust_PDF()

        headings = ['Rollno', 'Name', 'Phone No', 'Gender', 'DOB', 'Address', 'Department', 'Course']


        pdf.content(f"Student Record By Department {self.v1.get()}", headings, self.pdata)

        pdf.output('pdf_file1.pdf')
        os.system('explorer.exe "pdf_file1.pdf"')


    def databaseConnection(self):
        try:
            self.conn = pymysql.connect(host='localhost',user='root',password='',db='my_college_db')
            self.curr = self.conn.cursor()
        except Exception as e:
                messagebox.showerror('Database Error','Error : \n'+str(e),parent=self.window)

    def get_all_data(self):
        try:
            self.mytable1.delete(*self.mytable1.get_children())
            # rollno	name	phone	gender	dob	address	department	course
            qry =" select * from student where department=%s"
            rowcount = self.curr.execute(qry,(self.v1.get()))
            data = self.curr.fetchall()
            # print(data)
            self.pdata = []
            if data:
                for row in data:
                    self.mytable1.insert('',END,values=row)
                    self.pdata.append(row)
            else:
                messagebox.showwarning('Empty','No Record Found',parent=self.window)
        except Exception as e:
                messagebox.showerror('Query Error','Error : \n'+str(e),parent=self.window)

    def get_all_department(self):
        try:
            qry =" select * from department"
            rowcount = self.curr.execute(qry)
            data = self.curr.fetchall()
            self.dept_list=[]
            if data:
                self.c1.set("Choose Department")
                for row in data:
                    self.dept_list.append(row[0])
            else:
                self.c1.set("No Department")

            self.c1.config(values=self.dept_list)
        except Exception as e:
                messagebox.showerror('Query Error','Error : \n'+str(e),parent=self.window)

#---------- testing -------------
if __name__ == '__main__':
    dummywindow = Tk()
    Record2Class(dummywindow)
    dummywindow.mainloop()