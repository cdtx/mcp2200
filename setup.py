import os
from setuptools import setup

setup(
    name='cdtx-mcp2200',
    version='0.0.1',
    description='Cross platform access to the Microchip MCP220 HID device',
    author='cdtx',
    classifiers=[
        'Programming Language :: Python :: 3.4',
    ],
    packages = ('cdtx.mcp2200',),
    namespace_packages = ('cdtx',),
    install_requires = ['pyusb']
)


