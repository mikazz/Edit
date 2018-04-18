# coding: utf-8

GREETING_MESSAGE = "Hello World"
SIGNATURE_TXT_NOT_FOUND_MESSAGE = "Please be sure that the file you want to open exists and that it is in the same folder of this editor."
ABOUT_APP_MESSAGE = "Tkinter App"

from tkinter import *
from tkinter import filedialog, messagebox

import time




def notDone():
    messagebox.showwarning('Info', 'Working on it')


def onClosing():
    """
        ask before leaving the application 
    """
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        w.destroy()


class Application(Tk):

    contentIsChanged = False

    def about(self):
        """
            this method prints info about application 
        """
        MESSAGE = ABOUT_APP_MESSAGE
        messagebox.showinfo('Info', MESSAGE)

        
    def topWindow(self):
        #self.tb.focus_set()
        return True


    def newFile(self):
        """
             this method implements open file functionality
        """
        if self.contentIsChanged:
            self.saveFileAs()

        self.tb.delete(1.0, END)
        self.fn = None
        self.sb.config(text = 'New file')


    def openFile(self):
        """
             this method implements open file functionality
        """
        if self.contentIsChanged:
            self.saveFileAs()
        dlg = filedialog.Open(initialfile = self.fn)
        f = dlg.show()
        if len(f):
            self.tb.delete(1.0, END)
            self.tb.insert(END, open(f).read())
            self.fn = f
            self.sb.config(text = 'Opened ' + self.fn)


    def saveFileAs(self):
        """
             this method implements save file as functionality
        """
        dlg = filedialog.SaveAs(initialfile = self.fn)
        f = dlg.show()
        if len(f):
            self.fn = f
            self.saveFile()


    def saveFile(self):
        """
             this method implements save file functionality
        """
        if (self.fn):
            plik = open(self.fn, 'w')
            #plik.write(self.tb.get(1.0, END).encode('utf-8'))
            plik.write(self.tb.get(1.0, END))

            plik.close()
            self.sb.config(text = 'Saved ' + self.fn)
        else:
            self.saveFileAs()


    def add_date(self):
        """
             this method adds date signature in:
             dd/mm/yyyy format
        """
        full_date = time.localtime()
        day = str(full_date.tm_mday)
        month = str(full_date.tm_mon)
        year = str(full_date.tm_year)
        date = "\n" + day + '/' + month + '/' + year
        self.tb.insert(0.0, date + '\n')


    def add_signature(self):
        """
             this method adds signature from a text file
        """
        try:
            with open("signature.txt") as f:
                self.tb.insert(0.0, f.read() + '\n')

        except IOError:
            MESSAGE = SIGNATURE_TXT_NOT_FOUND_MESSAGE
            messagebox.showwarning("\"signature.txt\" not found.", MESSAGE)


    def __init__(self, title):
        Tk.__init__(self)
        self.title(title)

        menubar = Menu(self)

        # Create a pulldown menu, and add it to the menu bar

        # File pulldown menu
        main_menu = Menu(menubar, tearoff=0)
        main_menu.add_command(label="New", command=self.newFile)
        main_menu.add_command(label="Open", command=self.openFile)
        main_menu.add_command(label="Save", command=self.saveFile)
        main_menu.add_command(label="Save As", command=self.saveFileAs)
        main_menu.add_separator()
        main_menu.add_command(label="Print", command=notDone)
        main_menu.add_separator()
        main_menu.add_command(label="Quit", command=self.quit)
        menubar.add_cascade(label="File", menu=main_menu)


        # Edit pulldown menu
        main_menu = Menu(menubar, tearoff=0)
        main_menu.add_command(label="Find", command=notDone)
        menubar.add_cascade(label="Edit", menu=main_menu)


        # Help pulldown menu
        main_menu = Menu(menubar, tearoff=0)
        main_menu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=main_menu)


        # Options pulldown menu
        main_menu = Menu(menubar, tearoff=0)
        main_menu.add_command(label="Always on top", command=self.topWindow)   
        menubar.add_cascade(label="Options", menu=main_menu)


        # Insert pulldown menu
        main_menu = Menu(menubar, tearoff=0)
        main_menu.add_command(label="Insert date", command=self.add_date)
        main_menu.add_command(label="Insert signature", command=self.add_signature)
        menubar.add_cascade(label="Insert", menu=main_menu)


        # display the menu
        self.config(menu=menubar)

        # Top bar
        self.sb = Label(self, relief = FLAT, anchor = W)
        self.sb.pack(expand = 0, fill = X, side = BOTTOM)


        # Bottom bar
        self.sb = Entry(self, relief = SUNKEN)
        self.sb.pack(expand = 0, fill = Y, side = BOTTOM)

    
        self.tb = Text(self, font=("courier new", 16))

             
        self.tb.pack(expand=1, fill = BOTH)
        self.tb.insert(END, GREETING_MESSAGE)

    
        self.fn = None

        self.sb.config(text = 'Ready')


        #focus on top
        #self.tb.focus_set()



if __name__ == '__main__':

    w = Application('Edit')
   
    try:
        #w.about()

        w.call('wm', 'attributes', '.', '-topmost', '1')
        w.geometry('1000x600+100+100')

        w.protocol("WM_DELETE_WINDOW", onClosing)
        w.mainloop()

    except:
        pass
    

