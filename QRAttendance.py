# im going to create qr scanner for attendance using sqlite3 as database

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import ttk
import sqlite3
import datetime
import pyqrcode
import png
from pyqrcode import QRCode
import cv2
import numpy as np
import os
import sys
import time
import qrcode

# create table on database student id first name, last name, time out,time in
conn = sqlite3.connect('StudentAttendanceSystem.db')
c = conn.cursor()
c.execute("""CREATE TABLE if not exists student (
            student_id text,
            first_name text,
            last_name text,
            time_in text,
            time_out text
            )""")
conn.commit()
conn.close()

