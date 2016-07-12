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
"""
import arcpy
import argparse
import copy
import json
import sys
import urllib
import urllib2
import urlparse


def post(url, data):
    """
    A simple helper function to post data
    :param url: the url to post to
    :param data: the data (dictionary) to send in the request
    :return: the response as a dictionary
    """
    data['f'] = 'json'
    d = urllib.urlencode(data)
    response = urllib2.urlopen(url, d).read()
    return json.loads(response)


def get(url, params):
    """
    A simple helper function to get data
    :param url: the url/rest end point to hit
    :param params: the paramaters to use
    :return: the response as a dictionary
    """
    params['f'] = 'json'
    p = urllib.urlencode(params)
    response = urllib2.urlopen(url+"?"+p).read()
    return json.loads(response)


def get_token(org_url, username, password, expiration=60):
    """
    This gets the token from Portal, when Portal/Built-in authentication is present
    :param org_url: The REST url to the portal (arcgis.com/sharing/rest)
    :param username: The username to authenticate with
    :param password: The password to use
    :param expiration: How long to make the token valid for (minutes)
    :return: the token as a string
    """
    url = urlparse.urljoin(org_url, "sharing/rest/generateToken")
    data = {
        'username': username,
        'password': password,
        'referer': org_url,
        'f': 'json',
        'expiration': expiration
    }
    response = post(url, data)
    token = response["token"]
    return token


def configure_gnss_popup(map_data, visible=False):
    """
    This updates the visibility of all of the GPS
    related attributes
    :param map_data: The map data (dictionary/json) to update
    :param visible: Visible (True) or not (False)
    :return: the modified map_data dictionary
    """
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
                        'ESRIGNSS_NUMSATS',
                        'ESRIGNSS_FIXDATETIME']
    for operational_layer in map_data["operationalLayers"]:
        if "popupInfo" in operational_layer and "fieldInfos" in operational_layer["popupInfo"]:
            for field_info in operational_layer["popupInfo"]["fieldInfos"]:
                # Set all fields as visible
                if field_info["fieldName"].upper() in fields_to_update:
                    field_info["visible"] = visible
                # Format specific fields
                if field_info["fieldName"].upper() == 'ESRIGNSS_H_RMS':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"].upper() == 'ESRIGNSS_V_RMS':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"].upper() == 'ESRIGNSS_LATITUDE':
                    field_info["format"]["places"] = 8
                if field_info["fieldName"].upper() == 'ESRIGNSS_LONGITUDE':
                    field_info["format"]["places"] = 8
                if field_info["fieldName"].upper() == 'ESRIGNSS_ALTITUDE':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"].upper() == 'ESRIGNSS_PDOP':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"].upper() == 'ESRIGNSS_HDOP':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"].upper() == 'ESRIGNSS_VDOP':
                    field_info["format"]["places"] = 2
                if field_info["fieldName"].upper() == 'ESRIGNSS_FIXDATETIME':
                    field_info["format"]["dateFormat"] = "shortDateShortTime"
                    field_info["format"]["timezone"] = "utc"
    return map_data


def get_map(org_url, token, map_id):
    """
    This grabs the map item data (json) from Portal/AGO
    :param org_url: The REST URL to hit
    :param token: The authentication token to use
    :param map_id: The id of the map to use
    :return: the dictionary/json of the map_data
    """
    map_path = "{}/sharing/rest/content/items/{}/data".format(org_url, map_id)
    params = {
        "token": token,
        "f": "json",
        "referer": "http://www.esri.com/AGO/7A9FA550-0E7C-412B-9BFC-F42C25062123"
    }
    map_data = get(map_path, params)
    map_details_path = "{}/sharing/rest/content/items/{}".format(org_url, map_id)
    res = get(map_details_path,params)
    owner = res["owner"]
    folder_id = res["ownerFolder"]

    return map_data, owner, folder_id


def update_map(org_url, token, username, map_data, map_id, folder_id):
    """
    This submits the changes to Portal/AGO
    :param org_url: The REST url to hit
    :param token: The authentication token to use
    :param username: The username (needed to build url)
    :param map_data: The map dictionary/json object
    :param map_id: The map id to update
    :return:
    """
    text = json.dumps(map_data).encode('utf8', errors='replace')
    params = {
        "token": token,
        "text": text,
        "f": "json"
    }
    if folder_id and folder_id != "":
        map_path = "{}/sharing/rest/content/users/{}/{}/items/{}/update".format(org_url,username,folder_id, map_id)
    else:
        map_path = "{}/sharing/rest/content/users/{}/items/{}/update".format(org_url,username, map_id)
    arcpy.AddMessage(map_path)
    ret = post(map_path, params)
    return ret

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Configure GNSS Popup Info")
    # Can supply multiple ids to configure multiple maps
    parser.add_argument('ids', help="The id of the map to use", nargs="+")
    parser.add_argument('visible',help="Set GNSS attributes visible", choices=["true","false"])
    # Optional arguments if using at commandline, only supports built-in security
    parser.add_argument('-u',dest='username', help="The username to authenticate with")
    parser.add_argument('-p',dest= 'password', help="The password to authenticate with")
    parser.add_argument('-url',dest= 'org_url', help="The REST url of the org/portal to use")
    args = parser.parse_args()

    # Check that if one of the optional arguments is provided, they must all be
    if any([args.username, args.password, args.org_url]) and not all([args.username, args.password, args.org_url]):
        arcpy.AddError("Must specify username, password, and org_url, missing at least one parameter.")
        sys.exit(-1)

    try:
        arcpy.AddMessage("Getting Token...")
        if args.username:
            token = get_token(args.org_url,args.username, args.password)
            org_url = args.org_url
        else:
            token_info = arcpy.GetSigninToken()
            if token_info is None:
                arcpy.AddError("You are not signed into a Portal or AGOL Organization.")
                sys.exit(-1)
            else:
                token = token_info['token']
            org_url = arcpy.GetActivePortalURL()
    except Exception as e:
        arcpy.AddError("Error Getting Token. Check username, password, and url.")
        arcpy.AddError(e)
        sys.exit()

    for map_id in args.ids:
        try:
            arcpy.AddMessage("Getting Map...")
            map_data, owner, folder_id = get_map(org_url.rstrip('/'), token, map_id)
            arcpy.AddMessage("Configuring Map...")
            map_data2 = configure_gnss_popup(copy.deepcopy(map_data), args.visible.lower()=="true")
            arcpy.AddMessage("Updating Maps...")
            ret = update_map(org_url.rstrip('/'), token, owner, map_data2, map_id, folder_id)
            if "error" not in ret:
                arcpy.AddMessage("Successfully Configured Map Item Id: {}".format(map_id))
            else:
                arcpy.AddError("Error Updating Map")
                arcpy.AddError(ret)
        except Exception as e:
            arcpy.AddError("Error Configuring id: {}".format(map_id))
            arcpy.AddError(e)

