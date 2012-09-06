# !/bin/bash

echo "import pytestemb source files"
rm -r pytestemb/disutil/pytestemb/*.py
cp -v ../src/pytestemb/*.py pytestemb/disutil/pytestemb
cd ./pytestemb/disutil/
python setup.py sdist
echo "end"
 



    
    