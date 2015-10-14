#!/bin/bash

DISTDIR="dist"

rm -rf $DISTDIR
git checkout --theirs master -- $DISTDIR

cd $DISTDIR
# make a subdirectory for each package
for wheel in *; do
	package_name=$(echo $wheel | cut -d - -f 1)
	if [ ! -e $package_name ]; then
		mkdir $package_name
	fi
	mv $wheel $package_name
	echo "Put $wheel in $package_name"
done

cd ..

git add --all $DISTDIR
git commit -m "Updated wheels from `git log master -1 --pretty=short --abbrev-commit`"
