#!/usr/bin/env bash

echo "TRAVIS_OS_NAME = ${TRAVIS_OS_NAME}"

if [[ "${TRAVIS_OS_NAME}" == "linux" ]]; then
    curl -L https://packagecloud.io/tarantool/${TARANTOOL_VERSION}/gpgkey | sudo apt-key add -
    release=`lsb_release -c -s`
    sudo apt-get -y install apt-transport-https
    sudo rm -f /etc/apt/sources.list.d/*tarantool*.list
    echo "deb https://packagecloud.io/tarantool/${TARANTOOL_VERSION}/ubuntu/ $release main" | sudo tee /etc/apt/sources.list.d/tarantool_${TARANTOOL_VERSION}.list
    echo "deb-src https://packagecloud.io/tarantool/${TARANTOOL_VERSION}/ubuntu/ $release main" | sudo tee -a /etc/apt/sources.list.d/tarantool_${TARANTOOL_VERSION}.list
    sudo apt-get -qq update
    sudo apt-get -y install tarantool tarantool-queue
    sudo tarantoolctl stop example || exit 0
    sudo apt-get install pandoc
elif [[ "${TRAVIS_OS_NAME}" == "osx" ]]; then
    if [[ "${TARANTOOL_VERSION}" == "1_7" ]]; then
        brew install tarantool --HEAD
    else
        brew install tarantool
    fi

    brew install lua@5.1
    luarocks-5.1 install https://raw.githubusercontent.com/tarantool/rocks/gh-pages/queue-scm-1.rockspec
fi
