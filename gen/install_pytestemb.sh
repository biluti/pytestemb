# !/bin/bash



echo "install pytestemb"
mkdir /usr/local/lib/python2.7/dist-packages/pytestemb

cd ../src/pytestemb/ 
tar -cf - `find . -name "*.py" -print` | ( cd /usr/local/lib/python2.7/dist-packages/pytestemb && tar xBf - )


echo "end"
 

 
 
