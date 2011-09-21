# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2011 Fourth Paradigm Development, Inc.
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
from django import template
from django import shortcuts
from django import forms
from django.views.decorators import vary

from django_openstack import api
from django_openstack.auth import views as auth_views
from django.contrib import messages

from django import forms

import json

#from savage.network import zeromq

piston_contact = 'http://dev.pistoncloud.com/Contact'


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
    # Is this the right place for the code activation?
    if request.method == 'POST':
        postreturned = request.POST
        pentos_uri = postreturned.get('pentos_uri')
        pentos_checksum = postreturned.get('pentos_checksum')
        messages.info(request, "URI: %s" % pentos_uri)
        messages.info(request, "Checksum: %s" % pentos_checksum)
        
        # Build Update Command
        update_cmd = json.dumps({'update': True, 'url': pentos_uri, 'checksum': pentos_checksum})
        # messages.info(request, "update_cmd: %s" % update_cmd)

        #with zeromq.InterruptingChild() as child:
        #    reply = json.loads(child.send_recv(update_cmd))
        #    time.sleep(0.3) # let it finish...
        #    reply = json.loads(child.send_recv(status_cmd))
        #    self.assertEquals(reply['status'], 'complete')
        #    self.assertEquals(file(self.output_file.name, 'rb').read(), 'rawr\n')
        
        return shortcuts.render_to_response('dash_pistonupdating.html', {
        }, context_instance=template.RequestContext(request))
    else:
        return shortcuts.render_to_response('dash_pistonupdates.html', {
        }, context_instance=template.RequestContext(request))

def pistonexpired(request):
    return shortcuts.render_to_response('dash_pistonexpired.html', {
    }, context_instance=template.RequestContext(request))
    
def pistonfeedback(request):
    return shortcuts.render_to_response('dash_pistonfeedback.html', {
    }, context_instance=template.RequestContext(request))
    

    
    