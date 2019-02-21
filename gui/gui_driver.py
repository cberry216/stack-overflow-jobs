import tkinter as tk


class GUIDriver(tk.Frame):

    def __init__(self, parent, width, height):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.window_width = width
        self.window_height = height
        self.frames = self.build_layout()

    def build_layout(self):
        filter_frame_width = int(self.window_width * 0.6)
        filter_frame_height = int(self.window_height * 0.4)

        entry_frame_width = filter_frame_width
        entry_frame_height = self.window_height - filter_frame_height

        info_frame_width = self.window_width - filter_frame_width
        info_frame_height = self.window_height

        database_frame_width = int(0.1 * self.window_width)
        database_frame_height = filter_frame_height

        parameter_frame_width = self.window_width - info_frame_width - database_frame_width
        parameter_frame_height = filter_frame_height

        order_frame_width = entry_frame_width
        order_frame_height = int(0.05 * self.window_height)

        jobs_frame_width = entry_frame_width
        jobs_frame_height = self.window_height - filter_frame_height - order_frame_height

        frameReference = {}

        filterFrame = tk.Frame(
            self,
            width=filter_frame_width,
            height=filter_frame_height
        )
        filterFrame.grid(row=0, column=0)

        entryFrame = tk.Frame(
            self,
            width=entry_frame_width,
            height=entry_frame_height
        )
        entryFrame.grid(row=1, column=0)

        infoFrame = tk.Frame(
            self,
            width=info_frame_width,
            height=info_frame_height
        )
        infoFrame.config(background='blue')
        infoFrame.grid(row=0, column=1, rowspan=2)
        frameReference['infoFrame'] = infoFrame

        databaseFrame = tk.Frame(
            filterFrame,
            width=database_frame_width,
            height=database_frame_height
        )
        databaseFrame.config(background="green")
        databaseFrame.grid(row=0, column=0)
        frameReference['databaseFrame'] = databaseFrame

        parameterFrame = tk.Frame(
            filterFrame,
            width=parameter_frame_width,
            height=parameter_frame_height
        )
        parameterFrame.config(background="red")
        parameterFrame.grid(row=0, column=1)
        frameReference['parameterFrame'] = parameterFrame

        orderFrame = tk.Frame(
            entryFrame,
            width=order_frame_width,
            height=order_frame_height
        )
        orderFrame.config(background='purple')
        orderFrame.grid(row=0, column=0)
        frameReference['orderFrame'] = orderFrame

        jobsFrame = tk.Frame(
            entryFrame,
            width=jobs_frame_width,
            height=jobs_frame_height
        )
        jobsFrame.config(background='cyan')
        jobsFrame.grid(row=1, column=0)
        frameReference['jobsFrame'] = jobsFrame

        return frameReference
