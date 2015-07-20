import threading, sys, os, time, platform, subprocess
import wx

PRE_SCAN_RESULT = None

def preScan():
    global PRE_SCAN_RESULT
    PRE_SCAN_RESULT = []
    # scan disk list
    proc = subprocess.Popen(["diskutil", "list"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    disks = proc.communicate()
    disks = disks[0]
    index = disks.find("/dev/")
    while index != -1:
        rest = disks[index:]
        splitted = rest.split(" ")
        disk = splitted[0]
        disk = disk[:-1]
        PRE_SCAN_RESULT.append(disk)
        index = disks.find("/dev/", index+5)

def scanForNew():
    newDisk = None
    size = None
    # scan again and return new device
    proc = subprocess.Popen(["diskutil", "list"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    disks = proc.communicate()
    disks = disks[0]
    index = disks.find("/dev/")
    while index != -1:
        rest = disks[index:]
        splitted = rest.split(" ")
        disk = splitted[0]
        disk = disk[:-1]
        if not PRE_SCAN_RESULT == None and not disk in PRE_SCAN_RESULT:
            newDisk = disk
            infoIndex = splitted.index("GB")
            size = splitted[infoIndex-1] + " " + splitted[infoIndex]
            if size.startswith("*"):
                size = size[1:]
        index = disks.find("/dev/", index+5)
    if not newDisk == None:
        if not "rdisk" in newDisk:
            index = newDisk.find("disk")
            path = newDisk[:index]
            name = "r"+newDisk[index:]
            newRdisk = path+name
            return newDisk, newRdisk, size
        else:
            return newDisk, newDisk, size
    else:
        return None, None, None
