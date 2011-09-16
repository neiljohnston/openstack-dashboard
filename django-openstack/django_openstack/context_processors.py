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
import json
import urllib2

from django.conf import settings
from django_openstack import api
from django.contrib import messages
from openstackx.api import exceptions as api_exceptions


def tenants(request):
    if not request.user or not request.user.is_authenticated():
        return {}

    try:
        return {'tenants': api.token_list_tenants(request, request.user.token)}
    except api_exceptions.BadRequest, e:
        messages.error(request, "Unable to retrieve tenant list from\
                                  keystone: %s" % e.message)
        return {'tenants': []}


def swift(request):
    return {'swift_configured': settings.SWIFT_ENABLED}

def pentos(request):
    #JSON Payload
    
    #'release':{'version' : '1.0',
    # 'uri' : 'http://updates.pistoncloud.com/update-releasetimestamp.tar',
    # 'notes' : 'Release notes for display in UI',
    # 'release_date' : 'human readable release date',
    # 'release_timestamp' : '1316154243',
    # 'checksum', '4038471504',
    # 'manifest', 'not currently in use'
    #}
    
    updateurl = 'updates.pistoncloud.com'
    updatemsg = 'Update Message'
    
    #Default states - Revise for prod.
    update = True
    version = '1.0'
    timestamp = ''
    licensed = False
    releasenote = ''
    
    #Update Path
    
    #Pull current PentOS version from existing arista/cluster
    install_version = '0.0'
    #Pull latest PentOS version from updates.pistoncloud.com
    
    #request for current verson info
    version = '1.1'
    #parse version response
    #compare install version to current
    
    
    
    return {'pentos': {
        'update': update,
        'version': version,
        'releasenote': releasenote,
        'timestamp': timestamp,
        'licensed': licensed,
        },
    }

def piston(request):
    extendedtools = True
    datatracking = False
    
    return {'piston': {
        'extendedtools': extendedtools,
        'datatracking': datatracking,
       },
    }

