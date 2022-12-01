# im going to create time-based attendance system using qrcode scanner
# import libraries
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import pyqrcode
from pyqrcode import QRCode
import png
import os
import datetime
import time
import cv2 as cv
import random
import smtplib

def random_id():
    # connect to database
    conn = sqlite3.connect("StudentAttendanceSystem.db")

    # create cursor
    c = conn.cursor()

    # create table tblstudent
    c.execute("""CREATE TABLE IF NOT EXISTS tblstudent (
                student_id integer PRIMARY KEY,
                student_fname text,
                student_lname text,
                student_course text,
                student_year text,
                student_section text,
                student_email text,
                student_contact text
            )""")

    global studentran
    studentran = random.randint(10000000, 99999999)
    print(studentran)
    # add student info from form
    c.execute("INSERT INTO tblstudent VALUES (:student_id, :student_fname, :student_lname, :student_course, :student_year, :student_section, :student_email, :student_contact)", {
        'student_id': studentran,
        'student_fname': last_name_entry.get(),
        'student_lname': first_name_entry.get(),
        'student_course': course_combobox.get(),
        'student_year': year_combobox.get(),
        'student_section': section_combobox.get(),
        'student_email': email_entry.get(),
        'student_contact': contact_number_entry.get()
    })

    # commit changes
    conn.commit()

    # clear the text boxes
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    course_combobox.delete(0, END)
    year_combobox.delete(0, END)
    section_combobox.delete(0, END)
    email_entry.delete(0, END),
    contact_number_entry.delete(0, END)

    # display message
    messagebox.showinfo("Student Attendance System", "Student ID: " + str(studentran) + " added successfully!")
    sendStuNoEmail()

def sendStuNoEmail():
    # get the student_email and Student_ID from database
    conn = sqlite3.connect("StudentAttendanceSystem.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tblstudent WHERE student_id = {}".format(studentran))
    for record in c.fetchall():
        student_last_name = record[1]
        student_email = record[6]
        student_id = record[0]

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("hirotoshitest@gmail.com", "nhqdiwtariodmlxy")
    message = """

                Hello Mr/Ms. {} Here is your Student No.

                Hello Student your Student Number is {}
                Have a Great Day!

                """.format(student_last_name, str(student_id))

    s.sendmail("hirotoshitest@gmail.com", student_email, message)
    s.quit()
    messagebox.showinfo("Student Attendance System", "Student ID: " + str(student_id) + " sent to " + student_email)


# get student info on search bar and display on entry boxes
def searchstudent():
    # connect to database
    conn = sqlite3.connect("StudentAttendanceSystem.db")

    # create cursor
    c = conn.cursor()

    # create table tblstudent
    c.execute("""CREATE TABLE IF NOT EXISTS tblstudent (
                student_id integer PRIMARY KEY,
                student_fname text,
                student_lname text,
                student_course text,
                student_year text,
                student_section text,
                student_email text,
                student_contact text
            )""")

    # search student
    c.execute("SELECT * FROM tblstudent WHERE student_id = " + search_bar.get())

    # commit changes
    conn.commit()

    # clear the text boxes
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    course_combobox.delete(0, END)
    year_combobox.delete(0, END)
    section_combobox.delete(0, END)
    email_entry.delete(0, END),
    contact_number_entry.delete(0, END)

    # display student info to entry boxes
    for record in c.fetchall():
        first_name_entry.insert(0, record[1])
        last_name_entry.insert(0, record[2])
        course_combobox.insert(0, record[3])
        year_combobox.insert(0, record[4])
        section_combobox.insert(0, record[5])
        email_entry.insert(0, record[6])
        contact_number_entry.insert(0, record[7])


def deletestudent():
    # connect to database
    conn = sqlite3.connect("StudentAttendanceSystem.db")

    # create cursor
    c = conn.cursor()

    # create table tblstudent
    c.execute("""CREATE TABLE IF NOT EXISTS tblstudent (
                student_id integer PRIMARY KEY,
                student_fname text,
                student_lname text,
                student_course text,
                student_year text,
                student_section text,
                student_email text,
                student_contact text
            )""")

    # delete student
    c.execute("DELETE from tblstudent WHERE student_id = " + search_bar.get())

    # commit changes
    conn.commit()

    # close connection
    conn.close()

    # clear the text boxes
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    course_combobox.delete(0, END)
    year_combobox.delete(0, END)
    section_combobox.delete(0, END)
    email_entry.delete(0, END),
    contact_number_entry.delete(0, END)

    # display message
    messagebox.showinfo("Student Attendance System", "Student deleted successfully!")

