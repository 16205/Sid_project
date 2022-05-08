#! /usr/bin/env python

import os
# os.system('raspivid -t 0 -hf -vf -w 1296 -h 972 --nopreview -o - | nc -l 5000')
os.system("raspivid -o - -t 0 -w 1296 -h 972 -fps 12  | cvlc -vvv stream:///dev/stdin --sout '#rtp{sdp=rtsp://:8080/}' :demux=h264")