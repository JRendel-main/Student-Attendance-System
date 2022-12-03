from tkinter import *
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from PIL import ImageTk, Image
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import sqlite3
import pyqrcode
from pyqrcode import QRCode
import pyqrcode
import png
import os
import datetime
import time
import random
import smtplib
import shutil
import cv2

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
        'student_contact': contact_number_entry.get(),
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
    c.execute("SELECT * FROM tblstudent WHERE student_id = {}".format(int(studentran)))
    for record in c.fetchall():
        student_last_name = record[1]
        student_email = record[6]
        student_id = record[0]

    c.execute("SELECT * FROM tblstudent WHERE student_id = " + str(studentran))

    # commit changes
    conn.commit()

    # display student info to entry boxes
    for record in c.fetchall():
        student_last_name = record[2]
        student_first_name = record[1]
        student_id = record[0]
        student_year = record[4]
        student_section = record[5]

    # create folder based on student year and section
    if not os.path.exists("StudentQRCode"):
        os.mkdir("StudentQRCode")
    if not os.path.exists("StudentQRCode/" + student_year):
        os.mkdir("StudentQRCode/" + student_year)
    if not os.path.exists("StudentQRCode/" + student_year + "/" + student_section):
        os.mkdir("StudentQRCode/" + student_year + "/" + student_section)

    # check if qr code is already generated for student id if not generate qr code else display error message
    if not os.path.exists("StudentQRCode/" + student_year + "/" + student_section + "/" + student_last_name + ".png"):
        qr = pyqrcode.create(student_id)
        qr.png("StudentQRCode/" + student_year + "/" + student_section + "/" + "Student " + student_last_name + ".png",
               scale=8)
        messagebox.showinfo("Student Attendance System", "QR Code generated successfully!")
    else:
        messagebox.showerror("Student Attendance System", "QR Code already generated!")

    # send student id and qr code to student email
    email = student_email
    send_to_email = student_email
    subject = 'Student ID'
    message = 'Your Student ID is: {}'.format(student_id)
    file_location = "StudentQRCode/" + student_year + "/" + student_section + "/" + "Student " + student_last_name + ".png"
    file_name = "Student " + student_last_name + ".png"

    # create a multipart message and set headers
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # open the file to be sent
    attachment = open(file_location, 'rb')

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % file_name)

    # attach the instance 'p' to instance 'msg'
    msg.attach(p)

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("hirotoshitest@gmail.com", "nhqdiwtariodmlxy")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(email, send_to_email, text)

    # terminating the session
    s.quit()


    # display message
    messagebox.showinfo("Student Attendance System", "Student ID: " + str(student_id) + " sent to " + student_email + " successfully!")


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
    moveQRCode()
    conn.commit()
    # close connectio
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

# generate qr code for student id and save to folder named based on student year and section
def generateqrcode():
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

    # display student info to entry boxes
    for record in c.fetchall():
        student_id = record[0]
        student_fname = record[1]
        student_lname = record[2]
        student_course = record[3]
        student_year = record[4]
        student_section = record[5]
        student_email = record[6]
        student_contact = record[7]

    # display image of qr code from folder based on student year and section display on qrcode_frame on center using place
    qrcode_image = ImageTk.PhotoImage(Image.open("StudentQRCode/" + student_year + "/" + student_section + "/" + "Student "+ student_lname + ".png"))
    qrcode_label = Label(qrcode_frame, image=qrcode_image)
    qrcode_label.image = qrcode_image
    qrcode_label.place(relx=0.5, rely=0.5, anchor=CENTER)
    def removeqrcode():
        # remove qr code label
        qrcode_label.destroy()

    # create button that removes qr code from qrcode frame
    remove_qrcode_button = Button(qrcode_frame, text="Remove QR Code", command=removeqrcode)
    remove_qrcode_button.place(relx=0.5, rely=0.9, anchor=CENTER)

    # close connection
    conn.close()

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

def moveQRCode():
    # get student id, year, section
    student_id = search_bar.get()
    # connect to database
    conn = sqlite3.connect("StudentAttendanceSystem.db")

    # create cursor
    c = conn.cursor()

    # fetch student info
    c.execute("SELECT * FROM tblstudent WHERE student_id = " + student_id)
    records = c.fetchall()

    # get student year and section
    for record in records:
        student_lname = record[2]
        student_year = record[4]
        student_section = record[5]
    # create folder based on student year and section if not exist
    if not os.path.exists("StudentQRCode/" + year_combobox.get() + "/" + section_combobox.get()):
        os.makedirs("StudentQRCode/" + year_combobox.get() + "/" + section_combobox.get())
    # move qr code from studentqrcode folder to studentqrcode based on student year and section
    shutil.move("StudentQRCode/" + student_year + "/" + student_section + "/" + "Student " + student_lname + ".png", "StudentQRCode/" + year_combobox.get() + "/" + section_combobox.get() + "/" + "Student " + student_lname + ".png")
    print("QR Code Moved")

# create main ui
root = Tk()
root.title("Student Attendance System")
# set size to monitor size
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry("%dx%d" % (width, height))