# update student info
def updatestudent():
    # connect to database
    conn = sqlite3.connect("StudentAttendanceSystem.db")

    # create cursor
    c = conn.cursor()

    # create table tblstudent
    c.execute("""CREATE TABLE IF NOT EXISTS tblstudent (
                student_id integer PRIMARY KEY,
                student_fname text,
                student_lname text,
                student_course text,
                student_year text,
                student_section text,
                student_email text,
                student_contact text
            )""")

    # update student
    c.execute("""UPDATE tblstudent SET
                student_fname = :student_fname,
                student_lname = :student_lname,
                student_course = :student_course,
                student_year = :student_year,
                student_section = :student_section,
                student_email = :student_email,
                student_contact = :student_contact
                WHERE student_id = :student_id""",
                {
                    'student_fname': first_name_entry.get(),
                    'student_lname': last_name_entry.get(),
                    'student_course': course_combobox.get(),
                    'student_year': year_combobox.get(),
                    'student_section': section_combobox.get(),
                    'student_email': email_entry.get(),
                    'student_contact': contact_number_entry.get(),
                    'student_id': search_bar.get()
                })

    # commit changes
    conn.commit()

    # close connection
    conn.close()

    # clear the text boxes
    first_name_entry.delete(0, END)
    last_name_entry.delete(0, END)
    course_combobox.delete(0, END)
    year_combobox.delete(0, END)
    section_combobox.delete(0, END)
    email_entry.delete(0, END),
    contact_number_entry.delete(0, END)

    # display message
    messagebox.showinfo("Student Attendance System", "Student updated successfully!")


def searchqr():
    # create search bar
    search_bar = Entry(qrcode_frame, width=30, font=("Arial", 12))
    search_bar.place(x=10, y=10)

    # create search button
    search_button = Button(qrcode_frame, text="Search", width=30, font=("Arial", 12))
    search_button.place(x=10, y=60)
    
    # create canvas for qr
    canvas = Canvas(qrcode_frame, width=300, height=300)
    canvas.place(x=10, y=110)

    # create qr code
    qr = pyqrcode.create(search_bar.get())

    # create image qr.png
    qr.png("qr.png", scale=8)

    # open image qr.png
    qr_image = PhotoImage(file="qr.png")

    # display image qr.png
    canvas.create_image(0, 0, anchor=NW, image=qr_image)

    # delete image qr.png
    os.remove("qr.png")

def viewStudentLIst():
    # connect to database
    conn = sqlite3.connect("StudentAttendanceSystem.db")

    # create cursor
    c = conn.cursor()

    # create table tblstudent
    c.execute("""CREATE TABLE IF NOT EXISTS tblstudent (
                student_id integer PRIMARY KEY,
                student_fname text,
                student_lname text,
                student_course text,
                student_year text,
                student_section text,
                student_email text,
                student_contact text
            )""")

    # view student list
    c.execute("SELECT *, oid FROM tblstudent")
    records = c.fetchall()
    # create new window and add treeview
    view_student_list_window = Toplevel()
    view_student_list_window.title("Student List")
    view_student_list_window.geometry("800x600")
    view_student_list_window.resizable(False, False)
    view_student_list_window.state("zoomed")
    # set treeview width and height
    treeview = ttk.Treeview(view_student_list_window, height=50)
    treeview.pack(side=LEFT, fill=BOTH, expand=True)
    # create scrollbar
    scrollbar = ttk.Scrollbar(view_student_list_window, orient=VERTICAL, command=treeview.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    # configure treeview
    treeview.configure(yscrollcommand=scrollbar.set)
    tree = ttk.Treeview(view_student_list_window)
    tree["columns"] = ("one", "two", "three", "four", "five", "six", "seven", "eight")
    tree.column("one", width=100)
    tree.column("two", width=100)
    tree.column("three", width=100)
    tree.column("four", width=100)
    tree.column("five", width=100)
    tree.column("six", width=100)
    tree.column("seven", width=120)
    tree.column("eight", width=120)
    tree.heading("one", text="Student ID")
    tree.heading("two", text="First Name")
    tree.heading("three", text="Last Name")
    tree.heading("four", text="Course")
    tree.heading("five", text="Year")
    tree.heading("six", text="Section")
    tree.heading("seven", text="Email")
    tree.heading("eight", text="Contact Number")
    tree.pack(side=LEFT, fill=BOTH, expand=1)
    for record in records:
        tree.insert("", 0, values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7]))

    # commit changes
    # center items in treeview
    for col in tree["columns"]:
        tree.column(col, anchor=CENTER)
    # close connection


    # CENTER TREEVIEW to window
    tree.place(x=10, y=10)

    # add back button
    back_button = Button(view_student_list_window, text="Back", width=30, font=("Arial", 12), command=view_student_list_window.destroy)
    back_button.place(x=10, y=550)


    # commit changes
    conn.commit()

    # close connection
    conn.close()

