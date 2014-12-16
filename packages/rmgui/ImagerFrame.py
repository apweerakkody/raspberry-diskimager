import wx
import sys, os, platform, pexpect, subprocess, time
import SDDetectDialog

BASE_PATH = None

################################################################################
# MAIN FRAME OF APPLICATION ####################################################
################################################################################
class ImagerFrame(wx.Frame):
    def __init__(self,parent,id,title,base_path):
        wx.Frame.__init__(self,parent,id,title,size=(400,270))
        self.parent = parent
        self.base_path = base_path
        global BASE_PATH
        BASE_PATH = base_path
        self.disk = None
        self.imagePath = None
        self.Bind(wx.EVT_CLOSE, self.Close)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.Initialize()
        self.__ValidateInput()
        self.SetSizer(self.mainSizer)
        self.Center()
        self.Show()

    def Close(self, event=None):
        self.Destroy()
        sys.exit(0)

    def Initialize(self):
        selectImg = wx.Button(self,-1,label="Select image file")
        self.imgLabel = wx.StaticText(self,-1,label="No image selected")
        detectSD = wx.Button(self,-1,label="Detect SD-Card")
        self.sdLabel = wx.StaticText(self,-1,label="No SD Card detected")
        self.runBtn = wx.Button(self,-1,label="Execute")

        # bind elements
        selectImg.Bind(wx.EVT_BUTTON, self.SelectImageClicked)
        detectSD.Bind(wx.EVT_BUTTON, self.DetectSDClicked)
        self.runBtn.Bind(wx.EVT_BUTTON, self.ExecuteClicked)

        contentSizer = wx.BoxSizer(wx.VERTICAL)
        contentSizer.Add(selectImg)
        contentSizer.Add(self.imgLabel,flag=wx.TOP,border=2)
        contentSizer.Add(detectSD,flag=wx.TOP,border=40)
        contentSizer.Add(self.sdLabel,flag=wx.TOP,border=2)
        contentSizer.Add(self.runBtn,flag=wx.TOP,border=40)
        self.mainSizer.Add(contentSizer,flag=wx.ALL,border=20)

    def SelectImageClicked(self, event):
        openFileDialog = wx.FileDialog(self, "Open IMG file", "", "",
                                       "IMG files (*.img)|*.img", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if openFileDialog.ShowModal() == wx.ID_OK:
            imgFile = openFileDialog.GetPath()
            if imgFile.endswith("img"):
                self.imagePath = imgFile
                info = "Selected Image: %s" % self.imagePath
                self.imgLabel.SetLabel(str(info))
        self.mainSizer.Fit(self)

    def DetectSDClicked(self, event):
        dlg = SDDetectDialog.SDDetectDialog(self,-1,"Detect SD Card")
        if dlg.ShowModal() == wx.ID_OK:
            self.disk = dlg.rdisk
            self.diskName = dlg.disk
            info = "SD Card detected: %s" % self.disk
            self.sdLabel.SetLabel(str(info))
        else:
            print "SD Card not detected!"
        self.__ValidateInput()

    def __ValidateInput(self):
        if not self.disk == None and not self.imagePath == None:
            # image selected and sd card detected
            self.runBtn.Enable()
        else:
            self.runBtn.Disable()

    def ExecuteClicked(self, event):
        dlg = wx.MessageDialog(self, "Ready to write image file to disk " + self.disk + "\nThis app will close when the process is finished. A command prompt will ask for your user password and then write the disk.\nYou will see no progress, just wait until the command is complete and the Imager app closes!", "Ready to write disk...", style=wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            #proc = subprocess.Popen(["sudo","dd", "bs=1m","if=" + shellquote(self.imagePath), "of="+self.disk])
            #proc = subprocess.Popen(["sudo", "echo", "if=" + shellquote(self.imagePath)])
            path = os.path.split(self.imagePath)[0]
            filename = os.path.basename(self.imagePath)
            os.chdir(path)
            os.system("sudo diskutil eraseDisk fat32 RASPMEDIA "+self.diskName)
            os.system("echo Disabling SD Card for image writing...")
            os.system("sudo umount "+self.diskName+"s2")
            os.system("echo ================================================")
            os.system("echo ================================================")
            os.system("echo WRITING IMAGE TO YOUR SD CARD, DO NOT CLOSE THIS WINDOW OR THE IMAGER APPLICATION!")
            os.system("echo ================================================")
            os.system("echo RaspMedia Imager will be closed when the process is finished.")
            os.system("echo PLEASE WAIT! Writing the image can take up to 30 minutes depending on your SD Card speed!")
            os.system("echo ...")
            os.system("sudo dd bs=1m if="+filename+" of="+self.disk)
            self.Close()
        



def shellquote(s):
    return s.replace(" ", "\ ")
# HELPER METHOD to get correct resource path for image file
def resource_path(relative_path):
    global BASE_PATH
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        #print "BASE PATH FOUND: "+ base_path
    except Exception:
        #print "BASE PATH NOT FOUND!"
        base_path = BASE_PATH
    #print "JOINING " + base_path + " WITH " + relative_path
    resPath = os.path.normcase(os.path.join(base_path, relative_path))
    #resPath = base_path + relative_path
    #print resPath
    return resPath
