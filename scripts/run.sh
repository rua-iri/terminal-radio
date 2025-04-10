#!/bin/bash
cd /opt/terminal_radio

CMD=${1:-play}



VENV=./.venv
PYTHON=$VENV/bin/python3
PIP=$VENV/bin/pip3

$PYTHON main.py $CMD

