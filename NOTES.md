apparat_launcher notes
==========

![logo](https://raw.githubusercontent.com/yafp/apparat_launcher/master/apparat_launcher/gfx/core/128/appIcon.png)


# Developing
## Debugging
Usage: ```python -m pdb apparat_launcher.py```

## Pylint
Pylint is a linter for Python.
Usage: ```pylint *.py```

## Travis CI
Travis CI can help doing automated builds after each commit to the repository. Repo needs a ```.travis.yml``` in the core folder
https://travis-ci.org/profile/yafp


# Documentation
## Epydoc
Generating API documentation via epydoc

### HTML Output
Usage:  ```epydoc apparat_launcher/*.py --name=apparat_launcher --url=https://github.com/yafp/apparat_launcher --graph=classtree -v -o apidoc/```



# Building

## Requirements.txt
### Pre-Requirements
Usage: ```pip install pipreqs```

### Creation of requirements.txt
Usage:  ```pipreqs /path/to/project```

## setup.py
* http://python-packaging.readthedocs.io/en/latest/minimal.html

### Help
Usage: 
```python setup.py --help```
```python setup.py --help install```


### Tests
Usage: ```python setup.py test```

### Builds
Usage: ```python setup.py build```

### Install
Usage: ```python setup.py install```







