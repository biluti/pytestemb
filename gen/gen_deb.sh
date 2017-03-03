# !/bin/bash



PACKAGE_NAME="pytestemb-lib"

echo "copy pytestemb source files"

#DISTPACKAGE=$(python3 -c "import site; print(list(filter(lambda x: x.find('/usr/local/') != -1 , site.getsitepackages()))[0])")

DISTPACKAGE="/usr/lib/python3/dist-packages/"

echo $DISTPACKAGE

mkdir -p deb$DISTPACKAGE
rm -rf deb$DISTPACKAGE*


rm -rf ../src/pytestemb/*.pyc
cp -rv ../src/pytestemb/ deb$DISTPACKAGE


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

rm -r ./deb$DISTPACKAGE*

echo "end"
