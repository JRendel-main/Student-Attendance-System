import tkinter as tk
import tkinter.ttk as ttk
import sqlite3 as sl
import random
import smtplib
from tkinter import messagebox as mb
import math

def main():
    # hide root window
    root.withdraw()
    def viewProfile():
        # create view profile window
        view_profile = tk.Toplevel(win)
        view_profile.title("View Profile")
        view_profile.geometry("1250x720")
        view_profile.state("zoomed")
        view_profile.resizable(False, False)

        # create view profile frame
        view_profile_frame = tk.Frame(view_profile, bg="white")
        view_profile_frame.place(relx=0.5, rely=0.5, anchor="center")

        # get student details from database and display to treeview
        conn = sl.connect('college.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE student_id = ?", (entry_1.get(),))
        student = c.fetchone()

        # create treeview and add columns to it displaying student details
        tree = ttk.Treeview(view_profile_frame, columns=("Student ID", "First Name", "Last Name", "Course", "Address", "Email", "Password"))
        tree.heading("#0", text="Student ID")
        tree.heading("#1", text="First Name")
        tree.heading("#2", text="Last Name")
        tree.heading("#3", text="Course")
        tree.heading("#4", text="Address")
        tree.heading("#5", text="Email")
        tree.heading("#6", text="Password")
        tree.insert("", "end", text=student[0], values=(student[1], student[2], student[3], student[4], student[5], student[6]))
        tree.pack()
        tree.column("#0", width=100)
        tree.column("#1", width=100)
        tree.column("#2", width=100)
        tree.column("#3", width=100)
        tree.column("#4", width=100)
        tree.column("#5", width=150)
        tree.column("#6", width=100)

        # create back button
        back_button = tk.Button(view_profile_frame, text="Back", command=view_profile.destroy)
        back_button.pack()

    def editProfile():
        def save():
            conn = sl.connect('college.db')
            c = conn.cursor()
            c.execute("UPDATE students SET first_name = ?, last_name = ?, course = ?, address = ?, email = ?, password = ? WHERE student_id = ?", (ent1.get(), ent2.get(), ent3.get(), ent4.get(), ent5.get(), ent6.get(), entry_1.get()))
            conn.commit()
            conn.close()
            mb.showinfo("Success", "Profile Updated Successfully")
            
            tree.delete(*tree.get_children())
            conn = sl.connect('college.db')
            c = conn.cursor()
            c.execute("SELECT * FROM students WHERE student_id = ?", (entry_1.get(),))
            student = c.fetchone()
            tree.insert("", "end", text=student[0], values=(student[1], student[2], student[3], student[4], student[5], student[6]))
            tree.column("#0", width=100)
            tree.column("#1", width=100)
            tree.column("#2", width=100)
            tree.column("#3", width=100)
            tree.column("#4", width=100)
            tree.column("#5", width=150)
            tree.column("#6", width=100)
            conn.close()
            
        # create edit profile window
        edit_profile = tk.Toplevel(win)
        edit_profile.title("Edit Profile")
        edit_profile.geometry("1250x720")
        edit_profile.state("zoomed")

        # create treeview and add columns to it displaying student details from database and edit them
        conn = sl.connect('college.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students WHERE student_id = ?", (entry_1.get(),))
        student = c.fetchone()

        # create edit profile frame
        edit_profile_frame = tk.Frame(edit_profile, bg="white")
        edit_profile_frame.place(relx=0.5, rely=0.5, anchor="center")

        # create treeview and add columns to it displaying student details
        tree = ttk.Treeview(edit_profile_frame, columns=("Student ID", "First Name", "Last Name", "Course", "Address", "Email", "Password"))
        tree.heading("#0", text="Student ID")
        tree.heading("#1", text="First Name")
        tree.heading("#2", text="Last Name")
        tree.heading("#3", text="Course")
        tree.heading("#4", text="Address")
        tree.heading("#5", text="Email")
        tree.heading("#6", text="Password")
        tree.insert("", "end", text=student[0], values=(student[1], student[2], student[3], student[4], student[5], student[6]))
        tree.pack()
        tree.column("#0", width=100)
        tree.column("#1", width=100)
        tree.column("#2", width=100)
        tree.column("#3", width=100)
        tree.column("#4", width=100)
        tree.column("#5", width=150)
        tree.column("#6", width=100)

        # add entry boxes to edit student details
        ent1 = tk.Entry(edit_profile_frame, width=30)
        ent1.insert(0, student[1])
        ent1.pack()
        ent2 = tk.Entry(edit_profile_frame, width=30)
        ent2.insert(0, student[2])
        ent2.pack()
        ent3 = tk.Entry(edit_profile_frame, width=30)
        ent3.insert(0, student[3])
        ent3.pack()
        ent4 = tk.Entry(edit_profile_frame, width=30)
        ent4.insert(0, student[4])
        ent4.pack()
        ent5 = tk.Entry(edit_profile_frame, width=30)
        ent5.insert(0, student[5])
        ent5.pack()
        ent6 = tk.Entry(edit_profile_frame, width=30)
        ent6.insert(0, student[6])
        ent6.pack()
        # create back button
        back_button = tk.Button(edit_profile_frame, text="Back", command=edit_profile.destroy)
        back_button.pack()

        # create save button
        save_button = tk.Button(edit_profile_frame, text="Save", command=save)
        save_button.pack()

    def viewAllStudents():
        # create view all students window
        view_all_students = tk.Toplevel(win)
        view_all_students.title("View All Students")
        view_all_students.geometry("1250x720")
        view_all_students.state("zoomed")
        view_all_students.resizable(False, False)

        # create view all students frame
        view_all_students_frame = tk.Frame(view_all_students, bg="white")
        view_all_students_frame.place(relx=0.5, rely=0.5, anchor="center")

        # get student details from database and display to treeview
        conn = sl.connect('college.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        students = c.fetchall()

        # create treeview and add columns to it displaying student details set width to 100
        
        
        tree = ttk.Treeview(view_all_students_frame, columns=("Student ID", "First Name", "Last Name", "Course", "Address", "Email", "Password"))
        tree.heading("#0", text="Student ID")
        tree.heading("#1", text="First Name")
        tree.heading("#2", text="Last Name")
        tree.heading("#3", text="Course")
        tree.heading("#4", text="Address")
        tree.heading("#5", text="Email")
        tree.heading("#6", text="Password")
        tree.column("#0", width=100)
        tree.column("#1", width=100)
        tree.column("#2", width=100)
        tree.column("#3", width=100)
        tree.column("#4", width=100)
        tree.column("#5", width=150)
        tree.column("#6", width=100)
        for student in students:
            tree.insert("", "end", text=student[0], values=(student[1], student[2], student[3], student[4], student[5], student[6]))
        tree.pack()

        # create back button
        back_button = tk.Button(view_all_students_frame, text="Back", command=view_all_students.destroy)
        back_button.pack()

    def editStudents():
        # create edit students window
        edit_students = tk.Toplevel(win)
        edit_students.title("Edit Students")
        edit_students.geometry("1250x720")
        edit_students.state("zoomed")
        edit_students.resizable(False, False)

        # create edit students frame
        edit_students_frame = tk.Frame(edit_students, bg="white")
        edit_students_frame.place(relx=0.5, rely=0.5, anchor="center")

        # get student details from database and display to treeview and edit them
        conn = sl.connect('college.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        students = c.fetchall()

        # create editable treeview and add columns to it displaying student details
        tree = ttk.Treeview(edit_students_frame, columns=("Student ID", "First Name", "Last Name", "Course", "Address", "Email", "Password"))
        tree.heading("#0", text="Student ID")
        tree.heading("#1", text="First Name")
        tree.heading("#2", text="Last Name")
        tree.heading("#3", text="Course")
        tree.heading("#4", text="Address")
        tree.heading("#5", text="Email")
        tree.heading("#6", text="Password")
        for student in students:
            tree.insert("", "end", text=student[0], values=(student[1], student[2], student[3], student[4], student[5], student[6]))
        tree.pack()

        # highlight selected row and display student details in entry boxes to edit
        def selectItem(a):
            curItem = tree.focus()
            print(tree.item(curItem))
            ent1.delete(0, "end")
            ent1.insert(0, tree.item(curItem)["values"][0])
            ent2.delete(0, "end")
            ent2.insert(0, tree.item(curItem)["values"][1])
            ent3.delete(0, "end")
            ent3.insert(0, tree.item(curItem)["values"][2])
            ent4.delete(0, "end")
            ent4.insert(0, tree.item(curItem)["values"][3])
            ent5.delete(0, "end")
            ent5.insert(0, tree.item(curItem)["values"][4])
            ent6.delete(0, "end")
            ent6.insert(0, tree.item(curItem)["values"][5])
            ent7.delete(0, "end")
            ent7.insert(0, tree.item(curItem)["values"][6])
        tree.bind('<<TreeviewSelect>>', selectItem)

        # create entry boxes to edit student details
        ent1 = tk.Entry(edit_students_frame, width=30)
        ent1.pack()
        ent2 = tk.Entry(edit_students_frame, width=30)
        ent2.pack()
        ent3 = tk.Entry(edit_students_frame, width=30)
        ent3.pack()
        ent4 = tk.Entry(edit_students_frame, width=30)
        ent4.pack()
        ent5 = tk.Entry(edit_students_frame, width=30)
        ent5.pack()
        ent6 = tk.Entry(edit_students_frame, width=30)
        ent6.pack()
        ent7 = tk.Entry(edit_students_frame, width=30)
        ent7.pack()

        # create save button to save edited student details
        def save():
            conn = sl.connect('college.db')
            c = conn.cursor()
            c.execute("UPDATE students SET first_name = ?, last_name = ?, course = ?, address = ?, email = ?, password = ? WHERE student_id = ?", (ent2.get(), ent3.get(), ent4.get(), ent5.get(), ent6.get(), ent7.get(), ent1.get()))
            conn.commit()
            conn.close()
            mb.showinfo("Success", "Student details updated successfully!")
        save_button = tk.Button(edit_students_frame, text="Save", command=save)
        save_button.pack()

        # create back button
        back_button = tk.Button(edit_students_frame, text="Back", command=edit_students.destroy)
        back_button.pack()

    def deleteStudents():
        # create delete students window
        delete_students = tk.Toplevel(win)
        delete_students.title("Delete Students")
        delete_students.geometry("1250x720")
        delete_students.state("zoomed")
        delete_students.resizable(False, False)

        # create delete students frame
        delete_students_frame = tk.Frame(delete_students, bg="white")
        delete_students_frame.place(relx=0.5, rely=0.5, anchor="center")

        # get student details from database and display to treeview and delete them
        conn = sl.connect('college.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        students = c.fetchall()

        # create treeview and add columns to it displaying student details
        tree = ttk.Treeview(delete_students_frame, columns=("Student ID", "First Name", "Last Name", "Course", "Address", "Email", "Password"))
        tree.heading("#0", text="Student ID")
        tree.heading("#1", text="First Name")
        tree.heading("#2", text="Last Name")
        tree.heading("#3", text="Course")
        tree.heading("#4", text="Address")
        tree.heading("#5", text="Email")
        tree.heading("#6", text="Password")
        
        tree.column("#0", width=100)
        tree.column("#1", width=100)
        tree.column("#2", width=100)
        tree.column("#3", width=100)
        tree.column("#4", width=100)
        tree.column("#5", width=150)
        tree.column("#6", width=100)
        for student in students:
            tree.insert("", "end", text=student[0], values=(student[1], student[2], student[3], student[4], student[5], student[6]))
        tree.pack()

        # highlight selected row and delete student details from database
        def selectItem(a):
            curItem = tree.focus()
            print(tree.item(curItem))
            conn = sl.connect('college.db')
            c = conn.cursor()
            c.execute("DELETE FROM students WHERE student_id = ?", (tree.item(curItem)["text"],))
            conn.commit()
            conn.close()
            mb.showinfo("Success", "Student deleted successfully!")
        tree.bind('<<TreeviewSelect>>', selectItem)

        # create back button
        back_button = tk.Button(delete_students_frame, text="Back", command=delete_students.destroy)
        back_button.pack()


    # create main window student portal
    win = tk.Tk()
    win.title("Student Portal")
    win.geometry("500x500")
    win.resizable(False, False)

    # create menubar
    menubar = tk.Menu(win)
    win.config(menu=menubar)
    # create student menu
    student_menu = tk.Menu(menubar, tearoff=0)
    student_menu.add_command(label="View Profile", command=viewProfile)
    student_menu.add_command(label="Edit Profile", command=editProfile)
    student_menu.add_command(label="Logout", command=win.destroy)
    menubar.add_cascade(label="Student", menu=student_menu)

    # create course menu
    course_menu = tk.Menu(menubar, tearoff=0)
    course_menu.add_command(label="View All Students", command=viewAllStudents)
    course_menu.add_command(label="Edit Students", command=editStudents)
    course_menu.add_command(label="Delete Students", command=deleteStudents)
    menubar.add_cascade(label="Other Students", menu=course_menu)

    # create label welcome message and display student name
    conn = sl.connect('college.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE student_id = ?", (entry_1.get(),))
    student = c.fetchone()
    welcome_label = tk.Label(win, text="Welcome " + student[1] + " " + student[2])
    welcome_label.configure(font=("Arial", 20))
    welcome_label.pack()
    win.mainloop()


def enrollmentform():
    def addStudent():
        mb.showinfo("OTP Verification", "OTP has been sent to your registered email address.")
        digits = "0123456789"
        OTP = ""
        for i in range(6):
            OTP += digits[math.floor(random.random() * 10)]
        print(OTP)
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("hirotoshitest@gmail.com", "nhqdiwtariodmlxy")
        message = """
            
            Hello Mr/Ms. {} Here is your Student No.

            Hello Student your Student Number is {}
            and your Password is "pass" change it on edit profile menu

            """.format(entry_4.get(), OTP)

        s.sendmail("hirotoshitest@gmail.com", entry_6.get(), message)
        s.quit()
        mb.showinfo("OTP Verification", "OTP has been sent to your registered email address.")
        # create table students and insert into database
        conn = sl.connect('college.db')
        c = conn.cursor()
        c.execute(
            "CREATE TABLE IF NOT EXISTS students (student_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, course TEXT, address TEXT, email TEXT, password TEXT)")
        c.execute(
            "INSERT INTO students VALUES (:student_id, :first_name, :last_name, :course, :address, :email, :password)",
            {
                'student_id': int(OTP),
                'first_name': entry_3.get(),
                'last_name': entry_4.get(),
                'course': combobox_1.get(),
                'address': entry_5.get(),
                'email': entry_6.get(),
                'password': 'pass'
            })
        conn.commit()
        conn.close()
        mb.showinfo("Success", "Student Added")
        toplevel, toplevel_2.destroy()

    def cancel():
        toplevel_2.withdraw()

    toplevel_2 = tk.Toplevel()
    toplevel_2.geometry("640x480")
    frame_2 = ttk.Frame(toplevel_2)
    frame_2.configure(height=200, width=200)
    lbl3 = ttk.Label(frame_2)
    lbl3.configure(
        font="{Arial Rounded MT Bold} 20 {bold}",
        text='Enrollment Form')
    lbl3.place(anchor="center", relx=0.5, rely=0.5, x=0, y=0)
    frame_2.place(
        anchor="center",
        relheight=0.1,
        relwidth=1.0,
        relx=0.5,
        rely=0.05,
        x=0,
        y=0)
    frame_3 = ttk.Frame(toplevel_2)
    frame_3.configure(height=200, width=200)
    label_4 = ttk.Label(frame_3)
    label_4.configure(font="{Britannic Bold} 12 {}", text='First Name')
    label_4.place(anchor="n", relx=0.5, rely=0.05, x=0, y=0)
    entry_3 = ttk.Entry(frame_3)
    entry_3.place(anchor="n", relx=0.5, rely=0.13, x=0, y=0)
    label_5 = ttk.Label(frame_3)
    label_5.configure(font="{Britannic Bold} 12 {}", text='Last Name')
    label_5.place(anchor="n", relx=0.5, rely=0.21, x=0, y=0)
    entry_4 = ttk.Entry(frame_3)
    entry_4.place(anchor="n", relx=0.5, rely=0.28, x=0, y=0)

    combobox_1 = ttk.Combobox(frame_3)
    combobox_1['values'] = ('BSIT', 'BSBA', 'BSMA', 'BIT')
    combobox_1.configure(state="normal")
    combobox_1.place(anchor="nw", relx=0.29, rely=0.45, x=0, y=0)
    label_6 = ttk.Label(frame_3)
    label_6.configure(font="{Britannic Bold} 12 {}", text='Course')
    label_6.place(anchor="n", relx=0.5, rely=0.37, x=0, y=0)
    label_7 = ttk.Label(frame_3)
    label_7.configure(font="{Britannic Bold} 12 {}", text='Address')
    label_7.place(anchor="n", relx=0.5, rely=0.53, x=0, y=0)
    entry_5 = ttk.Entry(frame_3)
    entry_5.place(anchor="n", relx=0.5, rely=0.6, x=0, y=0)
    label_8 = ttk.Label(frame_3)
    label_8.configure(font="{Britannic Bold} 12 {}", text='Email')
    label_8.place(anchor="n", relx=0.5, rely=0.67, x=0, y=0)
    entry_6 = ttk.Entry(frame_3)
    entry_6.place(anchor="n", relx=0.5, rely=0.73, x=0, y=0)
    button_1 = tk.Button(frame_3, command=addStudent)
    button_1.configure(background="#52ef66", text='Send OTP')
    button_1.place(anchor="n", relx=0.2, rely=0.85, x=0, y=0)
    button_2 = tk.Button(frame_3, command=cancel)
    button_2.configure(background="#fa474b", text='Cancel')
    button_2.place(anchor="n", relx=0.8, rely=0.85, x=0, y=0)
    frame_3.place(
        anchor="center",
        relheight=0.7,
        relwidth=0.5,
        relx=0.5,
        rely=0.5,
        x=0,
        y=0)
    toplevel_2.mainloop()


def login():
    conn = sl.connect('college.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE student_id = ? AND password = ?", (entry_1.get(), entry_2.get()))
    if c.fetchone() is not None:
        print("Login Successful")
        mb.showinfo("Login", "Login Successful")
        main()
    else:
        print("Login Failed")
        mb.showerror("Error", "Invalid Student ID or Password")


root = tk.Tk()
# hide root
root.withdraw()
# remove root window
toplevel = tk.Toplevel(root)
toplevel.geometry("1024x576")
toplevel.configure(background='gray')
label_1 = ttk.Label(toplevel)
label_1.configure(
    font="{Arial Rounded MT Bold} 24 {}",
    relief="flat",
    text='College Enrollment System\n')
label_1.place(
    anchor="center",
    bordermode="outside",
    relheight=0.081,
    relx=0.5,
    rely=0.13,
    x=0,
    y=0)
frame_1 = ttk.Frame(toplevel)
frame_1.configure(height=200, width=200)
label_2 = ttk.Label(frame_1)
label_2.configure(
    font="{Arial Rounded MT Bold} 24 {}",
    relief="flat",
    text='Login')
label_2.place(anchor="center", relx=0.5, rely=0.14, x=0, y=0)
entry_1 = ttk.Entry(frame_1)
entry_1.place(anchor="center", relx=0.6, rely=0.42, x=0, y=0)
entry_2 = ttk.Entry(frame_1, show='*')
entry_2.place(anchor="center", relx=0.6, rely=0.64, x=0, y=0)
label_3 = ttk.Label(frame_1)
label_3.configure(font="{@Malgun Gothic} 16 {}", text='Student No: ')
label_3.place(anchor="nw", relx=0.1, rely=0.35, x=0, y=0)
label_4 = ttk.Label(frame_1)
label_4.configure(font="{@Malgun Gothic} 16 {}", text='Password: ')
label_4.place(anchor="nw", relx=0.1, rely=0.57, x=0, y=0)
button_1 = ttk.Button(frame_1)
button_1.configure(text='Login', command=login)
button_1.place(anchor="center", relx=0.5, rely=0.79, x=0, y=0)
label_5 = ttk.Label(frame_1)
label_5.configure(
    font="{Arial} 7 {}",
    justify="center",
    takefocus=True,
    text='New enrollee? Click here to enroll')
label_5.place(anchor="center", relx=.5, rely=0.91, x=0, y=0)
frame_1.place(
    anchor="nw",
    relheight=0.47,
    relwidth=0.39,
    relx=0.3,
    rely=0.31,
    x=0,
    y=0)
# run function when label_5 is clicked
label_5.bind("<Button-1>", lambda event: enrollmentform())
root.mainloop()
