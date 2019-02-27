import tkinter as tk
from html2text import html2text
from tkinter import scrolledtext as st
from random import randint
from db_interface import DBInterface

ID_INDEX = 0
TITLE_INDEX = 1
COMPANY_INDEX = 2
SUMMARY_INDEX = 3
LINK_INDEX = 4
TAGS_INDEX=5
STATE_INDEX = 7
CITY_INDEX = 6
REMOTE_INDEX = 8
PUBLISHED_INDEX = 9

DB_NAME = 'db.sqlite'


class GUIDriver(tk.Frame):

    def __init__(self, parent, width, height):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.window_width = width
        self.window_height = height
        self.frames = self.build_layout()
        self.interface = DBInterface(DB_NAME)
        self.entries_initialized = False
        self.entry_list = self.interface.get_all_entries()
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
        self.current_info_dict = {}
        self.sort_order = {
            'id': 'ASC',
            'title': 'ASC',
            'company': 'ASC',
            'state': 'ASC',
            'published': 'ASC'
        }
        # self.entryScrolledText = st.ScrolledText(self.frames['jobsFrame'])
        # self.entryScrolledText.config(width=self.frames['jobsFrame']['width'])
        # self.entryScrolledText.grid(row=0, column=0)
        self.entryScrolledText = tk.Text(
            self.frames['jobsFrame'],
            width=self.frames['jobsFrame']['width']    
        )
        self.entryScrolledText.grid(row=0, column=0)
        self.entryScrollbar = tk.Scrollbar(self.frames['jobsFrame'])
        self.entryScrollbar.grid(row=0, column=1)

        self.add_frame_components()

    def build_layout(self):
        filter_frame_width = int(self.window_width * 0.6)
        filter_frame_height = int(self.window_height * 0.4)

        entry_frame_width = filter_frame_width
        entry_frame_height = self.window_height - filter_frame_height

        right_frame_width = self.window_width - filter_frame_width
        right_frame_height = self.window_height

        database_frame_width = int(0.1 * self.window_width)
        database_frame_height = filter_frame_height

        parameter_frame_width = self.window_width - right_frame_width - database_frame_width
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

        rightFrame = tk.Frame(
            self,
            width=right_frame_width,
            height=right_frame_height
        )
        rightFrame.grid(row=0, column=1, rowspan=2)

        infoFrame = tk.Frame(
            rightFrame,
            width=right_frame_width,
            height=right_frame_height
        )
        infoFrame.grid(row=0, column=0)
        infoFrame.grid_propagate(False)
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
        orderFrame.grid_columnconfigure(1, weight=4)
        orderFrame.grid_columnconfigure(2, weight=2)
        orderFrame.grid_columnconfigure(3, weight=1)
        orderFrame.grid_columnconfigure(4, weight=2)
        orderFrame.grid_columnconfigure(5, weight=2)
        orderFrame.grid_rowconfigure(0, weight=1)
        frame_reference['orderFrame'] = orderFrame

        jobsFrame = tk.Frame(
            entryFrame,
            width=jobs_frame_width,
            height=jobs_frame_height,
        )
        jobsFrame.grid(row=1, column=0)
        jobsFrame.grid_propagate(False)
        jobsFrame.grid_columnconfigure(0, weight=9)
        jobsFrame.grid_columnconfigure(1, weight=1)
        frame_reference['jobsFrame'] = jobsFrame

        return frame_reference

    def add_frame_components(self):
        self.add_parameter_fields()
        self.add_database_label()
        self.add_offline_database_button()
        self.add_purge_database_button()
        self.add_concat_database_button()
        self.add_entries_label()
        self.add_single_launch_components()

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
            text="No Preference",
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
        submitButton.grid(row=4, column=0, columnspan=5, sticky="NEWS")

        clearButton = tk.Button(
            using_frame,
            text="Clear",
            command=self.clear_filters
        )
        clearButton.grid(row=4, column=5, sticky="NEWS")

    def filter_results(self):
        if self.entries_initialized:
            filter_dict = {}
            filter_dict['location'] = self.parameter_fields['location_null'].get()
            filter_dict['state'] = self.parameter_fields['state'].get()
            filter_dict['city'] = self.parameter_fields['city'].get()
            filter_dict['tags'] = self.parameter_fields['tags'].get()
            filter_dict['title'] = self.parameter_fields['title'].get()
            filter_dict['company'] = self.parameter_fields['company'].get()
            filter_dict['remote'] = self.parameter_fields['remote'].get()

            and_results = True if self.parameter_fields['results'].get() == "AND" else False
            self.interface.filter_entries(filter_dict, and_results)
            self.entry_list = self.interface.all_entries
            self.write_entries_to_text()
        else:
            print('Database entries not initialized')

    def clear_filters(self):
        self.parameter_fields['state'].set('')
        self.parameter_fields['city'].set('')
        self.parameter_fields['tags'].set('')
        self.parameter_fields['title'].set('')
        self.parameter_fields['company'].set('')

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

    def add_single_launch_components(self):
        using_frame = self.frames['infoFrame']
        selectFrame = tk.Frame(
            using_frame,
            width=using_frame['width']
        )
        selectFrame.grid(row=0, column=0)

        selectIdLabel = tk.Label(
            selectFrame,
            text="Enter ID Of Job: "
        )
        selectIdLabel.grid(row=0, column=0)

        selectIdEntry = tk.Entry(
            selectFrame
        )
        selectIdEntry.grid(row=0, column=1)
        self.current_info_dict['id'] = selectIdEntry

        selectIdButton = tk.Button(
            selectFrame,
            text="Get Info",
            command=self.get_single_job_info
        )
        selectIdButton.grid(row=0, column=2)

        titleFrame = tk.Frame(
            using_frame,
            # width=using_frame
        )
        titleFrame.grid_columnconfigure(0, weight=1)
        titleFrame.grid_columnconfigure(1, weight=3)
        titleFrame.grid(row=1, column=0)

        titleLabel = tk.Label(
            titleFrame,
            text="Title: "
        )
        titleLabel.grid(row=0, column=0)

        titleEntry = tk.Entry(
            titleFrame
        )
        titleEntry.grid(row=0, column=1)
        self.current_info_dict['title'] = titleEntry

        companyFrame = tk.Frame(
            using_frame,
        )
        companyFrame.grid_columnconfigure(0, weight=1)
        companyFrame.grid_columnconfigure(1, weight=3)
        companyFrame.grid(row=2, column=0)

        companyLabel = tk.Label(
            companyFrame,
            text="Company: "
        )
        companyLabel.grid(row=0, column=0)

        companyEntry = tk.Entry(
            companyFrame
        )
        companyEntry.grid(row=0, column=1)
        self.current_info_dict['company'] = companyEntry

        linkFrame = tk.Frame(
            using_frame
        )
        linkFrame.grid_columnconfigure(0, weight=1)
        linkFrame.grid_columnconfigure(1, weight=2)
        linkFrame.grid(row=3, column=0)

        linkLabel = tk.Label(
            linkFrame,
            text="Link: "
        )
        linkLabel.grid(row=0, column=0)

        linkEntry = tk.Entry(
            linkFrame
        )
        linkEntry.grid(row=0, column=1)
        self.current_info_dict['link'] = linkEntry

        tagsFrame = tk.Frame(
            using_frame
        )
        tagsFrame.grid_columnconfigure(0, weight=1)
        tagsFrame.grid_columnconfigure(1, weight=2)
        tagsFrame.grid(row=4, column=0)

        tagsLabel = tk.Label(
            tagsFrame,
            text="Tags: "
        )
        tagsLabel.grid(row=0, column=0)

        tagsEntry = tk.Entry(
            tagsFrame
        )
        tagsEntry.grid(row=0, column=1)
        self.current_info_dict['tags'] = tagsEntry

        stateFrame = tk.Frame(
            using_frame
        )
        stateFrame.grid_columnconfigure(0, weight=1)
        stateFrame.grid_columnconfigure(1, weight=2)
        stateFrame.grid(row=5, column=0)

        stateLabel = tk.Label(
            stateFrame,
            text="State: "
        )
        stateLabel.grid(row=0, column=0)

        stateEntry = tk.Entry(
            stateFrame
        )
        stateEntry.grid(row=0, column=1)
        self.current_info_dict['state'] = stateEntry

        cityFrame = tk.Frame(
            using_frame
        )
        cityFrame.grid_columnconfigure(0, weight=1)
        cityFrame.grid_columnconfigure(1, weight=2)
        cityFrame.grid(row=6, column=0)

        cityLabel = tk.Label(
            cityFrame,
            text="City: "
        )
        cityLabel.grid(row=0, column=0)

        cityEntry = tk.Entry(
            cityFrame
        )
        cityEntry.grid(row=0, column=1)
        self.current_info_dict['city'] = cityEntry

        remoteFrame = tk.Frame(
            using_frame
        )
        remoteFrame.grid_columnconfigure(0, weight=1)
        remoteFrame.grid_columnconfigure(1, weight=2)
        remoteFrame.grid(row=7, column=0)

        remoteLabel = tk.Label(
            remoteFrame,
            text="Allows Remote: "
        )
        remoteLabel.grid(row=0, column=0)

        remoteEntry = tk.Entry(
            remoteFrame
        )
        remoteEntry.grid(row=0, column=1)
        self.current_info_dict['remote'] = remoteEntry

        summaryLabel = tk.Label(
            using_frame,
            text="Summary: "
        )
        summaryLabel.grid(row=8, column=0)

        summaryFrame = tk.Frame(
            using_frame,
        )
        summaryFrame.grid(row=9, column=0, columnspan=3)

        summaryText = tk.Text(
            summaryFrame,
            wrap=tk.WORD,
            width=64,
            height=34
        )
        summaryText.grid(row=0, column=0, stick="NEWS")
        summaryText.config(background="#eeeeee")
        self.current_info_dict['summary'] = summaryText



    def get_single_job_info(self):
        entry_id = self.current_info_dict['id'].get()
        current_entry = self.interface.get_single_entry(int(entry_id))
        self.current_info_dict['title'].delete(0, tk.END)
        self.current_info_dict['title'].insert(tk.END, current_entry[TITLE_INDEX])
        self.current_info_dict['company'].delete(0, tk.END)
        self.current_info_dict['company'].insert(tk.END, current_entry[COMPANY_INDEX])
        self.current_info_dict['link'].delete(0, tk.END)
        self.current_info_dict['link'].insert(tk.END, current_entry[LINK_INDEX])
        self.current_info_dict['tags'].delete(0, tk.END)
        self.current_info_dict['tags'].insert(tk.END, current_entry[TAGS_INDEX])
        self.current_info_dict['state'].delete(0, tk.END)
        self.current_info_dict['state'].insert(tk.END, current_entry[STATE_INDEX] if current_entry[STATE_INDEX] is not None else 'None')
        self.current_info_dict['city'].delete(0, tk.END)
        self.current_info_dict['city'].insert(tk.END, current_entry[CITY_INDEX] if current_entry[CITY_INDEX] is not None else 'None')
        self.current_info_dict['remote'].delete(0, tk.END)
        self.current_info_dict['remote'].insert(tk.END, "YES" if current_entry[REMOTE_INDEX] == 1 else "NO")
        self.current_info_dict['summary'].delete('1.0', tk.END)
        self.current_info_dict['summary'].insert(tk.END, html2text(current_entry[SUMMARY_INDEX]))


    def init_offline_database(self):
        if not self.entries_initialized:
            print('Offline Working')
            self.write_entries_to_text()
            self.entries_initialized = True

    def init_purge_database(self):
        if not self.entries_initialized:
            print('Purge Working')
            self.write_entries_to_text()
            self.entries_initialized = True

    def init_concat_database(self):
        if not self.entries_initialized:
            print('Concat Working')
            self.write_entries_to_text()
            self.entries_initialized = True

    def write_entries_to_text(self):
        self.entryScrolledText.config(state=tk.NORMAL)
        self.entryScrolledText.delete(1.0, tk.END)
        for i in range(len(self.entry_list)):
            self.write_single_entry_to_text(self.entry_list[i], i)
        self.entryScrolledText.config(state=tk.DISABLED)

    def write_single_entry_to_text(self, entry, row):
        entry_id = self.format_to_length(str(entry[ID_INDEX]), 11)
        entry_title = self.format_to_length(str(entry[TITLE_INDEX]), 38)
        entry_company = self.format_to_length(str(entry[COMPANY_INDEX]), 26)
        entry_state = self.format_to_length(str(entry[STATE_INDEX]), 14)
        entry_city = self.format_to_length(str(entry[CITY_INDEX]), 21)
        entry_published = self.format_to_length(str(entry[PUBLISHED_INDEX]), 24)

        self.entryScrolledText.insert(
            tk.END, f'{entry_id}{entry_title}{entry_company}{entry_state}{entry_city}{entry_published}\n')

    def format_to_length(self, attribute, length):
        if len(attribute) > length:
            return attribute[:length-4] + '... '
        else:
            return attribute + ' ' * (length - len(attribute))

    def sort_entries_by_id(self):
        print('Sorting by id: ', end='')
        self.entry_list.sort(key=lambda x: x[ID_INDEX])
        if self.sort_order['id'] == 'ASC':
            self.sort_order['id'] = 'DESC'
            print('Ascending')
        else:
            self.sort_order['id'] = 'ASC'
            self.entry_list = list(reversed(self.entry_list))
            print('Descending')
        self.write_entries_to_text()

    def sort_entries_by_title(self):
        print('Sorting by title: ', end='')
        self.entry_list.sort(key=lambda x: x[TITLE_INDEX])
        if self.sort_order['title'] == 'ASC':
            self.sort_order['title'] = 'DESC'
            print('Ascending')
        else:
            self.sort_order['title'] = 'ASC'
            self.entry_list = list(reversed(self.entry_list))
            print('Descending')
        self.write_entries_to_text()

    def sort_entries_by_company(self):
        print('Sorting by company: ', end='')
        self.entry_list.sort(key=lambda x: x[COMPANY_INDEX])
        if self.sort_order['company'] == 'ASC':
            self.sort_order['company'] = 'DESC'
            print('Ascending')
        else:
            self.sort_order['company'] = 'ASC'
            self.entry_list = list(reversed(self.entry_list))
            print('Descending')
        self.write_entries_to_text()

    def sort_entries_by_state(self):
        print('Sorting by state: ', end='')
        self.entry_list.sort(key=lambda x: x[STATE_INDEX] if x[STATE_INDEX] is not None else '-')
        if self.sort_order['state'] == 'ASC':
            self.sort_order['state'] = 'DESC'
            print('Ascending')
        else:
            self.sort_order['state'] = 'ASC'
            self.entry_list = list(reversed(self.entry_list))
            print('Descending')
        self.write_entries_to_text()

    def sort_entries_by_published(self):
        print('Sorting by published: ', end='')
        self.entry_list.sort(key=lambda x: x[PUBLISHED_INDEX])
        if self.sort_order['published'] == 'ASC':
            self.sort_order['published'] = 'DESC'
            print('Ascending')
        else:
            self.sort_order['published'] = 'ASC'
            self.entry_list = list(reversed(self.entry_list))
            print('Descending')
        self.write_entries_to_text()
