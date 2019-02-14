#!/bin/bash

USAGE='usaeg: ./build.sh build|install'
CWD=$PWD

build(){
    # check out v0.9.0
    [[ ! -d webssh ]] && \
    git clone --branch=v0.9.0 https://github.com/myelintek/webssh.git

    # link myelintek src to webssh
    ln -vf ./src/myelintek.py ./webssh/webssh/myelintek.py
    ln -vf ./src/myeHandler.py ./webssh/webssh/myeHandler.py
    ln -vf ./src/myelintek_setup.py ./webssh/myelintek_setup.py
    ln -vf ./src/myeIndex.html ./webssh/webssh/templates/myeIndex.html
    ln -vf ./src/myeMain.js ./webssh/webssh/static/js/myeMain.js

    cd webssh && python2.7 myelintek_setup.py bdist_wheel
    
    [[ $? -eq 0 ]] && echo "build success, the wheel package is at $CWD/webssh/dist" || echo "build fail!! error code = $?"

}

function install(){
    pip uninstall -y myewebssh 2>/dev/null
    pip install $CWD/webssh/dist/myewebssh*
}

[[ $# == 0 ]] && echo $USAGE

while [[ $# > 0 ]]
do
	key="$1"
	shift
	case $key in
		install)
            build
			install
			shift
			;;
		build)
            build
			shift
			;;
		-h|--help)
			echo $USAGE
			shift
			;;
		*)
			# unknown option
			echo $USAGE ", unknown parameter: $key, "
			;;
	esac
done
