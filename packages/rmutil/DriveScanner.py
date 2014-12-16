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
        print "DISK FOUND: ", disk
        PRE_SCAN_RESULT.append(disk)
        index = disks.find("/dev/", index+5)
    print ""
    print "PRE SCAN RESULT: ", PRE_SCAN_RESULT

def scanForNew():
    newDisk = None
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
        print "DISK FOUND: ", disk
        if not PRE_SCAN_RESULT == None and not disk in PRE_SCAN_RESULT:
            newDisk = disk
        index = disks.find("/dev/", index+5)
    print ""
    if not newDisk == None:
        print "NEW DISK: ", newDisk
        if not "rdisk" in newDisk:
            index = newDisk.find("disk")
            path = newDisk[:index]
            name = "r"+newDisk[index:]
            newRdisk = path+name
            print "Using raw disk name for dd command: ", newRdisk
            return newDisk, newRdisk
        else:
            return newDisk, newDisk
    else:
        return None
