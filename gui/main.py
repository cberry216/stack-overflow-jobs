import tkinter as tk

root = tk.Tk()
root.wm_title('Window Title')
root.config(background='#ffffff')

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
SCREEN_PAD = 100

window_width = screen_width - SCREEN_PAD
window_height = screen_height - SCREEN_PAD

filter_frame_width = int(window_width * 0.6)
filter_frame_height = int(window_height * 0.4)

entry_frame_width = filter_frame_width
entry_frame_height = window_height - filter_frame_height

info_frame_width = window_width - filter_frame_width
info_frame_height = window_height

database_frame_width = int(0.1 * window_width)
database_frame_height = filter_frame_height

parameter_frame_width = window_width - info_frame_width - database_frame_width
parameter_frame_height = filter_frame_height

order_frame_width = entry_frame_width
order_frame_height = int(0.05 * window_height)

jobs_frame_width = entry_frame_width
jobs_frame_height = window_height - filter_frame_height - order_frame_height

mainFrame = tk.Frame(
    root,
    width=window_width,
    height=window_height
)
mainFrame.grid(row=0, column=0, padx=10, pady=2)

filterFrame = tk.Frame(
    mainFrame,
    width=filter_frame_width,
    height=filter_frame_height
)
filterFrame.grid(row=0, column=0)

entryFrame = tk.Frame(
    mainFrame,
    width=entry_frame_width,
    height=entry_frame_height
)
entryFrame.grid(row=1, column=0)

infoFrame = tk.Frame(
    mainFrame,
    width=info_frame_width,
    height=info_frame_height
)
infoFrame.config(background='blue')
infoFrame.grid(row=0, column=1, rowspan=2)

databaseFrame = tk.Frame(
    filterFrame,
    width=database_frame_width,
    height=database_frame_height
)
databaseFrame.config(background="green")
databaseFrame.grid(row=0, column=0)

parameterFrame = tk.Frame(
    filterFrame,
    width=parameter_frame_width,
    height=parameter_frame_height
)
parameterFrame.config(background="red")
parameterFrame.grid(row=0, column=1)

orderFrame = tk.Frame(
    entryFrame,
    width=order_frame_width,
    height=order_frame_height
)
orderFrame.config(background='purple')
orderFrame.grid(row=0, column=0)

jobsFrame = tk.Frame(
    entryFrame,
    width=jobs_frame_width,
    height=jobs_frame_height
)
jobsFrame.config(background='cyan')
jobsFrame.grid(row=1, column=0)

root.mainloop()
