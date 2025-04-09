#!/usr/bin/env bash
# Rename the contents of an extracted PrairieLearn "Download Best Submitted Files" zip for MossNet compatibility
# Niema Moshiri 2024
set -e

# check args
if [ $# -ne 2 ] ; then
    echo "USAGE: $0 <input_submissions_dir> <output_renamed_dir>"; exit 1
fi
if [ ! -d "$1" ] ; then
    echo "Extracted PrairieLearn 'Best Submissions' folder not found: $1"; exit 1
fi
if [ -d "$2" ] ; then
    echo "Output renamed submissions folder already exists: $2"; exit 1
fi
numfiles=$(find "$1" -type f -name "*.*" | wc -l)
if [ $numfiles -eq 1 ] ; then
    echo "Invalid PrairieLearn 'Best Submissions' folder: $1"; echo "It should contain student email folders, each of which contains assignment category folders, which contain source code files"; exit 1
fi

# copy files to output directory
curr=1
mkdir "$2"
for f in $(find "$1" -type f -name "*.*") ; do
    echo -ne "Renaming file $curr of $numfiles...\r"
    email=$(echo "$f" | python3 -c "from sys import stdin; print([s for s in stdin.read().split('/') if '@' in s][0].split('_')[0].strip())")
    dest="$2/$email/$(echo $f | rev | cut -d'/' -f1 | rev | sed 's/.*[0-9]\{4,\}_//')"
    mkdir -p "$2/$email"
    cp "$f" "$dest"
    curr=$((curr + 1))
done
echo "Successfully renamed $numfiles files"
