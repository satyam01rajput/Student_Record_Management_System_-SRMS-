from tkinter import*
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class CourseClass:
    def __init__(self,root):
       self.root = root
       self.root.title("Result Management System")
       self.root.geometry("970x500+30+220")
       self.root.config(bg="white")
       self.root.focus_force()

       title=Label(self.root,text= "Manage Course Details",font=("goudy old style" , 20 , "bold"),bg="#033054",fg="white").place(x=1,y=5,width=970,height=40)

       self.var_course = StringVar()
       self.var_duration = StringVar()
       self.var_charges = StringVar()

       lbl_courseName = Label(self.root,text="Course Name",font=("goudy old style",15,'bold'),bg="white").place(x=10,y=60)
       lbl_duration = Label(self.root,text="Duration",font=("goudy old style",15,'bold'),bg="white").place(x=10,y=100)
       lbl_charges = Label(self.root,text="Charges",font=("goudy old style",15,'bold'),bg="white").place(x=10,y=140)
       lbl_description = Label(self.root,text="Description",font=("goudy old style",15,'bold'),bg="white").place(x=10,y=180)

       self.txt_courseName = Entry(self.root,textvariable=self.var_course,font=("goudy old style",15,'bold'),bg="lightyellow")
       self.txt_courseName.place(x=150,y=60,width=200)
       txt_duration = Entry(self.root,textvariable=self.var_duration,font=("goudy old style",15,'bold'),bg="lightyellow").place(x=150,y=100,width=200)
       txt_charges = Entry(self.root,textvariable=self.var_charges,font=("goudy old style",15,'bold'),bg="lightyellow").place(x=150,y=140,width=200)
       self.txt_description = Text(self.root,font=("goudy old style",15,'bold'),bg="lightyellow")
       self.txt_description.place(x=150,y=180,width=400,height=150)

       self.btd_add = Button(self.root,text="Save",font=("goudy old style",15,"bold"),bg="#065494",fg="white",cursor="hand2",command=self.add)
       self.btd_add.place(x=150,y=390,width=110,height=40)
       self.btd_update = Button(self.root,text="Update",font=("goudy old style",15,"bold"),bg="#2db940",fg="white",cursor="hand2",command=self.update)
       self.btd_update.place(x=270,y=390,width=110,height=40)
       self.btd_delete = Button(self.root,text="Delete",font=("goudy old style",15,"bold"),bg="#d81822",fg="white",cursor="hand2",command=self.delete)
       self.btd_delete.place(x=390,y=390,width=110,height=40)
       self.btd_clear = Button(self.root,text="Clear",font=("goudy old style",15,"bold"),bg="#646A6B",fg="white",cursor="hand2",command=self.clear)
       self.btd_clear.place(x=510,y=390,width=110,height=40)

       self.var_search = StringVar()
       lbl_search_courseName = Label(self.root,text="Course Name",font=("goudy old style",15,'bold'),bg="white").place(x=520,y=60)
       txt_search_courseName =  Entry(self.root,textvariable=self.var_search,font=("goudy old style",15,'bold'),bg="lightyellow").place(x=650,y=60,width=180)
       btn_search = Button(self.root,text="Search",font=("goudy old style",15,"bold"),bg="#065494",fg="white",cursor="hand2",command=self.search).place(x=850,y=60,width=110,height=30)

       self.C_Frame = Frame(self.root,bd=2,relief=RIDGE)
       self.C_Frame.place(x=650,y=100,width=310,height=340)

       scrolly=Scrollbar(self.C_Frame,orient=VERTICAL)
       scrollx=Scrollbar(self.C_Frame,orient=HORIZONTAL)
       self.course_Table = ttk.Treeview(self.C_Frame,columns=("id","name","duration","charges","description"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
       
       scrollx.pack(side=BOTTOM,fill=X)
       scrolly.pack(side=RIGHT,fill=Y)
       scrollx.config(command=self.course_Table.xview)
       scrolly.config(command=self.course_Table.yview)

       self.course_Table.heading("id",text="ID")
       self.course_Table.heading("name",text="Name")
       self.course_Table.heading("duration",text="Duration")
       self.course_Table.heading("charges",text="Charges")
       self.course_Table.heading("description",text="Description")
       self.course_Table["show"] = 'headings'
       self.course_Table.column("id",width=50)
       self.course_Table.column("name",width=150)
       self.course_Table.column("duration",width=100)
       self.course_Table.column("charges",width=100)
       self.course_Table.column("description",width=200)
       self.course_Table.pack(fill=BOTH,expand=1)
       self.course_Table.bind("<ButtonRelease-1>",self.get_data)
       self.show()

    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete("1.0",END)
        self.txt_courseName.config(state=NORMAL)

    def delete(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error","Course name should be required",parent=self.root)
            else:
                cur.execute("select * from course where name=?",(self.var_course.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Please select course from the list",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete",parent=self.root)
                    if op==True:
                        cur.execute("delete from course where name =?",(self.var_course.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Course Deleted",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")        



    def get_data(self,ev):
        self.txt_courseName.config(state="readonly")
        r=self.course_Table.focus()
        content=self.course_Table.item(r)
        row=content["values"]
        # print(row)

        if not row or len(row) < 5:  # Prevent IndexError (This 2 lines is added fromAI)
          return
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        # self.var_course.set(row[4])
        self.txt_description.delete("1.0",END)
        self.txt_description.insert(END,row[4])


    def add(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error","Course name should be required",parent=self.root)
            else:
                cur.execute("select * from course where name=?",(self.var_course.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Course name already present",parent=self.root)
                else:
                    cur.execute("insert into course(name,duration,charges,description)values(?,?,?,?)",(
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0",END)

                    ))
                    con.commit()
                    messagebox.showinfo("Success","Course Added Successfullly",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def update(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error","Course name should be required",parent=self.root)
            else:
                cur.execute("select * from course where name=?",(self.var_course.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Select Course from list",parent=self.root)
                else:
                    cur.execute("update course set duration=?,charges=?,description=? where name=?",(
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0",END),
                        self.var_course.get()

                    ))
                    con.commit()
                    messagebox.showinfo("Success","Course Updated Successfullly",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def show(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute("select * from course ")
            rows=cur.fetchall()
            self.course_Table.delete(*self.course_Table.get_children())
            for row in rows:
                self.course_Table.insert('',END,values=row)
            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur=con.cursor()
        try:
            cur.execute(f"select * from course where name LIKE '%{self.var_search.get()}%'")
            rows=cur.fetchall()
            self.course_Table.delete(*self.course_Table.get_children())
            for row in rows:
                self.course_Table.insert('',END,values=row)
            
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")



if __name__ == "__main__":
    root=Tk()
    obj=CourseClass(root)
    root.mainloop()