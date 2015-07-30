from PIL import Image
import shutil
import os
import tkinter as tk
import queue
import threading
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


class GUI:

    def __init__(self):
        self.dirname = 'C:/'
        self.tk = tk.Tk()
        self.tk.title('Image Checker')
        self.tk.frame = tk.Frame(self.tk)
        self.tk.text = tk.Text(self.tk.frame, height=1, width=30)
        self.tk.text.pack(side='left')
        self.tk.browsebutton = tk.Button(
            self.tk.frame, text='Browse...', command=self.askDirectory)
        self.tk.browsebutton.pack(side='left')
        self.tk.startbutton = tk.Button(
            self.tk.frame, text='Start Check', command=self.processFiles)
        self.tk.startbutton.pack(side='left')
        self.tk.text.delete(1.0, tk.END)
        self.tk.text.insert(tk.END, self.dirname)
        self.tk.frame.pack()
        self.tk.progressbar = ttk.Progressbar(
            self.tk, orient='horizontal', mode='indeterminate', maximum=50)
        self.tk.progressbar.pack(fill='x', pady=2)
        self.tk.mainloop()

    def askDirectory(self):
        self.dirname = filedialog.askdirectory()
        self.tk.text.delete(1.0, tk.END)
        self.tk.text.insert(tk.END, self.dirname)

    def processFiles(self):
        self.dirname = self.tk.text.get(1.0, tk.END).rstrip('\n')
        self.queue = queue.Queue()
        ProcessFiles(self.queue, self.dirname, self.tk.progressbar).start()


class ProcessFiles(threading.Thread):

    def __init__(self, queue, dirname, progressbar):
        threading.Thread.__init__(self)
        self.queue = queue
        self.dirname = dirname
        self.progressbar = progressbar

    def run(self):
        numberofcorruptfiles = 0
        numberoffiles = 0
        numberofimages = 0
        self.progressbar.start()
        corruptPath = os.path.join(self.dirname, 'corrupt')
        if not os.path.exists(corruptPath):
            os.makedirs(corruptPath)
        for dirpath, dirnames, files in os.walk(self.dirname):
            for file in files:
                numberoffiles += 1
                if file.lower().endswith(('.tif', '.jpg', '.jpeg', '.tiff', '.gif')):
                    numberofimages += 1
                    try:
                        fullname = os.path.join(dirpath, file)
                        fp = open(fullname, "rb")
                        Image.open(fp)
                        fp.close()
                    except Exception:
                        fp.close()
                        try:
                            shutil.move(fullname, corruptPath)
                        except Exception:
                            pass
                        numberofcorruptfiles += 1
        self.progressbar.stop()
        messagebox.showinfo("Done!", "%(numberoffiles)s files found.\n%(numberofimages)s images processed.\n%(numberofcorruptfiles)s corrupt images found." % {
                            "numberoffiles": numberoffiles, "numberofimages": numberofimages, "numberofcorruptfiles": numberofcorruptfiles})


if __name__ == '__main__':
    gui = GUI()
