import sqlite3
def create_db():
    con=sqlite3.connect(database="rms.db")
    cur=con.cursor()
    cur.execute("Create Table If Not Exists course(id INTEGER PRIMARY KEY AUTOINCREMENT,name text,duration text,charges text,description text)")
    con.commit()

    cur.execute("Create Table If Not Exists student(roll INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,dob text,contact text,admission text,course text,state text,city text,pin text,address text)")
    con.commit()

    cur.execute("Create Table If Not Exists result(rid INTEGER PRIMARY KEY AUTOINCREMENT,roll text,name text,course text,duration text,charges text,marks_ob text,full_marks text,per text)")
    con.commit()

    cur.execute("Create Table If Not Exists employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,f_name text,l_name text,contact text,email text,question text,answer text,password text)")
    con.commit()

    con.close()

    
   
create_db()