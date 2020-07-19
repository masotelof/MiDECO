#!/bin/bash

FileExt='inp'

echo "Program mDE"
echo "Executing the files within the directory $1"
echo "Using the options from $2"

for fileinp in "${1}"/*.inp
do
	if [[ -f $fileinp ]]; then
		filename=$(basename "$fileinp")
		fname="${filename%.*}"
		path=$(dirname "$fileinp")
		fileeout="${path}/${fname}.eout"
		binaryfile="${path}/${fname}.dat"

		if [[ ! -f "${fileeout}" ]]; then
			python3 run_mDE.py -i ${fileinp} -o ${fileeout} -b ${binaryfile} -c ${2} -l debug
		else
			echo "File ${fname}.eout already exists"
		fi
	fi
done
