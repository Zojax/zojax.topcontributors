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
from zope.component import getUtility
from zope.location import LocationProxy
from zope.traversing.browser import absoluteURL
from zope.app.security.interfaces import IAuthentication, PrincipalLookupError

from zojax.layout.interfaces import ILayout
from zojax.layoutform import Fields, PageletDisplayForm
from zojax.principal.profile.interfaces import IProfileFields
from zojax.principal.profile.interfaces import IPersonalProfile

from zojax.cache.keys import Path
from zojax.cache.view import cache
from zojax.cache.timekey import TimeKey, each6hours

from zojax.topcontributors.interfaces import \
    ITopContributors, ITopContributorsAware


class TopContributorsPortlet(object):

    def listMembers(self):
        view = getattr(self.manager, 'view', None)
        if ILayout.providedBy(view):
            context = view.maincontext
        else:
            context = self.context

        while not ITopContributorsAware.providedBy(context):
            context = context.__parent__
            if context is None:
                return ()

        auth = getUtility(IAuthentication)
        contributors = ITopContributors(context)

        members = []
        for score, principal in contributors[:self.number]:
            try:
                principal = auth.getPrincipal(principal)
            except PrincipalLookupError:
                continue

            members.append(LocationProxy(principal, self))

        return members

    @cache('portlet.topcontributors', Path, TimeKey(each6hours))
    def updateAndRender(self):
        return super(TopContributorsPortlet, self).updateAndRender()


class PrincipalView(PageletDisplayForm):

    @property
    def fields(self):
        content = self.content
        configlet = getUtility(IProfileFields)

        portlet = self.context.__parent__

        fields = []
        for name in portlet.fields:
            field = configlet.get(name)
            if field is not None and field.visible:
                if content.get(name, field.missing_value) \
                        is not field.missing_value:
                    fields.append(field)

        return Fields(*fields)

    def update(self):
        request = self.request
        context = self.context

        profile = IPersonalProfile(context)

        self.author = profile.title
        self.avatar = profile.avatarUrl(request)

        space = profile.space
        if space is not None:
            self.profile = '%s/'%absoluteURL(space, request)
        else:
            self.profile = None

        self.content = profile.getProfileData()

        super(PrincipalView, self).update()

    def getContent(self):
        return self.content
