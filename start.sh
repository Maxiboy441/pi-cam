#!/bin/bash
chmod +x ./streamfiles/stream.sh
chmod +x ./timelapsfiles/timelaps.sh

nohup ./timelapsfiles/timelaps.sh > /dev/null 2>&1 &
TIMELAPS_PID=$!

nohup ./streamfiles/stream.sh > /dev/null 2>&1 &
STREAM_PID=$!

apt-get update
apt-get install -y python3

nohup python3 ./streamfiles/webservice.py > /dev/null 2>&1 &
WEBSERVICE_PID=$!

check_process() {
    if ps -p $1 > /dev/null 2>&1; then
        echo "$2 is running (PID: $1)"
    else
        echo "$2 is not running"
    fi
}

sleep 3

check_process $TIMELAPS_PID "timelaps.sh"

check_process $STREAM_PID "stream.sh"

pgrep -f "python3 ./streamfiles/webservice.py" > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "webservice.py is running"
else
    echo "webservice.py is not running"
fi

echo "Script completed. All services have been started."
