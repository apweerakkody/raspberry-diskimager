from packages.rmgui import ImagerFrame as rm_app
import os, platform
try:
    import wx
except ImportError:
    raise ImportError,"Wx Python is required."


# set working directory to scripts path
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
base_path = dname
app = wx.App()

frame = rm_app.ImagerFrame(None, -1, 'RPi Disk Imager', base_path)

app.MainLoop()
