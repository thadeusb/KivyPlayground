#!/bin/bash

export PATH=$PATH:/home/thadeusb/Workspace/Android/android-sdk-linux/tools/:/home/thadeusb/Workspace/Android/android-sdk-linux/platform-tools
cd /home/thadeusb/Workspace/Android/Kivy-1.0.9-android/
rm -rf bin
rm -rf ~/.android/debug.keystore
adb uninstall org.thadeusb.kworld
python build.py --dir /home/thadeusb/Workspace/KivyPlayground/kworld --package org.thadeusb.kworld --name "Kaboodle World" --version 1.0.0 debug installd
# adb -d install -r /home/thadeusb/Workspace/Android/Kivy-1.0.9-android/bin/KaboodleWorld-1.0.0-debug.apk
cd /home/thadeusb/Workspace/KivyPlayground/kworld
