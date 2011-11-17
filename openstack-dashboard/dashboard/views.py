# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2011 Nebula, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Views for home page.
"""

import urlparse

from django import template
from django import shortcuts
from django.views.decorators import vary

from django_openstack.auth import views as auth_views

from savage.command.commands import arista as savage

@vary.vary_on_cookie
def splash(request):
    if request.user:
        if request.user.is_admin():
            return shortcuts.redirect('syspanel_overview')
        else:
            return shortcuts.redirect('dash_overview')

    form, handled = auth_views.Login.maybe_handle(request)
    if handled:
        return handled
    return shortcuts.render_to_response('splash.html', {
        'form': form,
    }, context_instance=template.RequestContext(request))


def pistondownloads(request):
    return shortcuts.render_to_response('dash_pistondownloads.html', {
    }, context_instance=template.RequestContext(request))

def pistonupdates(request):
    # TODO(neil) Is this the right place for the code activation?
    status, message = '', ''
    if request.method == 'POST':
        r = request.POST
        uri, chk = r.get('pentos_uri'), r.get('pentos_checksum')
        if uri is None or chk is None:
            status, message = 'error', 'Malformed update request.'
        else:
            purl = urlparse.urlparse(uri, scheme='')
            if purl.scheme in ('http', 'https'):
                status, message = savage.update_request(uri, chk)
            else:
                status, message = 'error', 'Unsupported update url'
    elif request.method == 'GET':
        status, message = savage.update_status()

    return shortcuts.render_to_response('dash_pistonupdates.html', dict(
        status=status, message=message),
        context_instance=template.RequestContext(request))

def pistonexpired(request):
    return shortcuts.render_to_response('dash_pistonexpired.html', {
    }, context_instance=template.RequestContext(request))

def pistonfeedback(request):
    return shortcuts.render_to_response('dash_pistonfeedback.html', {
    }, context_instance=template.RequestContext(request))
