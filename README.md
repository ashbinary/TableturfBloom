# TableturfBloom

TableturfBloom is a GUI tool for adding and editing Tableturf Battle cards, [conveniently named after a K-pop song.](https://www.youtube.com/watch?v=AO6BlpKi3G0)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required libraries.

```bash
pip install byml
pip install zstd
pip install mmh3
pip install pyglet
```
This tool was made using Python 3.10.11, and may not work on earlier versions.

## Usage

Before running, make sure the `RSDB/MiniGameCardInfo.Product.XXX.rstbl.byml.zs` file from Splatoon 3's romFS is dumped and added to the root folder of the tool.

```
usage: TableturfBloom.py [-h] -n [NAME] [-num [NUMBER]] [-t [TYPE]] [-r [RARITY]]

options:
  -h, --help                      show help message and exit
  -n [NAME], -name [NAME]         input for the Tableturf card's internal name
  -num [NUMBER], -number [NUMBER] input for the Tableturf card's number (defaults to the byml's length)
  -t [TYPE], -type [TYPE]         input for the Tableturf card's category (defaults to "WeaponMain")
  -r [RARE], -rarity [RARE]       input for the Tableturf card's rarity ("Common", "Rare", or "Fresh")
```

Exiting the program will overwrite the `MiniGameCardInfo.Product.XXX.rstbl.byml.zs` file with the new card layout.
