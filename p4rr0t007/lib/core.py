# -*- coding: utf-8 -*-
import re
import sys
import logging
from itertools import imap
from nicelog.formatters import Colorful

DEFAULT_ENCODING = 'utf-8'

# enforce utf-8
reload(sys)
sys.setdefaultencoding(DEFAULT_ENCODING)


def utf8(string):
    return string.encode('utf-8', 'ignore')


def colorize_logger(logger, stream=None, level=logging.DEBUG):
    logger.handlers = []
    logger.filters = []
    stream = stream or sys.stderr
    handler = logging.StreamHandler(stream=stream)
    handler.setLevel(level)
    handler.setFormatter(Colorful())
    logger.addHandler(handler)
    return logger


def get_logger(name=None, level=logging.DEBUG):
    logger = logging.getLogger(name)
    colored = colorize_logger(logger)
    return colored


def is_valid_python_name(string=None):
    string = string or br''
    return re.match(r'^[a-zA-Z_][\w_]*$', string) is not None


def python_object_name(item, module=True):
    if not isinstance(item, type):
        return python_object_name(type(item))

    return br'.'.join(filter(is_valid_python_name, (module and item.__module__, item.__name__)))


def typeof(item):
    return repr(type(item))


__internal_attr_regex__ = re.compile(r'^__(?P<attr>[a-zA-z_]\w)')


def string_to_int(s):
    return int(bytes(s).encode('hex'), 16)


def lpad(s, length, char='\0'):
    return s.rjust(length, char)


def rpad(s, length, char='\0'):
    return s.ljust(length, char)


def int_to_string(i):
    return format(int(i), 'x')


def xor(left, right):
    maxlength = max(map(len, (left, right)))

    ileft = string_to_int(rpad(left, maxlength))
    iright = string_to_int(rpad(right, maxlength))
    xored = ileft ^ iright
    return int_to_string(xored)


def slugify(string):
    return re.sub(r'\W+', '_', string.strip()).lower()


def is_internal_attribute(name):
    return __internal_attr_regex__.match(name) is not None


def unpack_object_key(key, prefix='#', suffix=''):
    return utf8(key).lstrip(prefix).rstrip(suffix)


def pack_object_key(key, prefix='#', suffix=''):
    key = unpack_object_key(key, prefix, suffix)
    return b''.join(map(utf8, [prefix, key, suffix]))


class ObjectKeyError(KeyError):
    def __init__(self, odict, key):
        tmpl = '{0} does not contain key: {1}'
        msg = tmpl.format(odict, key)
        super(ObjectKeyError, self).__init__(msg)


class ObjectDict(dict):
    def __init__(self, *args, **kw):
        self.__ordered_keys = []
        super(ObjectDict, self).__init__(*args, **kw)
        self.__ordered_keys.extend(self.keys())

    def __setitem__(self, key, value):
        key = pack_object_key(key)
        if key not in self.__ordered_keys:
            self.__ordered_keys.append(key)

        return super(ObjectDict, self).__setitem__(key, value)

    def __getitem__(self, key):
        key = pack_object_key(key)
        return super(ObjectDict, self).__getitem__(key)

    def iterkeys(self):
        for key in imap(unpack_object_key, super(ObjectDict, self).iterkeys()):
            yield key

    # def items(self):
    #     return list(self.iteritems())

    # def iteritems(self):
    #     for key in self.__ordered_keys:
    #         ukey = unpack_object_key(key)
    #         value = self.get(ukey)
    #         yield key, value

    def itervalues(self):
        for key in imap(unpack_object_key, super(ObjectDict, self).iterkeys()):
            yield self[key]

    def __getattr__(self, attr):
        if is_internal_attribute(attr):
            return super(ObjectDict, self).__getattribute__(attr)

        try:
            return self[attr]
        except (KeyError, ):
            raise ObjectKeyError(self, attr)

        except (AttributeError, ):
            return super(ObjectDict, self).__getattribute__(attr)


class BinaryString(bytes):
    @classmethod
    def from_int(cls, value):
        return cls(hex(value).decode('hex'))

    @classmethod
    def from_unicode(cls, string, encoding=None):
        encoding = encoding or DEFAULT_ENCODING
        return cls(string.encode(encoding))

    def to_hex(self):
        return self.encode('hex')

    def to_int(self):
        return int(self.to_hex(), 16)

    def to_binary_representation(self):
        return '{0:b}'.format(self.to_int())

    @classmethod
    def ensure_can_xor(cls, other):
        if not isinstance(other, BinaryString):
            raise TypeError('cannot XOR a BinaryString with a')

        return BinaryString(other)

    def xor_with(self, other, from_left=True, encoding=None):
        if isinstance(other, unicode):
            other = BinaryString.from_unicode(other, encoding)

        elif isinstance(other, bytes):
            other = BinaryString(other)

        if from_left:
            left = self
            right = other
        else:
            left = other
            right = self

        other = self.ensure_can_xor(other)

        value = self.to_int() ^ other.to_int()
        return BinaryString.from_int(value)

    def __xor__(self, other):
        return self.xor_with(other)

    def __rxor__(self, other):
        return self.xor_with(other, from_left=False)


class String(unicode):
    __options__ = {}

    def __init__(self, data):
        super(String, self).__init__(data, **self.__options__)

    @classmethod
    def new(cls, data):
        return cls(data)

    def slugify(self, repchar='-'):
        slug_regex = re.compile(r'(^[{0}._-]+|[^a-z-A-Z0-9_.-]+|[{0}._-]+$)'.format(repchar))
        strip_regex = re.compile(r'[{0}._-]+'.format(repchar))

        transformations = [
            lambda x: slug_regex.sub(repchar, x),
            lambda x: strip_regex.sub(repchar, x),
            lambda x: x.strip(repchar)
        ]
        result = unicode(self)
        for process in transformations:
            result = process(result)

        return self.new(result)


class SafeString(String):
    __options__ = {
        'errors': 'ignore'
    }


def force_unicode(s):
    return SafeString(s)


def slugify_string(name, repchar):
    slug_regex = re.compile(r'(^[{0}._-]+|[^a-z-A-Z0-9_.-]+|[{0}._-]+$)'.format(repchar))
    strip_regex = re.compile(r'[{0}._-]+'.format(repchar))

    transformations = [
        lambda x: slug_regex.sub(repchar, x),
        lambda x: strip_regex.sub(repchar, x),
        lambda x: x.strip(repchar),
        lambda x: x.lower(),
    ]
    result = name
    for process in transformations:
        result = process(result)

    return result


def nonempty_string(string):
    return isinstance(string, basestring) and len(string.strip()) > 0
