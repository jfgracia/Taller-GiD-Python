#!/bin/sh -f

rm -f "$2/$1.log"
rm -f "$2/$1.post.res"
rm -f "$2/$1.err"

# OutputFile: $2/$1.log
# ErrorFile: $2/$1.err

# Para OSX se hace un ejecutable usando la utiletia pyinstaller

"$3/main" "$2/$1"