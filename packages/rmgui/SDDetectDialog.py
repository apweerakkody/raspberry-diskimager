import wx
import os, sys, platform, time
import packages.rmutil.DriveScanner as DriveScanner

STATE_STARTUP = 0
STATE_PRE_SCAN_DONE = 1
STATE_SCAN_SUCCESS = 2
STATE_SCAN_ERROR = 3
################################################################################
# DIALOG FOR SD DETECTION ######################################################
################################################################################
class SDDetectDialog(wx.Dialog):
    def __init__(self,parent,id,title):
        wx.Dialog.__init__(self,parent,id,title)
        self.parent = parent
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.state = STATE_STARTUP
        self.disk = None
        self.rdisk = None
        self.diskSize = None
        self.__InitUI()
        self.SetSizerAndFit(self.mainSizer)
        self.state
        self.Center()

    def __InitUI(self):
        self.infoLabel = wx.StaticText(self,-1,label="Remove SD Card if inserted and click \"Next\"")
        self.info2Label = wx.StaticText(self,-1,label="")
        self.next = wx.Button(self,-1,label="Next")
        self.cancel = wx.Button(self,-1,label="Cancel")

        self.next.Bind(wx.EVT_BUTTON, self.NextClicked)
        self.cancel.Bind(wx.EVT_BUTTON, self.Cancel)

        buttonSizer = wx.BoxSizer()
        buttonSizer.Add(self.cancel,flag=wx.ALL,border=5)
        buttonSizer.Add(self.next,flag=wx.ALL,border=5)

        self.mainSizer.Add(self.infoLabel,flag=wx.LEFT|wx.TOP|wx.RIGHT,border=15)
        self.mainSizer.Add(self.info2Label,flag=wx.LEFT|wx.RIGHT,border=15)
        self.mainSizer.Add(buttonSizer,flag=wx.ALL|wx.ALIGN_CENTER_HORIZONTAL,border=15)
    
    def Cancel(self,event=None):
        self.EndModal(wx.ID_CANCEL)
        self.Destroy

    def NextClicked(self,event):
        if self.state == 0:
            DriveScanner.preScan()
            self.state = STATE_PRE_SCAN_DONE
            self.infoLabel.SetLabel("Insert SD Card and click \"Next\"")
        elif self.state == 1:
            time.sleep(5)
            self.disk, self.rdisk, self.diskSize = DriveScanner.scanForNew()
            if self.disk == None:
                self.state = STATE_SCAN_ERROR
                self.next.SetLabel("Close")
                self.infoLabel.SetLabel("SD Card not detected!")
            else:
                self.state = STATE_SCAN_SUCCESS
                self.next.SetLabel("OK")
                info = "SD Card detected: %s" % self.disk
                self.infoLabel.SetLabel(str(info))
                if not self.diskSize == None:
                    info2 = "Size: %s" % self.diskSize
                    self.info2Label.SetLabel(str(info2))
        elif self.state == 2:
            self.EndModal(wx.ID_OK)
            self.Destroy()
        elif self.state == 3:
            self.Cancel()