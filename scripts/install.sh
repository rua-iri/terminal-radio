

# Set up Python virtual environment
VENV='.venv'
PYTHON=$VENV/bin/python3
PIP=$VENV/bin/pip3

echo "Installing Python Requirements"
python3 -m venv $VENV
$PIP install -r requirements.txt 1> /dev/null
echo "Done\n\n"




# Create necessary files and directories
echo "Creating Necessary Files and Folders"
if [ ! -d logs ]; then
    mkdir logs/
fi

if [ ! -f resource/radio_sources.sqlite ]; then
    sqlite3 resource/radio_sources.sqlite < resource/schema.sql
fi

echo "Done\n\n"




# Install ffmpeg (for ffplay)
echo "Installing Packages"
if ! dpkg -l ffmpeg >/dev/null; then
    sudo apt install ffmpeg 1> /dev/null
fi
echo "Done\n\n"



# move to installation directory and set up
# symbolic link to add to $PATH
echo "Moving to Installation Directory"
sudo cp -ar . /opt/terminal_radio

if [ ! -L /usr/local/bin/terminal_radio ]; then 
    sudo ln -s /opt/terminal_radio/scripts/run.sh /usr/local/bin/terminal_radio
fi

sudo chown $USER /opt/terminal_radio/
sudo cp ./scripts/autocomplete.sh /usr/share/bash-completion/completions/_terminal_radio
echo "Done\n\n\n\n"



final_output=$(cat << "EOF"
\e[32m
 _                      _             _                 _ _       
| |                    (_)           | |               | (_)      
| |_ ___ _ __ _ __ ___  _ _ __   __ _| |  _ __ __ _  __| |_  ___  
| __/ _ | '__| '_ ` _ \| | '_ \ / _` | | | '__/ _` |/ _` | |/ _ \ 
| ||  __| |  | | | | | | | | | | (_| | | | | | (_| | (_| | | (_) |
 \__\___|_|  |_| |_| |_|_|_| |_|\__,_|_| |_|  \__,_|\__,_|_|\___/ 
                                     ______                       
                                    |______|                      
\e[0m


Setup Complete!


\e[32mterminal_radio\e[0m - start the application
\e[32mterminal_radio update\e[0m - Manage radio sources
\e[32mterminal_radio logs\e[0m - View the application logs
\e[32mterminal_radio show\e[0m - View the list of sources\n
EOF
)

echo "$final_output"





