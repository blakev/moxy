#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# >>
#   moxy, 2020
#   Blake VandeMerwe
# <<

from typing import List

try:
    import cython  # type: ignore
except ImportError:  # pragma: no cover
    compiled: bool = False
else:  # pragma: no cover
    try:
        compiled = cython.compiled
    except AttributeError:
        compiled = False

__version__ = (0, 1, 0)
VERSION = version_str = '.'.join(map(str, __version__))

__all__ = [
    '__version__',
    'VERSION',
    'version_str',
    'version_info',
    'version_info_str',
    'compiled',
]


def version_info_str() -> str:
    items: List[str] = []
    for k, v in version_info().items():
        items.append('{:>30} {}'.format(k + ':', str(v).replace('\n', ' ')))
    return '\n'.join(items)


def version_info() -> dict:
    import sys
    import platform
    from pathlib import Path
    info = {
        'moxy version': VERSION,
        'moxy compiled': compiled,
        'install path': Path(__file__).resolve().parent,
        'python version': sys.version,
        'platform': platform.platform(),
    }
    return info
