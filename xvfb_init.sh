#!/bin/sh
export DISPLAY=:1   
Xvfb $DISPLAY -ac -screen 0 1280x1024x8 &
sleep 1 
while [ 1 = 1 ]
do
sleep 1;
done
