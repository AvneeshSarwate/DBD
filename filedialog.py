'''
Created on Apr 13, 2013

@author: avneeshsarwate
'''
import wx
 
wildcard = "Python source (*.py; *.pyc)|*.py;*.pyc|" \
         "All files (*.*)|*.*"
 
########################################################################
class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Multi-file type wx.FileDialog Tutorial")
        panel = wx.Panel(self, wx.ID_ANY)
 
        btn = wx.Button(panel, label="Open File Dialog")
        btn.Bind(wx.EVT_BUTTON, self.onOpenFile)
 
     #----------------------------------------------------------------------
    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultFile="",
            wildcard=wildcard,
            style=wx.SAVE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            print "You chose the following file(s):"
            for path in paths:
                print path
        dlg.Destroy()
 
#----------------------------------------------------------------------
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()