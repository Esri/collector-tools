"""
   This sample shows how to configure the GNSS fields for a popup
   in a webmap using the ArcREST library
"""

import arcrest
from arcresthelper import securityhandlerhelper
import argparse


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
            print(shh.message)
        else:
            # Get portal instance
            portal_admin = arcrest.manageorg.Administration(securityHandler=shh.securityhandler)
            # Loop over all of the item ids (feature services)
            for item_id in args.item_ids:
                try:
                    # Get the feature service item url from the id
                    item_url = portal_admin.content.getItem(itemId=item_id).url
                    # Update the definition
                    errors = update_definition(item_url,shh.securityhandler)
                    if not errors:
                        print("Successfully updated required fields for item id: {}".format(item_id))
                    else:
                        print("Failed to update service layers: {}".format(",".join(errors)))
                except Exception as e:
                    print("Error updating item id: {}. Please verify the item ID is a feature service".format(item_id))
                    print(e)
    except Exception as e:
        print(e)


def update_definition(url,security_handler):
    """
    This sets the 'required fields' to in the template to be null
    rather than empty white spaces or 0. Required fields are fields that
    have the nullable property set to false
    :param url: The url of the feature service to update
    :param security_handler: The authentication information
    :return:
    """
    # Get the service based on the url
    service = arcrest.hostedservice.AdminFeatureService(url,security_handler,initialize=True)
    errors = []
    # We need to update each layers json definition
    for layer in service.layers:
        # fields where nullable == False
        fields_not_null = []
        fs_layer = arcrest.hostedservice.AdminFeatureServiceLayer(layer._url,security_handler,initialize=True)
        layer_dict = fs_layer._json_dict
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
        res = fs_layer.updateDefinition(layer_dict)
        if "success" not in res:
            errors.append(layer._url)
    return errors


if __name__ == "__main__":
    # Get all of the commandline arguments
    parser = argparse.ArgumentParser("Set Required Fields to be Null")
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
    parser.add_argument('-ids', dest='item_ids', help="The ids of the map to configure", nargs="+", required=True)
    args = parser.parse_args()
    main(args)
