# https://github.com/roseman/idle/blob/master/config-keys.def

__author__ = 'mikazz'
__version__ = 'v1.1.1 (Alpha)'
__license__ = 'All rights reserved'


README = """
#
# README:
#

File >
    New - Creates blank file
    New With Template - Creates blank file with extention and code template 
    Open - Opens file
    Open Recent - Finds recently opened files
    Reload File - Reloads file to the point since last save
    Append From File - Appends whole file at the end of current file
    Save - Saves file
    Save As - Saves file as (with a new name)
    New Folder - Creates New Folder in /Edit/ editor directory
    Set File Name - Saves copy of renamed file
    Print - printCurrent file
    New Window - Creates new application window
    Quit - Quits the application

Edit >
    Run Code
    Run Code in System Terminal
    Find
    Count Letters

Options >
    Always On Top - Sets Window on top of other
    Syntax Highlighting - Enables code highlighting according to file extension
    Word Wrap - Words wrapping at the end of the line
    AutoSave - Saves file every desired time
    Full screen - Removes Window border
    Increase Font Size - by 1 point
    Decrease Font Size - by 1 point
    
Insert >
    Insert date - Inserts date
    Insert signature - Inserts given signature from a text file

View >
    Goto TOP - Goes to the first line of a file
    Goto END - Goes to the last line of a file
    Goto Line - Goes to the desired line
    Goto End Of Line - Goes far right
    Goto Start Of Line - Goes far left
    Select - Selects lines from : to
    
Terminal >
    Clear Terminal - (Ctrl + Del) - Clears the Terminal
    Clear Terminal on run - (T/F) - Clears the Terminal when new run is initialized
    Show exit codes (T/F) - Shows exit codes when run is initialized

"""

# Codes
GREETING_MESSAGE = """for i in range(10):
    print("Hello " + str(i) )"""
SIGNATURE_TXT_NOT_FOUND_MESSAGE = "Signature file not found. It should be in the same folder of this editor."
ABOUT_APP_MESSAGE = "Edit App"

# None for default settings

# Window colors

WINDOW_BACKGROUND_COLOR =  "#181818"# change to "yellow" nxt time

PULLDOWN_BACKGROUND_COLOR = "#181818" # Dark grey
PULLDOWN_FOREGROUND_COLOR = "#aaaaaa" # Light Grey
PULLDOWN_ACTIVE_BACKGROUND_COLOR = "#181818" # Dark grey
PULLDOWN_ACTIVE_FOREGROUND_COLOR = "#ffffff" # White
CHECKBUTTON_SELECT_COLOR = "#aaaaaa"

TOPBAR_BACKGROUND_COLOR = "#181818" 
TOPBAR_FOREGROUND_COLOR = "#aaaaaa" # Light Grey
TOPBAR_ACTIVE_BACKGROUND_COLOR = "#181818" 
TOPBAR_ACTIVE_FOREGROUND_COLOR = "#ffffff" # White

BOTTOMBAR_BACKGROUND_COLOR = "#181818" 
BOTTOMBAR_FOREGROUND_COLOR = "#aaaaaa" # Light Grey
BOTTOMBAR_ACTIVE_BACKGROUND_COLOR = "#181818" 
BOTTOMBAR_ACTIVE_FOREGROUND_COLOR = "#ffffff" # White

# Text Widget colors
DEFAULT_TEXT_COLOR_BACKGROUND = "#111111" #"#181818" # Dark grey
DEFAULT_TEXT_COLOR_FOREGROUND = "#ffffff" # White
TEXT_FOUND_COLOR_FOREGROUND = "red"
TEXT_FOUND_COLOR_BACKGROUND = "black"

CURSOR_COLOR = "white"
FOREGROUND_SELECT_COLOR = None
BACKGROUND_SELECT_COLOR = None
INACTIVE_SELECT_BACKGROUND_COLOR = None

# Command line
COMMANDLINE_CURSOR_COLOR = "white"
TERMINAL_BACKGROUND_COLOR = "#0a0a0a" #Dark
TEXT_ERROR_COLOR_FOREGROUND = "red"

# Line numbers
LINENUMBERS_COLOR_BACKGROUND = "#111111"
LINENUMBERS_COLOR_FOREGROUND = "#aaaaaa"
SELECTION_LINENUMBERS_COLOR_FOREGROUND = "#ffffff"

# Directory Browser
DIRECTORY_BROWSER_COLOR_BACKGROUND = "#111111" # Dark grey
DIRECTORY_BROWSER_COLOR_FOREGROUND = "#ffffff" # White

SNIPPETLIST_COLOR_BACKGROUND = "#111111"
SNIPPETLIST_COLOR_FOREGROUND = "#ffffff"

FONT_TYPE = "courier new"
DEFAULT_FONT_SIZE = 16


# FILETYPES
ftypes = [
    ('All files', '*'),
    ('Python code files', '*.py'), 
    ('Perl code files', '*.pl;*.pm'),  # semicolon trick
    ('R Cran files', '*.r'),
    ('Java code files', '*.java'),
    ('JavaScript code files', '*.js'),
    ('Scala code files', '*.scala'),
    ('C++ code files', '*.cpp;*.h'),   # semicolon trick
    ('Text files', '*.txt')  
]

PYTHON_TEMPLATE = """
def main():
    print('Hello, world!')

if __name__ == '__main__':
    main()
  """


import time
from datetime import datetime

import re
import os
import platform
import subprocess

from tkinter import *
from tkinter import simpledialog, filedialog, messagebox
import tkinter as tk
import tkinter.ttk as ttk

# Code Highlighting
try:
    from pygments import lex

except ImportError:
    pass

# Printing
try:
    import cups
    CUPS_AVAILABLE = True
except ImportError:
    CUPS_AVAILABLE = False

try:
    import WIN32PRINT_AVAILABLE
    WIN32PRINT_AVAILABLE = True
except ImportError:
    WIN32PRINT_AVAILABLE = False

# Get system type
SYSTEMTYPE = platform.system()





class ScrollListbox(tk.Frame):
    """
        A listbox with the vertical scrollbar built in.
    """
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self._lbox = tk.Listbox(self, *args, **kwargs)
        self._vscroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self._lbox.pack(fill=tk.BOTH, expand=1, side=tk.LEFT)
        self._vscroll.pack(fill=tk.Y, side=tk.RIGHT)

    def Listbox(self):
        return self._lbox
    
    def Scrollbar(self):
        return self._vscroll


class PrintDialogLinux(tk.Toplevel):
    """
        A dialog for handling printing.
    """
    BUTTONWIDTH = 20
    def __init__(self, parent, filename, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)
        if not CUPS_AVAILABLE:
            messagebox.showerror('CUPS Not Available!', 'CUPS is necessary to print. Please install!', parent=self)
            self.destroy()
            return

        self.parent = parent
        self.filename = filename
        self.grab_set()
        self.wm_title("Print Code...")


        self.conn = cups.Connection()
        printerDictRef = self.conn.getPrinters()

        self.printerListFrame = ttk.Labelframe(self, text="Printers")
        self.printerList = ScrollListbox(self.printerListFrame)

        for key in printerDictRef.keys():
            self.printerList.Listbox.insert(tk.END, key)

        self.printerList.pack(expand=1, fill=tk.BOTH)
        self.printerListFrame.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.printButton = tk.Button(self, text="Print", command=self.sendToPrinter, width=self.BUTTONWIDTH)
        self.printButton.grid(row=1, column=0)

        self.cancelButton = tk.Button(self, text="Cancel", command=self.destroy, width=self.BUTTONWIDTH)
        self.cancelButton.grid(row=1, column=1)

        self.getPrinterSelected()

    def __del__(self):
        """
            Make sure when this gets recycled that we've released the grab.
        """
        self.grab_release()

    def destroy(self):
        """
            Release the grab, and destroy the dialog.
        """
        self.grab_release()
        tk.Toplevel.destroy(self)

    def getPrinterSelected(self):
        return self.printerList.Listbox.get(tk.ACTIVE)

    def sendToPrinter(self):
        try:
            self.conn.printFile(self.getPrinterSelected(), self.filename, "{0} - Edit".format(self.filename), {})

        except cups.IPPError:
            messagebox.showerror('Failed to Print!', 'Failed to Print! Check printer!', parent=self)


class PrintDialogWindows(tk.Toplevel):
    """
        A dialog for handling printing.
    """
    def __init__(self, parent, printData, *args, **kwargs):
        tk.Toplevel.__init__(self, parent, *args, **kwargs)

        if not WIN32PRINT_AVAILABLE:
            messagebox.showerror('WIN32PRINT Not Available!', 'WIN32PRINT is necessary to print. Please install!', parent=self)

            self.destroy()
            return
        self.parent = parent
        self.printData = printData
        self.grab_set()
        self.wm_title("Print Code...")


    def __del__(self):
        """
            Make sure when this gets recycled that we've released the grab.
        """
        self.grab_release()

    def destroy(self):
        """
            Release the grab, and destroy the dialog.
        """
        self.grab_release()
        tk.Toplevel.destroy(self)


class MyDialog:
    '''
        Dialog box
    '''
    def __init__(self, parent):

        top = self.top = Toplevel(parent)

        tk.Label(top, text="Value").pack()

        self.e = Entry(top)
        self.e.pack(padx=5)

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

    def ok(self):
        print ("value is", self.e.get())
        self.top.destroy()

class CD:
    '''
        Context manager for changing the current working directory
    '''
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


