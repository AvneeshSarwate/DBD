#!/usr/bin/env python
   2 
   3 # popup.py
   4 
   5 import wx
   6 
   7 app = wx.PySimpleApp()
   8 
   9 class MyPopupMenu(wx.Menu):
  10     def __init__(self, WinName):
  11         wx.Menu.__init__(self)
  12 
  13         self.WinName = WinName
  14         item = wx.MenuItem(self, wx.NewId(), "Item One")
  15         self.AppendItem(item)
  16         self.Bind(wx.EVT_MENU, self.OnItem1, item)
  17         item = wx.MenuItem(self, wx.NewId(),"Item Two")
  18         self.AppendItem(item)
  19         self.Bind(wx.EVT_MENU, self.OnItem2, item)
  20         item = wx.MenuItem(self, wx.NewId(),"Item Three")
  21         self.AppendItem(item)
  22         self.Bind(wx.EVT_MENU, self.OnItem3, item)
  23 
  24     def OnItem1(self, event):
  25         print "Item One selected in the %s window"%self.WinName
  26 
  27     def OnItem2(self, event):
  28         print "Item Two selected in the %s window"%self.WinName
  29 
  30     def OnItem3(self, event):
  31         print "Item Three selected in the %s window"%self.WinName
  32 
  33 class MyWindow(wx.Window):
  34     def __init__(self, parent, color):
  35         wx.Window.__init__(self, parent, -1)
  36         self.color = color
  37         self.SetBackgroundColour(color)
  38         self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
  39 
  40     def OnRightDown(self,event):
  41         self.PopupMenu(MyPopupMenu(self.color), event.GetPosition())
  42 
  43 class MyFrame(wx.Frame):
  44     def __init__(self):
  45         wx.Frame.__init__(self,None, -1, "Test", size=(300, 200))
  46         sizer = wx.GridSizer(2,2,5,5)
  47         sizer.Add(MyWindow(self,"blue"),1,wx.GROW)
  48         sizer.Add(MyWindow(self,"yellow"),1,wx.GROW)
  49         sizer.Add(MyWindow(self,"red"),1,wx.GROW)
  50         sizer.Add(MyWindow(self,"green"),1,wx.GROW)
  51         self.SetSizer(sizer)
  52         self.Show()
  53 
  54 frame = MyFrame()
  55 app.SetTopWindow(frame)
  56 app.MainLoop()
