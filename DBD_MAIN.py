#!/usr/bin/python

# repository.py

import wx
import sys
from music21 import *
from music21 import midi
from pprint import pprint
from wx.lib.mixins.listctrl import CheckListCtrlMixin, ListCtrlAutoWidthMixin
import wx.lib.mixins.listctrl  as  listmix
import phrase
import features
import time
import os
import shutil
import random
import Levenshtein as lv
import subprocess
import pickle

class EditableListCtrl(wx.ListCtrl, listmix.TextEditMixin):
    ''' TextEditMixin allows any column to be edited. '''
 
    #----------------------------------------------------------------------
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        """Constructor"""
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)

packages = [(' ', '5.8Maaaaaaaaaaaa', 'base'), (' ', '145k', 'base'),
    (' ', '71k', 'base'), (' ', '717k', 'base'), (' ', '139k', 'base'),
    (' ', '5.8M', 'base'), (' ', '74k', 'base'), (' ', '74k', 'base')]

class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin, ListCtrlAutoWidthMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        CheckListCtrlMixin.__init__(self)
        ListCtrlAutoWidthMixin.__init__(self)

class IntObj():
    def __int__(self):
        self.phrase = phrase.Phrase()
        self.file = ""
        self.features = []
        self.tag = ""

objs = {}




