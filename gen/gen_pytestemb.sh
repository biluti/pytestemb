# !/bin/bash



echo "import pytestemb source files"

rm -r pytestemb/disutil/pytestemb/*
mkdir -p  pytestemb/disutil/pytestemb/
cp -rv ../src/pytestemb/* pytestemb/disutil/pytestemb

cd ./pytestemb/disutil/
python setup.py sdist
echo "end"
 



    
    