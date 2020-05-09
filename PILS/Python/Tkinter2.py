'''
Created on 27 janv. 2020

@author: gresset6u
'''

import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    def createWidgets(self):
        self.QUIT = tk.Button(self, text="QUIT", fg="red",  command=root.destroy)
        self.QUIT.pack(side="left")
        hi_there = tk.Button(self, text="Hello", command=self.say_hi)
        hi_there.pack(side="left")
    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
