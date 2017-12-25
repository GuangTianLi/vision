"""
Copy from Scrapy

his module provides some functions and classes to record and report
references to live object instances.

If you want live objects for a particular class to be tracked, you only have to
subclass from object_ref (instead of object).

About performance: This library has a minimal performance impact when enabled,
and no performance penalty at all when disabled (as object_ref becomes just an
alias to object in that case).
"""

from __future__ import print_function

import weakref
from collections import defaultdict
from time import time

NoneType = type(None)
live_refs = defaultdict(weakref.WeakKeyDictionary)


class object_ref(object):
    """Inherit from this class (instead of object) to a keep a record of live
    instances"""

    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        live_refs[cls][obj] = time()
        return obj
