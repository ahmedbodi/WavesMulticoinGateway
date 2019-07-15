# Waves-Multicoin-Gateway

The project realizes a Multicoin-Gateway for the Wavesplatform.
To do that, it makes use of the Waves-Gateway-Framework.
Common logic of how a such an Gateway operates is already defined in the Framework.
This project does only define the logic that is necessary to communicate with a Multicoin node.

## Getting started

The requirements of this project are defined in the file: requirements.txt.
Please run the following command to install them:
```bash
pip3 install -r requirements.txt
```
This will also install the framework.

You have to provide a configuration for the Waves-Multicoin-Gateway.
```
# when using prod mode, file logging is enabled
environment = debug
```
This configuration file must be named `config.cfg` and be placed in the root directory.
You have to replace the addresses with your own ones.

The server can be started by calling: `python3.5 main.py`.

## Coverage
```bash
python3.5 -m nose waves_multicoin_gateway/test --with-coverage --cover-package waves_multicoin_gateway
```

## Linting
```bash
python3.5 -m pylint main.py
python3.5 -m pylint waves_multicoin_gateway
```
