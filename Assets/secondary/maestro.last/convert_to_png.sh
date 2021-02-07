#! /bin/bash
input_files=(*.svg)

for file in "${input_files[@]}"; do  # loop through the array
    filename=$(basename -- "$file" .svg)
    inkscape -w 75 -h 75 "$file" -e "../../${filename,,}.png"
done
