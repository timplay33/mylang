#!/usr/bin/env python3
"""
Setup script for MyLang Programming Language
"""

from setuptools import setup, find_packages
import os

# Read the README file


def read_readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='mylang',
    version='1.0.0',
    description='A simple, strongly-typed programming language with modern architecture',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='MyLang Team',
    author_email='team@mylang.dev',
    url='https://github.com/timplay33/mylang',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Compilers',
        'Topic :: Software Development :: Interpreters',
    ],
    keywords='programming-language interpreter compiler',
    entry_points={
        'console_scripts': [
            'mylang=mylang.__main__:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
