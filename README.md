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

## Setup & Run

> **_NOTE:_** This program currently runs on a linux machine running a debian based distribution

```bash
git clone https://github.com/rua-iri/terminal-radio

cd terminal-radio

./scripts/install.sh

terminal_radio
```

## Add New Stations

```
make update
```

Then enter the required data.

### Manually Add Stations

In order to add new stations to the program you first have to find the link to streams.

These will typically be a link to a file with the extension `.m3u8`.

Then add the station's logo to the json file in `jpeg`, `png` or `webp` format.

Finally add all this information to the `resource/sources.json` file, the structure is outlined in `resource/sources.example.json` and the new station will be available when the program next runs.

## Troubleshooting

In case a station doesn't stop playing after the program has been exited then it may require some intervention.

Run the following to find any processes associated with `ffplay`.

```bash
ps -aux | grep ffplay
```

Then identify the parent process and run:

```bash
kill -9 <process_id>
```

If successful the `ffplay` process should have been killed and sound will no longer play.

### Unable to fetch YouTube streams

Sometimes the yt-dlp package will be out of date and unable to fetch links to the streams.

To remedy this run the below command to update the package.

```bash
pip3 install "yt-dlp[default]" --upgrade
```
