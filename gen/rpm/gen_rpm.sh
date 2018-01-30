# !/bin/bash


#
# Packing python junit from pip 
# $ /usr/local/bin/fpm --verbose -s python -t rpm junit-xml
#




clean()
{
	echo "clean"
	rm -rfv pytestemb/disutil/build
	rm -rfv pytestemb/disutil/dist
	rm -rfv pytestemb/disutil/pytestemb
	rm -rfv pytestemb/disutil/pytestemb.egg-info
}


if [ "$1" == "clean" ]; then
	clean
	echo "end"
	exit
fi



echo "import pytestemb source files"
mkdir -p  pytestemb/disutil/pytestemb


cp -v ../../src/pytestemb/*.py pytestemb/disutil/pytestemb


cd ./pytestemb/disutil/
#python setup.py -v bdist_rpm --force-arch noarch --requires 'python-colorama python-junit-xml'
python setup.py -v bdist_rpm --force-arch noarch


echo "end"
 


 
