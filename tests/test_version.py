#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# >>
#   moxy, 2020
#   LiveViewTech
# <<

import pytest

from moxy.version import *


def test_version():
    assert version_str == VERSION
    assert all(map(lambda d: isinstance(d, int), __version__))


def test_version_info():
    info = version_info()
    assert isinstance(info, dict)
    assert info['moxy version'] == VERSION


def test_version_info_str():
    info = version_info_str()
    assert info.strip().startswith('moxy')
