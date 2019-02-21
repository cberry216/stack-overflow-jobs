import tkinter as tk
from gui_driver import GUIDriver

root = tk.Tk()
root.wm_title('Window Title')
root.config(background='#ffffff')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
SCREEN_PAD = 100

gui_width = screen_width - SCREEN_PAD
gui_height = screen_height - SCREEN_PAD

gui = GUIDriver(root, width=gui_width, height=gui_height)
gui.grid(row=0, column=0)


root.mainloop()