class TextLineNumbers(tk.Canvas):
    '''
        Line numbering for Text widget
    '''
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''
            Redraw line numbers
        '''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]

            self.create_text(2,y,
                             anchor="nw",
                             text=( f'{linenum:>2}' ),
                             fill=LINENUMBERS_COLOR_FOREGROUND,
                             activefill=SELECTION_LINENUMBERS_COLOR_FOREGROUND)


            i = self.textwidget.index("%s+1line" % i)


# http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
class AutocompleteEntry(tk.Entry):
    def __init__(self, lista, *args, **kwargs):
        
        tk.Entry.__init__(self, *args, **kwargs)
        self.lista = lista        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Return>", self.selection)
        self.bind("<Escape>", self.clear)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        
        self.lb_up = False

    def changed(self, name, index, mode):  

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:            
                if not self.lb_up:
                    self.lb = Listbox()
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Return>", self.selection)

                    #x,y=canv.winfo_pointerxy()
                    #x_MOUSE=canv.canvasx(x)
                    #y_MOUSE=canv.canvasy(y)

                    line, column = tb.index(INSERT).split('.')


                    
                    #self.lb.place(x=self.winfo_x(), y=0+self.winfo_height() ) #self.winfo_y()+self.winfo_height()
                    #self.lb.place(x=X_MOUSE, y=Y_MOUSE ) #DOBRE dla myszy
                    self.lb.place(x=line, y=column ) #self.winfo_y()+self.winfo_height()


                    self.lb_up = True
                
                self.lb.delete(0, END)
                for w in words:
                    self.lb.insert(END,w)
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False
        
    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def clear(self, event):
        self.lb.destroy()

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':                
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)                
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:                        
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)        
                self.lb.selection_set(first=index)
                self.lb.activate(index) 

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*')
        return [w for w in self.lista if re.match(pattern, w)]


class CustomText(tk.Text):
    '''
        Customized text widget
    '''
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.event_generate("<<Change>>", when="tail")
            #self.see("insert") # follow view with the insert

        if (args[0] in ("insert", "replace", "delete")):
            self.event_generate("<<Change_Line>>", when="tail")

        # return what the actual widget returned
        return result

    
# Styling
#Then you prefix the widgets with either tk or ttk :
# f1 = tk.Frame(..., bg=..., fg=...)
# f2 = ttk.Frame(..., style=...)




class SystemTerminal(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)



##    terminalHeight = 100
##    terminalWidth = 100
##
##    self.systemTerminal = Frame(self, height=terminalHeight, width=terminalWidth)
##    self.systemTerminal.grid(column=4, row=0, sticky=N+E+S+W)
##    
##    wid = self.systemTerminal.winfo_id()
##    os.system("""xterm -into %d -bg "#181818" -geometry 40x20 -fa "Monospace" -fs 10 &""" % wid)








class DirectoryBrowser(tk.Frame):
    '''
        Directory browser
    '''
    def __init__(self, master, path):
        tk.Frame.__init__(self, master)
        self.tree = ttk.Treeview(self, style="Black.TLabelframe", padding=0, show="tree", height=50) #, height=40

        #self.tree.heading("#0", text=path, anchor='n')

        abspath = os.path.abspath(path)
        #root_node = self.tree.insert("", "end", text=abspath, open=True)
        root_node = self.tree.insert("", "end", open=True)

        self.process_directory(root_node, abspath)


        self.tree.grid(column=0,row=0)
        #self.tree.pack(expand = 1, fill = Y, side = TOP)
        #self.grid()

    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.tree.insert(parent, 'end', text=p, open=False)
            if isdir:
                self.process_directory(oid, abspath)


class Application(Tk):


    contentIsChanged = False

    recentFiles = []

    fileTemplates = ["Python", "R", "Scala"]

    defaultFontSize = DEFAULT_FONT_SIZE

    currentDirectory = ""

    snippetListPython = [["1", "print(\"Hello World\")"], ["two","def"], ["three","trujga"], ["four","czwurka"] ]


    def showSettings(self):
        pass
    

    def exitCommand(self):
        """
            Ask before leaving the application 
        """
        if messagebox.askokcancel("Quit","Are you sure?"):
            w.destroy()


    def readme(self):
        """
            Shows the README message 
        """
        Readme = Tk()
        Readme.title("Readme")

        ReadmeText = Text(Readme,
                          font=("courier new", 14),
                          highlightthicknes=0,
                          foreground=DEFAULT_TEXT_COLOR_FOREGROUND,
                          background=DEFAULT_TEXT_COLOR_BACKGROUND,
                          bd=0)
        ReadmeText.grid()
        ReadmeText.insert(0.0, README)
        ReadmeText["state"] = DISABLED
        Readme.mainloop()


    def customPaste(self, event):
        """
            Linux fix for Text Widget:
            When some text is copied and pasted in a tkinter textbox
            and if there is selected text, it won't remove (replace) selected text

            Event: "<<Paste>>" for self.tb
        """
        # If there is no text inside textbox do nothing  
        if not self.tb.tag_ranges("sel"):
            return

        # If there is, delete it
        self.tb.delete("sel.first", "sel.last")

        # And insert clipboard content
        self.tb.insert("insert", self.tb.clipboard_get())

        return "break"

        
    def setGreetingMessage(self):
        pass
        
        
    def showDialog(self, event):
        MyDialog(w)


    def showFancyListbox(self, event):
        FancyListbox(w, selectmode='multiple')


    def showRightMouseMenu(self, event):
        # display the popup menu
        try:
            self.RightMouseMenu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.RightMouseMenu.grab_release()        

##    def key(self, event):
##        #print ("pressed", repr(event.char))
##        pass


    def callback(self, event):
        #print ("clicked at", event.x, event.y)
        pass


    def _on_change(self, event):
        """
            Check if
            "insert", "replace", "delete"
            "mark", "set", "insert"
            "xview", "moveto"
            "xview", "scroll"
            "yview", "moveto"
            "yview", "scroll"
            has been performed
        """
        self.linenumbers.redraw()
        self.updateLabelCoordinates()


    # Its checking same thing as above, (syntax highlighting purpose only), better solution?
    def _line_change(self, event):
        """
            Check if
            "insert", "replace", "delete"
            has been performed
        """
        self.line_highlight()
        self.autocomplete()
        

    def updateLabelCoordinates(self):
        """
            Updates and prints INSERT (Cursor) Coordinates on Label
            Ln: Line_Position Col: Column_Position
        """
        line, column = self.tb.index(INSERT).split('.')
        cords = "Ln: {ln} Col: {col}".format(ln=line, col=column)
        self.labelBar.config(text = cords)
        
        # No formatting option / comment out above 3 lines
        #self.labelBar.config(text = (self.tb.index("insert")) )


         
    def showListbox(self):
        ListBox(w, selectmode='multiple')


    def refresh(self):

        abspath = os.path.abspath(self.currentDirectory)
        root_node = self.tree.insert("", "end", text=abspath, open=True)
        w.db.process_directory(root_node, abspath)

        #w.db.process_directory()


    def getWorkingDirectory(self):
        """
            Selects a directory thats stored in:
            currentDirectory
        """

        dirName = filedialog.askdirectory()
        self.currentDirectory = dirName

        
    def about(self):
        """
            Prints info about application 
        """
        aboutMsg = "Edit Version {version}\n 2018".format(version = __version__)
        messagebox.showinfo('Info', aboutMsg)


    def topWindow(self):
        """
            Forces window to stay on top 
        """
        if self.always_on_top.get() == True:
            w.call('wm', 'attributes', '.', '-topmost', '1')
        else:
            w.call('wm', 'attributes', '.', '-topmost', '0')

    
    def fullscreen(self):
        """
            Enables fullscreen mode 
        """
        if self.enable_fullscreen.get() == True:
            w.attributes("-fullscreen", True)
        else:
            w.attributes("-fullscreen", False)


    def newWindow(self):
        """
           Creates new application window
        """
        Application()


    def undo(self):
        """
            Undo last operation to the text box.
        """
        try:
            self.tb.edit_undo()
            self.labelBar.config(text = 'Undo')

        except:
            pass


    def redo(self):
        """
            Redo last change undone on the text box.
        """
        try:
            self.tb.edit_redo()
            self.labelBar.config(text = 'Redo')

        except:
            pass


    def printCurrent(self):
        """
            Prints the document
        """

        if SYSTEMTYPE == 'Linux':
            self.saveFile()

            printDialog = PrintDialogLinux(self, self.fn)
            self.wait_window(printDialog)


        elif SYSTEMTYPE == 'Windows':
            self.saveFile()
            
            printDialog = PrintDialogLinux(self, currentEditor.getTextContent())
            self.wait_window(printDialog)
        else:
            messagebox.showerror('Printing Not Supported!', 'Printing not supported on this platform!', parent=self)


    def selectAll(self, *args):
        """
            Selects whole text
        """
        # Selects / highlights all the text.
        self.tb.tag_add(SEL, "1.0", END)
        
        # Set mark position to the end and scroll to the end of selection.
        self.tb.mark_set(INSERT, END)
        self.tb.see(INSERT)


    def copyPath(self):
        """
            Copy file path to clipboard
        """
        self.clipboard_clear()
        self.clipboard_append(str(self.fn))
        self.labelBar.config(text = 'File path copied to clipboard')


    def wordWrap(self):
        """
            Enable word wrapping
        """
        if self.word_wrap.get() == True:
            self.tb.config(wrap="word")
            self.labelBar.config(text = 'Word Wrap enabled')
            # Fix for linenumbers reacting with delay
            self.linenumbers.redraw()

        else:
            self.tb.config(wrap="none")
            # Fix for linenumbers reacting with delay
            self.linenumbers.redraw()


    def revertFile(self, event):
        """
            Save a copy of a file after opening, and
        """
        pass


    def newFile(self):
        """
            Implements 'new file' functionality
        """
        if self.contentIsChanged:
            self.saveFileAs()

        self.tb.delete(1.0, END)
        self.fn = None
        self.labelBar.config(text = 'New Untitled file')
        w.title("Untitled")


    def newFileWithTemplate(self):
        if self.contentIsChanged:
            self.saveFileAs()

        self.tb.delete(1.0, END)
        self.tb.insert(END, PYTHON_TEMPLATE)
        self.fn = "Untitled" + ".py"
        self.labelBar.config(text = 'New Untitled file')
        w.title(self.fn)

        self.checkLexerType()
        self.syntaxHighlighting()
        

    def openFile(self):
        """
            Implements 'open file' functionality
        """
        if self.contentIsChanged:
            self.saveFileAs()

        dlg = filedialog.Open(initialfile = self.fn, filetypes=ftypes)        
        f = dlg.show()

        if len(f):
            self.tb.delete(1.0, END)
            self.tb.insert(END, open(f).read())
            self.fn = f

        if not self.fn:
            return
        
        self.labelBar.config(text = 'Opened ' + self.fn)
        w.title(self.fn)

        if self.fn not in self.recentFiles:
            self.recentFiles.insert(0, str(self.fn))
            self.populateOpenRecentFilesMenu()
        else:
            pass
            #self.recentFiles.insert(0, self.recentFiles.pop(self.fn))

        self.checkLexerType()
        self.syntaxHighlighting() #its faster to call function and check inside it for T/F or check T/F here?

        
    def openRecent(self, f):
    
        def load():

            print(self.contentIsChanged)

            if self.contentIsChanged:
                result = messagebox.askyesno("Content is changed","Do you want to save?")

                if result == True:
                    self.saveFile()
                else:
                    return


            self.tb.delete(1.0, END)
            self.tb.insert(END, open(f).read())
            self.fn = f

            self.checkLexerType()
            self.syntaxHighlighting() #its faster to call function and check inside it for T/F or check T/F here?
            
        return load


    def reloadFile(self):
        if not self.fn:
            return

        self.tb.delete(1.0, END)
        self.tb.insert(END, open(self.fn).read())

        self.checkLexerType()
        self.syntaxHighlighting() #its faster to call function and check inside it for T/F or check T/F here?
                    
        
    def appendFromFile(self):
        # moze dodac filetypes tylko tych co w self.fn?
        dlg = filedialog.Open(initialfile = self.fn, filetypes=ftypes)        
        f = dlg.show()
        self.tb.insert(END, "\n" + open(f).read())
        

    def populateOpenRecentFilesMenu(self):
        """
            Populates Main Menu with recent opened files
        """
        self.recentMenu.delete(0, 'end')

        for counter, name in enumerate(self.recentFiles):
            self.recentMenu.add_command(label=("{}. {}".format(counter, self.recentFiles[counter]) ),
                                        command=self.openRecent(name))


    def populateFileTemplateMenu(self):
        """
            Populates Main Menu with recent opened files
        """
        for name in self.fileTemplates:
            self.recentMenu.add_command(label=("{}".format(name) ), command=self.openRecent(name))

            
    def saveFile(self):
        """
            Implements 'save file' functionality
        """
        # If file is not empty
        if (self.fn):
            file = open(self.fn, 'w')
            file.write(self.tb.get(1.0, END))

            file.close()
            self.labelBar.config(text = 'Saved ' + self.fn)
            w.title(self.fn)
        else:
            self.saveFileAs()


    def saveFileAs(self):
        """
            Implements 'save file as' functionality
        """
        dlg = filedialog.SaveAs(initialfile = self.fn, filetypes = ftypes)
        f = dlg.show()
        if len(f):
            self.fn = f
            self.saveFile()
            self.labelBar.config(text = 'Saved as ' + self.fn)
            w.title(self.fn)


    def autoSave(self):
        """
            Auto-saves file
        """
        if self.auto_save.get() == True:
            
            w.after(5000, self.autoSave) # time in milliseconds 1000 = 1 sec
            print("autosaved")
            
            if (self.fn):
                file = open(self.fn, 'w')
                file.write(self.tb.get(1.0, END))
                file.close()
                

                full_time = time.localtime()
                hour = str(full_time.tm_hour)
                min = str(full_time.tm_min)
                sec = str(full_time.tm_sec)

                time_now = hour + ":" + min + ":" + sec

                
                self.labelBar.config(text = 'Autosaved ' + time_now + " " + self.fn)
                w.title(self.fn)
            else:
                self.saveFileAs()

        else:
           pass


    def newFolder(self):
        """
            Implements 'New Folder' functionality
        """
        folderName = simpledialog.askstring('New Folder', 'Set the folder name', initialvalue='', parent=self)
        if folderName is not None:
            self.executeCMD("mkdir " + folderName)
        else:
            pass


    def setFileName(self):
        """
            Implements 'Set File Name' functionality
        """
        self.fn = simpledialog.askstring('File name', 'Set the file name', initialvalue='', parent=self)
        w.title(self.fn)


    def changeFontSize(self):
        size = simpledialog.askstring('Font size', 'Set the size', initialvalue='', parent=self)
        #self.tb.config(font=("courier new", size))

        self.tb.config(font=(FONT_TYPE, size))

        # Fix for linenumbers reacting with delay
        self.linenumbers.redraw()


    def increaseFontSize(self):
        """
            Increase Font Size by 1 
        """
        self.defaultFontSize=self.defaultFontSize + 1
        # Can this be done without overwriting font type? font[1]=self.defaultFontSize ?
        self.tb.config(font=(FONT_TYPE, self.defaultFontSize ))
        self.linenumbers.redraw()


    def decreaseFontSize(self):
        """
            Decrease Font Size by 1 
        """
        self.defaultFontSize=self.defaultFontSize - 1
        self.tb.config(font=(FONT_TYPE, self.defaultFontSize ))
        self.linenumbers.redraw()


    def countLetters(self):
        """
            Implements 'Count Letters' functionality
        """
        lettersNumber = sum(c != ' ' for c in self.tb.get(1.0, END))
        lineNumber = int(self.tb.index('end').split('.')[0]) - 1  # returns line count
        self.labelBar.config(text = "Number of letters: " + str(lettersNumber-1) + " Number of lines: " + str(lineNumber))


    def insertDate(self):
        """
            Adds date signature in:
            dd/mm/yyyy format
        """
        full_date = time.localtime()
        day = str(full_date.tm_mday)
        month = str(full_date.tm_mon)
        year = str(full_date.tm_year)
        
        date = day + '/' + month + '/' + year
        self.tb.insert(1.0, date + '\n')
        self.labelBar.config(text = 'Date added')


    def insertSignature(self):
        """
            Adds signature from a text file
        """
        try:
            with open("signature.txt") as f:
                self.tb.insert(1.0, f.read() + '\n')

        except IOError:
            self.labelBar.config(text = SIGNATURE_TXT_NOT_FOUND_MESSAGE)


    def populateSnippet(self):
        """
            Adds snippets from a text file
        """
    
        if str(self.fn).lower().endswith('.py'):
            interpreter = "python3"

            snippetList = self.snippetListPython
            print(snippetList)

            for item in snippetList:
                snippetList.insert(END, item)


    def addSnippet(self, event):
        """
            Adds snippets from a text file
        """

        try:
            print(snippetList)
            self.tb.insert("insert", snippetList[0][1] + "\n" )

        except IOError:
            self.labelBar.config("Cant add")



    def _make_blanks(self, n):
        if True:
            ntabs, nspaces = divmod(n, 4)
            return '    ' * ntabs + ' ' * nspaces  #\t = 4 spaces
        else:
            return ' ' * n


    def classifyws(self, s, tabwidth):
        raw = effective = 0
        for ch in s:
            if ch == ' ':
                raw = raw + 1
                effective = effective + 1
            elif ch == '    ': #\t = 4 spaces
                raw = raw + 1
                effective = (effective // 4 + 1) * tabwidth
            else:
                break
        return raw, effective


    def indentRegion(self):
        """
            Adds 4 spaces at the beginning of each line
        """
        head, tail, chars, lines = self.getRegion()
        for pos in range(len(lines)):
            line = lines[pos]
            if line:
                raw, effective = self.classifyws(line, 4)
                effective = effective + 4
                lines[pos] = self._make_blanks(effective) + line[raw:]
        self.setRegion(head, tail, chars, lines)
        return "break"


    def dedentRegion(self):
        """
            Deletes 4 spaces at the beginning of each line
        """
        head, tail, chars, lines = self.getRegion()
        for pos in range(len(lines)):
            line = lines[pos]
            if line:
                raw, effective = self.classifyws(line, 4)
                effective = max(effective - 4, 0)
                lines[pos] = self._make_blanks(effective) + line[raw:]
        self.setRegion(head, tail, chars, lines)
        return "break"


    def getRegion(self):
        """
            Gets the content of the selected text area
        """
        text = self.tb
        first, last = self.getSelectionIndices()
        if first and last:
            head = self.tb.index(first + " linestart")
            tail = self.tb.index(last + "-1c lineend +1c")
        else:
            head = self.tb.index("insert linestart")
            tail = self.tb.index("insert lineend +1c")
        chars = self.tb.get(head, tail)
        lines = chars.split("\n")
        return head, tail, chars, lines


    def setRegion(self, head, tail, chars, lines):
        """
            Sets the content of the selected text area
        """
        text = self.tb
        newchars = "\n".join(lines)
        if newchars == chars:
            text.bell()
            return
        self.tb.tag_remove("sel", "1.0", "end")
        self.tb.mark_set("insert", head)
        self.tb.delete(head, tail)
        self.tb.insert(head, newchars)
        self.tb.tag_add("sel", head, "insert")


    def getSelectionIndices(self):
        try:
            first = self.tb.index("sel.first")
            last = self.tb.index("sel.last")
            return first, last
        except TclError:
            return None, None


    def commentRegion(self):
        """
            Commenting out region for Python
            adds ## at the beginning of each line
            ##comment
        """
        head, tail, chars, lines = self.getRegion()

        for pos in range(len(lines) - 1):
            line = lines[pos]
            lines[pos] = '##' + line
        self.setRegion(head, tail, chars, lines)
        return "break"


    def commentRegionHTML(self):
        """
            Commenting out region for HTML
            <!-- comment -->
        """
        head, tail, chars, lines = self.getRegion()

        for pos in range(len(lines) - 1):
            line = lines[pos]
            lines[pos] = '<!--' + line + '-->'

        self.setRegion(head, tail, chars, lines)
        return "break"


    def commentRegionTraditional(self):
        """
            Traditional Commenting out region
            /*comment*/
        """
        head, tail, chars, lines = self.getRegion()

        print(head)
        print(tail)
        print(chars)
        print(lines)

        for pos in range(len(lines)-1):
            line = lines[pos]
            lines[0] = '/*' + '\n'
            lines[pos] = str(pos) + line
            lines[-1] = '*/'

        self.setRegion(head, tail, chars, lines)
        return "break"

    
    def uncommentRegion(self):
        """
            Uncommenting region for Python
            removes ## at the beginning of line
        """
        head, tail, chars, lines = self.getRegion()

        for pos in range(len(lines)):
            line = lines[pos]
            if not line:
                continue
            if line[:2] == '##':
                line = line[2:]
            elif line[:1] == '#':
                line = line[1:]
            lines[pos] = line
        self.setRegion(head, tail, chars, lines)
        return "break"


##    def checkFileExtension(self):
##        if self.fn is None:
##            return ('All files', '*')
##
##        elif str(self.fn).lower().endswith(".py"):
##            return ('Python code files', '*.py')
##
##        elif str(self.fn).endswith(".java"):
##            return ".java"
##
##        elif str(self.fn).lower().endswith(".r"):
##            return ".r"


    def changeColorScheme(self):
        """
            Defining new Text widget to get new color scheme
        """
        pass


    def popup(self):
        self.w=popupWindow(self.master)
        #self.b["state"] = "disabled" 
        #self.master.wait_window(self.w.top)
        #self.b["state"] = "normal"


    def entryValue(self):
        return self.w.value


    def find(self):
        """
            'Searching' functionality
        """
        # Remove found tag
        self.tb.tag_remove('found', '1.0', END)
        # Search for word

        #focus on top

        search = self.cmdLine.get("1.0", "end-1c")

        if search == "":
            self.labelBar.config(text = "Nothing to look for. Type search first!")
            # set focus to commandLine if it is empty
            self.cmdLine.focus_set()
            return

        else:

            list_of_words = re.findall(r"\b" + search + r"\b", self.tb.get(1.0, END))

            # If list of words is empty
            if not list_of_words:
                self.labelBar.config(text = "Found 0 results while looking for: \"" + search + "\"")       
            else:
                self.labelBar.config(text = ("Found: " + str(len(list_of_words)) + " results while looking for: \"" + search + "\"") )
                
            
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


    def executeInTerminal(self, event):
        """
            Execute Commandline in a Terminal
        """
        queue = self.cmdLine.get("1.0", "end-1c")
        process = subprocess.Popen(queue, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the process to terminate
        out, err = process.communicate()
        errcode = process.returncode

        self.terminal.insert(1.0, out)
        self.terminal.insert(1.0, err)

        self.cmdLine.delete("1.0", "end-1c") # Remove executed line
        return "break"


    def runCode(self):
        """
            Save the current file and try to run the code in a Terminal
        """

        self.terminal.tag_config('error', foreground=TEXT_ERROR_COLOR_FOREGROUND)

        # Save file
        # If already exists
        if (self.fn):
            self.saveFile()

        # If not, create new file
        else:
            self.saveFileAs()

        # If file has no name
        if not self.fn:
            return

        compiler = None
        
        # Check file type
        if str(self.fn).lower().endswith('.py'):
            interpreter = "python3"

        elif str(self.fn).lower().endswith('.java'):
            compiler = "javac"
            interpreter = "java"

        elif str(self.fn).lower().endswith('.r'):
            interpreter = "Rscript"

        elif str(self.fn).lower().endswith('.cs'):
            interpreter = "mcs"

        elif str(self.fn).lower().endswith('.scala'):
            compiler = "scalac"
            interpreter = "scala"

        elif str(self.fn).lower().endswith('.txt'):
            pass

        else:
            interpreter = simpledialog.askstring('Set Interpreter', 'Set the interpreter to run the code', initialvalue='', parent=self)


        # Clear terminal on new run
        if self.new_run_clean_terminal.get() == True:
            self.clearTerminal()
  
        else:
            pass

        if  self.show_terminal.get() == False:

            self.show_terminal.set(True)
            self.cmdLine.grid()
            self.terminal.grid()

        else:
            pass


        #self.labelBar.config(text = 'Running ' + str(self.fn) )
        
##        process = subprocess.Popen((interpreter + " " + self.fn), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
##        startTime = datetime.now()
##        # wait for the process to terminate
##        out, err = process.communicate()
##        errcode = process.returncode
##
##
##        if str(self.fn).lower().endswith('.cs'):
##            compiledFile = os.path.splitext(self.fn)[0]+'.exe'
##            self.executeCMD("." + compiledFile)


        #if str(self.fn).lower().endswith('.scala'):

##        if compiler is None:
##            pass
##
##        else:

##            process = subprocess.Popen((compiler + " " + self.fn), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
##            out, err = process.communicate()
##            errcode = process.returncode
##
##            self.terminal.insert(END, out)
##            self.terminal.insert(END, err)
##            self.terminal.insert(END, self.fn + " compiled")
##            self.terminal.see("insert")
##            self.tb.focus_set()

        if str(self.fn).lower().endswith('.scala'):
            print(compiler)
            print(interpreter)
            file = os.path.basename(self.fn)

            self.executeCMD("scalac " + file)
            self.terminal.insert(END, "compiled")
            
            compiledFile = os.path.splitext(file)[0]
            self.executeCMD("scala " + compiledFile)
            self.terminal.insert(END, "executed")


        interpreter = simpledialog.askstring('Set Interpreter', 'Set the interpreter to run the code', initialvalue='', parent=self)



            #process = subprocess.Popen((compiler + " " + self.fn), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
##            out, err = process.communicate()
##            errcode = process.returncode

##            self.terminal.insert(END, out)
##            self.terminal.insert(END, err)
##            self.terminal.insert(END, self.fn + " compiled")
##            self.terminal.see("insert")
##            self.tb.focus_set()

##            compiledFile = os.path.splitext(self.fn)[0]
##            print(compiledFile)
##
        process = subprocess.Popen((interpreter + " " + self.fn), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        errcode = process.returncode

        self.terminal.insert(END, out)
        self.terminal.insert(END, err)
        self.terminal.see("insert")
        self.tb.focus_set()





##        # Show terminal exit codes
##        if self.show_terminal_exit_codes.get() == True:
##
##            self.terminal.insert(END, "-----------------------" + "\n")
##            self.terminal.insert(END, "Executed in: " + str(datetime.now() - startTime) + "\n")
##            self.terminal.insert(END, "Terminated with code: " + str(errcode) + "\n")        
##        else:
##            pass
##
##        self.terminal.insert(END, out)
##        self.terminal.insert(END, err)
##        self.terminal.see("insert")
##        #self.labelBar.config(text = 'Terminated run of ' + compiledFile)
##        self.tb.focus_set()


    def runCodeInSystemTerminal(self):
        """
            Save the current file and run the code in a new System Terminal Window
        """

        interpreter = simpledialog.askstring('Set Interpreter', 'Set the interpreter to run the code', initialvalue='', parent=self)
        
        if interpreter and SYSTEMTYPE == 'Linux':
            print("chmod +x " + self.fn)
            self.executeCMD("chmod +x " + self.fn)
            subprocess.Popen('xterm -hold -T {title} -e {intrp} {fn}'''.format(intrp=interpreter, fn=self.fn, title="Run"), shell=True)

        elif interpreter and SYSTEMTYPE == 'Windows':
            subprocess.Popen('cmd.exe /K /u {intrp} {fn}'.format(intrp=interpreter, fn=self.fn), shell=True)


    def highlightCurrentLine(self, delay=8):
        """
            Highlighting line that moves with the cursor
        """
        # delay=8 (8 is a maximum value (time) without having to experience lag when scrolling down/up (like 9, 10 etc)

        if self.highlight_current_line.get() == True:

            def delayedHighlightCurrentLine():
                self.tb.tag_remove('currentLine', 1.0, "end")
                self.tb.tag_add('currentLine', 'insert linestart', 'insert lineend+1c')
            # This bound function is called before the cursor actually moves.
            # So delay checking the cursor position and moving the highlight 8 ms (time).

            self.after(delay, delayedHighlightCurrentLine)

        else:
            self.tb.tag_remove('currentLine', 1.0, "end")


    def balance(self, myStr):
        openList = ["[","{","("]
        closeList = ["]","}",")"]
        stack = []
        for bracket in myStr:
            if bracket in openList:
                stack.append(bracket)

            elif bracket in closeList:
                pos = closeList.index(bracket)
                if ((len(stack) > 0) and (openList[pos] == stack[len(stack)-1])):
                    stack.pop()
                else:
                    return "Unbalanced"
                    
        if len(stack) == 0:
            return "Balanced"

    #self.tb.tag_remove('', '1.0', END)
    #self.tb.tag_configure('matchingBracket', background='white')
    

    def balanceBrackets(self):

        strToBalance = "((( )))"
        self.balance(strToBalance)


    def syntaxHighlighting(self):
        """
            Enable highlighting
        """
        if self.syntax_highlighting.get() == True:
            self.create_tags()
            self.all_highlight()

        else:
            self.remove_tags()


    def create_tags(self):
        """
            Create tags and colors for highlighting
        """

        #https://stackoverflow.com/questions/32058760/improve-pygments-syntax-highlighting-speed-for-tkinter-text

        self.tb.tag_configure('Token.Keyword', foreground='#93C763')  # def class if for else return pass with try except finally print
        self.tb.tag_configure('Token.Keyword.Namespace', foreground='#93C763')  # from import
        self.tb.tag_configure('Token.Name.Decorator', foreground='#CC7A00')  # @deco
        self.tb.tag_configure('Token.Operator.Word', foreground='#93C763')  # and, in

        self.tb.tag_configure('Token.Name.Namespace', foreground='#885EAD')  # import a (color of import)
        self.tb.tag_configure('Token.Name.Class', foreground='#678CB1')  # name of the class
        self.tb.tag_configure('Token.Name.Exception', foreground='#FB0000')  # Error name
        self.tb.tag_configure('Token.Name.Function', foreground='#678CB1')  # Function name
        self.tb.tag_configure('Token.Name.Function.Magic', foreground='#678CB1')  # __init__
        self.tb.tag_configure('Token.Name.Builtin', foreground='#E0E2E4')  # len range input enumerate dir
        self.tb.tag_configure('Token.Name.Builtin.Pseudo', foreground='#E0E2E4')  # self cls

        self.tb.tag_configure('Token.Literal.String.Doc', foreground='#EC7600')  # """docstring"""
        self.tb.tag_configure('Token.Literal.String.Double', foreground='#EC7600')  # string
        self.tb.tag_configure('Token.Literal.String.Single', foreground='#EC7600')  # string

        self.tb.tag_configure('Token.Comment.Single', foreground='#66747B')  # commment
        self.tb.tag_configure('Token.Literal.Number.Integer', foreground='#E0E2E4')  # 1 2 numbers
        self.tb.tag_configure('Token.Literal.String.Escape', foreground='#E0E2E4')  # \t \n
        self.tb.tag_configure('Token.Operator', foreground='#E0E2E4')  # . + - / * == =

        self.tb.tag_configure('Token.Punctuation', foreground='#E0E2E4')  # : [] () {} ,
        self.tb.tag_configure('Token.Name', foreground='#E0E2E4')  # Variable name etc.


    def remove_tags(self):
        """
            Remove tags and colors for highlighting
        """
        for tag in self.tb.tag_names():
            self.tb.tag_remove(tag, '1.0', 'end')


    def all_highlight(self, event=None):
        """
            Highlight All Text
        """
        # Retrieve all text
        src = self.tb.get('1.0', 'end - 1c')

        # Cancel all highlights once
        for tag in self.tb.tag_names():
            self.tb.tag_remove(tag, '1.0', 'end')

        # Highlight
        self._highlight('1.0', src)


    def line_highlight(self, event=None):
        """
            Highlight only the current line
        """
        start = 'insert linestart'
        end = 'insert lineend'

        # Retrieve the text of the current line
        src = self.tb.get(start, end)

        # Remove line highlighting
        for tag in self.tb.tag_names():
            self.tb.tag_remove(tag, start, end)

        # Highlight
        self._highlight(start, src)


    def checkLexerType(self):
        global LEXER_TYPE
        # http://pygments.org/docs/lexers/
        from pygments.lexers import TextLexer
        LEXER_TYPE = TextLexer()

        print("checked for lexer")
        
        if str(self.fn).lower().endswith('.py'):
            from pygments.lexers import PythonLexer
            LEXER_TYPE = PythonLexer()
            
        elif str(self.fn).lower().endswith('.java'):
            from pygments.lexers import JavaLexer
            LEXER_TYPE = JavaLexer()

        elif str(self.fn).lower().endswith('.r'):
            # *.S, *.R, .Rhistory, .Rprofile, .Renviron
            from pygments.lexers import SLexer
            LEXER_TYPE = SLexer()

        elif str(self.fn).lower().endswith('.cs'):
            from pygments.lexers import CSharpLexer
            LEXER_TYPE = CSharpLexer()

        elif str(self.fn).lower().endswith('.html'):
            from pygments.lexers import HtmlLexer
            LEXER_TYPE = HtmlLexer()

        elif str(self.fn).lower().endswith('.scala'):
            from pygments.lexers import ScalaLexer
            LEXER_TYPE = ScalaLexer()

        elif str(self.fn).lower().endswith(('.sas', '.SAS')):
            from pygments.lexers import SASLexer
            LEXER_TYPE = SASLexer()


    def _highlight(self, start, src):
        """
            Highlighting
        """
        self.tb.mark_set('range_start', start)

        global LEXER_TYPE
        
        for token, content in lex(src, LEXER_TYPE ): # i.e PythonLexer()
            self.tb.mark_set(
                'range_end', 'range_start+{0}c'.format(len(content))
            )
            self.tb.tag_add(str(token), 'range_start', 'range_end')
            self.tb.mark_set('range_start', 'range_end')


    def gotoTOP(self):
        """
            Jump to the top of file
        """
        self.tb.mark_set("insert", 1.0)
        self.tb.see("insert")
        self.tb.focus_set()
        return "break"


    def gotoEND(self):
        """
            Jump to the end of file
        """
        self.tb.mark_set("insert", END)
        self.tb.see("insert")
        self.tb.focus_set()
        return "break"


    def gotoLine(self):
        """
            Jump to the given line
        """
        lineNum = simpledialog.askstring('Goto Line', 'Set the line number', initialvalue='', parent=self)

        if lineNum is not None:
            self.tb.mark_set("insert", float(lineNum))
            self.tb.see("insert")
            self.tb.focus_set()

            # Show selection on given line
            EOL = str(self.tb.index(tk.INSERT)) + " lineend"
            self.tb.tag_add(SEL, float(lineNum), EOL )
        else:
            pass

        return "break"


    def gotoStartOfLine(self):
        """
            Jump to the Start Of Line
        """
        SOL = str(self.tb.index(tk.INSERT)) + " linestart"
        self.tb.mark_set("insert", SOL)
        self.tb.see("insert")
        self.tb.focus_set()
        

    def gotoEndOfLine(self):
        """
            Jump to the End Of Line
        """
        EOL = str(self.tb.index(tk.INSERT)) + " lineend"
        self.tb.mark_set("insert", EOL)
        self.tb.see("insert")
        self.tb.focus_set()


    def selectLines(self):
        """
            Select given lines
        """
        startLineNum = simpledialog.askstring('Goto Line', 'Set the line number', initialvalue='', parent=self)
        endLineNum = simpledialog.askstring('Goto Line', 'Set the line number', initialvalue='', parent=self)

        if startLineNum is not None and endLineNum is not None:
            self.tb.mark_set("insert", float(startLineNum))
            self.tb.see("insert")
            self.tb.focus_set()

            # Show selection on given line
            #EOL = str(self.tb.index(tk.INSERT)) + " lineend"
            
            self.tb.tag_add(SEL, float(startLineNum), float(endLineNum) )
        else:
            pass

        return "break"


    def tab2spaces4(self, event):
        """
            Replacing tabs with 4 spaces

            Callback for the indentation key (Tab Key) in the editor widget. 
            Event: '<Tab>'
        """
        self.tb.insert(self.tb.index("insert"), "    ")
        return "break"


    def smartReturn(self, event):
        """
            Auto adding 4 spaces when hitting Return Key
            Callback for the Return Key in the editor widget.
            Event: '<Return>'
        """
        indentation = ""
        lineindex = self.tb.index("insert").split(".")[0]
        linetext = self.tb.get(lineindex + ".0", lineindex + ".end")

        for character in linetext:
            if character in [" ", "\t"]:
                indentation += character
            else:
                break
                
        self.tb.insert(self.tb.index("insert"), "\n" + indentation)
        return "break"


    def showDirectoryBrowser(self):
        if self.show_directory_browser.get() == True:
            #self.db.grid()
            self.db.grid(column=0,row=0, sticky=N+S+E+W)
            self.labelBar.config(text = "Directory browser enabled")

        else:

            self.db.grid_remove()
            self.labelBar.config(text = "Directory browser disabled")


    def showTerminal(self):
        """
            Shows / Hides the Terminal
        """
        if self.show_terminal.get() == True:

            #self.cmdLine.grid()
            #self.terminal.grid()
            self.cmdLine.grid(column=4, row=1, sticky=N+E+S+W)
            self.terminal.grid(column=4, row=0, sticky=N+E+S+W)
            
            self.grid_columnconfigure(2, weight=1)
            self.grid_columnconfigure(4, weight=3)
            self.labelBar.config(text = "Terminal enabled")
            
        else:
            self.cmdLine.grid_remove()
            self.terminal.grid_remove()
            self.grid_columnconfigure(2, weight=1)
            self.grid_columnconfigure(4, weight=0)
            self.labelBar.config(text = "Terminal disabled")


    def showSystemTerminal(self):
        """
            Shows / Hides System Terminal
        """
        if self.show_system_terminal.get() == True:
            self.systemTerminal.grid(column=4, row=0, sticky=N+E+S+W)

        else:
            self.systemTerminal.grid_remove()
            


    def showSnippetList(self):
        """
            Shows / Hides Snippets List
        """
        if self.show_snippet_list.get() == True:
            #self.snippetList.grid()
            self.snippetList.grid(column=0, row=0, sticky=N+S+E+W)
            self.labelBar.config(text = "Snippet List enabled")

            self.populateSnippet
            
        else:
           self.snippetList.grid_remove()
           self.labelBar.config(text = "Snippet List disabled")


    def showLabelBar(self):
        """
            Shows / Hides bottom bar
        """
        if self.show_label_bar.get() == True:
            #self.labelBar.grid()
            self.labelBar.grid(column=2, row=1,sticky=N+S+E+W)
            
        else:
           self.labelBar.grid_remove()

    def showScrollBar(self):

        if self.show_scroll_bar.get() == True:
            self.vsb.grid(column=3, row=0, sticky=N+E+S+W)
            #self.vsb.grid()
            
        else:
           self.vsb.grid_remove()


    #############################################################################
    # Terminal commands
    #############################################################################

    def clearTerminal(self):
        """
            Clears the terminal
        """
        self.terminal.delete(1.0, END)


    def logTerminal(self, msg):
        self.terminal.insert(1.0, msg)


    def executeCMD(self, queue):
        """
            Execute given line in a Terminal
        """
        
        process = subprocess.Popen(queue, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Wait for the process to terminate
        out, err = process.communicate()
        errcode = process.returncode
        #print(out)
        #print(err)

        #moze dac jakis zielony kolor dla gita w terminalu?
        self.terminal.insert(1.0, out)
        self.terminal.insert(1.0, err)

    #############################################################################
    # Git commands
    #############################################################################


#1. Create a "repository" (project) with a git hosting tool (like Bitbucket)
#2. Copy (or clone) the repository to your local machine
#3. Add a file to your local repo and "commit" (save) the changes
#4. "Push" your changes to your master branch
#5. Make a change to your file with a git hosting tool and commit
#6. "Pull" the changes to your local machine
#7. Create a "branch" (version), make a change, commit the change
#8. Open a "pull request" (propose changes to the master branch)
#9. "Merge" your branch to the master branch



##Connect - From the Team Explorer section, click the Connect... button in the GitHub invitation section to
#login to the extension. The extension supports two-factor authentication (2fa) with GitHub and
#stores credentials in the Windows Credential store so that Git Operations within Visual Studio work with
#your GitHub repositories. The extension also supports logging into a GitHub Enterprise instance.

##Clone - Once connected, click on the Clone button to list all repositories that you have access to on GitHub.
##Create - The create dialog lets you create a repository on GitHub.com and locally that are connected together.
##Publish - For a local-only repository, click on the Sync navigation item to get the GitHub publish control. This make it quick to publish your local work up to GitHub.
##Open in Visual Studio - once you log-in with the extension, GitHub.com will show a new button next to repositories labeled "Open in VisualStudio." Click on the button to clone the repository to Visual Studio.
##Create Gist - Create gists by using the GitHub context menu when you right-click on selected text
##Open/Link to GitHub - Easily open on GitHub or share a link to the code you're working on by using the GitHub context menu.
##Pull Requests - View your repository's Pull Requests and create new ones from the Pull Requests button in the Team Explorer Home
##See Pull Request diffs - See all Pull Request changes as individual diff views and open changed files directly from the Pull Request details view
##Review Pull Requests - Start a review and submit a review that comments, approves, or request changes to the Pull Request
##Inline Comments - Add review comments to the Pull Request changes you're reviewing directly from the VS diff view
##Fork - From Team Explorer Home, fork a repository you have already cloned.




        

    def gitVersion(self):
        """
            Check git version

            git --version

        """
        self.executeCMD("git --version")


    def gitInit(self):
        """
            Create a new local repository
            git init

        """
        global repositoryFolder

        repositoryFolder = simpledialog.askstring('Git', 'Set the repository name', initialvalue='', parent=self)

        self.executeCMD("git init " + repositoryFolder)


    def gitClone(self):
        """
            Clone the repository
            git clone

        """

        global repositoryFolder
    
        repositoryFolder = simpledialog.askstring('Set folder name', 'Set the folder project name', initialvalue='', parent=self)

        if repositoryFolder is not None:
            self.executeCMD("mkdir " + repositoryFolder)

        else:
            pass
         

        with CD(repositoryFolder):

            repositoryAddres = simpledialog.askstring('Git Clone', 'Set the address', initialvalue='https://github.com/username/username.github.io', parent=self)
            self.executeCMD("git clone " + repositoryAddres)

            # https://github.com/mikazz/RSnippets.git

            global repositoryName
            repositoryName = RSnippets

            logTerminal(msg="Done")  
        
        
    def gitAdd(self):

        global repositoryFolder
        print(repositoryFolder)

        with CD(repositoryFolder):

            self.saveFileAs

            self.executeCMD("git add --all")

            #self.executeCMD("touch " + self.fn)
            
            #process = subprocess.call("ls")

            #out, err = process.communicate()
            #errcode = process.returncode
            #print(out)
            #print(errcode)
        
        
    def gitCommit(self):
        """
            Commit changes to head (but not yet to the remote repository)
            git init

        """
        global repositoryFolder

        with CD(repositoryFolder):

            commitMessage = simpledialog.askstring('Git', 'Set the commit message', initialvalue='', parent=self)
            self.executeCMD("git commit -m " + str("\"" + commitMessage + "\"" ) )


    def gitPush(self):
        """
            Send changes to the master branch of your remote repository
            git push origin master

        """
        global repositoryFolder

        with CD(repositoryFolder):
            self.executeCMD("git push origin master")


    def __init__(self):
        Tk.__init__(self)

        #self.bind("<Key>", self.key)
        #self.bind("<Button-1>", self.callback)

        # Set default File name to None
        self.fn = None

        ################################################ Styles

        style = ttk.Style()
        style.theme_use('clam')
        
        ################################################ Main Menu Bar
        # http://effbot.org/tkinterbook/menu.htm#menu.Menu.add-method
        
        menubar = Menu(self,
                       background=TOPBAR_BACKGROUND_COLOR,
                       foreground=TOPBAR_FOREGROUND_COLOR,
                       activeforeground=TOPBAR_ACTIVE_FOREGROUND_COLOR,
                       activebackground=TOPBAR_ACTIVE_BACKGROUND_COLOR,
                       bd=0)

        # Creates a pulldown menus, and adds them to the main menu bar

        # Show File pulldown menu
        main_menu = Menu(menubar,
                         tearoff=0,
                         background=PULLDOWN_BACKGROUND_COLOR,
                         foreground=PULLDOWN_FOREGROUND_COLOR,
                         activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR,
                         activebackground=PULLDOWN_BACKGROUND_COLOR,
                         bd=0)

        main_menu.add_command(label="New", command=self.newFile, accelerator="Ctrl+N")
        self.bind('<Control-Key-n>', lambda e: self.newFile())
        self.bind('<Control-Key-N>', lambda e: self.newFile())


        # Add newFileWithTemplateMenu pulldown menu
        self.newFileWithTemplateMenu = Menu(self, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR,  activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_BACKGROUND_COLOR, bd=0)
        main_menu.add_cascade(label="New With Template", command=self.newFileWithTemplateMenu)

        self.newFileWithTemplateMenu.add_command(label="Python", command=self.newFileWithTemplate)

##        self.recentMenu = Menu(self, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR,  activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_BACKGROUND_COLOR, bd=0)
##        main_menu.add_cascade(label="Open Recent", menu=self.recentMenu)




        
        main_menu.add_command(label="Open", command=self.openFile, accelerator="Ctrl+O")
        self.bind('<Control-Key-o>', lambda e: self.openFile())
        self.bind('<Control-Key-O>', lambda e: self.openFile())


        # Add options for openRecent pulldown menu
        self.recentMenu = Menu(self, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR,  activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_BACKGROUND_COLOR, bd=0)
        main_menu.add_cascade(label="Open Recent", menu=self.recentMenu)


        main_menu.add_command(label="Reload File", command=self.reloadFile)
        
        main_menu.add_command(label="Append From File", command=self.appendFromFile)

        main_menu.add_separator()

        main_menu.add_command(label="Save", command=self.saveFile, accelerator="Ctrl+S")
        self.bind('<Control-Key-s>', lambda e: self.saveFile())
        self.bind('<Control-Key-S>', lambda e: self.saveFile())

        main_menu.add_command(label="Save As", command=self.saveFileAs, accelerator="Ctrl+Shift+S")
        self.bind('<Control-Shift-Key-s>', lambda e: self.saveFileAs())
        self.bind('<Control-Shift-Key-S>', lambda e: self.saveFileAs())

        main_menu.add_command(label="New Folder", command=self.newFolder)

        main_menu.add_command(label="Set File Name", command=self.setFileName)

        main_menu.add_separator()
        
        main_menu.add_command(label="Print", command=self.printCurrent, accelerator="Ctrl+P")
        self.bind('<Control-Key-p>', lambda e: self.printCurrent())
        self.bind('<Control-Key-P>', lambda e: self.printCurrent())

        main_menu.add_separator()

        main_menu.add_command(label="New Window", command=self.newWindow)

        main_menu.add_command(label="Quit", command=self.exitCommand, accelerator="Ctrl+Q")
        self.bind('<Control-Key-q>', lambda e: exitCommand())
        self.bind('<Control-Key-Q>', lambda e: exitCommand())
        
        menubar.add_cascade(label="File", menu=main_menu)


        # Show Edit pulldown menu        
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR,  activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_BACKGROUND_COLOR, bd=0)

        main_menu.add_command(label="Run Code", command=self.runCode, accelerator="Ctrl+R")
        self.bind('<Control-Key-r>', lambda e: self.runCode())
        self.bind('<Control-Key-R>', lambda e: self.runCode())

        main_menu.add_command(label="Run Code in System Terminal", command=self.runCodeInSystemTerminal)

        main_menu.add_command(label="Find", command=self.find, accelerator="Ctrl+F")
        self.bind('<Control-Key-f>', lambda e: self.find())
        self.bind('<Control-Key-F>', lambda e: self.find())
        
        #main_menu.add_command(label="Find and Replace", command=self.findAndReplace)

        main_menu.add_command(label="Count Letters", command=self.countLetters)

        main_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        self.bind('<Control-Key-y>', lambda e: self.redo())
        self.bind('<Control-Key-Y>', lambda e: self.redo())
        
        main_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        self.bind('<Control-Key-z>', lambda e: self.undo())
        self.bind('<Control-Key-Z>', lambda e: self.undo())

        main_menu.add_command(label="Select All", command=self.selectAll, accelerator="Ctrl+A")
        self.bind('<Control-Key-a>', lambda e: self.selectAll())
        self.bind('<Control-Key-A>', lambda e: self.selectAll())

        main_menu.add_command(label="Indent region", command=self.indentRegion, accelerator="Ctrl+]")
        self.bind('<Control-Key-bracketright>', lambda e: self.indentRegion())

        main_menu.add_command(label="Dedent region", command=self.dedentRegion, accelerator="Ctrl+[")
        self.bind('<Control-Key-bracketleft>', lambda e: self.dedentRegion())

        main_menu.add_command(label="Comment Out Region", command=self.commentRegion)
        main_menu.add_command(label="Uncomment Region", command=self.uncommentRegion)


        main_menu.add_command(label="Comment Out HTML", command=self.commentRegionHTML)
        main_menu.add_command(label="Comment Out Traditional", command=self.commentRegionTraditional)


        menubar.add_cascade(label="Edit", menu = main_menu)


        # Show Options pulldown menu
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR,  activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_BACKGROUND_COLOR, bd=0)

        self.always_on_top = BooleanVar() # True/False option for always on top
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="Always on top", onvalue=True, offvalue=False, variable=self.always_on_top, command=self.topWindow)

        self.syntax_highlighting = BooleanVar() # True/False option for syntax highlighting
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="Syntax Highligthing", onvalue=True, offvalue=False, variable=self.syntax_highlighting, command=self.syntaxHighlighting)


        self.highlight_current_line = BooleanVar() # True/False option for word_wrap
        self.highlight_current_line.set(False)  # Default value
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="Highlight Current Line", onvalue=True, offvalue=False, variable=self.highlight_current_line, command=self.highlightCurrentLine)


        self.word_wrap = BooleanVar() # True/False option for word_wrap
        self.word_wrap.set(False)  # Default value
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="Word Wrap", onvalue=True, offvalue=False, variable=self.word_wrap, command=self.wordWrap)

        self.auto_save = BooleanVar() # True/False option for auto_save
        self.auto_save.set(False)  # Default value
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="AutoSave", onvalue=True, offvalue=False, variable=self.auto_save, command=self.autoSave)

        main_menu.add_command(label="Colorscheme", command=self.changeColorScheme)
        main_menu.add_command(label="Change Working Directory", command=self.getWorkingDirectory)

        main_menu.add_command(label="REFRESH DIRECTORY", command=self.refresh)

        main_menu.add_command(label="Populate Snippet List", command=self.populateSnippet)

        main_menu.add_command(label="Dialog test", command=self.showDialog)

        main_menu.add_command(label="Settings", command=self.showSettings)

        main_menu.add_command(label="Change Font Size", command=self.changeFontSize)

        #main_menu.add_command(label="Fullscreen", command=self.fullscreen)
        self.enable_fullscreen = BooleanVar() # True/False option for word_wrap
        self.enable_fullscreen.set(False)  # Default value
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="Fullscreen", onvalue=True, offvalue=False, variable=self.enable_fullscreen, command=self.fullscreen)

        main_menu.add_command(label="Increase Font Size", command=self.increaseFontSize, accelerator="Ctrl+Plus")
        self.bind('<Control-Key-plus>', lambda e: self.increaseFontSize())
        #self.bind('<Button-4>', lambda e: self.increaseFontSize())
        #self.bind('<Control-Key>', lambda e: self.increaseFontSize())

        main_menu.add_command(label="Decrease Font Size", command=self.decreaseFontSize, accelerator="Ctrl+Minus")
        self.bind('<Control-Key-minus>', lambda e: self.decreaseFontSize())
        #self.bind('<Button-5>', lambda e: self.decreaseFontSize())
        #self.bind('<Control-Key>', lambda e: self.decreaseFontSize())

        menubar.add_cascade(label="Options", menu=main_menu)

        # Show Insert pulldown menu
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR,  activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_BACKGROUND_COLOR, bd=0)
        main_menu.add_command(label="Insert Date", command=self.insertDate)
        main_menu.add_command(label="Insert Signature", command=self.insertSignature)


        menubar.add_cascade(label="Insert", menu=main_menu)


        # Show View pulldown menu
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR,  activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_BACKGROUND_COLOR, bd=0)
        main_menu.add_command(label="Goto TOP", command=self.gotoTOP)
        main_menu.add_command(label="Goto END", command=self.gotoEND)
        main_menu.add_command(label="Goto Line", command=self.gotoLine)
        
        main_menu.add_command(label="Goto End Of Line", command=self.gotoEndOfLine, accelerator="Ctrl+RIGHT")
        self.bind('<Control-Key-Right>', lambda e: self.gotoEndOfLine())

        main_menu.add_command(label="Goto Start Of Line", command=self.gotoStartOfLine, accelerator="Ctrl+LEFT")
        self.bind('<Control-Key-Left>', lambda e: self.gotoStartOfLine())
        
        main_menu.add_command(label="Select Lines", command=self.selectLines)

        
        menubar.add_cascade(label="View", menu=main_menu)

        
        # Show Terminal pulldown menu
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR,  activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_BACKGROUND_COLOR, bd=0)

        main_menu.add_command(label="Clear Terminal", command=self.clearTerminal, accelerator="Ctrl+Del")
        self.bind('<Control-Key-Delete>', lambda e: self.clearTerminal())

        self.new_run_clean_terminal = BooleanVar() # True/False option for cleaning terminal on run
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="Clear Terminal on run", onvalue=True, offvalue=False, variable=self.new_run_clean_terminal)

        self.show_terminal_exit_codes = BooleanVar() # True/False option for showing exit codes
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="Show Exit Codes", onvalue=True, offvalue=False, variable=self.show_terminal_exit_codes)

        menubar.add_cascade(label="Terminal", menu=main_menu)


        # Show Window pulldown menu
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR,  activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_BACKGROUND_COLOR, bd=0)

        self.show_terminal = BooleanVar() # True/False option for showing terminal
        self.show_terminal.set(False)  # Default value
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="Show Terminal", onvalue=True, offvalue=False, variable=self.show_terminal, command=self.showTerminal)

        self.show_system_terminal = BooleanVar() # True/False option for showing system terminal
        self.show_system_terminal.set(False)  # Default value
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="Show System Terminal", onvalue=True, offvalue=False, variable=self.show_system_terminal, command=self.showSystemTerminal)

        self.show_directory_browser = BooleanVar() # True/False option for showing browser directory 
        self.show_directory_browser.set(False) # Default value
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="Show Directory Browser", onvalue=True, offvalue=False, variable=self.show_directory_browser, command=self.showDirectoryBrowser) #, accelerator="Ctrl+2"
        
        self.show_snippet_list = BooleanVar()
        self.show_snippet_list.set(False)  # Default value
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="Show Snippet List", onvalue=True, offvalue=False, variable=self.show_snippet_list, command=self.showSnippetList)
        
        self.show_label_bar = BooleanVar()
        self.show_label_bar.set(True)  # Default value
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="Show Bottom Bar", onvalue=True, offvalue=False, variable=self.show_label_bar, command=self.showLabelBar)

        self.show_scroll_bar = BooleanVar()
        self.show_scroll_bar.set(True)  # Default value
        main_menu.add_checkbutton(selectcolor=CHECKBUTTON_SELECT_COLOR, label="Show Scroll Bar", onvalue=True, offvalue=False, variable=self.show_scroll_bar, command=self.showScrollBar)
        menubar.add_cascade(label="Window", menu=main_menu)


        # Show Git pulldown menu
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR, activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_BACKGROUND_COLOR, bd=0, relief='flat')
        main_menu.add_command(label="Version", command=self.gitVersion)
        main_menu.add_command(label="Clone repository", command=self.gitClone)
        main_menu.add_command(label="Initialize empty repository", command=self.gitInit)
        main_menu.add_command(label="Add current file", command=self.gitAdd)
        main_menu.add_command(label="Commit changes", command=self.gitCommit)
        main_menu.add_command(label="Push changes to master branch", command=self.gitPush)
        menubar.add_cascade(label="Git", menu=main_menu)


        #ttk.Style().configure("Black.TMenubutton",fill="white", border=0, relief="flat", font=('Helvetica', 8), background=DIRECTORY_BROWSER_COLOR_BACKGROUND, foreground=DIRECTORY_BROWSER_COLOR_FOREGROUND,highlightthickness=0,highlightcolor="black")

        # Show Help pulldown menu        
        main_menu = Menu(menubar, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR, activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_BACKGROUND_COLOR, bd=0, relief='flat')

        main_menu.add_command(label="Readme", command=self.readme, hidemargin=True)
        main_menu.add_command(label="About", command=self.about)
        menubar.add_cascade(label="Help", menu=main_menu)




        # Display the menu
        self.config(menu=menubar)



        #ttk.Style.theme_use('clam')


                ##('orient',
                ## 'background',
                ## 'bordercolor',
                ## 'troughcolor',
                ## 'lightcolor',
                ## 'darkcolor',
                ## 'arrowcolor',
                ## 'arrowsize',
                ## 'gripcount',
                ## 'sliderlength')
                ##        

        ttk.Style().configure("Black.TLabelframe",fill="white", border=0, relief="flat", font=('Helvetica', 8), background=DIRECTORY_BROWSER_COLOR_BACKGROUND, foreground=DIRECTORY_BROWSER_COLOR_FOREGROUND,highlightthickness=0,highlightcolor="white")

        ################################################ Directory Browser area ################################################

        self.currentDirectory
        
        # Get the directory of the script being run:
        if self.fn is None:
            self.currentDirectory = os.path.dirname(os.path.abspath(__file__))

        else:
            self.currentDirectory = self.fn
        
        self.db = DirectoryBrowser(self, path=self.currentDirectory )

        ################################################ Label Bottom bar ################################################

        self.labelBar = Label(self,
                              relief = FLAT,
                              anchor = W,
                              foreground=BOTTOMBAR_FOREGROUND_COLOR,
                              background=BOTTOMBAR_BACKGROUND_COLOR,
                              bd=0,
                              text = 'Ready')

        #self.labelBar.grid(column=2,row=1,sticky=N+S+E+W)

        #https://github.com/roseman/idle/blob/master/statusbar.py

        
        ################################################ New Text widget ################################################

        self.tb = CustomText(self,
                             undo=1,
                             maxundo=-1,
                             cursor="xterm",
                             setgrid=1,
                             wrap=N,
                             font=("courier new", DEFAULT_FONT_SIZE),
                             foreground=DEFAULT_TEXT_COLOR_FOREGROUND,
                             background=DEFAULT_TEXT_COLOR_BACKGROUND,
                             bd=0,
                             width=75,
                             selectforeground=FOREGROUND_SELECT_COLOR,
                             selectbackground=BACKGROUND_SELECT_COLOR,
                             inactiveselectbackground=INACTIVE_SELECT_BACKGROUND_COLOR,
                             insertbackground=CURSOR_COLOR, # Cursor color
                             insertwidth = 2,
                             highlightthickness=0)         # White border around the edges of text widget. No border = 0
        
        self.tb.bind("<<Change>>", self._on_change)
        self.tb.bind("<Configure>", self._on_change)
        self.tb.bind('<Tab>', self.tab2spaces4)

        #self.tb.bind('<Return>', self.smartReturn)
        #self.tb.bind('<BackSpace>', self.smartBackspace)

        # Line changed
        #self.tb.bind("<<Change_Line>>", self._line_change) # to bylo dobre
        self.tb.bind('<<Change_Line>>', self.line_highlight)
        #self.tb.bind('<Control-l>', self.all_highlight)

        self.tb.bind('<Control-l>', self.balanceBrackets)


        self.tb.bind("<<Paste>>", self.customPaste)

        self.tb.tag_configure('currentLine', background='#1e1e1e')

        
        self.tb.bind('<Key>', lambda _: self.highlightCurrentLine())
        self.tb.bind('<Button-1>', lambda _: self.highlightCurrentLine())
        #self.highlightCurrentLine()

        
        #self.tb.bind("<Button-3>", self.showFancyListbox) # Button-2 on Aqua

        #self.tb.grid(column=2,row=0, sticky=N+E+S+W)

        ################################################ Y Scrollbar ################################################

        style.layout('arrowless.Vertical.TScrollbar', 
         [('Vertical.Scrollbar.trough',
           {'children': [('Vertical.Scrollbar.thumb', 
                          {'expand': '1', 'sticky': 'nswe'})],
            'sticky': 'ns'})])

        style.configure("Vertical.TScrollbar",
        gripcount=0,
        background="#181818", # tlo suwaka
        darkcolor="#181818", # ciemne refleksy / dol i prawy bok
        lightcolor="#181818", # jasne refleksy / gora i lewy bok
        troughcolor="#111111",
        bordercolor="#111111",
        bd = 0,
        activeforeground = "white",
        relief = "flat")

        style.map("arrowless.Vertical.TScrollbar",
            background=[('pressed', 'active', '#1e1e1e'),
                        ('active', '#191919'),
                        ('!active', '#161616')],

            #relief = [('active',"flat"), ('!active','flat')],
            #troughcolor=[('active', "#111111"),('!active', "#111111")]
            )

        self.vsb = ttk.Scrollbar(orient="vertical",
                                 command=self.tb.yview,
                                 style="arrowless.Vertical.TScrollbar")

        self.tb.config(yscrollcommand=self.vsb.set )  # Add y scrollbar 

        ################################################ Line Numbers ################################################
        
        self.linenumbers = TextLineNumbers(self,
                                           width=50,
                                           background=LINENUMBERS_COLOR_BACKGROUND,
                                           bd=0,
                                           highlightthickness=0)
        self.linenumbers.attach(self.tb)

        ################################################ Bottom bar command line ################################################

        self.cmdLine = Text(self,
                            font=("courier new", 10),
                            foreground=DEFAULT_TEXT_COLOR_FOREGROUND,
                            background=BOTTOMBAR_BACKGROUND_COLOR,
                            bd=0,
                            height=0,
                            insertbackground=COMMANDLINE_CURSOR_COLOR,
                            highlightthickness=0)

        self.cmdLine.bind('<Return>', self.executeInTerminal)

        ################################################ Terminal ################################################

        self.terminal = Text(self,
                             wrap=CHAR, # Wrap whole words
                             font=("courier new", 14),
                             foreground=DEFAULT_TEXT_COLOR_FOREGROUND,
                             background=TERMINAL_BACKGROUND_COLOR,
                             bd=0,
                             height=60,
                             insertbackground=COMMANDLINE_CURSOR_COLOR,
                             highlightthickness=0)

        ################################################ Snippet List ################################################

        self.snippetList = Listbox(self,
                                   highlightthickness=0,
                                   foreground=SNIPPETLIST_COLOR_FOREGROUND,
                                   background=SNIPPETLIST_COLOR_BACKGROUND,
                                   bd=0)

        self.snippetList.bind('<Return>', self.addSnippet)
        
        ################################################ Content List ################################################

