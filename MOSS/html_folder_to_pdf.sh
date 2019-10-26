#!/usr/bin/env bash
# Recursively convert all HTML files in this folder (and sub-folders) to PDF
if [ "$#" -ne 1 ] ; then
    echo "USAGE: $0 <HTML_folder>" ; exit 1
fi

for f in $(find $1 -name *.html) ; do wkhtmltopdf $ARGS $f $(echo $f | rev | cut -d'.' -f2- | rev).pdf ; done
pdfunite $1/*.pdf $(echo $1 | sed 's:/*$::').pdf
