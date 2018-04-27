# coding: utf-8

# Codes
GREETING_MESSAGE = """1
2
3
Hello
HelloWORLD
HelloWorld
Hello World Hello
DO IT Hello
Hello hELLO

Hello
"""
SIGNATURE_TXT_NOT_FOUND_MESSAGE = "Please be sure that the file you want to open exists and that it is in the same folder of this editor."
ABOUT_APP_MESSAGE = "Tkinter App"

# Window colors
PULLDOWN_BACKGROUND_COLOR = "black"
PULLDOWN_FOREGROUND_COLOR = "#aaaaaa" # Light Grey

PULLDOWN_ACTIVEBACKGROUND_COLOR = "#181818" # Dark grey
PULLDOWN_ACTIVEFOREGROUND_COLOR = "#ffffff" # White

# Text Widget colors
DEFAULT_TEXT_COLOR_BACKGROUND = "#111111" # Dark grey
DEFAULT_TEXT_COLOR_FOREGROUND = "#ffffff" # White
TEXT_FOUND_COLOR_FOREGROUND = "red"
TEXT_FOUND_COLOR_BACKGROUND = "black"

from tkinter import *
from tkinter import filedialog, messagebox

import time
import re


def notDone():
    messagebox.showwarning('Info', 'Working on it')


def onClosing():
    """
        ask before leaving the application 
    """
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        w.destroy()


class popupWindow(object):
    def __init__(self, master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Find")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()



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
             this method implements 'new file' functionality
        """
        if self.contentIsChanged:
            self.saveFileAs()

        self.tb.delete(1.0, END)
        self.fn = None
        self.sb.config(text = 'New file')


    def openFile(self):
        """
             this method implements 'open file' functionality
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
             this method implements 'save file as' functionality
        """
        dlg = filedialog.SaveAs(initialfile = self.fn)
        f = dlg.show()
        if len(f):
            self.fn = f
            self.saveFile()
            self.sb.config(text = 'Saved as ' + self.fn)


    def saveFile(self):
        """
             this method implements 'save file' functionality
        """
        if (self.fn):
            file = open(self.fn, 'w')
            #plik.write(self.tb.get(1.0, END).encode('utf-8'))
            file.write(self.tb.get(1.0, END))

            file.close()
            self.sb.config(text = 'Saved ' + self.fn)
        else:
            self.saveFileAs()


    def countLetters(self):
        """
             this method implements 'Count Letters' functionality
        """
        lettersNumber = sum(c != ' ' for c in self.tb.get(1.0, END))
        self.sb.config(text = 'Number of letters: ' + str(lettersNumber-1))


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


    def changeColorScheme(self):
        """
            defining new Text widget
        """
        col_bg = "black"
        col_fg = "white"

        self.tb["bg"] = col_bg
        self.tb["fg"] = col_fg
        #self.insert(END, "")
        self.sb.config(text = "Color scheme changed")

    def popup(self):
        self.w=popupWindow(self.master)
        #self.b["state"] = "disabled" 
        #self.master.wait_window(self.w.top)
        #self.b["state"] = "normal"

    def entryValue(self):
        return self.w.value


    def searchEngine(self):
        # Remove found tag
        self.tb.tag_remove('found', '1.0', END)
        search = "Hello"

        list_of_words = re.findall(r"\b" + search + r"\b", self.tb.get(1.0, END))
        print(list_of_words)

        for word in list_of_words:
            idx = '1.0'
            while idx:
                idx = self.tb.search(word, idx, nocase=1, stopindex=END)
                if idx:
                    lastidx = '%s+%dc' % (idx, len(word))
                    self.tb.tag_add('found', idx, lastidx)
                    idx = lastidx

        # Define found tag for Text Widget
        self.tb.tag_config('found', foreground=TEXT_FOUND_COLOR_FOREGROUND, background=TEXT_FOUND_COLOR_BACKGROUND)


    def replaceAll(self):
        findtext = str(find.get(1.0, END))
        replacetext = str(replace.get(1.0, END))
        alltext = str(text.get(1.0, END))
        alltext1 = all.replace(findtext, replacetext)
        text.delete(1.0, END)
        text.insert("1.0", alltext1)
        

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
        main_menu.add_command(label="Find", command=self.searchEngine)
        main_menu.add_command(label="Test Find", command=self.popup)
        main_menu.add_command(label="Find and Replace", command=self.replaceAll)
        main_menu.add_command(label="Count Letters", command=self.countLetters)
        menubar.add_cascade(label="Edit", menu = main_menu)


        # Help pulldown menu
        main_menu = Menu(menubar, tearoff=0)
        main_menu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=main_menu)

        
        # Options pulldown menu
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR, activebackground=PULLDOWN_ACTIVEBACKGROUND_COLOR, activeforeground=PULLDOWN_ACTIVEFOREGROUND_COLOR)
        main_menu.add_command(label="Always on top", command=self.topWindow)
        main_menu.add_command(label="Colorscheme", command=self.changeColorScheme)
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
        #self.sb = Entry(self, relief = SUNKEN)
        #self.sb.pack(expand = 0, fill = Y, side = BOTTOM)

        # Text widget area
        self.tb = Text(self, font=("courier new", 16), bg=DEFAULT_TEXT_COLOR_BACKGROUND, fg=DEFAULT_TEXT_COLOR_FOREGROUND, bd=0)
        self.tb.pack(expand=1, fill = BOTH)
        self.tb.insert(END, GREETING_MESSAGE)


        self.fn = None
        self.sb.config(text = 'Ready')


        #focus on top
        #self.tb.focus_set()



if __name__ == '__main__':

    w = Application('Edit')
   
    try:
        # About application popup
        #w.about()

        w.call('wm', 'attributes', '.', '-topmost', '1')
        w.geometry('1000x600+100+100')
        #w.configure(background='black')

        # Ask before leaving the application
        w.protocol("WM_DELETE_WINDOW", onClosing)
        w.mainloop()

    except BaseException as e:
        print(e)

