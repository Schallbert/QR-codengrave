import tkinter as tk
from tkinter import ttk

from webbrowser import open_new


def _callback(url):
    open_new(url)


class GuiStatusBar:
    def __init__(self, main, options):
        self._main = main
        self._options = options

        self.frame = self._init_status_bar()

    def set_status_ready(self):
        self._status_label.config(foreground='#00A877', text='Status: \u2713 Ready')
        pass

    def set_status_not_ready(self):
        self._status_label.config(foreground='black', text='Status: \u231b Not Ready')

    def set_status_text(self, text):
        self._status_label.config(foreground='black', text='Status: ' + text)

    def set_job_duration(self, td):
        self._duration_label.config(text='Estimated job duration: ' + str(td))

    def set_qr_size(self, millimeters):
        self._size_label.config(text='QR-code size: {:.0f}'.format(millimeters) + 'x{:.0f}'.format(millimeters) + 'mm')

    def _init_status_bar(self):
        status_bar_frame = tk.Frame(bd=5)
        status_bar_frame['relief'] = 'flat'
        status_bar_frame.grid(column=0, row=5, columnspan=5, sticky='SW', **self._options)

        # Status
        self._status_label = ttk.Label(status_bar_frame, width=18)
        self.set_status_not_ready()
        self._status_label.grid(column=0, row=0, sticky='W', **self._options)

        # Estimated job duration ' hh:mm:ss '
        self._duration_label = ttk.Label(status_bar_frame, text='Estimated job duration: Unknown', width=32)
        self._duration_label.grid(column=1, row=0, sticky='W', **self._options)

        # Estimated QR-code size ' nnn x nnn mm '
        self._size_label = ttk.Label(status_bar_frame, text='QR-code size: Unknown', width=32)
        self._size_label.grid(column=2, row=0, sticky='W', **self._options)

        # Estimated QR-code size ' nnn x nnn mm '

        self._schallbert_label = ttk.Label(status_bar_frame, text='\xa9 Schallbert 2023',
                                           foreground='#00A877', cursor="hand2", width=17)
        self._schallbert_label.grid(column=3, row=0, sticky='E', **self._options)
        self._schallbert_label.bind("<Button-1>", lambda e: _callback('https://schallbert.de/'))

        return status_bar_frame
