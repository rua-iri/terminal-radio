

# Set up Python virtual environment
VENV='.venv'
PYTHON=$VENV/bin/python3
PIP=$VENV/bin/pip3

echo "Installing Python Requirements"
python3 -m venv $VENV
$PIP install -r requirements.txt 1> /dev/null
echo "Done\n\n"





echo "Creating Necessary Files and Folders"
# Create necessary files and directories
if [ ! -d logs ]; then 
    mkdir logs/
fi

if [ ! -f resource/sources.json ]; then
    cp resource/sources.example.json resource/sources.json
fi

echo "Done\n\n"




echo "Installing Packages"
# Install ffmpeg (for ffplay)
sudo apt install ffmpeg 1> /dev/null
echo "Done\n\n"


echo "Moving to Installation Directory"

# move to installation directory and set up
# symbolic link to add to $PATH
sudo cp -ar . /opt/terminal_radio

if [ ! -L /usr/local/bin/terminal_radio ]; then 
    sudo ln -s /opt/terminal_radio/scripts/run.sh /usr/local/bin/terminal_radio
fi

sudo chown rory /opt/terminal_radio/

echo "Done\n\n"


sudo cp ./scripts/autocomplete.sh /usr/share/bash-completion/completions/_terminal_radio


printf "\n\nSetup Complete! \n"