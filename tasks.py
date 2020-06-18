#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# >>
#   moxy, 2020
#   Blake VandeMerwe
# <<

import os
import glob
from pathlib import Path

from invoke import task

DIR = Path(__file__).resolve().parent


@task
def clean(c):
    c.run(f'rm -rf `find . -type d -name __pycache__`')
    c.run(f"rm -f `find . -type f -name '*.py[co]'`")
    c.run(f"rm -f `find . -type f -name '*~'`")
    c.run(f"rm -f `find . -type f -name '.*~'`")

    remove_files = [
        'moxy/*.c',
        'moxy/*.so',
        '.coverage',
        '.coverage.*',
    ]

    removables = [
        '.cache',
        '.pytest_cache',
        '.mypy_cache',
        'htmlcov',
        '*.egg-info',
        'dist',
        'build',
        'coverage.xml'
    ]
    for item in removables:
        c.run(f'rm -rf {item}')
    for item in remove_files:
        c.run(f'rm -f {item}')


@task
def test(c, cython=False, coverage=False):
    if cython:
        build_cython(c, debug=True)
    c.run(f'python -m pytest --cov=moxy')
    if coverage:
        c.run(f'coverage html')
        c.run(f'xdg-open htmlcov/index.html')

@task
def build_cython(c, debug=False):
    cmd = 'python setup.py build_ext --force --inplace'
    if debug:
        c.run(f'{cmd} --define CYTHON_TRACE')
    else:
        c.run(f'{cmd}')


@task(pre=(test, clean))
def build(c):
    build_cython(c, debug=False)
    c.run(f'python setup.py sdist bdist_wheel')
    c.run(f'SKIP_CYTHON=1 python setup.py bdist_wheel')
    c.run(f'twine check dist/*')


@task
def lint(c):
    source_files = []
    folders = 'moxy tests'
    for folder in folders.split(' '):
        source_files.extend(glob.glob(os.path.join(DIR, folder, '*.py'), recursive=True))
    files = " ".join(source_files)

    commands = [
        f'isort -rc -y',
        f'yapf -rpq {files}',
        f'mypy --pretty --no-site-packages --ignore-missing-imports {files}',
    ]
    for command in commands:
        cmd = command.split(' ')[0]
        print(f'----- {cmd} -----')
        c.run(command)

