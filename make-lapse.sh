#!/bin/bash
mkdir renamed
cp *.JPG renamed/.
cd renamed
ls *.JPG| awk 'BEGIN{ a=0 }{ printf "mv %s myfile%04d.JPG\n", $0, a++ }' | bash

# Para high quality:
# avconv -y -r 10 -i myfile%4d.JPG -r 10 -vcodec libx264 -q:v 3  -vf crop=4256:2832,scale=iw:ih tlfullhiqual.mp4;

avconv -y -r 10 -i myfile%4d.JPG -r 10 -vcodec libx264 -q:v 20 -vf crop=3840:2880,scale=iw/4:ih/4 tlsmallowqual.mp4;
mv *.mp4 ../.
cd ..
rm -r renamed