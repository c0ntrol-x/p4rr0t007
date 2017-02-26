# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from p4rr0t007.lib import tr4nsl33t


def test_transleet():
    tr4nsl33t('coOl direct translations', extended=True).should.equal('(001 |)!|23(7 7|24n5147!0n5')
    tr4nsl33t('coOl direct translations', ultimate=True).should.equal(u'\xa2\xf8\u03a9\u2113 \u03b4\xa1\u044f\u0259\xa2\u03c4 \u03c4\u044f\u03b1\u03b7$\u2113\u03b1\u03c4\xa1\xf8\u03b7$')
