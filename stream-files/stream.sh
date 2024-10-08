#!/bin/bash
while true; do
  rpicam-still --flicker 50hz --awb fluorescent -o "./images/new.jpg"
  rm ./images/latest.jpg
  mv ./images/new.jpg ./images/latest.jpg
  SLEEP_TIME=$((60))
  sleep $SLEEP_TIME
done