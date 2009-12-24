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
from zope import interface, schema
from zope.component.interfaces import IObjectEvent
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('zojax.topcontributors')


class ITopContributorsAware(interface.Interface):
    """ marker interface for object that supports top-contributors """


class ITopContributors(interface.Interface):
    """ contributors rating """

    def remove(principal):
        """ remove principal score """

    def contribute(principal, score):
        """ contribute to """

    def __len__():
        """ total contributors """

    def __iter__():
        """ yeilding (score, principal) from bigger score to lower """

    def __getitem__(key):
        """ get (score, principal) by index """


class IScore(interface.Interface):
    """ score information """

    score = schema.Int(
        title = u'Score',
        required = True)

    principal = schema.TextLine(
        title = u'Principal',
        required = True)
