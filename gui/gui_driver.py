import tkinter as tk
from tkinter import scrolledtext as st
from random import randint

ID_INDEX=0
TITLE_INDEX=1
COMPANY_INDEX=2
STATE_INDEX=7
CITY_INDEX=6
PUBLISHED_INDEX=9


class GUIDriver(tk.Frame):

    def __init__(self, parent, width, height):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.window_width = width
        self.window_height = height
        self.frames = self.build_layout()
        self.entry_list = []
        self.parameter_fields = {
            'location_null': tk.BooleanVar(),
            'state': tk.StringVar(),
            'city': tk.StringVar(),
            'tags': tk.StringVar(),
            'title': tk.StringVar(),
            'company': tk.StringVar(),
            'remote': tk.BooleanVar(),
            'results': tk.StringVar()
        }
        self.location_include_nulls = tk.BooleanVar()
        self.allows_remote = tk.BooleanVar()
        self.and_or_results = tk.StringVar()
        self.entryScrolledText = st.ScrolledText(self.frames['jobsFrame'])
        self.entryScrolledText.config(width=self.frames['jobsFrame']['width'])
        self.entryScrolledText.grid(row=0, column=0)

        # TODO: Remove this
        for i in range(100):
            self.entry_list.append(
                (
                    i,
                    'title ' + str(randint(100000,999999)),
                    'company ' + str(randint(100000, 999999)),
                    0,
                    0,
                    0,
                    'city ' + str(randint(100000, 999999)),
                    'state ' + str(randint(100000, 999999)),
                    0,
                    'published ' + str(randint(100000, 999999))
                )
            )

        self.add_frame_components()

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

        frame_reference = {}

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
        frame_reference['infoFrame'] = infoFrame

        databaseFrame = tk.Frame(
            filterFrame,
            width=database_frame_width,
            height=database_frame_height,
        )
        databaseFrame.config(background="green")
        databaseFrame.grid(row=0, column=0)
        databaseFrame.grid_propagate(False)
        databaseFrame.grid_columnconfigure(0, weight=1)
        databaseFrame.grid_rowconfigure(1, weight=1)
        databaseFrame.grid_rowconfigure(2, weight=1)
        databaseFrame.grid_rowconfigure(3, weight=1)
        frame_reference['databaseFrame'] = databaseFrame

        parameterFrame = tk.Frame(
            filterFrame,
            width=parameter_frame_width,
            height=parameter_frame_height
        )
        parameterFrame.config(background="red")
        parameterFrame.grid(row=0, column=1)
        parameterFrame.grid_propagate(False)
        parameterFrame.grid_columnconfigure(0, weight=1)
        parameterFrame.grid_columnconfigure(1, weight=1)
        parameterFrame.grid_columnconfigure(2, weight=1)
        parameterFrame.grid_columnconfigure(3, weight=1)
        parameterFrame.grid_columnconfigure(4, weight=1)
        parameterFrame.grid_columnconfigure(5, weight=1)
        parameterFrame.grid_rowconfigure(0, weight=1)
        parameterFrame.grid_rowconfigure(1, weight=1)
        parameterFrame.grid_rowconfigure(2, weight=1)
        parameterFrame.grid_rowconfigure(3, weight=1)
        parameterFrame.grid_rowconfigure(4, weight=1)
        frame_reference['parameterFrame'] = parameterFrame

        orderFrame = tk.Frame(
            entryFrame,
            width=order_frame_width,
            height=order_frame_height
        )
        orderFrame.config(background='purple')
        orderFrame.grid(row=0, column=0)
        orderFrame.grid_propagate(False)
        orderFrame.grid_columnconfigure(0, weight=1)
        orderFrame.grid_columnconfigure(1, weight=1)
        orderFrame.grid_columnconfigure(2, weight=1)
        orderFrame.grid_columnconfigure(3, weight=1)
        orderFrame.grid_columnconfigure(4, weight=1)
        orderFrame.grid_columnconfigure(5, weight=1)
        orderFrame.grid_rowconfigure(0, weight=1)
        frame_reference['orderFrame'] = orderFrame

        # jobsCanvas = tk.Canvas(
        #     entryFrame,
        #     width=jobs_frame_width,
        #     height=jobs_frame_height
        # )
        # jobsCanvas.config(background='steelblue')
        # jobsCanvas.grid(row=1, column=0)
        # jobsCanvas.grid_propagate(False)
        # jobsCanvas.grid_columnconfigure(0, weight=1)
        # jobsCanvas.grid_columnconfigure(1, weight=1)
        # jobsCanvas.grid_columnconfigure(2, weight=1)
        # jobsCanvas.grid_columnconfigure(3, weight=1)
        # jobsCanvas.grid_columnconfigure(4, weight=1)
        # frame_reference['jobsCanvas'] = jobsCanvas

        # jobsScrollbar = tk.Scrollbar(
        #     entryFrame,
        #     command=jobsCanvas.yview
        # )
        # jobsScrollbar.config(background="maroon")
        # jobsScrollbar.grid(row=0, column=1, rowspan=2)

        # jobsCanvas.configure(yscrollcommand=jobsScrollbar.set)
        # # jobsCanvas.bind('<Configure>', self.on_configure)

        jobsFrame = tk.Frame(
            entryFrame,
            width=jobs_frame_width,
            height=jobs_frame_height,
        )
        jobsFrame.config(background='cyan')
        jobsFrame.grid(row=1, column=0)
        jobsFrame.grid_propagate(False)
        # jobsFrame.grid_columnconfigure(0, weight=1)
        # jobsFrame.grid_columnconfigure(1, weight=1)
        # jobsFrame.grid_columnconfigure(2, weight=1)
        # jobsFrame.grid_columnconfigure(3, weight=1)
        # jobsFrame.grid_columnconfigure(4, weight=1)
        frame_reference['jobsFrame'] = jobsFrame

        return frame_reference
    
    def add_frame_components(self):
        self.add_parameter_fields()
        self.add_database_label()
        self.add_offline_database_button()
        self.add_purge_database_button()
        self.add_concat_database_button()
        self.add_entries_label()

    def add_parameter_fields(self):
        using_frame = self.frames['parameterFrame']

        locationLabel = tk.Label(
            using_frame,
            text="Location"
        )
        locationLabel.grid(row=0, column=0, sticky="NEWS")

        locationRadioNull = tk.Radiobutton(
            using_frame,
            text="Include NULL",
            variable=self.parameter_fields['location_null'],
            value=True,
            indicatoron=0
        )
        locationRadioNull.grid(row=0, column=1, sticky="NEWS")

        locationRadioNotNull = tk.Radiobutton(
            using_frame,
            text="No NULL",
            variable=self.parameter_fields['location_null'],
            value=False,
            indicatoron=0
        )
        locationRadioNotNull.grid(row=0, column=2, sticky="NEWS")

        stateLabel = tk.Label(
            using_frame,
            text="State"
        )
        stateLabel.grid(row=1, column=0, sticky="NEWS")

        stateEntry = tk.Entry(
            using_frame,
            textvariable=self.parameter_fields['state']
        )
        stateEntry.grid(row=1, column=1, columnspan=2, sticky="NEWS")

        cityLabel = tk.Label(
            using_frame,
            text="City"
        )
        cityLabel.grid(row=2, column=0, sticky="NEWS")

        cityEntry = tk.Entry(
            using_frame,
            textvariable=self.parameter_fields['city']
        )
        cityEntry.grid(row=2, column=1, columnspan=2, sticky="NEWS")

        tagsLabel = tk.Label(
            using_frame,
            text="Tags"
        )
        tagsLabel.grid(row=3, column=0, sticky="NEWS")

        tagsEntry = tk.Entry(
            using_frame,
            textvariable=self.parameter_fields['tags']
        )
        tagsEntry.grid(row=3, column=1, columnspan=2, sticky="NEWS")

        titleLabel = tk.Label(
            using_frame,
            text="Title"
        )
        titleLabel.grid(row=0, column=3, sticky="NEWS")

        titleEntry = tk.Entry(
            using_frame,
            textvariable=self.parameter_fields['title']
        )
        titleEntry.grid(row=0, column=4, columnspan=2, sticky="NEWS")

        companyLabel = tk.Label(
            using_frame,
            text="Company"
        )
        companyLabel.grid(row=1, column=3, sticky="NEWS")

        companyEntry = tk.Entry(
            using_frame,
            textvariable=self.parameter_fields['company']
        )
        companyEntry.grid(row=1, column=4, columnspan=2, sticky="NEWS")

        remoteLabel = tk.Label(
            using_frame,
            text="Remote"
        )
        remoteLabel.grid(row=2, column=3, sticky="NEWS")

        remoteRadioAllow = tk.Radiobutton(
            using_frame,
            text="Allows Remote",
            variable=self.parameter_fields['remote'],
            value=True,
            indicatoron=0
        )
        remoteRadioAllow.grid(row=2, column=4, sticky="NEWS")

        remoteRadioNotAllow = tk.Radiobutton(
            using_frame,
            text="No Remote",
            variable=self.parameter_fields['remote'],
            value=False,
            indicatoron=0
        )
        remoteRadioNotAllow.grid(row=2, column=5, sticky="NEWS")

        resultsLabel = tk.Label(
            using_frame,
            text="Results"
        )
        resultsLabel.grid(row=3, column=3, sticky="NEWS")

        resultsRadioAnd = tk.Radiobutton(
            using_frame,
            text="AND",
            variable=self.parameter_fields['results'],
            value="AND",
            indicatoron=0
        )
        resultsRadioAnd.grid(row=3, column=4, sticky="NEWS")

        resultsRadioOr = tk.Radiobutton(
            using_frame,
            text="OR",
            variable=self.parameter_fields['results'],
            value="OR",
            indicatoron=0
        )
        resultsRadioOr.grid(row=3, column=5, sticky="NEWS")

        submitButton = tk.Button(
            using_frame,
            text="Filter",
            command=self.filter_results
        )
        submitButton.grid(row=4, column=0, columnspan=6, sticky="NEWS")

    def filter_results(self):
        print('Location Null: ' + str(self.parameter_fields['location_null'].get()))
        print('State: ' + str(self.parameter_fields['state'].get()))
        print('City: ' + str(self.parameter_fields['city'].get()))
        print('Tags: ' + str(self.parameter_fields['tags'].get()))
        print('Title: ' + str(self.parameter_fields['title'].get()))
        print('Company: ' + str(self.parameter_fields['company'].get()))
        print('Remote: ' + str(self.parameter_fields['remote'].get()))
        print('Results: ' + str(self.parameter_fields['results'].get()))


    def add_database_label(self):
        using_frame = self.frames['databaseFrame']
        databaseLabel = tk.Label(
            using_frame,
            text="Database Mode"
        )
        databaseLabel.grid(row=0, column=0, stick="EW")

    def add_offline_database_button(self):
        using_frame = self.frames['databaseFrame']
        offlineDatabaseButton = tk.Button(
            using_frame,
            text="Offline",
            command=self.init_offline_database,
        )
        offlineDatabaseButton.grid(row=1, column=0, sticky="NEWS")

    def add_purge_database_button(self):
        using_frame = self.frames['databaseFrame']
        purgeDatabaseButton = tk.Button(
            using_frame,
            text="Purge",
            command=self.init_purge_database,
        )
        purgeDatabaseButton.grid(row=2, column=0, sticky="NEWS")

    def add_concat_database_button(self):
        using_frame = self.frames['databaseFrame']
        concatDatabaseButton = tk.Button(
            using_frame,
            text="Concat",
            command=self.init_concat_database,
        )
        concatDatabaseButton.grid(row=3, column=0, sticky="NEWS")

    def add_entries_label(self):
        using_frame = self.frames['orderFrame']

        idButton = tk.Button(
            using_frame,
            text="ID",
            command=self.sort_entries_by_id
        )
        idButton.grid(row=0, column=0, sticky="NEWS")

        titleButton = tk.Button(
            using_frame,
            text="Title",
            command=self.sort_entries_by_title
        )
        titleButton.grid(row=0, column=1, sticky="NEWS")

        companyButton = tk.Button(
            using_frame,
            text="Company",
            command=self.sort_entries_by_company
        )
        companyButton.grid(row=0, column=2, sticky="NEWS")

        stateButton = tk.Button(
            using_frame,
            text="State",
            command=self.sort_entries_by_state
        )
        stateButton.grid(row=0, column=3, sticky="NEWS")

        cityButton = tk.Button(
            using_frame,
            text="City",
            state=tk.DISABLED
        )
        cityButton.grid(row=0, column=4, sticky="NEWS")

        publishedButton = tk.Button(
            using_frame,
            text="Published",
            command=self.sort_entries_by_published
        )
        publishedButton.grid(row=0, column=5, sticky="NEWS")



    def init_offline_database(self):
        print('Offline Working')
        self.write_entries_to_text()

    def init_purge_database(self):
        print('Purge Working')
        # self.write_reverse_entries_to_text()
        self.delete_entries()

    def init_concat_database(self):
        print('Concat Working')

    def write_entries_to_text(self):
        self.entryScrolledText.config(state=tk.NORMAL)
        self.entryScrolledText.delete(1.0, tk.END)
        for i in range(len(self.entry_list)):
            self.write_single_entry_to_text(self.entry_list[i], i)
        self.entryScrolledText.config(state=tk.DISABLED)

    def write_single_entry_to_text(self, entry, row):
        # using_frame = self.frames['jobsCanvas']

        entry_id = self.format_to_length(str(entry[ID_INDEX]), 19)
        entry_title = self.format_to_length(str(entry[TITLE_INDEX]), 22)
        entry_company = self.format_to_length(str(entry[COMPANY_INDEX]), 27)
        entry_state = self.format_to_length(str(entry[STATE_INDEX]), 22)
        entry_city = self.format_to_length(str(entry[CITY_INDEX]), 21)
        entry_published = self.format_to_length(str(entry[PUBLISHED_INDEX]), 24)

        self.entryScrolledText.insert(tk.END, f'{entry_id}{entry_title}{entry_company}{entry_state}{entry_city}{entry_published}\n')

        # titleText = tk.Text(
        #     using_frame,
        #     height=1
        # )
        # titleText.grid(row=row, column=TITLE_COLUMN)
        # titleText.insert(tk.END, entry_title)
        # titleText.config(state=tk.DISABLED)

        # companyText = tk.Text(
        #     using_frame,
        #     height=1
        # )
        # companyText.grid(row=row, column=COMPANY_COLUMN)
        # companyText.insert(tk.END, entry_company)
        # companyText.config(state=tk.DISABLED)

        # stateText = tk.Text(
        #     using_frame,
        #     height=1
        # )
        # stateText.grid(row=row, column=STATE_COLUMN)
        # stateText.insert(tk.END, entry_state)
        # stateText.config(state=tk.DISABLED)

        # cityText = tk.Text(
        #     using_frame,
        #     height=1
        # )
        # cityText.grid(row=row, column=CITY_COLUMN)
        # cityText.insert(tk.END, entry_city)
        # cityText.config(state=tk.DISABLED)

        # publishedText = tk.Text(
        #     using_frame,
        #     height=1
        # )
        # publishedText.grid(row=row, column=PUBLISHED_COLUMN)
        # publishedText.insert(tk.END, entry_published)
        # publishedText.config(state=tk.DISABLED)

    def format_to_length(self, attribute, length):
        if len(attribute) > length:
            return attribute[:length-3] + '...'
        else:
            return attribute + ' ' * (length - len(attribute))

    def sort_entries_by_id(self):
        print('Sorting by id')
        self.entry_list.sort(key=lambda x: x[ID_INDEX])
        self.write_entries_to_text()

    def sort_entries_by_title(self):
        print('Sorting by title')
        self.entry_list.sort(key=lambda x: x[TITLE_INDEX])
        self.write_entries_to_text()

    def sort_entries_by_company(self):
        print('Sorting by company')
        self.entry_list.sort(key=lambda x: x[COMPANY_INDEX])
        self.write_entries_to_text()

    def sort_entries_by_state(self):
        print('Sorting by state')
        self.entry_list.sort(key=lambda x: x[STATE_INDEX])
        self.write_entries_to_text()

    def sort_entries_by_published(self):
        print('Sorting by published')
        self.entry_list.sort(key=lambda x: x[PUBLISHED_INDEX])
        self.write_entries_to_text()

