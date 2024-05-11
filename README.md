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

## Run the app

Place `.txt` files into `./data` directory and run `app.py` with the provided venv.

```shell
source venv/bin/activate
python3 app.py
```

The `./data` directory is created if it doesn't exist. So you can run the app to initialise the input directory.

## Voices

You can run `./utils/tts.py` to list all available voices.