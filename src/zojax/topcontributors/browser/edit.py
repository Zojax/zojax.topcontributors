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
from zope import interface, component
from zojax.wizard.step import WizardStep
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.topcontributors.interfaces import \
    _, ITopContributors, ITopContributorsAware

from table import ContributorsTable


class TopContributors(WizardStep):

    def update(self):
        super(TopContributors, self).update()

        self.contributors = ITopContributors(self.context)

        request = self.request
        if 'contributors.remove' in request:
            ids = request.get('contributor.id', ())
            if not ids:
                IStatusMessage(request).add(
                    _('Please select members to remove.'), 'warning')
            else:
                for id in ids:
                    self.contributors.remove(id)

                IStatusMessage(request).add(_('Members have been removed.'))


class ContributorsTable(ContributorsTable):
    component.adapts(
        ITopContributorsAware, interface.Interface, TopContributors)

    pageSize = 20
    enabledColumns = ('id', 'member', 'score')
