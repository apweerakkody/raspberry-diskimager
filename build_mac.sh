#! /bin/sh

# clean up first
echo "Cleaning up old build and release directories..."
rm -rf build dist Release
mkdir Release

# get current directory and destination path
cwd=$(pwd)
destPath="$cwd/Release"
distPath="dist"

##### BUILD RASPMEDIA IMAGE TRANSFER #####
echo ""
echo "Compiling RPi Disk Imager..."
pyinstaller SPEC_RPiDiskImager.spec

# copy built version to tools directory
echo ""
echo "Making release file..."
distFile="$distPath/RPi Disk Imager.app"
destFile="$destPath/RPi Disk Imager.app"
cp -r "$distFile" "$destFile"

# remove build directories
echo "Cleaning up..."
rm -rf build dist

# modify plist file of app to be foreground
#echo "Updating Info.plist for RPi Disk Imager..."
#plist="$destFile/Contents/Info"
#defaults write "$plist" LSBackgroundOnly -string NO
#plist="$plist.plist"
#plutil -convert xml1 "$plist"

echo "Build done, bye bye..."
