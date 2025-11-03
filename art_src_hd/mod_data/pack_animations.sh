#!/bin/bash

MOD_DIR="core"

# for filename in "$MOD_DIR"/animations/avatar/male/*.txt; do
#     flare-spritesheetpacker --save-always --mod "$MOD_DIR"/ --animation "$filename"
# done
#
# for filename in "$MOD_DIR"/animations/enemies/*.txt; do
#     flare-spritesheetpacker --save-always --mod "$MOD_DIR"/ --animation "$filename"
# done

# for filename in "$MOD_DIR"/animations/loot/*.txt; do
#     flare-spritesheetpacker --save-always --mod "$MOD_DIR"/ --animation "$filename"
# done

SKIPPED_POWERS=(
    "bear_trap_trigger.txt"
    "runes_orange.txt"
    "runes_blue.txt"
    "spark_red_loop.txt"
    "status_freeze.txt"
)
for filename in "$MOD_DIR"/animations/powers/*.txt; do
    BASENAME=$(basename $filename)
    SKIP_FILE=0
    for skipped in "${SKIPPED_POWERS[@]}"; do
        if [ "$BASENAME" == "${skipped}" ]; then
            SKIP_FILE=1
            break
        fi
    done

    if [ $SKIP_FILE -eq 1 ]; then
        continue
    fi

    echo $filename
    flare-spritesheetpacker --save-always --mod "$MOD_DIR"/ --animation "$filename"
done

# use the packing result from bear trap power for trap trigger
cp "$MOD_DIR/animations/powers/bear_trap.txt" "$MOD_DIR/animations/powers/bear_trap_trigger.txt"

sed -i -e '/frame=[0-9]/d' -e 's/duration=400ms/duration=133ms/' -e '/#flare_sprite_packer/d' "$MOD_DIR/animations/powers/bear_trap_trigger.txt"
grep -h "frame=3" "$MOD_DIR/animations/powers/bear_trap.txt" | sed 's/frame=3/frame=0/g' >> "$MOD_DIR/animations/powers/bear_trap_trigger.txt"
grep -h "frame=2" "$MOD_DIR/animations/powers/bear_trap.txt" | sed 's/frame=2/frame=1/g' >> "$MOD_DIR/animations/powers/bear_trap_trigger.txt"
grep -h "frame=1" "$MOD_DIR/animations/powers/bear_trap.txt" | sed 's/frame=1/frame=2/g' >> "$MOD_DIR/animations/powers/bear_trap_trigger.txt"
grep -h "frame=0" "$MOD_DIR/animations/powers/bear_trap.txt" | sed 's/frame=0/frame=3/g' >> "$MOD_DIR/animations/powers/bear_trap_trigger.txt"

# use the packing result from rune power for orange/blue variants
cp "$MOD_DIR/animations/powers/runes.txt" "$MOD_DIR/animations/powers/runes_orange.txt"
cp "$MOD_DIR/animations/powers/runes.txt" "$MOD_DIR/animations/powers/runes_blue.txt"

sed -i -e '/frame=[0-3],0/d' -e '/frame=[0-3],2/d' -e 's/frame=\([0-3]\),1/frame=\1,0/g' -e 's/play_once/looped/g' -e '/#flare_sprite_packer/d' "$MOD_DIR/animations/powers/runes_orange.txt"
sed -i -e '/frame=[0-3],0/d' -e '/frame=[0-3],1/d' -e 's/frame=\([0-3]\),2/frame=\1,0/g' -e 's/play_once/looped/g' -e '/#flare_sprite_packer/d' "$MOD_DIR/animations/powers/runes_blue.txt"
