import codecs
from setuptools import setup
from webssh._version import __version__ as version


with codecs.open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='myewebssh',
    version=version,
    description='Web based ssh client',
    long_description=long_description,
    url='http://myelintek.com',
    packages=['webssh'],
    entry_points='''
    [console_scripts]
    wssh = webssh.myelintek:main
    ''',
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'tornado==5.1.1',
        'paramiko==2.4.2',
    ],
)
