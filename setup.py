from distutils.core import setup

setup(
    name='apparat',
    version_file = open(os.path.join(mypackage_root_dir, 'version.py'))
    version = version_file.read().strip()
    
    version='0.1dev',
    packages=['apparat',],
    license='GPL3,
    long_description=open('README.md').read(),
)
