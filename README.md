# Raspberry Disk Imager
Raspberry Disk Imager is a little Mac OSX application written in python using wxpython for UI, providing an easy way to detect your SD Card and flash an image on in.

Flashing is done in 3 steps:
* Selecting Image file
* Detect SD Card (step by step guidance)
* Image flashing

The tool formats the sd card, re-mounts and disables it and finally writes the image. Some of the used commands need administrator privileges, thus your password will be asked 3 times.
Always make sure the tool detected the right card and that the size of the detected card matches the size of your SD Card.

A compiled Mac OS App Bundle will be available soon here.

# Disclaimer
This tool is intended to make your life easier by flashing images on SD Cards for your Raspberry Pi withouth messing around with diskutil, terminal and dd and so on.
*BUT* this does not mean that you should stop to think! ;-)

Use this tool on your own risk, I take no responsibility if you accidentially format a wrong drive or harddisk or if anything that one might think of gets wrong.
You can use it for free, you can use it at your risk and if you find any problems don't hesitate to open an issue here.
