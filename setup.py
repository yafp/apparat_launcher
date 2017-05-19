#!/usr/bin/env python

from setuptools import setup


setup(
    ## project name
    name='apparat_launcher',

    ## description
    description='An application launcher for linux',
    long_description=open('README.md').read(),

    ## package name
    packages=['apparat_launcher'],

    ## version number
    version='0.1',

    ## Author & contact
    author='yafp',
    author_email='apparat_launcher@yafp.de',
    url='https://github.com/yafp/apparat_launcher',

    ## License
    license='GPLv3',

    ## What does your project relate to?
    keywords='application launcher',

    ## include images from gfx subfolder
    package_data={'apparat_launcher': [
        'gfx/core/*/*.png',
        'gfx/plugins/*/*/*.png',
    ]},


    include_package_data=True,

    install_requires=[
        #'wx>=3.0.0',
        #'psutil>=5.0.0',
        #'pyxdg>=0.25'
    ],

    ## See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        ## Environment
        'Environment :: X11 Applications :: Gnome',

        ## Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',

        ## Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        ## Specify the Python versions you support here. In particular, ensure
        ## that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
