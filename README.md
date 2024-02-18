# scattack

__Network attacks with Scapy__

This project was created to demonstrate the use of Scapy
to perform Wifi deauthentication, ARP cache poisoning and DHCP Starvation attacks for NEVA course at Sorbonne Université,
with the following instructions:

_Demonstrate the use of Scapy to perform Wifi deauthentication, ARP cache poisoning and DHCP Starvation attacks._
_Use the code from the suggested github repos (or more) to create a single platform to launch several attacks._

## Documentation

The documentation is available at <https://musikid.github.io/scattack>,
with the report available at <https://musikid.github.io/scattack/report.html>
or for the PDF format <https://musikid.github.io/scattack/index.pdf>.

## Development

### Setup

Ensure that you have Python 3.10 or higher installed.
It is recommended to use a virtual environment for development along with the `pdm` package manager.

```bash
cd scattack
pdm install -G:all
pdm use --venv in-project
sudo python -m scattack.gui
```

If you are using `pip` instead of `pdm`, you can install the dependencies with the following command:

```bash
cd scattack
python -m venv .venv
source .venv/bin/activate
pip install -e .
sudo python -m scattack.gui
```