##        self.contentList = Listbox(self)
##        self.contentList.config(highlightthickness=0, foreground=SNIPPETLIST_COLOR_FOREGROUND, background=SNIPPETLIST_COLOR_BACKGROUND, bd=0)
##
##        self.contentList.insert(1, ["def", "def", "def"])
##
##        self.contentList.grid(column=5,row=0,sticky=N+S+E+W)
##
##        content = ["one", "two", "three", "four"]
##
##        for item in content:
##            self.contentList.insert(END, item)

        ################################################ Right Mouse Menu for Terminal ################################################

        self.RightMouseMenu = Menu(self, tearoff=0, background=PULLDOWN_BACKGROUND_COLOR, foreground=PULLDOWN_FOREGROUND_COLOR, activeforeground=PULLDOWN_ACTIVE_FOREGROUND_COLOR, activebackground=PULLDOWN_BACKGROUND_COLOR, bd=0)#PULLDOWN_BACKGROUND_COLOR
        self.RightMouseMenu.add_command(label="Clear", command=self.clearTerminal )
        self.RightMouseMenu.add_command(label="Run", command = self.runCode )

        self.terminal.bind("<Button-3>", self.showRightMouseMenu)

        ################################################ Right Mouse Menu for DB ################################################

        self.RightMouseMenuDB = Menu(self, tearoff=0)
        self.RightMouseMenuDB.add_command(label="Next") # , command=next) etc...
        self.RightMouseMenuDB.add_command(label="Previous")
        self.RightMouseMenuDB.add_separator()
        self.RightMouseMenuDB.add_command(label="Home")

        self.tb.bind("<Button-3>", self.showRightMouseMenu)

        ################################################ Autocomplete entry ################################################

        lista = ['a', 'actions', 'additional', 'also', 'an', 'and', 'angle', 'are', 'as', 'be', 'bind', 'bracket', 'brackets', 'button', 'can', 'cases', 'configure', 'course', 'detail', 'enter', 'event', 'events', 'example', 'field', 'fields', 'for', 'give', 'important', 'in', 'information', 'is', 'it', 'just', 'key', 'keyboard', 'kind', 'leave', 'left', 'like', 'manager', 'many', 'match', 'modifier', 'most', 'of', 'or', 'others', 'out', 'part', 'simplify', 'space', 'specifier', 'specifies', 'string;', 'that', 'the', 'there', 'to', 'type', 'unless', 'use', 'used', 'user', 'various', 'ways', 'we', 'window', 'wish', 'you']
        self.entry = AutocompleteEntry(lista,
                                       self,
                                       highlightthickness=0,
                                       background= "blue", #"#161616",
                                       foreground=PULLDOWN_FOREGROUND_COLOR,
                                       bd=0)

        self.entry.grid(column=2, row=3)

        ################################################ System Terminal ################################################

        terminalHeight = 100
        terminalWidth = 100

        self.systemTerminal = Frame(self, height=terminalHeight, width=terminalWidth)
        self.systemTerminal.grid(column=4, row=0, sticky=N+E+S+W)
        
        wid = self.systemTerminal.winfo_id()
        os.system("""xterm -into %d -bg "#181818" -geometry 40x20 -fa "Monospace" -fs 10 &""" % wid)


    
        #self.db.grid(column=0,row=0, sticky=N+S+E+W)

        self.linenumbers.grid(column=1, row=0, sticky=N+E+S+W)

        #self.terminal.grid(column=4, row=0, sticky=N+E+S+W)
        #self.cmdLine.grid(column=4, row=1, sticky=N+E+S+W)

        #self.snippetList.grid(column=0, row=0, sticky=N+S+E+W)
        self.labelBar.grid(column=2, row=1,sticky=N+S+E+W)

        self.tb.grid(column=2,row=0, sticky=N+E+S+W)
        self.vsb.grid(column=3, row=0, sticky=N+E+S+W)

        #self.showDirectoryBrowser
        #self.showTerminal
        #self.showSnippetList
        #self.showLabelBar
        #self.showScrollBar



        #self.grid_columnconfigure(0, weight=0)

        #self.grid_columnconfigure(3, weight=1)
        #self.grid_columnconfigure(4, weight=1)

        self.grid_rowconfigure(0, weight=2)


        # Init
        self.configure(background=WINDOW_BACKGROUND_COLOR)
        self.tb.insert(END, GREETING_MESSAGE)
        self.checkLexerType()
        self.title("Edit")
        self.autoSave()



if __name__ == '__main__':

    w = Application()

    # Define window resolution
    #w.geometry('1200x800+100+100')
    #w.geometry('')

    w.mainloop()


