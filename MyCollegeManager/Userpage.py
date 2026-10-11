from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview

import face_recognition
import pymysql
from tkcalendar import DateEntry
from PIL import Image,ImageTk
class UserClass:
    defaultname = "default2.png"
    def __init__(self,pwindow):
        # self.window = Tk()  # create independent window
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

        self.headlbl = Label(self.window,text="User",background=mycolor2,font=('Cambria',22,'bold'),relief='groove',borderwidth=3)

        self.L1 = Label(self.window,text="Username",background=mycolor1,font=myfont1)
        self.L2 = Label(self.window,text="Password",background=mycolor1,font=myfont1)
        self.L3 = Label(self.window,text="Usertype",background=mycolor1,font=myfont1)
        self.L4 = Label(self.window,text="Picture",background=mycolor1,font=myfont1)

        self.t1 = Entry(self.window,font=myfont1)
        self.t2 = Entry(self.window,font=myfont1,show='*')
        self.v1 = StringVar()
        self.c1 = Combobox(self.window,values=['Admin','Employee'], textvariable=self.v1,font=myfont1,state='readonly')


        #----------- table --------------
        self.mytable1 = Treeview(self.window,columns=['c1','c2'],height=11)

        self.mytable1.heading('c1',text='Username')
        self.mytable1.heading('c2',text='Usertype')
        self.mytable1['show']='headings'
        self.mytable1.column('c1',width=200,anchor='center')
        self.mytable1.column('c2',width=200,anchor='center')

        self.mytable1.bind("<ButtonRelease-1>",lambda e: self.get_selected_row())

        #------------------- buttons ---------------------
        self.b1 = Button(self.window,text="Save",font=myfont1,background=mycolor2,command=self.save_data)
        self.b2 = Button(self.window,text="Update",font=myfont1,background=mycolor2,command=self.update_data)
        self.b3 = Button(self.window,text="Delete",font=myfont1,background=mycolor2,command=self.delete_data)
        self.b4 = Button(self.window,text="Fetch",font=myfont1,background=mycolor2,command=self.fetch_data)
        self.b5 = Button(self.window,text="Search",font=myfont1,background=mycolor2,command=self.get_all_data)


        self.imglbl = Label(self.window,relief='groove',borderwidth=1)
        self.b6 = Button(self.window,text="Choose",font=myfont1,background=mycolor2,command=self.chooseImage)
        self.b7 = Button(self.window,text="Capture",font=myfont1,background=mycolor2,command=self.capture_new)

        #---------- placements --------------------------
        self.headlbl.place(x=0,y=0,width=w1,height=70)
        x1 = 10
        y1 = 100
        x_diff = 150
        y_diff = 50

        self.L1.place(x=x1,y=y1)
        self.t1.place(x=x1+x_diff,y=y1)
        self.b4.place(x=x1+x_diff*2+80,y=y1,width=120,height=30)
        self.mytable1.place(x=x1+x_diff*3+80,y=y1)
        y1+=y_diff
        self.L2.place(x=x1,y=y1)
        self.t2.place(x=x1+x_diff,y=y1)
        self.b5.place(x=x1+x_diff*2+80,y=y1,width=120,height=30)
        y1+=y_diff
        self.L3.place(x=x1,y=y1)
        self.c1.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.L4.place(x=x1,y=y1)
        self.imgsize=150
        self.imglbl.place(x=x1+x_diff,y=y1 ,width=self.imgsize,height=self.imgsize)
        self.b6.place(x=x1+x_diff,y=y1+self.imgsize,width=self.imgsize,height=40)

        y1+=self.imgsize
        y1+=y_diff
        self.b7.place(x=x1+x_diff,y=y1,width=self.imgsize,height=40)
        y1+=50

        b_w = 120
        self.b1.place(x=x1,y=y1,width=b_w,height=40)
        self.b2.place(x=x1+x_diff,y=y1,width=b_w,height=40)
        self.b3.place(x=x1+x_diff*2,y=y1,width=b_w,height=40)



        #----------- calling required functions ----------

        self.window.bind("<FocusIn>", lambda e: self.show_capture_img())
        self.flag = False

        self.databaseConnection()
        self.clearpage()
        self.window.mainloop()




    def capture_new(self):
        self.flag = True
        from Capture_pic import CaptureClass
        obj = CaptureClass(self.window)
    def show_capture_img(self):
        if self.flag == True:
            self.flag = False  #reset
            filename = "captured_photo.jpg"

            #---  show image ---------
            self.img1 = Image.open(filename).resize((self.imgsize,self.imgsize)) # open and resize image
            self.pimg1 = ImageTk.PhotoImage(self.img1) # make photoimage as label can use this only
            self.imglbl.config(image=self.pimg1) # add image in label

            # -------- make name to use ------------
            path = filename.split("/")
            # print("path = ",path)
            name = path[-1]
            # print("name  = ",name)
            import time
            unique = str(int(time.time()))
            # print("unique = ",unique)
            self.actualname = unique+name
            # print("Actual Name = ",self.actualname)

            # detect face
            image = face_recognition.load_image_file(filename)
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) != 1:
                messagebox.showwarning("Input Error", "Please Select One Face Image ", parent=self.window)
                self.actualname = self.defaultname
                self.img1 = Image.open("user_image//" + self.actualname).resize((self.imgsize, self.imgsize))
                self.photoimg1 = ImageTk.PhotoImage(self.img1)
                self.imglbl.config(image=self.photoimg1)
                return False



    def chooseImage(self):
        filename = askopenfilename(filetypes=[ ('All Images',"*.jpg;*.png;*.jpeg") , ("png images ","*.png"),("Jpg Images","*.jpg")],parent=self.window)
        print("file name = ",filename)
        if filename!="":

            #---  show image ---------
            self.img1 = Image.open(filename).resize((self.imgsize,self.imgsize)) # open and resize image
            self.pimg1 = ImageTk.PhotoImage(self.img1) # make photoimage as label can use this only
            self.imglbl.config(image=self.pimg1) # add image in label

            # -------- make name to use ------------
            path = filename.split("/")
            # print("path = ",path)
            name = path[-1]
            # print("name  = ",name)
            import time
            unique = str(int(time.time()))
            # print("unique = ",unique)
            self.actualname = unique+name
            # print("Actual Name = ",self.actualname)

            # detect face
            image = face_recognition.load_image_file(filename)
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) != 1:
                messagebox.showwarning("Input Error", "Please Select One Face Image ", parent=self.window)
                self.actualname = self.defaultname
                self.img1 = Image.open("user_image//" + self.actualname).resize((self.imgsize, self.imgsize))
                self.photoimg1 = ImageTk.PhotoImage(self.img1)
                self.imglbl.config(image=self.photoimg1)
                return False

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
            #username	password	usertype	pic
            qry ="insert into user values(%s,%s,%s,%s)"
            rowcount = self.curr.execute(qry ,(self.t1.get(),self.t2.get(),self.v1.get(),self.actualname))
            self.conn.commit()
            if rowcount==1:

                #---- save image in folder -------
                if self.actualname!=self.defaultname:  # new image is selected
                    self.img1.save("user_image//"+self.actualname) # save in folder
                # ------------------
                messagebox.showinfo('Success','User Record Added successfully',parent=self.window)
                self.clearpage()
            else:
                messagebox.showwarning('Failure','User Record not Added \n Check All Fields',parent=self.window)
        except Exception as e:
                messagebox.showerror('Query Error','Error : \n'+str(e),parent=self.window)

    def update_data(self):
        if self.validation_check()==False:
            return # stop this function now
        try:
            #username	password	usertype	pic
            qry ="update user set password=%s, usertype=%s, pic=%s  where username=%s"
            rowcount = self.curr.execute(qry ,(self.t2.get(),self.v1.get(),self.actualname,self.t1.get()) )
            self.conn.commit()
            if rowcount==1:

                if self.actualname==self.oldname: # nothing new selected
                    pass
                else : # new image is selected
                    self.img1.save("user_image//"+self.actualname) # save in folder
                    if self.oldname==self.defaultname: # no image was given in past
                        # nothing to delete
                        pass
                    else:
                        import os
                        os.remove('user_image//'+self.oldname)


                messagebox.showinfo('Success','User Record Updated successfully',parent=self.window)
                self.clearpage()
            else:
                messagebox.showwarning('Failure','User Record not Updated \n Check All Fields',parent=self.window)
        except Exception as e:
                messagebox.showerror('Query Error','Error : \n'+str(e),parent=self.window)

    def delete_data(self):
        ans = messagebox.askquestion("Confirmation","Are you sure to delete?",parent=self.window)
        if ans=='yes':
            try:
                qry ="delete from user where username=%s"
                rowcount = self.curr.execute(qry ,(self.t1.get()) )
                self.conn.commit()
                if rowcount==1:
                    if self.oldname==self.defaultname: # no image was given in past
                        # nothing to delete
                        pass
                    else:
                        import os
                        os.remove('user_image//'+self.oldname)

                    messagebox.showinfo('Success','User Record Deleted successfully',parent=self.window)
                    self.clearpage()
                else:
                    messagebox.showwarning('Failure','User Record not Added \n Check All Fields',parent=self.window)
            except Exception as e:
                    messagebox.showerror('Query Error','Error : \n'+str(e),parent=self.window)

    def get_selected_row(self):
        id = self.mytable1.focus()
        # print("id = ",id)
        data = self.mytable1.item(id)
        # print("data = ",data)
        row_values = data['values']
        # print("Row values = ",row_values)
        pk_col = row_values[0]
        # print("pk column = ",pk_col)
        self.fetch_data(pk_col)

    def fetch_data(self,pk_column=None):
        if pk_column==None:
            un = self.t1.get()
        else:
            un = pk_column
        try:
            # rollno	name	phone	gender	dob	address	department	course
            qry =" select * from user where username=%s "
            rowcount = self.curr.execute(qry ,(un))
            data = self.curr.fetchone()
            # print(data)
            self.clearpage()
            if data:
                self.t1.insert(0,data[0])
                self.t2.insert(0,data[1])
                self.v1.set(data[2])
                self.actualname=data[3]
                self.oldname=data[3]

                self.img1 = Image.open("user_image//" + self.actualname).resize((self.imgsize, self.imgsize))  # open and resize image
                self.pimg1 = ImageTk.PhotoImage(self.img1)  # make photoimage as label can use this only
                self.imglbl.config(image=self.pimg1)  # add image in label
            else:
                messagebox.showwarning('Empty','No Record Found',parent=self.window)
        except Exception as e:
                messagebox.showerror('Query Error','Error : \n'+str(e),parent=self.window)

    def clearpage(self):
        self.t1.delete(0,END)
        self.t2.delete(0,END)
        self.c1.set("Choose Usertype")
        self.get_all_data()
        self.actualname=self.defaultname
        self.img1 = Image.open("user_image//"+self.actualname).resize((self.imgsize, self.imgsize))  # open and resize image
        self.pimg1 = ImageTk.PhotoImage(self.img1)  # make photoimage as label can use this only
        self.imglbl.config(image=self.pimg1)  # add image in label

    def get_all_data(self):
        try:
            self.mytable1.delete(*self.mytable1.get_children())
            ut = self.v1.get()
            if ut=="Choose Usertype":
                ut=""
            qry ="select * from user where usertype like %s"
            rowcount = self.curr.execute(qry,(ut+"%"))
            data = self.curr.fetchall()

            if data:
                for row in data:
                    r1 = [row[0],row[2]]
                    self.mytable1.insert('',END,values=r1)
            else:
                messagebox.showwarning('Empty','No Record Found',parent=self.window)
        except Exception as e:
                messagebox.showerror('Query Error','Error : \n'+str(e),parent=self.window)

    def validation_check(self):
        return True

#---------- testing -------------
if __name__ == '__main__':
    dummywindow = Tk()
    UserClass(dummywindow)
    dummywindow.mainloop()