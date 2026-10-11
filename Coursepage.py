from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview
import pymysql
from tkcalendar import DateEntry

class CourseClass:
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

        self.headlbl = Label(self.window,text="Course",background=mycolor2,font=('Cambria',22,'bold'),relief='groove',borderwidth=3)

        self.L1 = Label(self.window,text="Department",background=mycolor1,font=myfont1)
        self.L2 = Label(self.window,text="Course",background=mycolor1,font=myfont1)
        self.L3 = Label(self.window,text="Fee",background=mycolor1,font=myfont1)
        self.L4 = Label(self.window,text="Duration",background=mycolor1,font=myfont1)

        self.v1 = StringVar()
        self.c1 = Combobox(self.window,textvariable=self.v1,font=myfont1,state='readonly')
        self.t2 = Entry(self.window,font=myfont1)
        self.t3 = Entry(self.window,font=myfont1)
        self.t4 = Entry(self.window,font=myfont1)
        self.v2 = StringVar()
        self.c2 = Combobox(self.window,values=['Year(s)','Month(s)','Week(s)'],textvariable=self.v2,font=myfont1,state='readonly')

        #----------- table --------------
        self.mytable1 = Treeview(self.window,columns=['c1','c2','c3','c4','c5'],height=20)

        self.mytable1.heading('c1',text='Department')
        self.mytable1.heading('c2',text='Course')
        self.mytable1.heading('c3',text='Fee')
        self.mytable1.heading('c4',text='Duration')
        self.mytable1.heading('c5',text='Units')
        self.mytable1['show']='headings'
        self.mytable1.column('c1',width=100,anchor='center')
        self.mytable1.column('c2',width=100,anchor='center')
        self.mytable1.column('c3',width=100,anchor='center')
        self.mytable1.column('c4',width=100,anchor='center')
        self.mytable1.column('c5',width=100,anchor='center')
        self.mytable1.bind("<ButtonRelease-1>",lambda e: self.get_selected_row())

        #------------------- buttons ---------------------
        self.b1 = Button(self.window,text="Save",font=myfont1,background=mycolor2,command=self.save_data)
        self.b2 = Button(self.window,text="Update",font=myfont1,background=mycolor2,command=self.update_data)
        self.b3 = Button(self.window,text="Delete",font=myfont1,background=mycolor2,command=self.delete_data)
        self.b4 = Button(self.window,text="Fetch",font=myfont1,background=mycolor2,command=self.fetch_data)
        self.b5 = Button(self.window,text="Search",font=myfont1,background=mycolor2,command=self.get_all_data)

        #---------- placements --------------------------
        self.headlbl.place(x=0,y=0,width=w1,height=70)
        x1 = 10
        y1 = 100
        x_diff = 150
        y_diff = 50

        self.L1.place(x=x1,y=y1)
        self.c1.place(x=x1+x_diff,y=y1)
        self.b4.place(x=x1+x_diff*2+80,y=y1,width=120,height=30)
        self.mytable1.place(x=x1+x_diff*3+80,y=y1)
        y1+=y_diff
        self.L2.place(x=x1,y=y1)
        self.t2.place(x=x1+x_diff,y=y1)
        self.b5.place(x=x1+x_diff*2+80,y=y1,width=120,height=30)
        y1+=y_diff
        self.L3.place(x=x1,y=y1)
        self.t3.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.L4.place(x=x1,y=y1)
        self.t4.place(x=x1+x_diff,y=y1,width=120)
        self.c2.place(x=x1+x_diff+x_diff,y=y1,width=120)

        y1+=y_diff
        b_w = 120
        self.b1.place(x=x1,y=y1,width=b_w,height=40)
        self.b2.place(x=x1+x_diff,y=y1,width=b_w,height=40)
        self.b3.place(x=x1+x_diff*2,y=y1,width=b_w,height=40)

        #----------- calling required functions ----------
        self.databaseConnection()
        self.get_all_department()
        self.clearpage()
        self.window.mainloop()
    def databaseConnection(self):
        try:
            self.conn = pymysql.connect(host='localhost',user='root',password='',db='my_college_db')
            self.curr = self.conn.cursor()
        except Exception as e:
                messagebox.showerror('Query Error','Error : \n'+str(e),parent=self.window)

    def save_data(self):
        if self.validation_check()==False:
            return # stop this function now
        try:
            qry ="insert into course values(%s,%s,%s,%s,%s)"
            rowcount = self.curr.execute(qry ,(self.v1.get(),self.t2.get(),self.t3.get(),self.t4.get(),self.v2.get() ))
            self.conn.commit()
            if rowcount==1:
                messagebox.showinfo('Success','Course Record Added successfully',parent=self.window)
                self.clearpage()
            else:
                messagebox.showwarning('Failure','Course Record not Added \n Check All Fields',parent=self.window)
        except Exception as e:
                messagebox.showerror('Query Error','Error : \n'+str(e),parent=self.window)

    def update_data(self):
        if self.validation_check()==False:
            return # stop this function now
        try:
            #dname	cname	fee	duration	units

            qry ="update course set dname=%s, fee=%s, duration=%s, units=%s where cname=%s"
            rowcount = self.curr.execute(qry ,(self.v1.get(),self.t3.get(),self.t4.get(),self.v2.get(),self.t2.get() ))
            self.conn.commit()
            if rowcount==1:
                messagebox.showinfo('Success','Course Record Updated successfully',parent=self.window)
                self.clearpage()
            else:
                messagebox.showwarning('Failure','Course Record not Added \n Check All Fields',parent=self.window)
        except Exception as e:
                messagebox.showerror('Query Error','Error : \n'+str(e),parent=self.window)

    def delete_data(self):
        ans = messagebox.askquestion("Confirmation","Are you sure to delete?",parent=self.window)
        if ans=='yes':
            try:
                qry ="delete from course where cname=%s"
                rowcount = self.curr.execute(qry ,(self.t2.get()) )
                self.conn.commit()
                if rowcount==1:
                    messagebox.showinfo('Success','Course Record Deleted successfully',parent=self.window)
                    self.clearpage()
                else:
                    messagebox.showwarning('Failure','Course Record not Added \n Check All Fields',parent=self.window)
            except Exception as e:
                    messagebox.showerror('Query Error','Error : \n'+str(e),parent=self.window)

    def get_selected_row(self):
        id = self.mytable1.focus()
        # print("id = ",id)
        data = self.mytable1.item(id)
        # print("data = ",data)
        row_values = data['values']
        # print("Row values = ",row_values)
        pk_col = row_values[1]
        # print("pk column = ",pk_col)
        self.fetch_data(pk_col)

    def fetch_data(self,pk_column=None):
        if pk_column==None:
            crse = self.t2.get()
        else:
            crse = pk_column
        try:
            qry =" select * from course where cname=%s "
            rowcount = self.curr.execute(qry ,(crse))
            data = self.curr.fetchone()
            # print(data)
            self.clearpage()
            if data:
                self.v1.set(data[0])
                self.t2.insert(0,data[1])
                self.t3.insert(0,data[2])
                self.t4.insert(0,data[3])
                self.v2.set(data[4])
            else:
                messagebox.showwarning('Empty','No Record Found',parent=self.window)
        except Exception as e:
                messagebox.showerror('Query Error','Error : \n'+str(e),parent=self.window)

    def clearpage(self):
        self.c1.set("Choose Department")
        self.t2.delete(0,END)
        self.t3.delete(0,END)
        self.t4.delete(0,END)
        self.c2.current(0)
        self.get_all_data()

    def get_all_data(self):
        try:
            self.mytable1.delete(*self.mytable1.get_children())

            dept=self.v1.get()
            if dept=="Choose Department":
                dept=""

            qry =" select * from course where dname like %s"
            rowcount = self.curr.execute(qry,(dept+"%"))
            data = self.curr.fetchall()

            # print(data)
            if data:
                for row in data:
                    self.mytable1.insert('',END,values=row)
            else:
                messagebox.showwarning('Empty','No Record Found',parent=self.window)
        except Exception as e:
                messagebox.showerror('Query Error','Error : \n'+str(e),parent=self.window)

    def validation_check(self):
        return True

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
    CourseClass(dummywindow)
    dummywindow.mainloop()