def qrcodegen():
    # generate qr code based on student id on search bar
    # create qrcode
    qr = pyqrcode.create(search_bar.get())

    # create image qr.png
    qr.png("Student {}.png".format(search_bar.get()), scale=8)

    # open image qr.png
    qr_image = PhotoImage(file="Student {}.png".format(search_bar.get()))

    # display image to qr code frame
    canvas.create_image(0, 0, anchor=NW, image=qr_image)


# create main ui
root = Tk()
root.title("Student Attendance System")
# set size to monitor size
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

# create menu
menu = Menu(root)
root.config(menu=menu)
submenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Students", menu=submenu)
submenu.add_command(label="View Student Attendance")
submenu.add_command(label="View Student List", command=viewStudentLIst)
submenu.add_command(label="Exit", command=root.destroy)

submenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="About", command=root.destroy)

# create frame for student details place to left
student_details_frame = LabelFrame(root, text="Student Details")
student_details_frame.place(x=0, y=0, height=height, width=width / 3)

# create frame for button for and place in middle
button_frame = LabelFrame(root, text="Actions")
button_frame.place(x=width / 3, y=0, height=height, width=width / 3)

# create frame for qrcode place to right
qrcode_frame = LabelFrame(root, text="QRCode")
qrcode_frame.place(x=(width / 3) * 2, y=0, height=height, width=width / 3)


# create entry form and label for last name, firstname, combobox section, year, course with design

# create label for last name
last_name_label = Label(student_details_frame, text="Last Name", font=("Arial", 12))
last_name_label.place(x=10, y=10)

# create entry for last name
last_name_entry = Entry(student_details_frame, width=30, font=("Arial", 12))
last_name_entry.place(x=10, y=40)

# create label for first name
first_name_label = Label(student_details_frame, text="First Name", font=("Arial", 12))
first_name_label.place(x=10, y=70)

# create entry for first name
first_name_entry = Entry(student_details_frame, width=30, font=("Arial", 12))
first_name_entry.place(x=10, y=100)

# create label for section
section_label = Label(student_details_frame, text="Section", font=("Arial", 12))
section_label.place(x=10, y=130)

# create combobox for section
section_combobox = ttk.Combobox(student_details_frame, width=27, font=("Arial", 12))
section_combobox["values"] = ("A", "B", "C", "D")
section_combobox.place(x=10, y=160)

# create label for year
year_label = Label(student_details_frame, text="Year", font=("Arial", 12))
year_label.place(x=10, y=190)

# create combobox for year
year_combobox = ttk.Combobox(student_details_frame, width=27, font=("Arial", 12))
year_combobox["values"] = ("1", "2", "3", "4")
year_combobox.place(x=10, y=220)

# create label for course
course_label = Label(student_details_frame, text="Course", font=("Arial", 12))
course_label.place(x=10, y=250)

# create combobox for course
course_combobox = ttk.Combobox(student_details_frame, width=27, font=("Arial", 12))
course_combobox["values"] = ("BSIT", "BSCS", "BSIS", "BSA", "BSCrim")
course_combobox.place(x=10, y=280)

# create entry for email
email_label = Label(student_details_frame, text="Email", font=("Arial", 12))
email_label.place(x=10, y=310)

# create entry for email
email_entry = Entry(student_details_frame, width=30, font=("Arial", 12))
email_entry.place(x=10, y=340)

# create entry for contact number
contact_number_label = Label(student_details_frame, text="Contact Number", font=("Arial", 12))
contact_number_label.place(x=10, y=370)

# create entry for contact number
contact_number_entry = Entry(student_details_frame, width=30, font=("Arial", 12))
contact_number_entry.place(x=10, y=400)

# create buttons add, update, delete generate qr for student

add_button = Button(button_frame, text="Add", width=30, font=("Arial", 12), command=random_id)
add_button.place(x=10, y=10)

# create button update
update_button = Button(button_frame, text="Update", width=30, font=("Arial", 12), command=updatestudent)
update_button.place(x=10, y=60)

# create button delete
delete_button = Button(button_frame, text="Delete", width=30, font=("Arial", 12), command=deletestudent)
delete_button.place(x=10, y=110)

# create button generate qr
generate_qr_button = Button(button_frame, text="Generate QR", width=30, font=("Arial", 12), command=qrcodegen)
generate_qr_button.place(x=10, y=160)

# create search bar and button for qr and place on top
# create search bar
search_bar = Entry(qrcode_frame, width=30, font=("Arial", 12))
search_bar.place(x=10, y=10)

# create search button
search_button = Button(qrcode_frame, text="Search", width=30, font=("Arial", 12), command=searchstudent)
search_button.place(x=10, y=60)

root.mainloop()
