# !/bin/bash

mkdir -p pytestemb/disutil/pytestemb

echo "import pytestemb source files"

rm -r pytestemb/disutil/pytestemb/*

cp -rv ../src/pytestemb/* pytestemb/disutil/pytestemb
cp -rv ../src/script/* pytestemb/disutil/script
cd ./pytestemb/disutil/
python setup.py sdist upload -r parrotpy

rm -r ./pytestemb/*
rm -r ./script/*
echo "end"
 

