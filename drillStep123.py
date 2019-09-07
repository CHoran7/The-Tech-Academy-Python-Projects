import tkinter, sqlite3, os, time, shutil
from tkinter import *
from tkinter import filedialog

fPath = 'C:\\Drill File\\'
conn = sqlite3.connect('drill123.db')
sourcePath = ''
destinationPath = ''

class ParentWindow(Frame):
    def __init__ (self, master):
        Frame.__init__(self)

        self.master = master
        self.master.geometry('{}x{}'.format(600,200))#set window size
        self.master.title('Find files')#title that appears at the top of window

        #Creating the buttons and entries
        self.btnSource = Button(self.master, text="Source", width=15, height=1, command=lambda: browseDirectory(self))
        self.btnSource.grid(row=0, column=0, padx=(10,0), pady=(50,0))

        self.txtFName1 = Entry(self.master,text='',font=("Helvetica", 16), fg='black', bg='white', width=35)
        self.txtFName1.grid(row=0, column=1, padx=(20,0), pady=(50,0))

        self.btnDestination = Button(self.master, text="Destination", width=15, height=1, command=lambda: destinationDirectory(self))
        self.btnDestination.grid(row=1, column=0, padx=(10,0), pady=(10,0))

        self.txtFName2 = Entry(self.master,text='',font=("Helvetica", 16), fg='black', bg='white', width=35)
        self.txtFName2.grid(row=1, column=1, padx=(20,0), pady=(10,0))

        self.btnMoveFiles = Button(self.master, text="Move Files", width=15, height=1, command=lambda: moveFiles(self))
        self.btnMoveFiles.grid(row=2, column=0, padx=(10,0), pady=(50,0))

def browseDirectory(self):
    self.txtFName1.delete(0,END)
    dirname = filedialog.askdirectory(title='Please select a directory')
    print(dirname)
    self.txtFName1.insert(0,dirname)
    global sourcePath
    sourcePath = dirname

def destinationDirectory(self):
    self.txtFName2.delete(0,END)
    dirname = filedialog.askdirectory(title='Choose a destination directory')
    print(dirname)
    self.txtFName2.insert(0,dirname)
    global destinationPath
    destinationPath = dirname

def moveFiles(self):
    fList = os.listdir(sourcePath)
    with conn:
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS tbl_files( \
            ID INTEGER PRIMARY KEY AUTOINCREMENT, \
            col_fname TEXT, col_mtime TEXT \
            )")
        conn.commit()
        for i in fList:
            if i.endswith('.txt'):
                txtList = [(i),time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(os.path.getmtime(os.path.join(sourcePath, i))))]
                cur.execute("INSERT INTO tbl_files(col_fname, col_mtime) VALUES (?,?)", txtList)
                conn.commit()
    conn.close()
    for i in fList:
        if i.endswith('.txt'):
            print(i + " was last modified " + time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(os.path.getmtime(os.path.join(sourcePath, i)))))
            shutil.move(os.path.join(sourcePath, i), os.path.join(destinationPath, i))

if __name__ == "__main__":
    root = Tk()
    App = ParentWindow(root)
    root.mainloop()
