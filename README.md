# terminal-radio

<div align="center">
  <div>
    A command line program for listening to radio streams
    </div>
  <br/>
  <div>
<img src="https://github.com/user-attachments/assets/ca77fffc-ccf9-485d-bc17-9c0d7210f584" alt=terminal-radio logo" width="45%" />
    </div>
</div>


## Setup

```bash
git clone https://github.com/rua-iri/terminal-radio

cd terminal-radio

python3 -m venv .venv

source .venv/bin/activate

pip3 install -r requirements.txt

python3 terminal_radio/main.py
```

## Add Stations

In order to add new stations to the program you first have to find the link to streams.

These will typically be a link to a file with the extension `.m3u8`.

Then download the station's logo in `jpeg` or `png` format and save it in `resource/img/`.

Finally add all this information to the `resource/sources.json` file and the new station will be available when the program next runs.



