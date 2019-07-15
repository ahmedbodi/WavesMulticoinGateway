# Waves-Multicoin-Gateway

The project realizes a Multicoin-Gateway for the Wavesplatform.
To do that, it makes use of the Waves-Gateway-Framework.
Common logic of how a such an Gateway operates is already defined in the Framework.
This project does only define the logic that is necessary to communicate with a Multicoin node.

## Donations
- BTC: 19zaT1xsqnsjjiBsM4W4msSo9GrKy4T6nQ
- LTC: Ld8BoGKBuXc7wMHf9crPU9gWRb92KcgBur
- ETH: 0x979cb6eE64873a37C9B190267223f6202834cAE5
- BCH: qq4f4nt34ky9atge98jvpe6tjtxpznw8ncszlg4ymr
- ZEC: t1UBu72xrf1dbzEFrA9LA3QnUYmQF36AqEg
- BSV: qzasmr3ledh3df7r29drs5andy0welcfuq3c4qj948
- ETC: 0x61DCBd3B900610E39336688b64b87196eA5E7667

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
