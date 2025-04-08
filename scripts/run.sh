cd /opt/terminal_radio

if [ ! -z $1 ]; then
    CMD='play'
else
    CMD=$1
fi



VENV=./.venv
PYTHON=$VENV/bin/python3
PIP=$VENV/bin/pip3

$PYTHON main.py $CMD

