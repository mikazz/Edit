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

for i in range(10):
    print("1")
"""
SIGNATURE_TXT_NOT_FOUND_MESSAGE = "Please make sure that the file you want to open exists and that it is in the same folder of this editor."
ABOUT_APP_MESSAGE = "Tkinter App"


# None for default settings

# Window colors
PULLDOWN_BACKGROUND_COLOR = "#181818" # Dark grey
PULLDOWN_FOREGROUND_COLOR = "#aaaaaa" # Light Grey
PULLDOWN_ACTIVE_BACKGROUND_COLOR = "#181818" # Dark grey
PULLDOWN_ACTIVE_FOREGROUND_COLOR = "#ffffff" # White

TOPBAR_BACKGROUND_COLOR = "#181818" 
TOPBAR_FOREGROUND_COLOR = "#aaaaaa" # Light Grey
TOPBAR_ACTIVE_BACKGROUND_COLOR = "#181818" 
TOPBAR_ACTIVE_FOREGROUND_COLOR = "#ffffff" # White

BOTTOMBAR_BACKGROUND_COLOR = "#181818" 
BOTTOMBAR_FOREGROUND_COLOR = "#aaaaaa" # Light Grey
BOTTOMBAR_ACTIVE_BACKGROUND_COLOR = "#181818" 
BOTTOMBAR_ACTIVE_FOREGROUND_COLOR = "#ffffff" # White


# Text Widget colors
DEFAULT_TEXT_COLOR_BACKGROUND = "#111111" # Dark grey
DEFAULT_TEXT_COLOR_FOREGROUND = "#ffffff" # White
TEXT_FOUND_COLOR_FOREGROUND = "red"
TEXT_FOUND_COLOR_BACKGROUND = "black"
CURSOR_COLOR = "white"

# #00FF00 # Green


import time
import re

from tkinter import *
from tkinter import filedialog, messagebox
import tkinter as tk

#from pygments.lexers import PythonLexer


def notDone():
    messagebox.showwarning('Info', 'Working on it')


def onClosing():
    """
        ask before leaving the application 
    """
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        w.destroy()


##class TextLineNumbers(tk.Canvas):
##    def __init__(self, *args, **kwargs):
##        tk.Canvas.__init__(self, *args, **kwargs)
##        self.textwidget = None
##
##    def attach(self, text_widget):
##        self.textwidget = text_widget
##
##    def redraw(self, *args):
##        '''redraw line numbers'''
##        self.delete("all")
##
##        i = self.textwidget.index("@0,0")
##        while True :
##            dline= self.textwidget.dlineinfo(i)
##            if dline is None: break
##            y = dline[1]
##            linenum = str(i).split(".")[0]
##            self.create_text(2,y,anchor="nw", text=linenum)
##            i = self.textwidget.index("%s+1line" % i)
##
##
##class CustomText(tk.Text):
##    def __init__(self, *args, **kwargs):
##        tk.Text.__init__(self, *args, **kwargs)
##
##        # create a proxy for the underlying widget
##        self._orig = self._w + "_orig"
##        self.tk.call("rename", self._w, self._orig)
##        self.tk.createcommand(self._w, self._proxy)
##
##    def _proxy(self, *args):
##        # let the actual widget perform the requested action
##        cmd = (self._orig,) + args
##        result = self.tk.call(cmd)
##
##        # generate an event if something was added or deleted,
##        # or the cursor position changed
##        if (args[0] in ("insert", "replace", "delete") or 
##            args[0:3] == ("mark", "set", "insert") or
##            args[0:2] == ("xview", "moveto") or
##            args[0:2] == ("xview", "scroll") or
##            args[0:2] == ("yview", "moveto") or
##            args[0:2] == ("yview", "scroll")
##        ):
##            self.event_generate("<<Change>>", when="tail")
##
##        # return what the actual widget returned
##        return result    


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
            defining new Text widget to get new color scheme
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
        """
            this method implements 'searching' functionality
        """
        # Remove found tag
        self.tb.tag_remove('found', '1.0', END)
        # Search for word
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

        # Define found tag for Text Widget with its colors
        self.tb.tag_config('found', foreground=TEXT_FOUND_COLOR_FOREGROUND, background=TEXT_FOUND_COLOR_BACKGROUND)


    def syntaxHighlighting2(self):
        #self.tb.tag_config('for', foreground="blue")

        self.tb.config(insertbackground=CURSOR_COLOR)
        self.tb.highlightthickness = 0
        
        self.tb.tag_remove("tagname","1.0", END)
        first = "1.0"
        while(True):
            # for word
            first = self.tb.search("for", first, nocase=False, stopindex=END)
            if not first:
                break
            last = first + "+" + str(len("for")) + "c"
            self.tb.tag_add("tagname", first, last)
            first = last
        self.tb.tag_config("tagname", foreground="#00FF00")


    def syntaxHighlighting(self):
        self.tb.mark_set("range_start", "1.0")
        data = self.tb.get("1.0", END)
        for token, content in PythonLexer.lex(data, PythonLexer()):
            self.tb.mark_set("range_end", "range_start + %dc" % len(content))
            self.tb.tag_add(str(token), "range_start", "range_end")
            self.tb.mark_set("range_start", "range_end")
            

    def replaceAll(self):
        findtext = str(find.get(1.0, END))
        replacetext = str(replace.get(1.0, END))
        alltext = str(text.get(1.0, END))
        alltext1 = all.replace(findtext, replacetext)
        text.delete(1.0, END)
        text.insert("1.0", alltext1)
        

    def __init__(self):
        Tk.__init__(self)


        menubar = Menu(self, background=TOPBAR_BACKGROUND_COLOR, foreground=TOPBAR_FOREGROUND_COLOR, activeforeground=TOPBAR_ACTIVE_FOREGROUND_COLOR, activebackground=TOPBAR_ACTIVE_BACKGROUND_COLOR, bd=0)
        # Create a pulldown menu, and add it to the menu bar


        # File pulldown menu
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR,  activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_ACTIVE_BACKGROUND_COLOR)
        main_menu.add_command(label="New", command=self.newFile, accelerator="Ctrl+N")
        main_menu.add_command(label="Open", command=self.openFile, accelerator="Ctrl+O")
        main_menu.add_command(label="Save", command=self.saveFile, accelerator="Ctrl+S")
        main_menu.add_command(label="Save As", command=self.saveFileAs, accelerator="Ctrl+Alt+S")
        main_menu.add_separator()
        main_menu.add_command(label="Print", command=notDone)
        main_menu.add_separator()
        main_menu.add_command(label="Quit", command=self.quit, accelerator="Alt+F4")
        menubar.add_cascade(label="File", menu=main_menu)


        # Edit pulldown menu
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR,  activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_ACTIVE_BACKGROUND_COLOR)
        main_menu.add_command(label="Find", command=self.searchEngine)
        main_menu.add_command(label="Test Find", command=self.popup)
        main_menu.add_command(label="Find and Replace", command=self.replaceAll)
        main_menu.add_command(label="Count Letters", command=self.countLetters)
        menubar.add_cascade(label="Edit", menu = main_menu)


        # Help pulldown menu
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR,  activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_ACTIVE_BACKGROUND_COLOR)
        main_menu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=main_menu)

        
        # Options pulldown menu
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR, activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_ACTIVE_BACKGROUND_COLOR)
        main_menu.add_command(label="Always on top", command=self.topWindow)
        main_menu.add_command(label="Colorscheme", command=self.changeColorScheme)
        main_menu.add_command(label="Syntax Highligthing", command=self.syntaxHighlighting)
        menubar.add_cascade(label="Options", menu=main_menu)


        # Insert pulldown menu
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR, activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_ACTIVE_BACKGROUND_COLOR)
        main_menu.add_command(label="Insert date", command=self.add_date)
        main_menu.add_command(label="Insert signature", command=self.add_signature)
        menubar.add_cascade(label="Insert", menu=main_menu)


        # Display the menu
        self.config(menu=menubar)


##        self.tb = CustomText(self, font=("courier new", 16), foreground=DEFAULT_TEXT_COLOR_FOREGROUND, background=DEFAULT_TEXT_COLOR_BACKGROUND, bd=0)
##
##        # Turn on scrollbar in options?
##        #self.vsb = tk.Scrollbar(orient="vertical", command=self.text.yview)
##        #self.text.configure(yscrollcommand=self.vsb.set)
##
##        # Mayby define tags here?
##        #self.tb.tag_configure("bigfont", font=("Helvetica", "24", "bold"))
##        self.linenumbers = TextLineNumbers(self, width=30)
##        self.linenumbers.attach(self.tb)
##
##        #self.vsb.pack(side="right", fill="y")
##        self.linenumbers.pack(side="left", fill="y")
##        self.tb.pack(side="right", fill="both", expand=True)
##
##        self.tb.bind("<<Change>>", self._on_change)
##        self.tb.bind("<Configure>", self._on_change)
##
##        
##        self.bind("<Control-y>", self.redo)
##        self.bind("<Control-Y>", self.redo)
##        self.bind("<Control-Z>", self.undo)
##        self.bind("<Control-z>", self.undo)




##    # When things change?
##    def _on_change(self, event):
##        self.linenumbers.redraw()
##
##
##    def undo(self, event=None):
##        self.edit_undo()
##        
##
##    def redo(self, event=None):
##        self.edit_redo()


        #BOTTOMBAR_ACTIVE_BACKGROUND_COLOR = "#181818" 
        #BOTTOMBAR_ACTIVE_FOREGROUND_COLOR = "#ffffff" # White

        # Bottom bar
        self.sb = Label(self, relief = FLAT, anchor = W, foreground=BOTTOMBAR_FOREGROUND_COLOR, background=BOTTOMBAR_BACKGROUND_COLOR, bd=0)
        self.sb.pack(expand = 0, fill = X, side = BOTTOM) #BOTTOM


        # Bottom bar for command line?
        #self.sb = Entry(self, relief = SUNKEN)
        #self.sb.pack(expand = 0, fill = Y, side = BOTTOM)


        # Text widget area
        self.tb = Text(self, font=("courier new", 16), foreground=DEFAULT_TEXT_COLOR_FOREGROUND, background=DEFAULT_TEXT_COLOR_BACKGROUND, bd=0)

        # White border around the edges of text widget
        # widget.config(highlightbackground=COLOR) #for colored one
        # If you don't want that border at all, set the highlightthickness attribute to 0
        self.tb.config(highlightthickness=0)


        self.tb.pack(expand=1, fill = BOTH)
        self.tb.insert(END, GREETING_MESSAGE)


        self.fn = None
        self.sb.config(text = 'Ready')


        #focus on top
        #self.tb.focus_set()



if __name__ == '__main__':

    w = Application()
   
    try:
        # About application popup
        #w.about()
        w.title("Edit")

        w.call('wm', 'attributes', '.', '-topmost', '1')
        w.geometry('1000x600+100+100')
        w.configure(background='black')



        # Ask before leaving the application
        w.protocol("WM_DELETE_WINDOW", onClosing)
        w.mainloop()

    except BaseException as e:
        print(e)

