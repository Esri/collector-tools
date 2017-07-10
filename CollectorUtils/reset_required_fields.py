"""
   Copyright 2017 Esri
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
    response = urllib2.urlopen(url + "?" + p).read()
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
    data = dict(username=username, password=password, referer=org_url, f='json', expiration=expiration)
    response = post(url, data)
    token = response["token"]
    return token


def update_required_fields(item_id, org_url, token):
    """
    This sets the 'required fields' to in the template to be null
    rather than empty white spaces or 0. Required fields are fields that
    have the nullable property set to false
    :param item_id: The id of the service to update
    :param org_url: The url of the ogranization
    :param token: The token of an authenticated user
    :return: List of feature service layer urls that weren't updated successfully
    """
    # set the item url
    errors = []
    url = "{}/sharing/rest/content/items/{}".format(org_url, item_id)
    params = {'token': token}
    # get the items service url
    service_url = get(url, params)["url"]
    # get all of the layer ids for the service
    layer_ids = [layer["id"] for layer in get(service_url, params)["layers"]]
    # for each layer
    for layer_id in layer_ids:
        fields_not_null = []
        layer_url = "{}/{}".format(service_url, layer_id)
        # inject 'admin' into url so we can hit the updateDefinition endpoint
        index = layer_url.index("/services/")
        admin_layer_url = layer_url[0:index] + "/admin" + layer_url[index:]
        layer_dict = get(admin_layer_url, params)
        if "fields" in layer_dict:
            for field in layer_dict["fields"]:
                if not field["nullable"]:
                    fields_not_null.append(field["name"])
            if "templates" in layer_dict:
                for template in layer_dict["templates"]:
                    if "prototype" in template and "attributes" in template["prototype"]:
                        for field_name, value in template["prototype"]["attributes"].items():
                            if field_name in fields_not_null:
                                template["prototype"]["attributes"][field_name] = None
        # Need to remove lastEditDate so that the definition is actually updated
        if "editingInfo" in layer_dict and "lastEditDate" in layer_dict["editingInfo"]:
            del layer_dict["editingInfo"]["lastEditDate"]
        update_params = dict(token=token, f="json",
                             updateDefinition=json.dumps(layer_dict).encode('utf8', errors='replace'))
        # hit the updateDefinition end point to update the definition
        res = post("{}/updateDefinition".format(admin_layer_url), update_params)
        arcpy.AddError(res)
        if "success" not in res:
            errors.append(layer_url)
    return errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Reset Required fields to null")
    parser.add_argument('item_ids', help="The id of the map to use", nargs="+")
    # optional args for commandline use
    parser.add_argument('-u',dest ='username', help="The username to authenticate with")
    parser.add_argument('-p',dest='password', help="The password to authenticate with")
    parser.add_argument('-url', dest='org_url', help="The url of the org/portal to use")
    args = parser.parse_args()

    if any([args.username, args.password, args.org_url]) and not all([args.username, args.password, args.org_url]):
        arcpy.AddError("Must specify username, password, and org_url, missing at least one parameter.")
        sys.exit(-1)

    try:
        arcpy.AddMessage("Getting Token...")
        if args.username:
            token = get_token(args.org_url, args.username, args.password)
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
        sys.exit(-1)

    arcpy.AddMessage("Updating service definitions...")
    if isinstance(args.item_ids,list):
        for item_id in args.item_ids:
            try:
                errors = update_required_fields(item_id, org_url, token)
                if not errors:
                    arcpy.AddMessage("Successfully updated required fields for item id: {}".format(item_id))
                else:
                    arcpy.AddError("Failed to update service layers: {}".format(",".join(errors)))
            except Exception as e:
                arcpy.AddError("Error updating id: {}. Please verify the id is a valid service.".format(item_id))
                arcpy.AddError(e)
    else:
        try:
            errors = update_required_fields(args.item_ids, org_url, token)
            if not errors:
                arcpy.AddMessage("Successfully updated required fields for item id: {}".format(args.item_ids))
            else:
                arcpy.Error("Failed to update service layers: {}".format(",".join(errors)))
        except Exception as e:
            arcpy.AddError("Error updating id: {}. Please verify the id is a valid service.".format(args.item_ids))
            arcpy.AddError(e)
    arcpy.AddMessage("Completed.")
