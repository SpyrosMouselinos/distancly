#!/bin/bash
pip3 uninstall distancly -y
python3 setup.py sdist bdist_wheel
pip3 install dist/distancly-0.1-py3-none-any.whl
rm -rf build
rm -rf distancly.egg-info
