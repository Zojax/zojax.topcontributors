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
from zojax.topcontributors.interfaces import _


class ITopContributorsTable(interface.Interface):
    """ table """


class ITopContributorsPortlet(interface.Interface):
    """ portlet """

    label = schema.TextLine(
        title = _(u'Label'),
        required = False)

    number = schema.Int(
        title = _(u'Number of members'),
        description = _(u'Number of members to display'),
        default = 7,
        required = True)

    fields = schema.List(
        title = _(u'Profile fields'),
        description = _(u'List of profile fields to show in portlet.'),
        value_type = schema.Choice(vocabulary='profile.fields'),
        default = [],
        required = False)


class ITopContributorsPortletItem(interface.Interface):
    """ pagelet type """
