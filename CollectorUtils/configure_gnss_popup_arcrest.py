# -*- coding: UTF-8 -*-
"""
   Copyright 2016 Esri
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at
       http://www.apache.org/licenses/LICENSE-2.0
   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.​
    This sample copies assignments from one project to another feature service

   This sample shows how to configure the GNSS fields for a popup
   in a webmap using the ArcREST library
"""

import arcrest
from arcresthelper import securityhandlerhelper
import argparse
import json


def main(args):
    """
    This
    :param args: arguments from argparse
    :return:
    """
    securityinfo = {}
    securityinfo['security_type'] = args.security_type
    securityinfo['username'] = args.username
    securityinfo['password'] = args.password
    securityinfo['org_url'] = args.org_url
    securityinfo['proxy_url'] = args.proxy_url
    securityinfo['proxy_port'] = args.proxy_port
    securityinfo['referer_url'] = args.referer_url
    securityinfo['token_url'] = args.token_url
    securityinfo['certificatefile'] = args.certificate_file
    securityinfo['keyfile'] = args.keyfile
    securityinfo['client_id'] = args.client_id
    securityinfo['secret_id'] = args.secret_id
    try:
        # Authenticate
        shh = securityhandlerhelper.securityhandlerhelper(securityinfo)
        if not shh.valid:
            print (shh.message)
        else:
            # Get portal instance
            portal_admin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler)
            # Update each map by the provided id
            for map_id in args.map_ids:
                try:
                    # Get item
                    item = portal_admin.content.getItem(itemId=map_id).userItem
                    # Get the map data json
                    map_data = item.item.itemData('json')
                    # configure the GNSS popup fields
                    map_data = configure_gnss_popup(map_data, visible=args.visible)
                    # Update the item
                    item_params = arcrest.manageorg.ItemParameter()
                    item.updateItem(itemParameters=item_params,
                                    clearEmptyFields=True,
                                    data=None,
                                    serviceUrl=None,
                                    text=json.dumps(map_data).encode('utf8', errors='replace')
                                    )
                    print("Successfully Configured Map Item Id: {}".format(map_id))
                except Exception as e:
                    print("Error Configuring id: {}".format(map_id))
                    print(e)
    except Exception as e:
        print(e)


def configure_gnss_popup(map_data, visible=False):
    """
    This updates the visibility of all of the GPS
    related attributes
    :param map_data: The map data (dictionary/json) to update
    :param visible: Visible (True) or not (False)
    :return: the modified map_data dictionary
    """
    # The names of fields to be updated
    fields_to_update = ['ESRIGNSS_RECEIVER',
                        'ESRIGNSS_H_RMS',
                        'ESRIGNSS_V_RMS',
                        'ESRIGNSS_LATITUDE',
                        'ESRIGNSS_LONGITUDE',
                        'ESRIGNSS_ALTITUDE',
                        'ESRIGNSS_PDOP',
                        'ESRIGNSS_HDOP',
                        'ESRIGNSS_VDOP',
                        'ESRIGNSS_FIXTYPE',
                        'ESRIGNSS_CORRECTIONAGE',
                        'ESRIGNSS_STATIONID',
                        'ESRIGNSS_NUMSATS',
                        'ESRIGNSS_FIXDATETIME',
                        'ESRIGNSS_AVG_H_RMS',
                        'ESRIGNSS_AVG_V_RMS',
                        'ESRIGNSS_AVG_POSITIONS',
                        'ESRIGNSS_H_STDDEV']
    for operational_layer in map_data["operationalLayers"]:
        if "popupInfo" in operational_layer and "fieldInfos" in operational_layer["popupInfo"]:
            for field_info in operational_layer["popupInfo"]["fieldInfos"]:
                # Set all fields as visible/editable
                if field_info["fieldName"] in fields_to_update:
                    field_info["visible"] = visible
                    field_info['isEditable'] = False
                # Format specific fields
                if field_info["fieldName"] == 'ESRIGNSS_H_RMS':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"] == 'ESRIGNSS_V_RMS':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"] == 'ESRIGNSS_LATITUDE':
                    field_info["format"]["places"] = 8
                if field_info["fieldName"] == 'ESRIGNSS_LONGITUDE':
                    field_info["format"]["places"] = 8
                if field_info["fieldName"] == 'ESRIGNSS_ALTITUDE':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"] == 'ESRIGNSS_PDOP':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"] == 'ESRIGNSS_HDOP':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"] == 'ESRIGNSS_VDOP':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"] == 'ESRIGNSS_CORRECTIONAGE':
                    field_info["format"]["places"] = 0
                if field_info["fieldName"] == 'ESRIGNSS_FIXDATETIME':
                    field_info["format"]["dateFormat"] = "shortDateShortTime"
                    field_info["format"]["timezone"] = "utc"
                if field_info["fieldName"].upper() == 'ESRIGNSS_AVG_H_RMS':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"].upper() == 'ESRIGNSS_AVG_V_RMS':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"].upper() == 'ESRIGNSS_H_STDDEV':
                    field_info["format"]["places"] = 3
    return map_data

if __name__ == "__main__":
    # Get all of the commandline arguments
    parser = argparse.ArgumentParser("Configure GNSS Popup Info")
    parser.add_argument('-st', dest="security_type",
                        help="The security of the portal/org (Portal, LDAP, NTLM, OAuth, PKI)", default="Portal")
    parser.add_argument('-u', dest='username', help="The username to authenticate with", required=True)
    parser.add_argument('-p', dest='password', help="The password to authenticate with", required=True)
    parser.add_argument('-url', dest='org_url', help="The url of the org/portal to use", required=True)
    parser.add_argument('-purl', dest='proxy_url', help="The proxy url to use", default=None)
    parser.add_argument('-pport', dest='proxy_port', help="The proxy port to use", default=None)
    parser.add_argument('-rurl', dest='referer_url', help="The referer url to use", default=None)
    parser.add_argument('-turl', dest='token_url', help="The token url to use", default=None)
    parser.add_argument('-cert', dest='certificate_file', help="The certificate to use", default=None)
    parser.add_argument('-kf', dest='keyfile', help="The key file to use", default=None)
    parser.add_argument('-cid', dest='client_id', help="The client id", default=None)
    parser.add_argument('-sid', dest='secret_id', help="The secret id", default=None)
    parser.add_argument('-ids', dest='map_ids', help="The ids of the map to configure", nargs="+", required=True)
    parser.add_argument('-v', dest='visible', action="store_true", help="Set GNSS attributes visible", default=False)
    args = parser.parse_args()
    main(args)
