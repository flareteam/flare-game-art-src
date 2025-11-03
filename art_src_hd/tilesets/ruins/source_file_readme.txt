the source file is a bit complicated.

the first 4 layers are for default tiles, the 4 on the right side are for snow / frozen tiles.
Included are 2 world environments (one for default and one for frozen). 

To give the correct lighting effect - when rendering the default tiles - you need to use the "not frozen" world environment, else you need to use the "frozen" world environment

The bottom layers are masking layers needed for some special cases.

Also some tiles use an shadow catcher (pillars, statue), these renders have soft unwanted shadows by default (coming from the HDRI). these are really weak, but I removed them with gimp's curves function.
