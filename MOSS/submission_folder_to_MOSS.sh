#!/usr/bin/env bash
if [ "$#" -ne 2 ] ; then
    echo "USAGE: $0 <submission_folder> <language>"; exit 1
fi
cd $1
nums=$(ls -l */*.java | rev | cut -d'/' -f1 | rev | sort | uniq)

echo -n "Submitting code for $(echo $nums | tr ' ' '\n' | wc -l) problems to MOSS... "
for f in $nums ; do moss.pl -l $2 */$f > $f.log 2>/dev/null & done
echo "done"

echo -n "Waiting for jobs to finish... "
for job in $(jobs -p) ; do wait $job ; done
echo "done"
