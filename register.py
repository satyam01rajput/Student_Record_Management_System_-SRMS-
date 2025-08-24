from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3
import os
import re   # regex for validation

class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Window")
        self.root.geometry("1350x700+15+20")
        self.root.config(bg="white")

        self.bg = ImageTk.PhotoImage(file="Imagesss/b22.png")
        bg = Label(self.root, image=self.bg).place(x=200, y=0, relwidth=1, relheight=1)

        self.left = ImageTk.PhotoImage(file="Imagesss/b2.jpg")
        left = Label(self.root, image=self.left).place(x=80, y=100, width=400, height=500)

        # Register Frame
        frame1 = Frame(self.root, bg="white")
        frame1.place(x=480, y=100, width=700, height=500)

        title = Label(frame1, text="Register Here", font=("times new roman", 20, "bold"), bg="white", fg="darkgreen").place(x=50, y=30)

        # Row 1
        f_name = Label(frame1, text="First Name", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=100)
        self.txt_fname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_fname.place(x=50, y=130, width=250)

        l_name = Label(frame1, text="Last Name", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=100)
        self.txt_lname = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_lname.place(x=370, y=130, width=250)

        # Row 2
        contact = Label(frame1, text="Contact No.", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=170)
        self.txt_contact = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_contact.place(x=50, y=200, width=250)

        email = Label(frame1, text="Email", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=170)
        self.txt_email = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_email.place(x=370, y=200, width=250)

        # Row 3
        question = Label(frame1, text="Security Question.", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=240)
        self.cmb_que = ttk.Combobox(frame1, font=("times new roman", 13), state='readonly', justify=CENTER)
        self.cmb_que['values'] = ("Select", "First School Name", "Birth Place", "Pet Name", "Your best friend")
        self.cmb_que.place(x=50, y=270, width=250)
        self.cmb_que.current(0)

        answer = Label(frame1, text="Answer", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=240)
        self.txt_answer = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_answer.place(x=370, y=270, width=250)

        # Row 4
        password = Label(frame1, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=50, y=310)
        self.txt_password = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_password.place(x=50, y=340, width=250)

        cpassword = Label(frame1, text="Confirm password", font=("times new roman", 15, "bold"), bg="white", fg="gray").place(x=370, y=310)
        self.txt_cpassword = Entry(frame1, font=("times new roman", 15), bg="lightgray")
        self.txt_cpassword.place(x=370, y=340, width=250)

        # T&C
        self.var_chk = IntVar()
        chk = Checkbutton(frame1, text="I Agree to the terms and conditions", variable=self.var_chk, onvalue=1, offvalue=0, bg="white", font=("times new roman", 12)).place(x=50, y=380)

        btn_register = Button(frame1, text="Register Now", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.register_data).place(x=50, y=420, width=200, height=40)
        btn_login = Button(self.root, text="Sign In", command=self.login_window, font=("goudy old style", 15, "bold"), bg="#609bb9", cursor="hand2").place(x=180, y=460, width=200, height=40)

    def login_window(self):
        self.root.destroy()
        os.system("python login.py")

    def clear(self):
        self.txt_fname.delete(0, END)
        self.txt_lname.delete(0, END)
        self.txt_contact.delete(0, END)
        self.txt_email.delete(0, END)
        self.txt_answer.delete(0, END)
        self.txt_password.delete(0, END)
        self.txt_cpassword.delete(0, END)
        self.cmb_que.current(0)

    def register_data(self):
        # Empty fields check
        if (self.txt_fname.get()=="" or self.txt_email.get()=="" or 
            self.cmb_que.get()=="Select" or self.txt_answer.get()=="" or 
            self.txt_password.get()=="" or self.txt_cpassword.get()=="" or 
            self.txt_contact.get()==""):
            messagebox.showerror("Error", "All Fields are Required", parent=self.root)

        # First & Last name validation (alphabets only)
        elif not re.fullmatch(r"[A-Za-z]+", self.txt_fname.get()):
            messagebox.showerror("Error", "First name must contain only alphabets", parent=self.root)
        elif not re.fullmatch(r"[A-Za-z]+", self.txt_lname.get()):
            messagebox.showerror("Error", "Last name must contain only alphabets", parent=self.root)

        # Contact validation
        elif not re.fullmatch(r"[0-9]{10}", self.txt_contact.get()):
            messagebox.showerror("Error", "Contact Number must be exactly 10 digits", parent=self.root)

        # Email validation
        elif not re.fullmatch(r"[a-zA-Z0-9._%+-]+@gmail\.com", self.txt_email.get()):
            messagebox.showerror("Error", "Email must be valid and end with @gmail.com", parent=self.root)

        # Password match
        elif self.txt_password.get() != self.txt_cpassword.get():
            messagebox.showerror("Error", "Password Must Be Same", parent=self.root)

        # Terms & conditions
        elif self.var_chk.get() == 0:
            messagebox.showerror("Error", "Please agree our T&C", parent=self.root)

        else:
            try:
                con = sqlite3.connect(database="rms.db")
                cur = con.cursor()
                cur.execute("select * from employee where email=?", (self.txt_email.get(),))
                row = cur.fetchone()

                if row != None:
                    messagebox.showerror("Error", "User Already Exists", parent=self.root)
                else:
                    cur.execute(
                        "insert into employee(f_name, l_name, contact, email, question, answer, password) values (?, ?, ?, ?, ?, ?, ?)",
                        (
                            self.txt_fname.get(),
                            self.txt_lname.get(),
                            self.txt_contact.get(),
                            self.txt_email.get(),
                            self.cmb_que.get(),
                            self.txt_answer.get(),
                            self.txt_password.get()
                        )
                    )

                    con.commit()
                    con.close()
                    messagebox.showinfo("Success", "Registration Successful", parent=self.root)
                    self.clear()
                    self.login_window()
            except Exception as es:
                messagebox.showerror("Error", f"Error Due to : {str(es)}", parent=self.root)


# ---- main loop ----
root = Tk()
obj = Register(root)
root.mainloop()
