#!/usr/bin/bash

dir1=build
dir2=exe.win-amd64-3.5
dir=./$dir1/$dir2

rm -rf `find ${dir}/lib/PyQt5/ -type f | grep -Ev '(pyd|pyc|dll)'`
rm -rf ${dir}/lib/PyQt5/Qt5WebEngineCore.dll
rm -rf `find ${dir}/imageformats/ -type f | grep -v 'qico.dll'`

cd ./$dir1/
cp -r $dir2 wanbo
tar -zcf wanbo.tar.gz wanbo

