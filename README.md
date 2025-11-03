# HD Flare Art Sources

This repository contains updated Blender source files for https://github.com/flareteam/flare-game

These files support modern versions of Blender and use the EEVEE render backend. They are intended to be rendered at a larger resolution than the original flare-game assets (I've targeted a 3X resize). You can read more about the plan behind all of this here: https://github.com/flareteam/flare-game/issues/986

## Directory structure

- `art_src_hd` - The blend files are in here. Most, if not all, are accompanied by a "render.sh" shell script that will run the embedded Python scripts. You should also be able to run the scripts from directly in Blender, but sometimes the UI crashes. So I prefer the head-less method.
- `art_src_hd/mod_data` - A staging area where the Blender output is assembled. There is a script here to copy it to the `mods` folder on the top level
- `mods` - This is the complete mod that can be loaded in Flare. At the time of this writing, it is intended to be loaded on top of `fantasycore` and `empyrean_campaign`
- `tiled` - Contains versions of the tilesets to be used in Tiled, as well as a script to convert existing maps to the larger tile size

## Credits

Most of the credits are the same as flare-game. New textures (licensed CC0) sourced from cc0-textures.com have been added.

