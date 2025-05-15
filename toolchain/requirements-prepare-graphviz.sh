#!/bin/bash

# These commands should be executed in an environment
# python3 -m venv venv
# source venv/bin/activate

brew install graphviz
export CFLAGS="-I/opt/homebrew/include"
export LDFLAGS="-L/opt/homebrew/lib"
pip install pygraphviz