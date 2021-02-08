#! /bin/bash
input_files=(*.svg)

for file in "${input_files[@]}"; do  # loop through the array
    filename=$(basename -- "$file" .svg)
    inkscape -w 100 -h 100 "$file" -o "../${filename,,}.png"
done
