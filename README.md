# LDI_project
Final project for ELEN90088 System Optimisation &amp; Machine Learning

## Packages
### echo
Package for handling echo related tasks. Uses the python wrapper for sox, which requires the sox system library, as well as the python library
```
# optional - if you want support for mp3, flac and ogg files
$ apt-get install libsox-fmt-all
# install the sox command line tool
$ apt-get install sox
# install pysox
$ pip install sox
```

Read more [here](https://pysox.readthedocs.io/en/latest/)

#### generate_echos.py
Utilities to batch generate echo files suitable for testing algorithms.
A package will be supplied directly, but feel free to generate your own if required.