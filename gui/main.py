import tkinter as tk
from gui_driver import GUIDriver

root = tk.Tk()
root.wm_title('Window Title')
root.config(background='#ffffff')

# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# SCREEN_PAD = 100

gui_width = 1600
gui_height = 900

gui = GUIDriver(root, width=gui_width, height=gui_height)
gui.grid(row=0, column=0)


root.mainloop()
