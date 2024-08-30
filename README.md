# Text To Speech

## Installation

First requirements have to be installed within the virtual python environment at `./venv`:

```shell
source venv/bin/activate
pip install -r requirements.txt
```

If you don't have a virtual python environment under `./venv` you can initialise it with

```shell
python3 -m venv venv
```

After successful initialisation you can then activate it and install requirements as stated above.

### Upgrade

For upgrading the all requirements within the `requirements.txt` simply run:

```shell
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

## Configuration

Create a file `tts.json` in `./data` directory with the config of your directory and speakers. Here a config:

```json
{
  "folders": [
    {
      "dir": "./data/speaker1",
      "config": "./data/speaker1.json"
    },
    {
      "dir": "./data/speaker2",
      "config": "./data/speaker2.json"
    }
  ]
}
```

Create the directories mentioned in your config file and place `.txt` files in them.

Also create the mandatory speakers.json files that look like this:

```json
{
  "voice": "en-US-BrianMultilingualNeural",
  "rate": "+0%",
  "volume": "+0%",
  "pitch": "+0Hz"
}
```

This way you can create text for multiple speakers and configurations with a single run of the application.

## Run the app

Make sure required config files are in place. Then run:

```shell
source venv/bin/activate
python3 tts.py example
```

## Voices

You can run `./utils/tts.py` to list all available voices.

## SRT Translations

There is also support to automatically translate srt files into various languages. After running the script there will
be translations files next to the original.

### Default Languages

```shell
source venv/bin/activate
python3 srt_translate.py example/subtitles.srt
```

### Custom Languages

```shell
source venv/bin/activate
python3 srt_translate.py example/subtitles.srt en de,ru,hi
```