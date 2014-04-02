import wx
from gui_parts.Fan_Fiction_Download_Page import DownloadFanfiction
from gui_parts.Fan_Fiction_Read_Page import ReadFanfiction
from gui_parts.Fan_Fiction_Convert_Page import ConvertFanfiction


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Simple Notebook Example")

#-----------Menubar here ------------------#
        menubar = wx.MenuBar()

        file_menu = wx.Menu()
#        edit_menu = wx.Menu()
#        view_menu = wx.Menu()
        help_menu = wx.Menu()

#        file_menu.Append(101, '&Open', 'Open')
#        file_menu.Append(102, '&Save', 'Save')
        file_menu.Append(103, '&Quit', 'Quit')

#        edit_menu.Append(201, '&Copy', 'Copy')
#        edit_menu.Append(202, '&Cut', 'Cut')
#        edit_menu.Append(203, '&Paste', 'Paste')

        help_menu.Append(301, '&About', 'About')
        help_menu.Append(302, '&Help', 'Help')

        menubar.Append(file_menu, '&File')
#       menubar.Append(edit_menu, '&Edit')
        menubar.Append(help_menu, '&Help')
        wx.EVT_MENU(self, 103, self.on_quit)

        self.SetMenuBar(menubar)

        # Here we create a panel and a notebook on the panel
        panel = wx.Panel(self)
        notebook = wx.Notebook(panel)

        # create the page windows as children of the notebook
        self.download_page = DownloadFanfiction(notebook)
        self.read_page = ReadFanfiction(notebook)
        self.convert_page = ConvertFanfiction(notebook)

        # add the pages to the notebook with the label to show on the tab
        notebook.AddPage(self.download_page, "Download")
        notebook.AddPage(self.read_page, "Read")
        notebook.AddPage(self.convert_page, "Convert")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1, wx.EXPAND)
        self.SetMinSize((900, 600))
        panel.SetSizer(sizer)
        self.Maximize(True)

        # bindings here - change if possible
        self.download_page.url_button.Bind(wx.EVT_BUTTON, self.download_page.on_click)
        self.download_page.location_button.Bind(wx.EVT_BUTTON, self.download_page.choose_location)
        self.download_page.library.Bind(wx.EVT_LISTBOX_DCLICK, self.download_page.lib_click)

        self.read_page.next_page_button.Bind(wx.EVT_BUTTON, self.read_page.next_page)
        self.read_page.previous_page_button.Bind(wx.EVT_BUTTON, self.read_page.back_page)
        self.read_page.sec_next_page_button.Bind(wx.EVT_BUTTON, self.read_page.next_page)
        self.read_page.sec_prev_page_button.Bind(wx.EVT_BUTTON, self.read_page.back_page)
        self.read_page.open_folder_button.Bind(wx.EVT_BUTTON, self.read_page.choose_location)
        # Click list item to switch to chapter
        self.read_page.jump_to_list.Bind(wx.EVT_LISTBOX, self.read_page.jump)
        # Mouse scroll down
        self.read_page.html_window.Bind(wx.EVT_SCROLLWIN_LINEDOWN, self.read_page.get_pos_down)
        # Mouse scroll up
        self.read_page.html_window.Bind(wx.EVT_SCROLLWIN_LINEUP, self.read_page.get_pos_up)
        #Capture keydown events when reading
        self.read_page.html_window.Bind(wx.EVT_KEY_DOWN, self.read_page.page_up_down_shortcut)
        self.convert_page.choose_location_button.Bind(wx.EVT_BUTTON, self.convert_page.choose_location)

    def on_quit(self, event):
        """docstring for on"""
        self.Close()

if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
