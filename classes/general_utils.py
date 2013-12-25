# -*- coding: utf-8 -*-
import wx

error_messages = {'2': 'File not found'}


class utils:

    def error_alert_box(self, message):
        wx.MessageBox('{message}\nStory listing will be removed, re-add manually.'.format(message=message),
             'Error', wx.OK | wx.ICON_ERROR)
