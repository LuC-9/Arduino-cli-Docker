#!/bin/sh

echo 'Booting up Arduino Compiler...'

echo 'Çloning the Repository...'

cd /usr/src/
git clone $GITHUB_REPOURL sketch
cd sketch
mv *.ino sketch.ino

python -u /usr/src/app/compile.py

exit 0
