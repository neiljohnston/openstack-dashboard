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

# Imports for use in Dashboards request to server for release.json payload
# 
import json
import time
import os

from urllib2 import Request, urlopen, URLError, HTTPError

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


def getJSONasString(request, revisionurl):
    # Returns Piston's PentOS release information from the revision URL
    
    JSONstring = '' #Set the return string to empty, so we've a testable error
    
    #Pull latest release information from revisionurl
    revisionreq = Request(revisionurl)
    try:
        revisionreponse = urlopen(revisionreq)
    except URLError, e:
        if hasattr(e, 'reason'):
            messages.error(request, "URLError Reason:  %s" % e.reason)
        if hasattr(e, 'code'):
            messages.error(request, "URLError Code:  %s" % e.code)
        messages.info(request, "Unable to connect to Piston Update Service via internet. Please check internet connection.")
        return
    except HTTPError, e:
        if hasattr(e, 'reason'):
            messages.error(request, "URLError Reason:  %s" % e.reason)
        if hasattr(e, 'code'):
            messages.error(request, "URLError Code:  %s" % e.code)
        messages.info(request, "Unable to connect to Piston Update Service via internet. Please check internet connection.")
        return
    else:
        # Pull JSON package
        revisionreponse = revisionreponse.read()
        # Convert response to JSON
        JSONstring = str(revisionreponse)
    return JSONstring


def getTimestamp(request, filepath):
    try:
        file_timestamp = os.path.getctime(filepath)
    except OSError, e:
        messages.error(request, "OSError Code:  %s" % e.errno)
        file_timestamp = False
    return file_timestamp


def pentos(request):
    entitlement_key_path = './pentossupport/' #Replace for non-local env
    # /mnt/big/
    entitlement_key_name = 'entitlement.key'
    
    # /mnt/big/
    current_install_key_path = './pentossupport/' #Replace for non-local env
    current_install_key_name = 'entitlement.key'
    
    # this will be hosted on updates.pistoncloud.com
    revisionurl = 'http://onewheeldrive.net/release.json' #'http://updates.pistoncloud.com/release.json'
    
    update_available = False
    entitled = False

    #Pull latest release information from revisionurl at updates.pistoncloud.com
    #JSON Payload Format
    #
    #{'version' : '1.0',
    # 'uri' : 'http://updates.pistoncloud.com/update-releasetimestamp.tar',
    # 'notes' : 'Release notes for display in UI',
    # 'release_date' : 'human readable release date',
    # 'release_title' : 'Morgenstern'
    # 'release_timestamp' : '1316154243',
    # 'checksum': '4038471504',
    # 'manifest': 'not currently in use'
    #}
    
    JSONstring = getJSONasString(request, revisionurl)
    # Convert response to JSON
    if not JSONstring:
        messages.info(request, "No JSON Returned")
        return{}
    releaseJSON = json.loads(JSONstring)
    
    
    # *************************************************************
    #  Entitlement Handling
    # *************************************************************
    curent_time = time.time()
    entitlement_timestamp = getTimestamp(request, entitlement_key_path + entitlement_key_name)
    expiry_time = 90 * 24 * 60 * 60;
    if entitlement_timestamp:
        entitlement_expires = entitlement_timestamp + expiry_time
        entitled = (curent_time <= entitlement_expires)
    else:
        # Set Default UI behaviour for Entitlement if an OSError is thrown reaching entitlement key
        entitled = False


    # *************************************************************
    #  Update Logic
    # *************************************************************
    #request JSON describing latest PentOS release from updates.piston.com
    release_timestamp = releaseJSON['release_timestamp']
    #messages.info(request, "release_timestamp:  %s" % release_timestamp)
    # Get current PentOS intalls timestamp from existing arista/cluster
    installed_pentos_timestamp = getTimestamp(request, current_install_key_path + current_install_key_name)
    if installed_pentos_timestamp:
        #compare timestamps, note they need to be converted to floats
        update_available = float(installed_pentos_timestamp) < float(release_timestamp)
        # set update flag for UI to display update elements
    else:
        # Set Default UI behaviour if an OSError occures reaching PentOS Install Timestamp
        update_available = False
        
    # DEBUG OVERRIDE
    # update_available = True
    # entitled = False
    
    releaseJSON.update(entitled = entitled)
    releaseJSON.update(update=update_available)
    # messages.info(request, "releaseJSON:  %s" % releaseJSON)    
    return {'pentos': releaseJSON}
    

def piston(request):
    extendedtools = True
    # pentosJSONpath = '/mnt/big/pentos.json' #Anticipated
    pentosJSONpath = './pentossupport/pentos.json' #Current
    
    try:
        pentosfile = open(pentosJSONpath, 'r')
        pentosJSON = json.load(pentosfile)
        pentosfile.close()
        if pentosJSON['expanded_tools_download'] == True:
            # This catch expanded_tools_download when it's explicitely true
            extendedtools = pentosJSON['expanded_tools_download']
        else:
            # Account for config error if expanded_tools_download is invalid
            # by defaulting to hiding the tools link
            messages.error(request, "Your expanded_tools_download configuration may be incorrect, please validate.")
            extendedtools = False
    except IOError, e:
        messages.error(request, "IOError:  %s" % e)
        extendedtools = False
        
    datatracking = False
    return {'piston': {
        'expanded_tools_download': extendedtools,
        'tools_download_uri': pentosJSON['tools_download_uri'],
        'datatracking': datatracking,
       },
    }


