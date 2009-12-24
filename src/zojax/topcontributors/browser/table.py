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
import cgi
from zope import interface, component
from zope.component import getUtility, queryMultiAdapter
from zope.traversing.browser import absoluteURL
from zope.app.security.interfaces import IAuthentication, PrincipalLookupError

from zojax.table.table import Table
from zojax.table.column import Column, AttributeColumn
from zojax.principal.profile.interfaces import IPersonalProfile
from zojax.topcontributors.interfaces import \
    _, ITopContributors, ITopContributorsAware

from interfaces import ITopContributorsTable


class ContributorsTable(Table):
    interface.implements(ITopContributorsTable)
    component.adapts(
        ITopContributorsAware, interface.Interface, interface.Interface)

    title = _('Top contributors')

    pageSize = 20
    enabledColumns = ('id', 'member', 'score')
    msgEmptyTable = _('No contributors information.')

    def initDataset(self):
        self.dataset = ITopContributors(self.context)


class IdColumn(Column):
    component.adapts(
        interface.Interface, interface.Interface, ITopContributorsTable)

    name = u'id'
    title = u''

    def query(self, default=None):
        return self.content[1]

    def render(self):
        return '<input type="checkbox" name="contributor.id:list" value="%s"/>'% \
            cgi.escape(self.content[1])


class MemberColumn(Column):
    component.adapts(
        interface.Interface, interface.Interface, ITopContributorsTable)

    name = u'member'
    title = _('Member')

    def update(self):
        super(MemberColumn, self).update()

        self.auth = getUtility(IAuthentication)

    def query(self, default=None):
        return self.content[1]

    def render(self):
        try:
            principal = self.auth.getPrincipal(self.content[1])
        except PrincipalLookupError:
            return self.content[1]

        profile = IPersonalProfile(principal)

        space = profile.space
        if space is not None:
            return '<a href="%s/">%s</a>'%(
                absoluteURL(space, self.request), cgi.escape(profile.title))
        else:
            cgi.escape(profile.title)


class ScoreColumn(Column):
    component.adapts(
        interface.Interface, interface.Interface, ITopContributorsTable)

    name = 'score'
    title = _('Score')

    def query(self, default=None):
        return self.content[0]