class Trans(wx.Frame):
    def __init__(self, parent, id, title, objs):
        wx.Frame.__init__(self, parent, id, title, size=(750, 400))

        panel = wx.Panel(self, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hboxdrop = wx.BoxSizer(wx.HORIZONTAL)
        hboxsrc = wx.BoxSizer(wx.HORIZONTAL)
        

        leftPanel = wx.Panel(panel, -1)
        rightPanel = wx.Panel(panel, -1)
        topRowPan = wx.Panel(rightPanel, -1)
        dropPanel = wx.Panel(rightPanel, -1)
        srcpanel = wx.Panel(rightPanel, -1)
        
        srcpanel.SetSizer(hboxsrc)
        
        srclabel = wx.StaticText(srcpanel, -1, label="melody filename:")
        self.srctext = wx.TextCtrl(srcpanel, -1)
        srcbutton = wx.Button(srcpanel, -1, 'Browse', size=(100, -1))
        
        hboxsrc.Add(srclabel)
        hboxsrc.Add(self.srctext)
        hboxsrc.Add(srcbutton)
        
        

        #self.log = wx.TextCtrl(rightPanel, -1, style=wx.TE_MULTILINE)
        self.list = wx.ListCtrl(rightPanel, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'Melody', width=140)
        

        

        vbox2 = wx.BoxSizer(wx.VERTICAL)

        save = wx.Button(leftPanel, -1, 'Save Melody', size=(100, -1))

        view = wx.Button(topRowPan, -1, 'View', size=(100, -1))
        play = wx.Button(topRowPan, -1, 'Play', size=(100, -1))
        pos = wx.Button(topRowPan, -1, 'Tag Pos', size=(100, -1))
        neg = wx.Button(topRowPan, -1, 'Tag Neg', size=(100, -1))


        vbox2.Add(save, 0, wx.TOP, 50)

        hbox2.Add(play)
        hbox2.Add(view)
        hbox2.Add(pos)
        hbox2.Add(neg)
        
        topRowPan.SetSizer(hbox2)

        leftPanel.SetSizer(vbox2)

        self.concepts = [i.replace("\n", "") for i in open("log.txt").readlines()]    
        self.concept = self.concepts[0].replace("\n", "")
        conceptlabel = wx.StaticText(dropPanel, label="Concept:")
        self.cbox = wx.ComboBox(dropPanel, choices=self.concepts)
        
        percents = [str(i)+"%" for i in range(-90, 100, 10)]
        percentlabel = wx.StaticText(dropPanel, label="Range:")
        self.cbox2 = wx.ComboBox(dropPanel, choices=percents)
        
        vals = [str(i+1) for i in range(10)]
        numlabel = wx.StaticText(dropPanel, label="# results:")
        self.cbox3= wx.ComboBox(dropPanel, choices=vals)
        
        trans = wx.Button(dropPanel, -1, 'Transform!', size=(100, -1))
        
        hboxdrop.Add(conceptlabel)
        hboxdrop.Add(self.cbox)
        hboxdrop.Add(percentlabel)
        hboxdrop.Add(self.cbox2)
        hboxdrop.Add(numlabel)
        hboxdrop.Add(self.cbox3)
        hboxdrop.Add(trans)
        

        dropPanel.SetSizer(hboxdrop)
        
        vbox.Add(srcpanel)
        vbox.Add(dropPanel)
        vbox.Add(topRowPan)
        vbox.Add(self.list, 1, wx.EXPAND)
        
        #vbox.Add((-1, 10))

        rightPanel.SetSizer(vbox)


        hbox.Add(leftPanel, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(rightPanel, 1, wx.EXPAND)
        hbox.Add((3, -1))

        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)

        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        
        self.Bind(wx.EVT_BUTTON, self.onOpenFile, id=srcbutton.GetId())
        self.Bind(wx.EVT_BUTTON, self.onPlay, id=play.GetId())
        self.Bind(wx.EVT_BUTTON, self.onTrans, id=trans.GetId())
        self.Bind(wx.EVT_BUTTON, self.onSave, id=save.GetId())
        self.wildcard = ".mid"
        self.srcmel = 5
    
    def onPlay(self, event):
        phrase.play(self.finalvars[self.seli][2]) #??    
        
    def onTrans(self, event):
        self.list.DeleteAllItems()
        varList = []
        varList.append(self.srcmel)
        print type(varList[random.randrange(len(varList))])
        for i in range(100):
            varList.append(lv.supermorph(varList[random.randrange(len(varList))], 10))
        print "done making vars"
        
        pickle.dump(varList, open("pick", "w+"))
        
        arffhead = open("arff.txt").read()
        arffList = []
        arffList.append(arffhead)
        for i in range(len(varList)):
            if i % 100 == 0:
                print i
            feat = features.vect(features.phraseToScore(varList[i]))
            for j in feat:
                arffList.append(str(j) + ", ")
            arffList.append("neg \n")
        print "enough things in arfflist", len(arffList) == 7*len(varList)+1
        
        arffString = "".join(arffList)
        print "done calculating features"
        print arffString
        arffFile = open(self.concept + "/" + "test.arff", "w+")
        arffFile.write(arffString)
        arffFile.close()
        print "done making testfile"
#        return
#        varList = pickle.load(open("pick"))
        subprocess.call(["java","-classpath", ".:weka.jar", "Trainer", self.concept], stdout=open(self.concept+"/res.txt", "w+"))    
        
        res = open(self.concept + "/res.txt").read().split("\n")
        resvals = [float(i) for i in res[0:len(res)-1]]
        if resvals[len(resvals)-1] == "":
            resvals.pop()
        dists = [lv.levd(self.srcmel.n, i.n)+lv.levd(self.srcmel.t, i.t) for i in varList]
        sortpair = [(resvals[i], dists[i], varList[i]) for i in range(len(varList))]
        print "optlist made"
        def classComp0(x, y):
            if x[0]-y[0] > 0:
                return 1
            if x[0]-y[0] < 0:
                return -1
            if x[0]-y[0] == 0:
                return 0
        
        def classComp1(x, y):
            return x[1]-y[1]
        
        sortpair.sort(classComp0)
        
        percentage = ((float(self.cbox2.GetValue().split("%")[0]) / 2) + 50) / 100
        maxv = percentage + .025
        minv = percentage - .025
        
        mini = -1
        maxi = -1
        for i in range(len(sortpair)):
            if mini < 0 and sortpair[i][0] > minv:
                mini = i
            if maxi < 0 and sortpair[i][0] > maxv:
                maxi = i
            print mini, maxi , "mini maxi", sortpair[i][0], minv, maxv
        
        print mini, maxi , "mini maxi final"        
        
        crange = sortpair[mini:maxi]
        if len(crange) == 0:
            crange = sortpair[int(minv*100):int(maxv*100)]
        crange.sort(classComp1)
        
        numchoice = int(self.cbox3.GetValue())
        print len(crange), 'crange'
        print numchoice, "numchoice"
        self.finalvars = crange[0:numchoice]
        print "best choices selected"
        print len(self.finalvars), "finvars"
        for i in range(len(self.finalvars)):
            print i, "blagahba"
            self.list.InsertStringItem(i, self.concept+self.cbox2.GetValue()+str(i))
        
            
        
        
        
    
        
        
    def onOpenFile(self, event):
        """
        Create and show the Open FileDialog
        """
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=str(os.path.dirname(os.path.abspath(__file__))), 
            defaultFile="",
            wildcard=self.wildcard,
            style=wx.OPEN | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            
            paths = dlg.GetPaths()
            print "You chose the following file(s):"
            for path in paths:
                self.srcmel = features.scoreToPhrase(converter.parse(path))
                print path
                print self.srcmel
                self.srctext.Clear()
                self.srctext.write(path.split("/")[len((path.split("/")))-1])
        dlg.Destroy()

    def OnSelect(self, event):
        #print dir(event)
        self.seli = event.Index
        print event.Index
        print self.cbox.GetCurrentSelection()
        
    def onSave(self, event):
        """
        Create and show the Save FileDialog
        """
        srcdir = str(os.path.dirname(os.path.abspath(__file__)))
        dlg = wx.FileDialog(
            self, message="Save file as ...", 
            defaultDir=srcdir, 
            defaultFile="", wildcard=self.wildcard, style=wx.SAVE
            )
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "You chose the following filename: %s" % path
            sc = features.phraseToScore(self.finalvars[self.seli][2])
            midfile = midi.translate.streamToMidiFile(sc)
            
            print path, "yolo here"
            midfile.open(path, "wb")
            midfile.write()
            midfile.close()
            
        dlg.Destroy()

class Gen(wx.Frame):
    def __init__(self, parent, id, title, objs, session):
        wx.Frame.__init__(self, parent, id, title, size=(750, 400))

        self.session = session
        self.objs = objs 
        self.phrases = []
        self.sessioncount = 0
        self.seli = -1
        
        panel = wx.Panel(self, -1)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hboxsend = wx.BoxSizer(wx.HORIZONTAL)
        

        leftPanel = wx.Panel(panel, -1)
        rightPanel = wx.Panel(panel, -1)
        topRowPan = wx.Panel(rightPanel, -1)
        sendpan = wx.Panel(rightPanel, -1)
        

        #self.log = wx.TextCtrl(rightPanel, -1, style=wx.TE_MULTILINE)
        self.list = wx.ListCtrl(rightPanel, style=wx.LC_REPORT)
        self.list.InsertColumn(0, 'Name', width=140)


        vbox2 = wx.BoxSizer(wx.VERTICAL)
        
        pos = wx.Button(leftPanel, -1, 'Tag Pos', size=(100, -1))
        neg = wx.Button(leftPanel, -1, 'Tag Neg', size=(100, -1))
        gen = wx.Button(leftPanel, -1, 'Generate More', size=(100, -1))

        view = wx.Button(topRowPan, -1, 'View', size=(100, -1))
        play = wx.Button(topRowPan, -1, 'Play', size=(100, -1))
        delete = wx.Button(topRowPan, -1, 'Delete', size=(100, -1))
        save = wx.Button(topRowPan, -1, 'Save Melody', size=(100, -1))
        


        vbox2.Add(pos, 0, wx.TOP, 50)
        vbox2.Add(neg)
        vbox2.Add(gen)

        hbox2.Add(play)
        hbox2.Add(view)
        hbox2.Add(save)
        hbox2.Add(delete)
        
        topRowPan.SetSizer(hbox2)

        leftPanel.SetSizer(vbox2)

     
        self.concepts = [i.replace("\n", "") for i in open("log.txt").readlines()]    
        self.cbox = wx.ComboBox(sendpan, choices=self.concepts)
        self.concept = self.concepts[0].replace("\n", "")
        
        sendlabel = wx.StaticText(sendpan, label="tag example for:")
        sendpan.SetSizer(hboxsend)
        hboxsend.Add(sendlabel)
        hboxsend.Add(self.cbox)
        
        
        vbox.Add(sendpan)
        vbox.Add(topRowPan)
        vbox.Add(self.list, 1, wx.EXPAND)
        
        #vbox.Add((-1, 10))

        rightPanel.SetSizer(vbox)


        hbox.Add(leftPanel, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(rightPanel, 1, wx.EXPAND)
        hbox.Add((3, -1))

        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.Bind(wx.EVT_BUTTON, self.genMel, id=gen.GetId())
        self.Bind(wx.EVT_BUTTON, self.onPos, id=pos.GetId())
        self.Bind(wx.EVT_BUTTON, self.onNeg, id=neg.GetId())
        self.Bind(wx.EVT_BUTTON, self.onDel, id=delete.GetId())
        self.Bind(wx.EVT_BUTTON, self.onSave, id=save.GetId())
        self.Bind(wx.EVT_BUTTON, self.onPlay, id=play.GetId())
        
        self.wildcard = ".mid" 
    
    def onPlay(self, event):
        phrase.play(self.phrases[self.seli])
        
    def onSave(self, event):
        """
        Create and show the Save FileDialog
        """
        srcdir = str(os.path.dirname(os.path.abspath(__file__)))
        dlg = wx.FileDialog(
            self, message="Save file as ...", 
            defaultDir=srcdir, 
            defaultFile="", wildcard=self.wildcard, style=wx.SAVE
            )
        
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "You chose the following filename: %s" % path
            sc = features.phraseToScore(self.phrases[self.seli])
            midfile = midi.translate.streamToMidiFile(sc)
            
            print path, "yolo here"
            midfile.open(path, "wb")
            midfile.write()
            midfile.close()
            
        dlg.Destroy()
    
    def genMel(self, event):
        for i in range(10):
            self.sessioncount += 1
            p = lv.randgen()
            self.phrases.insert(0, p)
            self.list.InsertStringItem(0, self.session+"_"+str(self.sessioncount))
            
        return
    
    def onDel(self, event):
        self.list.DeleteItem(self.seli)
        self.phrases = self.phrases[0:self.seli] + self.phrases[self.seli+1:len(self.phrases)]
    
    def onPos(self, event):
        self.concept = self.cbox.GetValue()
        ob = IntObj()
        ob.phrase = self.phrases[self.seli]
        sc = features.phraseToScore(ob.phrase)
        ob.file = self.list.GetItemText(self.seli, 0)
        print ob.file, "dagnabit"
        ob.features = features.vect(sc)
        ob.tag = "pos"
        print "postapocalptic"
        srcdir = str(os.path.dirname(os.path.abspath(__file__)))
        self.objs[self.concept][ob.file] = ob
        log  = open(srcdir + "/" + self.concept + "/" + "log.txt", "a")
        log.write("\n" + ob.file + " " + ob.tag + " " + "no")
        midfile = midi.translate.streamToMidiFile(sc)
        print srcdir + "/" + self.concept + "/" + ob.file + ".mid"
        midfile.open(srcdir + "/" + self.concept + "/" + ob.file + ".mid", "wb")
        midfile.write()
        midfile.close()
        new.listL.InsertStringItem(0, " ")
        new.listL.SetStringItem(0, 1, ob.file + ".mid")
        new.listL.SetStringItem(0, 2, ob.tag)
        new.objs[self.concept][ob.file + ".mid"] = ob
        
        
    def onNeg(self, event):
        self.concept = self.cbox.GetValue()
        ob = IntObj()
        ob.phrase = self.phrases[self.seli]
        sc = features.phraseToScore(ob.phrase)
        ob.file = self.list.GetItemText(self.seli, 0)
        print ob.file, "dagnabit"
        ob.features = features.vect(sc)
        ob.tag = "neg"
        print "postapocalptic"
        srcdir = str(os.path.dirname(os.path.abspath(__file__)))
        self.objs[self.concept][ob.file] = ob
        log  = open(srcdir + "/" + self.concept + "/" + "log.txt", "a")
        log.write("\n" + ob.file + " " + ob.tag + " " + "no")
        midfile = midi.translate.streamToMidiFile(sc)
        print srcdir + "/" + self.concept + "/" + ob.file + ".mid"
        midfile.open(srcdir + "/" + self.concept + "/" + ob.file + ".mid", "wb")
        midfile.write()
        midfile.close()
        new.listR.InsertStringItem(0, " ")
        new.listR.SetStringItem(0, 1, ob.file + ".mid")
        new.listR.SetStringItem(0, 2, ob.tag)
        new.objs[self.concept][ob.file + ".mid"] = ob

    def OnSelect(self, event):
        #print dir(event)
        self.seli = event.Index
        print event.Index
        print self.phrases[event.Index]


class NewOne(wx.Frame):
    def __init__(self, parent, id, title, objs):
        wx.Frame.__init__(self, parent, id, title, size=(700, 300))
        
        

        self.selObj = 0
        self.selList = -1
        self.seli = -1

        panel = wx.Panel(self, -1)
        topsizer= wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(topsizer)
        topsizer.Add(panel,  flag=wx.EXPAND)
        
         #---------------------------------------------------
        vertmain = wx.BoxSizer(wx.VERTICAL)
        panel.SetSizer(vertmain)
        
        tophor = wx.BoxSizer(wx.HORIZONTAL)
        tophorP = wx.Panel(panel, -1)
        tophorP.SetSizer(tophor)
        
        midhor = wx.BoxSizer(wx.HORIZONTAL)
        midhorP = wx.Panel(panel, -1)
        midhorP.SetSizer(midhor)
        
        hormain = wx.BoxSizer(wx.HORIZONTAL)
        hormainP = wx.Panel(panel, -1)
        hormainP.SetSizer(hormain)
        
        leftvert = wx.BoxSizer(wx.VERTICAL)
        leftvertP = wx.Panel(hormainP, -1)
        leftvertP.SetSizer(leftvert)
        
        rightvert = wx.BoxSizer(wx.VERTICAL)
        rightvertP = wx.Panel(hormainP, -1)
        rightvertP.SetSizer(rightvert)
        
        leftbuttons = wx.BoxSizer(wx.HORIZONTAL)
        leftbuttonsP = wx.Panel(leftvertP, -1)
        leftbuttonsP.SetSizer(leftbuttons)
        
        rightbuttons = wx.BoxSizer(wx.HORIZONTAL)
        rightbuttonsP = wx.Panel(rightvertP, -1)
        rightbuttonsP.SetSizer(rightbuttons)
        
        
        lis = [i.replace("\n", "") for i in open("log.txt").readlines()]
        cbox = wx.ComboBox(tophorP, choices=lis)
        train = wx.Button(tophorP, -1, 'Train', size=(100, -1))
        newc = wx.Button(rightbuttonsP, -1, 'New Concept', size=(100, -1))
        selR = wx.Button(rightbuttonsP, -1, 'Select All', size=(100, -1))
        desR = wx.Button(rightbuttonsP, -1, 'Deselect All', size=(100, -1))
        selL = wx.Button(leftbuttonsP, -1, 'Select All', size=(100, -1))
        desL = wx.Button(leftbuttonsP, -1, 'Deselect All', size=(100, -1))
        view = wx.Button(midhorP, -1, 'View', size=(100, -1))
        play = wx.Button(midhorP, -1, 'Play', size=(100, -1))
        flip = wx.Button(hormainP, -1, 'Flip Tag', size=(100, -1))
        label = wx.StaticText(tophorP, label="Concept:")
        
        
        self.listL = CheckListCtrl(leftvertP)
        self.listL.Id = 1
        self.listL.InsertColumn(0, 'Train', width=35)
        self.listL.InsertColumn(1, 'Name')
        self.listL.InsertColumn(2, 'Tag')
            
            
        self.listR = CheckListCtrl(rightvertP)
        self.listR.Id = 0
        self.listR.InsertColumn(0, 'Train', width=35)
        self.listR.InsertColumn(1, 'Name')
        self.listR.InsertColumn(2, 'Tag')       
        
        leftbuttons.Add(selL)
        leftbuttons.Add(desL)
        leftvert.Add(self.listL, 1, flag=wx.EXPAND)
        leftvert.Add(leftbuttonsP)
        hormain.Add(leftvertP, 1, flag=wx.EXPAND)
        
        hormain.Add(flip, flag=wx.ALIGN_CENTER_VERTICAL)
        
        rightbuttons.Add(selR)
        rightbuttons.Add(desR)
        rightvert.Add(self.listR, 1, flag=wx.EXPAND)
        rightvert.Add(rightbuttonsP)
        hormain.Add(rightvertP, 1, flag=wx.EXPAND)
        
        tophor.Add(label)
        tophor.Add(cbox)
        tophor.Add(train)
        tophor.Add(newc)
        vertmain.Add(tophorP, flag=wx.ALIGN_CENTER_HORIZONTAL)
        
        midhor.Add(play)
        midhor.Add(view)
        vertmain.Add(midhorP, flag=wx.ALIGN_CENTER_HORIZONTAL)
        
        vertmain.Add(hormainP, 1, flag=wx.EXPAND)
        
        
        droppan = wx.Panel(panel, -1)
        dropbox = wx.BoxSizer(wx.HORIZONTAL)
        droppan.SetSizer(dropbox)
        dropbox.SetMinSize((50, 100))
        self.dropR = wx.TextCtrl(droppan, style = wx.TE_MULTILINE, size=(30, 30))
        self.dropL = wx.TextCtrl(droppan, style = wx.TE_MULTILINE, size=(30, 30))
        
        dropbox.Add(self.dropL, wx.EXPAND)
        dropbox.Add(self.dropR, wx.EXPAND)
        
        self.dropR.extra = self.listR
        self.dropL.extra = self.listL
        
        vertmain.Add(droppan, flag=wx.EXPAND)
        
        rd = FileDropPos(self.dropR)
        self.dropR.SetDropTarget(rd)
        rd.par = self
        rd.tag = "neg"
        
        ld = FileDropPos(self.dropL)
        self.dropL.SetDropTarget(ld)
        ld.par = self
        ld.tag = "pos"
        
        self.Centre()
        self.Show(True)
        
        self.concepts = open("log.txt").readlines()
        print self.concepts, type(objs)
        cbox.Clear()
        for k in self.concepts:
            i = k.replace("\n", "")
            objs[i] = dict()
            cbox.Append(i)
        self.concept = self.concepts[0].replace("\n", "")
        
        self.loadConcept(self.concept)
        
        cbox.Bind(wx.EVT_COMBOBOX, self.pickConcept)
        self.cbox = cbox
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)
        self.objs = objs
        
        self.Bind(wx.EVT_BUTTON, self.flip, id=flip.GetId())
        self.Bind(wx.EVT_BUTTON, self.train, id=train.GetId())
        self.Bind(wx.EVT_BUTTON, self.onPlay, id=play.GetId())
        self.Bind(wx.EVT_BUTTON, self.newCon, id=newc.GetId())
        
    def newCon(self, event):
        return
    
    
    def onPlay(self, event):
        phrase.play(self.selObj.phrase)
        
    def train(self, event):
        os.remove(self.concept + "/" + "train.arff")
        os.remove(self.concept + "/" +"log.txt")
        
        arffhead = open("arff.txt").read()
        arffList = []
        arffList.append(arffhead)
        
        logList = []
        
        numL = self.listL.GetItemCount()
        numR = self.listR.GetItemCount()
        
        for i in range(numL):
            logList.append(self.listL.GetItemText(i, 1).split(".")[0] + " ")
            logList.append(self.objs[self.concept][self.listL.GetItemText(i, 1)].tag + " ")
            if self.listL.IsChecked(i):
                logList.append("yes" + "\n")
                for k in self.objs[self.concept][self.listL.GetItemText(i, 1)].features:
                    arffList.append(str(k))
                    arffList.append(", ")
                arffList.append(self.objs[self.concept][self.listL.GetItemText(i, 1)].tag + "\n")
            else :
                logList.append("no" + "\n")
                
        for i in range(numR):
            logList.append(self.listR.GetItemText(i, 1).split(".")[0] + " ")
            logList.append(self.objs[self.concept][self.listR.GetItemText(i, 1)].tag + " ")
            if self.listR.IsChecked(i):
                logList.append("yes" + "\n")
                for k in self.objs[self.concept][self.listR.GetItemText(i, 1)].features:
                    arffList.append(str(k))
                    arffList.append(", ")
                arffList.append(self.objs[self.concept][self.listR.GetItemText(i, 1)].tag + "\n")
            else:
                logList.append("no" + "\n")
        
        arffString = "".join(arffList)
        print arffString
        arffFile = open(self.concept + "/" + "train.arff", "w+")
        arffFile.write(arffString)
        print 
        logString = "".join(logList)
        print logString
        logFile = open(self.concept + "/" + "log.txt", "w+")
        logFile.write(logString)
        
        
            
            
        
    def OnSelect(self, event):
        print "mofo"
        numL = self.listL.GetItemCount()
        numR = self.listR.GetItemCount()
        
        
        if event.GetId() == 1:
            for i in range(numR):
                self.listR.Select(i, on=0)
            print self.objs[self.concept]
            self.selObj = self.objs[self.concept][str(self.listL.GetItemText(event.Index, 1))]
            print self.selObj.phrase
            self.selList = self.listL
            self.selList.tag = "pos"
            print self.selList.tag
        
        if event.GetId() == 0:
            for i in range(numL):
                self.listL.Select(i, on=0)
            print self.objs[self.concept]
            self.selObj = self.objs[self.concept][str(self.listR.GetItemText(event.Index, 1))]
            print self.selObj.phrase
            self.selList = self.listR
            self.selList.tag = "neg"
            print self.selList.tag
        self.seli = event.Index

            
    def flip(self, event):
        if self.selList.tag == "pos":
            self.selObj.tag = "neg"
            exlist = self.listR
            print self.selList.GetItemText(self.seli, 1)
            index = exlist.InsertStringItem(0, " ")
            print index, "bitchass flip"
            exlist.SetStringItem(index, 1, self.selList.GetItemText(self.seli, 1))
            exlist.SetStringItem(index, 2, "neg")
            self.selList.DeleteItem(self.seli)
        if self.selList.tag == "neg":
            self.selObj.tag = "pos"
            exlist = self.listL
            index = exlist.InsertStringItem(0, " ")
            print index, "bitchass flip"
            exlist.SetStringItem(index, 1, self.selList.GetItemText(self.seli, 1))
            exlist.SetStringItem(index, 2, "pos")
            self.selList.DeleteItem(self.seli)
        
        
    def pickConcept(self, event):
        print type(self.cbox.GetValue())
        self.concept = self.cbox.GetValue()
        self.loadConcept(self.cbox.GetValue())
            
    def loadConcept(self, concept):
#        srcdir = os.path.dirname(os.path.abspath(__file__))
#        print srcdir
        print concept
        self.listL.DeleteAllItems()
        self.listR.DeleteAllItems()
        tunes = open(concept + "/log.txt").readlines()
        for k in tunes:
            if k.isspace():
                continue
            i = k.replace("\n", "")
            if(i.split(" ")[1] == "pos"):
                exlist = self.listL
            else:
                exlist = self.listR
            index = exlist.InsertStringItem(0, " ")
            print index, "bitchass"
            exlist.SetStringItem(index, 1, i.split(" ")[0] + ".mid")
            exlist.SetStringItem(index, 2, i.split(" ")[1])
            if(i.split(" ")[2] == "yes"):
                    self.listL.CheckItem(index)
            intobj = IntObj()
            intobj.file = i.split(" ")[0] + ".mid"
            print intobj.file
            midfile = converter.parse(concept + "/" + intobj.file)
            print type(midfile)
            intobj.phrase = features.scoreToPhrase(midfile)
            print "bufore"
            intobj.features = features.vect(midfile)
            print "shiit got wierd?"
            intobj.tag = i.split(" ")[1]
            objs[concept][intobj.file] = intobj
                    
        
        
        
        #---------------------------------------------------


class Trainer(wx.Frame):
    def __init__(self, parent, id, title, objs):
        wx.Frame.__init__(self, parent, id, title, size=(750, 400))

        panel = wx.Panel(self, -1)
        
         #---------------------------------------------------
#        vertmain = wx.BoxSizer(wx.VERTICAL)
#        panel.SetSizer(vertmain)
#        
#        tophor = wx.BoxSizer(wx.HORIZONTAL)
#        tophorP = wx.Panel(panel, -1)
#        tophorP.SetSizer(tophor)
#        
#        midhor = wx.BoxSizer(wx.HORIZONTAL)
#        midhorP = wx.Panel(panel, -1)
#        midhorP.SetSizer(midhor)
#        
#        hormain = wx.BoxSizer(wx.HORIZONTAL)
#        hormainP = wx.Panel(panel, -1)
#        hormainP.SetSizer(hormain)
#        
#        leftvert = wx.BoxSizer(wx.VERTICAL)
#        leftvertP = wx.Panel(hormainP, -1)
#        leftvertP.SetSizer(leftvert)
#        
#        rightvert = wx.BoxSizer(wx.VERTICAL)
#        rightvertP = wx.Panel(hormainP, -1)
#        rightvertP.SetSizer(rightvert)
#        
#        leftbuttons = wx.BoxSizer(wx.HORIZONTAL)
#        leftbuttonsP = wx.Panel(leftvertP, -1)
#        leftbuttonsP.SetSizer(leftbuttons)
#        
#        rightbuttons = wx.BoxSizer(wx.HORIZONTAL)
#        rightbuttonsP = wx.Panel(rightvertP, -1)
#        rightbuttonsP.SetSizer(rightbuttons)
#        
#        
#        lis = ['aba', 'daba', 'bob']
#        cbox = wx.ComboBox(tophorP, choices=lis)
#        train = wx.Button(tophorP, -1, 'Train', size=(100, -1))
#        selR = wx.Button(rightbuttonsP, -1, 'Select All', size=(100, -1))
#        desR = wx.Button(rightbuttons, -1, 'Deselect All', size=(100, -1))
#        selL = wx.Button(leftbuttonsP, -1, 'Select All', size=(100, -1))
#        desL = wx.Button(leftbuttonsP, -1, 'Deselect All', size=(100, -1))
#        view = wx.Button(midhorP, -1, 'View', size=(100, -1))
#        play = wx.Button(midhorP, -1, 'Play', size=(100, -1))
#        flip = wx.Button(hormainP, -1, 'Flip Tag', size=(100, -1))
#        
#        
#        self.listL = CheckListCtrl(panel)
#        self.listL.InsertColumn(0, 'Package', width=140)
#        self.listL.InsertColumn(1, 'Size')
#        self.listL.InsertColumn(2, 'Repository')
#
#        for i in packages:
#            index = self.list.InsertStringItem(1, i[0])
#            print index
#            self.list.SetStringItem(index, 1, i[1])
#            self.list.SetStringItem(index, 2, i[2])
#            
#        self.listR = CheckListCtrl(panel)
#        self.listR.InsertColumn(0, 'Package', width=140)
#        self.listR.InsertColumn(1, 'Size')
#        self.listR.InsertColumn(2, 'Repository')
#
#        for i in packages:
#            index = self.list.InsertStringItem(1, i[0])
#            print index
#            self.list.SetStringItem(index, 1, i[1])
#            self.list.SetStringItem(index, 2, i[2])
#        
#        rightbuttons.Add(selR)
#        rightbuttons.Add(desR)
#        rightvert.Add(self.listR)
#        rightvert.Add(rightbuttonsP)
#        hormain.Add(rightvertP)
#        
#        hormain.Add(flip)
#        
#        rightbuttons.Add(selL)
#        leftbuttons.Add(desL)
#        leftvert.Add(self.listR)
#        leftvert.Add(leftbuttonsP)
#        hormain.Add(leftvertP)
#        
#        tophor.Add(cbox)
#        tophor.Add(train)
#        vertmain.Add(tophorP)
#        
#        midhor.Add(play)
#        midhor.Add(view)
#        vertmain.Add(midhorP)
#        
#        vertmain.Add(hormainP)
#        
#        
        #---------------------------------------------------

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        dragbox = wx.BoxSizer(wx.VERTICAL)

        leftPanel = wx.Panel(panel, -1)
        rightPanel = wx.Panel(panel, -1)
        topRowPan = wx.Panel(rightPanel, -1)
        dragPanel = wx.Panel(panel, -1)

        #self.log = wx.TextCtrl(rightPanel, -1, style=wx.TE_MULTILINE)
        self.list = CheckListCtrl(rightPanel)
        self.list.Id = 500
        self.list.InsertColumn(0, 'Package', width=140)
        self.list.InsertColumn(1, 'Size')
        self.list.InsertColumn(2, 'Repository')

        for i in packages:
            index = self.list.InsertStringItem(1, i[0])
            print index
            self.list.SetStringItem(index, 1, i[1])
            self.list.SetStringItem(index, 2, i[2])

        vbox2 = wx.BoxSizer(wx.VERTICAL)

        sel = wx.Button(leftPanel, -1, 'Select All', size=(100, -1))
        des = wx.Button(leftPanel, -1, 'Deselect All', size=(100, -1))
        save = wx.Button(leftPanel, -1, 'Save Melody', size=(100, -1))

        view = wx.Button(topRowPan, -1, 'View', size=(100, -1))
        play = wx.Button(topRowPan, -1, 'Play', size=(100, -1))
        flip = wx.Button(topRowPan, -1, 'Flip Tag', size=(100, -1))
        train = wx.Button(topRowPan, -1, 'Train', size=(100, -1))

        self.Bind(wx.EVT_BUTTON, self.OnSelectAll, id=sel.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnDeselectAll, id=des.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnApply, id=save.GetId())

        vbox2.Add(sel, 0, wx.TOP, 50)
        vbox2.Add(des)
        vbox2.Add(save)

        hbox2.Add(play)
        hbox2.Add(view)
        hbox2.Add(flip)
        hbox2.Add(train)
        
        topRowPan.SetSizer(hbox2)

        leftPanel.SetSizer(vbox2)

        lis = ['aba', 'daba', 'bob']

        cbox = wx.ComboBox(rightPanel, choices=lis)
        self.cbox = cbox

        vbox.Add(cbox)
        vbox.Add(topRowPan)
        vbox.Add(self.list, 1, wx.EXPAND)
        
        #vbox.Add((-1, 10))

        rightPanel.SetSizer(vbox)

        self.text1 = wx.TextCtrl(dragPanel, size=(100, 100), style = wx.TE_MULTILINE)
        dt1 = FileDropPos(self.text1)
        self.text1.SetDropTarget(dt1)
        self.text1.AppendText("Drag Positive Examples Here")

        self.text2 = wx.TextCtrl(dragPanel, size=(100, 100), style = wx.TE_MULTILINE)
        dt2 = FileDropNeg(self.text2)
        self.text2.SetDropTarget(dt2)
        self.text2.AppendText("Drag Negative Examples Here")

        dragbox.Add(self.text1)
        dragbox.Add(self.text2)

        dragPanel.SetSizer(dragbox)

        hbox.Add(dragPanel)
        hbox.Add(leftPanel, 0, wx.EXPAND | wx.RIGHT, 5)
        hbox.Add(rightPanel, 1, wx.EXPAND)
        hbox.Add((3, -1))

        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)


        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect)

    def OnSelect(self, event):
       # print dir(event)
        print event.Index, event.Id
        g = event.Index
        
        print self.cbox.GetCurrentSelection()
        
    
        

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
        for g in range(5):
            self.list.Select(g, on=0)
        num = self.list.GetItemCount()
        for i in range(num):
            if i == 0: self.log.Clear()
            if self.list.IsChecked(i):
                print "boi", i
                #self.log.AppendText(self.list.GetItemText(i) + '\n')

