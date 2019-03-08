import profile
import tkinter as tk



from gui.app import App


def start():
    main = App(tk.Tk())
    main.mainloop()


profile.run('start()')
