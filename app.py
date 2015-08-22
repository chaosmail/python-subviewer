import tkinter as tk
import sys
import pysrt
import fs
from time import sleep


class Application(tk.Frame):
    def __init__(self, master=None, subs=[]):
        tk.Frame.__init__(self, master)
        self.subs = subs
        self.pack()
        master.attributes("-topmost", True)
        master.lift()
        self.font = ("Roboto", "32", "bold") 
        self.createWidgets()

    def createWidgets(self):
        self.sub_var = tk.StringVar()
        self.sub_label = tk.Label(self, textvariable=self.sub_var, font=self.font)
        self.sub_label.pack()

        def get_ms(t):
            return (t.hours*60*60 + t.minutes*60 + t.seconds)*1000 + t.milliseconds

        for sub in subs:
            start = get_ms(sub.start)
            duration =  get_ms(sub.end) - get_ms(sub.start)
            current_time = get_ms(sub.end)
            self.sub_label.after(start, self.update, start, duration, sub.text)
            self.sub_label.after(start + duration, self.update, start, duration, "")

    def updateText(self, val, verbose=""):
        if verbose:
            print(verbose)
        self.sub_var.set(val)

    def update(self, start, duration, text):
        self.updateText(text, verbose="%i (%i): %s" % (start, duration, text))


if __name__ == "__main__":
    filename = sys.argv[1]
    print('Starting %s' % filename)

    if fs.exists(filename):
        subs = pysrt.open(filename)

        root = tk.Tk()
        app = Application(master=root, subs=subs)
        app.mainloop()

    else:
        print('Please use a valid subtitle file')