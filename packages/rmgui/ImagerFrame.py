import wx
import sys, os, platform, subprocess, time
import SDDetectDialog

from appscript import *

BASE_PATH = None
INFO_SHOWN = False
DETECT_SD = 0
SELECT_IMAGE = 1

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
        self.cwd = os.getcwd()
        self.disk = None
        self.imagePath = None
        self.Bind(wx.EVT_CLOSE, self.Close)
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.Initialize()
        self.__ValidateInput()
        self.SetSizerAndFit(self.mainSizer)
        self.Center()
        self.Show()

    def Close(self, event=None):
        self.Destroy()
        sys.exit(0)

    def Initialize(self):
        print "Creating box sizers..."
        imgBox = wx.StaticBox(self,-1,label="Disk Image")
        imgBoxSizer = wx.StaticBoxSizer(imgBox,wx.VERTICAL)

        sdBox = wx.StaticBox(self,-1,label="SD Card")
        sdBoxSizer = wx.StaticBoxSizer(sdBox,wx.VERTICAL)

        print "Initializing UI elements..."
        selectImg = wx.Button(imgBox,-1,label="Select image file")
        self.imgLabel = wx.StaticText(imgBox,-1,label="No image selected!",size=(selectImg.GetSize()[0]*3,22))
        detectSD = wx.Button(sdBox,-1,label="Detect SD-Card")
        self.sdLabel = wx.StaticText(sdBox,-1,label="No SD Card detected",size=self.imgLabel.GetSize())
        self.sdLabel2 = wx.StaticText(sdBox,-1,label="",size=self.imgLabel.GetSize())
        self.runBtn = wx.Button(self,-1,label="Execute")
        exitBtn = wx.Button(self,-1,label="Exit")

        print "Binding elements..."
        # bind elements
        selectImg.Bind(wx.EVT_BUTTON, self.SelectImageClicked)
        detectSD.Bind(wx.EVT_BUTTON, self.DetectSDClicked)
        self.runBtn.Bind(wx.EVT_BUTTON, self.ExecuteClicked)
        exitBtn.Bind(wx.EVT_BUTTON, self.Close)

        print "CREATING UI..."

        buttonSizer = wx.BoxSizer()
        contentSizer = wx.BoxSizer(wx.VERTICAL)
        
        imgBoxSizer.Add(selectImg,flag=wx.ALL,border=3)
        imgBoxSizer.Add(self.imgLabel,flag=wx.ALL,border=3)
        
        sdBoxSizer.Add(detectSD,flag=wx.ALL,border=3)
        sdBoxSizer.Add(self.sdLabel,flag=wx.ALL,border=3)
        sdBoxSizer.Add(self.sdLabel2,flag=wx.ALL,border=3)
        
        buttonSizer.Add(exitBtn,flag=wx.ALL,border=5)
        buttonSizer.Add(self.runBtn,flag=wx.ALL,border=5)

        contentSizer.Add(imgBoxSizer,flag=wx.ALL,border=10)
        contentSizer.Add(sdBoxSizer,flag=wx.ALL,border=10)
        contentSizer.Add(buttonSizer,flag=wx.ALL|wx.ALIGN_CENTER_HORIZONTAL,border=10)
        self.mainSizer.Add(contentSizer,flag=wx.ALL,border=20)

    def ShowStartupInfoDialog(self, result):
        dlg = wx.MessageDialog(self,"This tool helps you to bring your image file on the SD Card for your Raspberry Pi by trying to automatically detecting the SD Card disk and wrapping the needed commands to erase the disk and copy the image.\n\nAll data on your SD Card will be deleted.\n\nPlease ALWAYS check the size of the detected SD Card if it fits to the size of your card!\nThe automatic detection was tested but may fail sometimes!\n\nNo warranty from my side if anything goes wrong! By clicking OK you confirm that you understand the risk. Use with care and at your own risk!\n\nIf you don't feel comfortable with what you're doing exit NOW by clicking Cancel!","IMPORTANT INFORMATION",style=wx.OK|wx.CANCEL|wx.ICON_EXCLAMATION)
        if dlg.ShowModal() == wx.ID_OK:
            global INFO_SHOWN
            INFO_SHOWN = True
            if result == SELECT_IMAGE:
                self.SelectImageClicked(None)
            elif result == DETECT_SD:
                self.DetectSDClicked(None)
        else:
            self.Close()

    def SelectImageClicked(self, event):
        if INFO_SHOWN:
            openFileDialog = wx.FileDialog(self, "Open IMG file", "", "",
                                           "IMG files (*.img)|*.img", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

            if openFileDialog.ShowModal() == wx.ID_OK:
                imgFile = openFileDialog.GetPath()
                if imgFile.endswith("img"):
                    self.imagePath = imgFile
                    info = self.imagePath
                    if len(info) > 45:
                        info = "..." + info[len(info)-45:]
                    self.imgLabel.SetLabel(str(info))
        else:
            self.ShowStartupInfoDialog(SELECT_IMAGE)

    def DetectSDClicked(self, event):
        if INFO_SHOWN:
            dlg = SDDetectDialog.SDDetectDialog(self,-1,"Detect SD Card")
            if dlg.ShowModal() == wx.ID_OK:
                self.disk = dlg.rdisk
                self.diskName = dlg.disk
                diskSize = dlg.diskSize
                info = "SD Card detected: %s" % self.disk
                self.sdLabel.SetLabel(str(info))
                info2 = "SC Card size: %s" % diskSize
                self.sdLabel2.SetLabel(str(info2))
            else:
                print "SD Card not detected!"
            self.__ValidateInput()
        else:
            self.ShowStartupInfoDialog(DETECT_SD)

    def __ValidateInput(self):
        if not self.disk == None and not self.imagePath == None:
            # image selected and sd card detected
            self.runBtn.Enable()
        else:
            self.runBtn.Disable()

    def ExecuteClicked(self, event):
        dlg = wx.MessageDialog(self, "Ready to write image file to disk " + self.disk + "\nThis app will close when the process is finished. A command prompt will ask for your user password and then write the disk.\nYou will see no progress, just wait until the command is complete and the Imager app closes!", "Ready to write disk...", style=wx.OK|wx.CANCEL)
        if dlg.ShowModal() == wx.ID_OK:
            path = os.path.split(self.imagePath)[0]
            filename = os.path.basename(self.imagePath)
            os.chdir(path)
            csPath = self.cwd + '/executables/cocoasudo'
            terminal = app('Terminal')
            cmd = "cd '" + self.cwd + "'"
            cmd +=(" && echo ------------------------------------------------")
            cmd +=(" && echo 'Please provide your Administrator password to proceed!'")
            cmd +=(" && sudo diskutil eraseDisk fat32 RASPMEDIA "+self.diskName)
            cmd +=(" && echo Disabling SD Card for image writing...")
            cmd +=(" && sudo diskutil unmount "+self.diskName+"s2")
            cmd +=(" && echo ================================================")
            cmd +=(" && echo ================================================")
            cmd +=(" && echo WRITING IMAGE TO YOUR SD CARD, DO NOT CLOSE THIS WINDOW OR THE IMAGER APPLICATION!")
            cmd +=(" && echo ================================================")
            cmd +=(" && echo RPi Disk Imager will be closed when the process is finished.")
            cmd +=(" && echo PLEASE WAIT! Writing the image can take up to 30 minutes depending on your SD Card speed!")
            cmd +=(" && echo ...")
            cmd +=(" && cd \""+path+"\"")
            cmd +=(" && sudo dd bs=1m if="+filename+" of="+self.disk)
            cmd +=(" && echo ================================================")
            cmd +=(" && echo ================================================")
            cmd +=(" && echo IMAGE SUCCESSFULLY WRITTEN TO YOUR SD CARD!")
            cmd +=(" && echo RPi Disk Imager will close now!")
            cmd +=(" && echo Bye bye...")
            terminal.do_script(cmd)
            '''
            os.system("echo " + pwd + " | sudo diskutil eraseDisk fat32 RASPMEDIA "+self.diskName)
            os.system("echo Disabling SD Card for image writing...")
            os.system("sudo diskutil unmount "+self.diskName+"s2")
            os.system("echo ================================================")
            os.system("echo ================================================")
            os.system("echo WRITING IMAGE TO YOUR SD CARD, DO NOT CLOSE THIS WINDOW OR THE IMAGER APPLICATION!")
            os.system("echo ================================================")
            os.system("echo RPi Disk Imager will be closed when the process is finished.")
            os.system("echo PLEASE WAIT! Writing the image can take up to 30 minutes depending on your SD Card speed!")
            os.system("echo ...")
            os.system("sudo dd bs=1m if="+filename+" of="+self.disk)
            os.system("echo ================================================")
            os.system("echo ================================================")
            os.system("echo IMAGE SUCCESSFULLY WRITTEN TO YOUR SD CARD!")
            os.system("echo RPi Disk Imager will close now!")
            os.system("echo Bye bye...")
            '''
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
