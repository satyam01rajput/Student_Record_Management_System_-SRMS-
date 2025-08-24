from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class reportClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Result Management System")
        self.root.geometry("1350x700+30+220")
        self.root.config(bg="white")
        self.root.focus_force()

        title = Label(self.root, text="View Student Result", font=("goudy old style", 20, "bold"), bg="#D4834D", fg="#262626")
        title.place(x=1, y=5, width=970, height=50)

        self.var_search = StringVar()
        self.var_id = ""

        # Search
        lbl_search = Label(self.root, text="Search By Roll No.", font=("goudy old style", 20, "bold"), bg="white").place(x=280, y=100)
        txt_search = Entry(self.root, textvariable=self.var_search, font=("goudy old style", 20, "bold"), bg="lightyellow")
        txt_search.place(x=520, y=100, width=150)
        
        btn_search = Button(self.root, text="Get", font=("goudy old style", 15, "bold"), bg="#065494", fg="white", cursor="hand2", command=self.search)
        btn_search.place(x=680, y=100, width=80, height=34)

        btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="grey", fg="white", cursor="hand2", command=self.clear)
        btn_clear.place(x=780, y=100, width=80, height=34)

        # Result Labels
        lbls = ["Roll No", "Name", "Course", "Marks Obtained", "Total Marks", "Percentage"]
        x_positions = [150, 300, 450, 600, 750, 900]
        for i, lbl in enumerate(lbls):
            Label(self.root, text=lbl, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE).place(x=x_positions[i], y=230, width=150, height=50)

        self.roll = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.roll.place(x=150, y=280, width=150, height=50)

        self.name = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.name.place(x=300, y=280, width=150, height=50)

        self.course = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.course.place(x=450, y=280, width=150, height=50)

        self.marks = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.marks.place(x=600, y=280, width=150, height=50)

        self.full = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.full.place(x=750, y=280, width=150, height=50)

        self.per = Label(self.root, font=("goudy old style", 15, "bold"), bg="white", bd=2, relief=GROOVE)
        self.per.place(x=900, y=280, width=150, height=50)

        # Delete Button
        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="red", fg="white", cursor="hand2", command=self.delete)
        btn_delete.place(x=500, y=350, width=150, height=34)

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error", "Roll No. should be req.", parent=self.root)
            else:
                cur.execute("SELECT * FROM result WHERE roll=?", (self.var_search.get(),))
                row = cur.fetchone()
                if row !=None:
                    self.var_id=row[0]
                    self.roll.config(text=row[1])
                    self.name.config(text=row[2])
                    self.course.config(text=row[3])
                    self.marks.config(text=row[6])
                    self.full.config(text=row[7])
                    self.per.config(text=row[8])
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

    def clear(self):
        self.var_id=""
        self.roll.config(text="")
        self.name.config(text="")
        self.course.config(text="")
        self.marks.config(text="")
        self.full.config(text="")
        self.per.config(text="")
        self.var_search.set("")

    def delete(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_id == "":
                messagebox.showerror("Error", "Search Student result first", parent=self.root)
            else:
                cur.execute("SELECT * FROM result WHERE rid=?", (self.var_id,))
                row = cur.fetchone()
                if row ==None:
                    messagebox.showerror("Error","Invalid Student Result",parent=self.root)
                    
                else:
                    op=messagebox.askyesno("Confirm","Do You Really want to delete",parent = self.root)
                    if op==True:
                        cur.execute("delete from result where rid=?",(self.var_id,))
                        con.commit()
                        messagebox.showinfo("Delete","Result Deleted Successfully",parent = self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
    

if __name__ == "__main__":
    root = Tk()
    obj = reportClass(root)
    root.mainloop()
