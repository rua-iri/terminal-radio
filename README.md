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
terminal_radio update
```

Then enter the required data.

### Manually Add Stations

In order to add new stations to the program you first have to find the link to streams.

These will typically be a link to a file with the extension `.m3u8`.

Then add the station's logo to the json file in `jpeg`, `png` or `webp` format.

Finally add all this information to the `resource/sources.json` file, the structure is outlined in `resource/sources.example.json` and the new station will be available when the program next runs.

### Change Image Display Type

By default the config file specifes that the application should display images in the sixel format.

There is an issue that many terminals do not yet support the sixel format, and so will not display anything when the image is rendered.

More information can be found about this [here](https://www.arewesixelyet.com/).

In order to change the image format so that it will display on all terminals, change the configuration file (`resource/config.yaml`) as follows.

```yaml
USE_SIXEL: false
```

If you would like to check whether your terminal supports sixel images, then run the following.

```bash
./scripts/autodetect_sixel.sh
```

If no error messages are shown, then your terminal supports them and no changes to the config need to be made.

## Troubleshooting

### Stream won't stop / Still running in the background

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

## Autocompletion

Autocompletion **should** work automatically with bash.

With Zsh there is a slight ammount of manual work involved at the minute.

I'm using [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh) to manage plugins, so this is how I achieved it.

```bash
cp scripts/autocomplete.zsh ~/.oh-my-zsh/custom/plugins/terminal_radio/_terminal_radio

touch ~/.oh-my-zsh/custom/plugins/terminal_radio/terminal_radio.plugin.zsh
```

Then add the following to your `.zshrc` file.

```zsh
plugins=(
    <other_plugins>
    terminal_radio
)
```

Then just update Zsh again and you should have autocompletion for the application.

```
source ~/.zshrc
```

## Uninstall

To uninstall the application simply run the following.

```bash
./scripts/uninstall.sh
```
