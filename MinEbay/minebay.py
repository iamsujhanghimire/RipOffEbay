# CSCI 120 - Final Project
# MinEbay
# Members: Sujhan Ghimire - Naveed Bin Sattar - Hanvit Choi - Misha Rashid Nasir

import tkinter as t
from PIL import ImageTk, Image
from tkinter import filedialog
import sqlite3 as s
import os


class minebay:
    def __init__(self):
        self.main = t.Tk()
        
         
    def addimage(self):
        img = ImageTk.PhotoImage(Image.open("resized.png"))
        panel = t.Label(image = img)
        panel.image = img
        panel.grid(row = 2, column = 0,columnspan = 3, rowspan = 3, padx = 5, pady = 5)
                
  
    def buttons(self):
        
        up = t.Button(self.main, text = "Upload", padx = 200, pady = 10, command = self.upwindow)
        see = t.Button(self.main, text = "Search", padx = 200, pady = 10, command = self.sewindow)
        exitwindow = t.Button(self.main, text = "Exit Program", command = self.main.destroy)
        
        up.grid(row = 0, column = 0)
        see.grid(row = 0, column = 1)
        exitwindow.grid(row = 6, column = 0, columnspan = 2, sticky = "S")        
        
    
    def showindow(self):
        self.main.title("MinEbay")
        self.main.geometry("900x400")
        self.buttons()
        self.addimage()
        self.main.mainloop()
    
        
    def upwindow(self):
        global nu
        ''' global nget
        global dget
        global pget
        ''' 
        global name
        global price
        global desc
        global cat
        
        
        nu = t.Toplevel()
        nu.title("Upload a File")
        nu.geometry("900x400")
        
        db = s.connect("items.db")
        cur = db.cursor()
         
        cur.execute(""" CREATE TABLE IF NOT EXISTS items (
                item_image blob,
                item_name text,
                itemprice integer,
                itemcateg text,
                itemdescription text
                )""")
        
        
        openbut = t.Button(nu, text = "Open a file", command = self.openfile)
        openbut.grid(row = 1, column = 1, padx = 2 ,pady = 1)
        
        #for name
        nlabel = t.Label(nu, text = "Enter the name of your listing: ")
        nlabel.grid(row = 2, column = 0, sticky = "E")
        name = t.Entry(nu)
        name.insert(0, "Name")
        name.grid(row = 2, column = 1, sticky = "W")        
        #nget = name.get() #retreive info
        
        #for price
        plabel = t.Label(nu, text = "Enter the price: $")
        plabel.grid(row = 3, column = 0, sticky = "E")
        price = t.Entry(nu, width = 4)
        price.insert(0, "0")
        price.grid(row = 3, column = 1, sticky = "W")        
        #pget = price.get() #retreive info
        
        #for description
        desc = t.Entry(nu)
        dlabel = t.Label(nu, text = "Enter a description: ")
        dlabel.grid(row = 5, column = 0, sticky = "E")
        desc.grid(row = 5, column = 1, sticky = "W")        
        desc.insert(0, "Enter a Description")
        
        #for category
        cavar = t.StringVar(nu)
        choices = {"--Choose a category--","Electronics", "Food Items", "Decor", "Computer & Accessories", "Stationary"}
        choices = sorted(choices)
        cavar.set('--Choose a category--')
        cat = t.OptionMenu(nu,cavar, *choices, command = self.setval)
        cat.grid(row = 4, column = 1, sticky = "W")
        clabel = t.Label(nu, text = "Category: ")
        clabel.grid(row = 4, column = 0, sticky = "E")
        #exit button
        ebut = t.Button(nu, text = "Back to Main Window", command = nu.destroy)        
        ebut.grid(row = 15, column = 0)
        
        #upload button
        upbut = t.Button(nu, text = "Upload", command = self.upload)
        upbut.grid(row = 15, column = 1)
                
         #check button
         #check = t.Button(nu,text = "Check Data", command = self.checkprint)
         #check.grid(row = 16, column = 1)
        
    def setval(self,value):
        
        global optionval
        optionval = value
        
    def convertobinary(self):
        with open(direc,'rb') as file:
            bindata = file.read()
        return bindata
    
    def convertofile(self, data, filename):
        with open(filename, 'wb') as file:
            file.write(data)
        
    
    def upload(self):
       
        db = s.connect("items.db")
        cur = db.cursor()
        
        nget = name.get()
        pget = price.get()       
        dget = desc.get()
        picget = self.convertobinary()
        #actually uploading data
        cur.execute("INSERT INTO items VALUES (:iimage, :iname, :iprice, :isetval, :idesc)",
                {
                    'iimage' : picget,
                    'iname' : nget,
                    'iprice' : pget,
                    'isetval' : optionval,
                    'idesc' : dget
                    }
                    
                    )
        
        
        
        
        db.commit()
        
        
        #clear text boxes
        printimg_label.config(image = '')
        name.delete(0, t.END)
        price.delete(0, t.END)
        cat['menu'].delete(0, t.END)
        desc.delete(0, t.END)
                
    def search(self):
        global actualpic
        itemname = searchterm.get()
        
        db = s.connect("items.db")
        cur = db.cursor()
        
        cur.execute("SELECT * from items")
        dat = cur.fetchall()
        
        for row in dat:
            pic = row[0]
            nam = row[1]
            price = row[2]
            category = row[3]
            description = row[4]
            
            THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
            my_file = os.path.join(THIS_FOLDER, nam + '.png')
            photopath = my_file
            
            self.convertofile(pic, photopath)
            
            
            
        if nam == itemname:    
            result = t.Toplevel()
            result.geometry("500x500")
            result.title("Search Results")
            
            path = os.path.join(THIS_FOLDER, nam + '.png')
            imagee = Image.open(path)
            imagee = imagee.resize((250,250), Image.ANTIALIAS)
            actualpic = ImageTk.PhotoImage(imagee)
            actualpic.image = path
            
           # f.grid(row = 0, column = 0)
            piclabel = t.Label(result, image = actualpic)
            namlabel = t.Label(result, text = nam)
            pricelabel = t.Label(result, text = price)
            catlabel = t.Label(result, text = category)
            desclabel = t.Label(result, text = description)
            
            piclabel.grid(row = 0, column = 1)
            namlabel.grid(row = 1, column = 1)
            pricelabel.grid(row = 2, column = 1)
            catlabel.grid(row = 3, column = 1)
            desclabel.grid(row = 4, column = 1)
            
            #all labels
            namlabel = t.Label(result, text = "Name: ")
            prlabel = t.Label(result, text = "Price: ")
            calabel = t.Label(result, text = "Category: ")
            deslabel = t.Label(result, text = "Description: ")
            
            namlabel.grid(row = 1, column = 0)
            prlabel.grid(row = 2, column = 0)
            calabel.grid(row = 3, column = 0)
            deslabel.grid(row = 4, column = 0)
        
    
    def checkprint(self):
        db = s.connect("items.db")
        cur = db.cursor()
        
        cur.execute("SELECT *, oid from items")
        rec = cur.fetchall()
        print(rec)
        
        
        
        db.commit()        
        
    def sewindow(self):
        
        global ns
        global searchterm
        
        ns = t.Toplevel()
        ns.title("Search for an existing product")
        ns.geometry("900x400")
        
        slabel = t.Label(ns, text = "Enter a search term: ")
        searchterm = t.Entry(ns)
        slabel.grid(row = 0, column = 0, sticky = "E")
        searchterm.grid(row = 0, column = 1, sticky = "W")
        #term = search.get()
        
        go = t.Button(ns, text = "GO", command = self.search)
        go.grid(row = 0, column = 2)
    

    def openfile(self):
        global printimg_label
        global printimg
        global direc
        
        nu.filename = filedialog.askopenfilename(initialdir = "/", title = "Select a Picture", filetypes = (("JPEG Files","*.jpg"),("PNG Files","*.png"),("All Files","*.*")))
        direc = nu.filename
        image = Image.open(direc)
        
        image = image.resize((250,250), Image.ANTIALIAS)
        
        printimg = ImageTk.PhotoImage(image)        
        printimg_label = t.Label(nu, image = printimg)
        printimg.image = direc
        printimg_label.grid(row = 0, column = 1)
         
if __name__ == '__main__':
    m = minebay()
    m.showindow()