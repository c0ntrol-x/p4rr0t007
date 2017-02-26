# -*- coding: utf-8 -*-
import os
import sys
from datetime import timedelta
from plant import Node

node = Node(__file__).dir
self = sys.modules[__name__]


self.BASE_URL = os.environ.get('BASE_URL') or 'http://localhost:5000'
self.SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(36).encode('hex')
self.SESSION_TYPE = 'redis'
self.SESSION_COOKIE_SECURE = True
self.PERMANENT_SESSION_LIFETIME = timedelta(hours=6)
self.SESSION_KEY_PREFIX = 'p4rr0t007:session:'
self.DEBUG = False


def update(**kw):
    for key, value in kw.items():
        setattr(self, key, value)

    if self.DEBUG:
        sys.stderr.write('\033[1;33m\n<settings>\n{}\n</settings>\n\033[0m'.format("\n".join(["{}={}".format(k, v) for k, v in self.__dict__.items() if k.upper() == k])))
