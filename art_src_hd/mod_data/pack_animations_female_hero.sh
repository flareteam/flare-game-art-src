#!/bin/bash

MOD_DIR="core"

# for filename in "$MOD_DIR"/animations/avatar/female/*.txt; do
#     flare-spritesheetpacker --save-always --mod "$MOD_DIR"/ --animation "$filename"
# done

SKIN_VARIANTS=(\
    'chain_coif'\
    'cloth_gloves'\
    'cloth_sandals'\
    'cloth_shirt'\
    'default_chest'\
    'default_feet'\
    'default_hands'\
    'default_legs'\
    'head_long'\
    'leather_gloves'\
    'leather_hood'\
    'mage_hood'\
    'mage_hood_alt1'\
    'mage_hood_alt2'\
    'plate_gauntlets'\
    'plate_helm'\
)

for skin_variant in "${SKIN_VARIANTS[@]}"; do
    filename="$MOD_DIR/animations/avatar/female_dark/${skin_variant}.txt"
    flare-spritesheetpacker --save-always --mod "$MOD_DIR"/ --animation "$filename"
done

