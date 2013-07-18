'''
Created on May 1, 2013

@author: avneeshsarwate
'''
'''
Created on Mar 23, 2013

@author: avneeshsarwate
'''
#!/usr/bin/python

# repository.py

import wx
import sys
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
import OSC

packages = [('abiword', '5.8M', 'base'), ('adie', '145k', 'base'),
    ('airsnort', '71k', 'base'), ('ara', '717k', 'base'), ('arc', '139k', 'base'),
    ('asc', '5.8M', 'base'), ('ascii', '74k', 'base'), ('ash', '74k', 'base')]

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)


class Repository(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(450, 400))

        panel = wx.Panel(self, -1)
        vert = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vert)
        
        #---------------------------------------------------
#        vertmain = wx.BoxSizer(wx.VERTICAL)
#        tophor = wx.BoxSizer(wx.HORIZONTAL)
#        midhor = wx.BoxSizer(wx.HORIZONTAL)
#        hormain = wx.BoxSizer(wx.HORIZONTAL)
#        leftvert = wx.BoxSizer(wx.VERTICAL)
#        rightvert = wx.BoxSizer(wx.VERTICAL)
#        leftbuttons = wx.BoxSizer(wx.HORIZONTAL)
#        rightbuttons = wx.BoxSizer(wx.HORIZONTAL)
        
        #----------------------------------------------------
        
        horpan1 = wx.Panel(panel, -1)
        hor1 = wx.BoxSizer(wx.HORIZONTAL)
        horpan1.SetSizer(hor1)
        txt = wx.TextCtrl(horpan1, -1)
        self.button = wx.Button(horpan1, -1, 'Enter', size=(100, -1))
        self.button.num = 1
        self.button.mes = "mes"
        label = wx.StaticText(horpan1, -1, label="Table 1 - Dish/Status:")
        hor1.Add(label)
        hor1.Add(txt)
        hor1.Add(self.button)
        vert.Add(horpan1)
        
        horpan2 = wx.Panel(panel, -1)
        hor2 = wx.BoxSizer(wx.HORIZONTAL)
        horpan2.SetSizer(hor2)
        txt2 = wx.TextCtrl(horpan2, -1)
        self.button2 = wx.Button(horpan2, -1, 'Enter', size=(100, -1))
        self.button2.num = 2
        self.button2.mes = "mes"
        label2 = wx.StaticText(horpan2, -1, label="Table 2 - Dish/Status:")
        hor2.Add(label2)
        hor2.Add(txt2)
        hor2.Add(self.button2)
        vert.Add(horpan2)
        
        horpan3 = wx.Panel(panel, -1)
        hor3 = wx.BoxSizer(wx.HORIZONTAL)
        horpan3.SetSizer(hor3)
        txt3 = wx.TextCtrl(horpan3, -1)
        self.button3 = wx.Button(horpan3, -1, 'Enter', size=(100, -1))
        self.button3.num = 3
        self.button3.mes = "mes"
        label3 = wx.StaticText(horpan3, -1, label="Table 3 - Dish/Status:")
        hor3.Add(label3)
        hor3.Add(txt3)
        hor3.Add(self.button3)
        vert.Add(horpan3)
        
        horpan4 = wx.Panel(panel, -1)
        hor4 = wx.BoxSizer(wx.HORIZONTAL)
        horpan4.SetSizer(hor4)
        txt4 = wx.TextCtrl(horpan4, -1)
        self.button4 = wx.Button(horpan4, -1, 'Enter', size=(100, -1))
        self.button4.num = 4
        self.button4.mes = "cup"
        label4 = wx.StaticText(horpan4, -1, label="Cup Update")
        hor4.Add(label4)
        hor4.Add(txt4)
        hor4.Add(self.button4)
        vert.Add(horpan4)
        
    
        
        self.Bind(wx.EVT_BUTTON, self.pressed)
        self.butlis = []
        self.butlis.append(txt)
        self.butlis.append(txt2)
        self.butlis.append(txt3)
        self.butlis.append(txt4)
        
        self.Centre()
        self.Show(True)
        
    def pressed(self, event):
        client = OSC.OSCClient()
        client.connect( ('128.112.70.168', 6349) )  
        mes = OSC.OSCMessage()
        mes.setAddress("/admin")
        strls = self.butlis[event.GetEventObject().num-1].GetValue().split(" ")
        tokens = []
        if event.GetEventObject().mes == "mes":
            tokens.append(str(event.GetEventObject().num))
            tokens.append("up")
        for i in strls:
            if i != "":
                tokens.append(i)
        if event.GetEventObject().mes == "cup":
            tokens.insert(1, "cup")
        strmes = " ".join(tokens)
        print strmes
        mes.append(strmes)
        client.send(mes)
        mes.clearData()
        
        #---------------------------------------------------

#        vbox = wx.BoxSizer(wx.VERTICAL)
#        hbox = wx.BoxSizer(wx.HORIZONTAL)
#        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
#
#        leftPanel = wx.Panel(panel, -1)
#        rightPanel = wx.Panel(panel, -1)
#
#        self.log = wx.TextCtrl(rightPanel, -1, style=wx.TE_MULTILINE)
#        self.list = CheckListCtrl(rightPanel)
#        self.list.InsertColumn(0, 'Package', width=140)
#        self.list.InsertColumn(1, 'Size')
#        self.list.InsertColumn(2, 'Repository')
#
#        for i in packages:
#            index = self.list.InsertStringItem(1, i[0])
#            print index
#            self.list.SetStringItem(index, 1, i[1])
#            self.list.SetStringItem(index, 2, i[2])
#
#        vbox2 = wx.BoxSizer(wx.VERTICAL)
#
#        sel = wx.Button(leftPanel, -1, 'Select All', size=(100, -1))
#        des = wx.Button(leftPanel, -1, 'Deselect All', size=(100, -1))
#        apply = wx.Button(leftPanel, -1, 'Apply', size=(100, -1))
#
#
#        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=sel.GetId())
#        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, id=des.GetId())
#        self.Bind(wx.EVT_BUTTON, self.OnApply, id=apply.GetId())
#
#        vbox2.Add(sel, 0, wx.TOP, 5)
#        vbox2.Add(des)
#        vbox2.Add(apply)
#
#        leftPanel.SetSizer(vbox2)
#
#        vbox.Add(self.list, 1, wx.EXPAND | wx.TOP, 3)
#        vbox.Add((-1, 10))
#        vbox.Add(self.log, 0.5, wx.EXPAND)
#        vbox.Add((-1, 10))
#
#        rightPanel.SetSizer(vbox)
#
#        hbox.Add(leftPanel, 0, wx.EXPAND | wx.RIGHT, 5)
#        hbox.Add(rightPanel, 1, wx.EXPAND)
#        hbox.Add((3, -1))
#
#        panel.SetSizer(hbox)
#
        

    def OnSelectAll(self, event):
        print "dos"
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i)

    def OnDeselectAll(self, event):
        print "dos"
        num = self.list.GetItemCount()
        for i in range(num):
            self.list.CheckItem(i, False)

    def OnApply(self, event):
        print "mofo"
        num = self.list.GetItemCount()
        for i in range(num):
            if i == 0: self.log.Clear()
            if self.list.IsChecked(i):
                print "boi", i
                self.log.AppendText(self.list.GetItemText(i) + '\n')

app = wx.App()
Repository(None, -1, 'Repository')
app.MainLoop()
