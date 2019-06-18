#!/bin/bash

if [ ${TOKEN} != "" ]; then
    mkdir -p /root/.vnc
    x11vnc -storepasswd ${TOKEN} /root/.vnc/passwd
    x11vnc -display :1 -xkb -shared -forever -rfbauth /root/.vnc/passwd
else
    x11vnc -display :1 -xkb -shared -forever
fi
