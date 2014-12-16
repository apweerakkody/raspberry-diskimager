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
        self.__InitUI()
        self.SetSizerAndFit(self.mainSizer)
        self.state
        self.Center()

    def __InitUI(self):
        self.infoLabel = wx.StaticText(self,-1,label="Remove SD card if inserted and click \"Next\"")
        self.next = wx.Button(self,-1,label="Next")

        self.next.Bind(wx.EVT_BUTTON, self.NextClicked)

        self.mainSizer.Add(self.infoLabel,flag=wx.ALL|wx.ALIGN_CENTER_HORIZONTAL,border=35)
        self.mainSizer.Add(self.next,flag=wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL,border=35)
        
    def NextClicked(self,event):
        if self.state == 0:
            DriveScanner.preScan()
            self.state = STATE_PRE_SCAN_DONE
            self.infoLabel.SetLabel("Insert SD card and click \"Next\"")
        elif self.state == 1:
            time.sleep(5)
            self.disk, self.rdisk = DriveScanner.scanForNew()
            if self.disk == None:
                self.state = STATE_SCAN_ERROR
                self.next.SetLabel("Close")
                self.infoLabel.SetLabel("SD card not detected!")
            else:
                self.state = STATE_SCAN_SUCCESS
                self.next.SetLabel("OK")
                info = "SD card found: %s" % self.disk
                self.infoLabel.SetLabel(str(info))
        elif self.state == 2:
            self.EndModal(wx.ID_OK)
            self.Destroy()
        elif self.state == 3:
            self.EndModal(wx.ID_CANCEL)
            self.Destroy