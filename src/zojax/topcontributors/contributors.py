##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import types
from BTrees.Length import Length
from BTrees.IOBTree import IOBTree
from BTrees.OIBTree import OIBTree
from BTrees.OOBTree import OOTreeSet

from zope import interface
from interfaces import ITopContributors


class TopContributors(object):
    interface.implements(ITopContributors)

    @property
    def scores(self):
        scores = self.data.get('scores')
        if not isinstance(scores, OOTreeSet):
            scores = OOTreeSet()
            self.data['scores'] = scores

        return scores

    @property
    def principals(self):
        principals = self.data.get('principals')
        if principals is None:
            principals = OIBTree()
            self.data['principals'] = principals

        return principals

    @property
    def length(self):
        length = self.data.get('length')
        if length is None:
            length = Length(len(self.principals))
            self.data['length'] = length

        return length

    def __len__(self):
        return self.length()

    def __iter__(self):
        len = self.length()

        keys = self.scores.keys()

        for idx in xrange(len-1, -1, -1):
            yield tuple(keys[idx])

    def __getitem__(self, key):
        len = self.length()
        scores = self.scores

        if isinstance(key, types.SliceType):
            start = key.start or 0
            if (-start) > len:
                start = 0
            stop = key.stop or len
            if stop > len:
                stop = len

            len = len - 1
            keys = scores.keys()
            values = []

            for idx in range(start, stop):
                values.append(tuple(keys[len-idx]))

            return values
        else:
            return tuple(scores.keys()[len-key-1])

    def remove(self, principal):
        principals = self.principals

        if principal in principals:
            score = principals[principal]

            self.scores.remove((score, principal))
            del principals[principal]
            self.length.change(-1)

    def contribute(self, principal, score):
        length = self.length
        scores = self.scores
        principals = self.principals

        oldscore = principals.get(principal)
        if oldscore is not None:
            del principals[principal]
            scores.remove((oldscore, principal))
            score = oldscore + score
            length.change(-1)

        length.change(1)
        scores.insert((score, principal))
        principals[principal] = score