class FileDropPos(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):

        print filenames, "pos"
        
        for i in filenames:
            srcdir = os.path.dirname(os.path.abspath(__file__))
            shutil.copy(i,  srcdir + "/" + self.par.concept)
            
            #copy file to directory
            #add file to log 
            k = IntObj
            k.file = i.split("/")[len(i.split("/"))-1].split(".")[0]
            k.phrase = features.scoreToPhrase(converter.parse(i))
            k.features = features.vect(converter.parse(i))
            k.tag = self.tag
            objs[self.par.concept][k.file] = k
            log  = open(srcdir + "/" + self.par.concept + "/" + "log.txt", "a")
            log.write("\n" + k.file + " " + k.tag + " " + "no")
            print k.file
            if k.tag == "pos":
                exlist = self.par.listL
            else:
                exlist = self.par.listR
            index = exlist.InsertStringItem(0, " ")
            print index
            exlist.SetStringItem(index, 1, k.file)
            exlist.SetStringItem(index, 2, self.tag)
            
            
            #copy file to direcyory
            #add filename to log 
            
                

class FileDropNeg(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):

        print filenames, "neg", self.window.extra

class FileDrop(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        
        print "motherfucker"
        
        for name in filenames:
            try:
                file = open(name, 'r')
                text = file.read()
                self.window.WriteText(text)
                file.close()
            except IOError, error:
                dlg = wx.MessageDialog(None, 'Error opening file\n' + str(error))
                dlg.ShowModal()
            except UnicodeDecodeError, error:
                dlg = wx.MessageDialog(None, 'Cannot open non ascii files\n' + str(error))
                dlg.ShowModal()
                
class DropFile(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size = (450, 400))

        self.text = wx.TextCtrl(self, -1, style = wx.TE_MULTILINE)
        dt = FileDrop(self.text)
        self.text.SetDropTarget(dt)
        self.Centre()
        self.Show(True)




app = wx.App()
Trans(None, -1, 'Transformer', objs)
#DropFile(None, -1, 'filedrop.py', objs)
#Trainer(None, -1, 'Repository', objs)
Gen(None, -1, 'Generator', objs, sys.argv[1])
new  = NewOne(None, -1, "Trainer", objs)
app.MainLoop()