def scanqr():
    def scanAttendanceWebcam():
        # create camera
        camera = cv2.VideoCapture(2)
        # create qr code detector
        detector = cv2.QRCodeDetector()
        # scan qr code from webcam and get student id and insert date and time to database based on student id
        while True:
            _, img = camera.read()
            data, bbox, _ = detector.detectAndDecode(img)
            if bbox is not None:
                if data:
                    # connect to database
                    conn = sqlite3.connect("StudentAttendanceSystem.db")
                    # create cursor
                    c = conn.cursor()
                    # check if student id already scanned today
                    # display current date and time
                    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
                    current_time = datetime.datetime.now().strftime("%H:%M:%S")
                    # insert date and time to database

                    c.execute("SELECT * FROM tblattendance WHERE student_id = " + data + " AND date = '" + current_date + "'")
                    records = c.fetchall()
                    if len(records) == 0:
                        # insert student id and date and time to database
                        c.execute("INSERT INTO tblattendance VALUES (:student_id, :date, :time)",
                                  {
                                      'student_id': data,
                                      'date': current_date,
                                      'time': current_time
                                  })
                        # commit changes
                        conn.commit()
                        # close connection
                        conn.close()
            cv2.imshow("code detector", img)
            if cv2.waitKey(1) == ord("q"):
                break
        camera.release()
        cv2.destroyAllWindows()
    conn = sqlite3.connect("StudentAttendanceSystem.db")
    # create cursor
    c = conn.cursor()

    # create table tblattendance
    c.execute("""CREATE TABLE IF NOT EXISTS tblattendance (
                student_id integer PRIMARY KEY,
                date text,
                time text,
                FOREIGN KEY (student_id) REFERENCES tblstudent(student_id)
            )""")
    # commit changes
    conn.commit()
    def insertable():
        # connect to database
        conn = sqlite3.connect("StudentAttendanceSystem.db")
        # create cursor
        c = conn.cursor()
        # clear treeview
        tree.delete(*tree.get_children())

        # fetch student last first name, last name from tblstudent and date and time from tblattendance
        c.execute("SELECT tblstudent.student_id, tblstudent.student_fname, tblstudent.student_lname, tblattendance.date, tblattendance.time FROM tblstudent INNER JOIN tblattendance ON tblstudent.student_id = tblattendance.student_id")
        records = c.fetchall()

        # insert student last first name, last name from tblstudent and compare date to date.entry and check if present or absent and time to treeview


        for record in records:
            date_entry1 = ''.join(letter for letter in str(date_entry.get()) if letter.isalnum())
            date_record = ''.join(letter for letter in str(record[3]) if letter.isalnum())
            if date_entry1 == date_record:
                tree.insert("", 0, values=(record[0], record[1], record[2], "Present", record[4]))
            else:
                tree.insert("", 0, values=(record[0], record[1], record[2], "Absent", "Not Applicable"))
            print("Date Entry: " + date_entry1)
            print("Date Record: " + date_record)
        # commit changes
        conn.commit()
        # close connection
        conn.close()
    # create new window for qr code scanner treeview, combobox, and search bar, and button
    scan_qr_window = Toplevel()
    scan_qr_window.title("Scan QR Code")
    scan_qr_window.geometry("800x600")
    scan_qr_window.resizable(False, False)
    scan_qr_window.state("zoomed")
    # create treeview
    treeview = ttk.Treeview(scan_qr_window, height=50)
    treeview.pack(side=LEFT, fill=BOTH, expand=True)
    # create scrollbar
    scrollbar = ttk.Scrollbar(scan_qr_window, orient=VERTICAL, command=treeview.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    # configure treeview
    treeview.configure(yscrollcommand=scrollbar.set)
    tree = ttk.Treeview(scan_qr_window)
    # add student id, firstname, lastname, attendance status, and date to treeview
    tree["columns"] = ("studentid", "fname", "lname", "status", "timein")
    tree.column("studentid", width=100)
    tree.column("fname", width=100)
    tree.column("lname", width=100)
    tree.column("status", width=100)
    tree.column("timein", width=100)
    tree.heading("studentid", text="Student ID")
    tree.heading("fname", text="First Name")
    tree.heading("lname", text="Last Name")
    tree.heading("status", text="Attendance Status")
    tree.heading("timein", text="Time In")
    tree.pack(side=LEFT, fill=BOTH, expand=1)
    # use tkcalendar to get date
    # create date label
    date_label = Label(scan_qr_window, text="Date: ", font=("Arial", 12))
    date_label.place(x=10, y=10)
    # create date entry
    date_entry = DateEntry(scan_qr_window, width=12, background="darkblue", foreground="white", borderwidth=2, font=("Arial", 12), date_pattern="yyyy-mm-dd")
    date_entry.place(x=60, y=10)
    # create display attendance button
    display_attendance_button = Button(scan_qr_window, text="Display Attendance", command=insertable, font=("Arial", 12))
    display_attendance_button.place(x=10, y=40)
    # create button for scan attendance using webcam
    scan_attendance_webcam_button = Button(scan_qr_window, text="Scan Attendance Using Webcam", command=scanAttendanceWebcam)
    scan_attendance_webcam_button.place(x=10, y=100)
    # create label for Last Scanned Attendance
    last_scanned_attendance_label = Label(scan_qr_window, text="Last Scanned Attendance", font=("Arial", 12))
    last_scanned_attendance_label.place(x=10, y=150)

# create menu
menu = Menu(root)
root.config(menu=menu)
submenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Students", menu=submenu)
submenu.add_command(label="View Student Attendance", command=scanqr)
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
generate_qr_button = Button(button_frame, text="Generate QR", width=30, font=("Arial", 12), command=generateqrcode)
generate_qr_button.place(x=10, y=160)

# create search bar and button for qr and place on top
# create search bar
search_bar = Entry(qrcode_frame, width=30, font=("Arial", 12))
search_bar.place(x=10, y=10)

# create search button
search_button = Button(qrcode_frame, text="Search", width=30, font=("Arial", 12), command=searchstudent)
search_button.place(x=10, y=60)

root.mainloop()
