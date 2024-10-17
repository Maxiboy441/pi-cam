#!/bin/bash
while true; do
  TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
  FOLDER=~/timelaps-files/images
  rpicam-still --flicker 50hz --awb fluorescent -o "./images/image_$TIMESTAMP.jpg"
  SLEEP_TIME=$((3600))
  sleep $SLEEP_TIME
done