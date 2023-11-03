#!/bin/bash

if [[ -z "$1" ]]; then
	echo "Please provide the directory path as an argument."
	exit 1
fi

if [ ! -d "$1" ]; then
	echo "Directory not found."
	exit 1
fi

BACKGROUND='black_image.jpg'

# Generage a black_image.
if [[ ! -e $BACKGROUND ]]; then
	convert -size 1920x1080 xc:black black_image.jpg
	echo "Generated a black background file: $BACKGROUND."
fi

# Iterate over MP3 files in the directory.
for file in "$1"/*.mp3; do
  echo "$file"
	if [[ -f $file ]]; then
    output="$1/$filename.mp4"
		# Get the base filename without extension
		filename=$(basename "$file" .mp3)

		echo "Converting $file."
		ffmpeg -loop 1 -i "$BACKGROUND" -i "$file" -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "$output"
		echo "Converted $file to $output"
	fi
done
