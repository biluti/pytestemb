# !/bin/bash

# gen deb for Ubuntu 14.04 & Python 2.7

PACKAGE_NAME="pytestemb-lib"

echo "copy pytestemb source files"

mkdir -p deb/usr/local/lib/python2.7/dist-packages
rm -rf deb/usr/local/lib/python2.7/dist-packages/*


rm -rf ../src/pytestemb/*.pyc
cp -rv ../src/pytestemb/ deb/usr/local/lib/python2.7/dist-packages


# write version
version=$(grep -h "VERSION_STRING *= " ../src/pytestemb/__init__.py | sed s/"VERSION_STRING .*= \""// | sed s/'"'//)
echo $version

sed -i '/^Package: / c\
Package: '${PACKAGE_NAME}'' ./deb/DEBIAN/control
sed -i '/^PACKAGE_NAME=/ c\
PACKAGE_NAME='${PACKAGE_NAME}'' ./deb/DEBIAN/prerm
sed -i '/^PACKAGE_NAME=/ c\
PACKAGE_NAME='${PACKAGE_NAME}'' ./deb/DEBIAN/postinst

sed -i '/^Version: / c\
Version: '${version}'' ./deb/DEBIAN/control


dpkg-deb --build deb $PACKAGE_NAME-${version}.deb

rm -r ./deb/usr/local/lib/python2.7/dist-packages/*

echo "end"
