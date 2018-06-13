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
"""
import arcpy
import argparse
import sys
import json
import urllib.request
import urllib.parse
import arcgis
from arcgis.gis import GIS

# Retrieve feature service item data.
def get_data(itemId, params):
    featureServiceItem_Url = "{}/sharing/rest/content/items/{}/data".format(args_parser.url, itemId)
    updateResponse = urllib.request.urlopen(featureServiceItem_Url,bytes(urllib.parse.urlencode(params),'utf-8')).read()
    return json.loads(updateResponse.decode("utf-8"))

# Retrieve feature service item owner and folder Id
def get_details(itemId, params):
    featureServiceItem_Url = "{}/sharing/rest/content/items/{}".format(args_parser.url, itemId)
    updateResponse = urllib.request.urlopen(featureServiceItem_Url,bytes(urllib.parse.urlencode(params),'utf-8')).read()
    return json.loads(updateResponse.decode("utf-8"))

# Update feature service item (Popup info)
def update_feature_service(itemId,owner,folder_id,gis,feaureService_data):
    params = {
        "token": gis._con.token,
        "text": json.dumps(feaureService_data).encode('utf8', errors='replace'),
        "f": "json"
        }

    if folder_id and folder_id != "":
        featureServiceItem_Url = "{}/sharing/rest/content/users/{}/{}/items/{}/update".format(args_parser.url,owner,folder_id, itemId)
    else:
        featureServiceItem_Url = "{}/sharing/rest/content/users/{}/items/{}/update".format(args_parser.url,owner, itemId)
    
    updateResponse = urllib.request.urlopen(featureServiceItem_Url,bytes(urllib.parse.urlencode(params),'utf-8')).read()
    result = json.loads(updateResponse.decode("utf-8"))
    if 'error' in result.keys():
        ex = result['error']['message']
        arcpy.AddMessage("Error..{}".format(ex))
    else:
        arcpy.AddMessage("Successfully configured popup and visibility on the Feature service Item..")
    

# Parse Command-line arguments
def parseArguments():
    parser = argparse.ArgumentParser(
        usage='Configure GNSS metadate fields visibility and popup')

    arcpy.AddMessage("Parsing Arguments..")

    parser.add_argument('url', help='Organization url')
    parser.add_argument('username', help='Organization username')
    parser.add_argument('password', help='Organization password')
    parser.add_argument('webmap_Name', type=str, help='Webmap Name')
    parser.add_argument('layerIndex', type=int, help='Feature Layer index. If not specified use 0 as index')

    args_parser = parser.parse_args()
    if '*' in args_parser.password:
        args_parser.password = password = arcpy.GetParameterAsText(2)
    arcpy.AddMessage("Done parsing arguments..")
    return args_parser


# Search for a Webmap and update GNSS Metadata fields popup info
def searchItems_UpdateGNSSMetadataFieldsPopup(args_parser):
    # Search ItemIds
    gis = GIS(args_parser.url, args_parser.username, args_parser.password)
    arcpy.AddMessage("Signed into organization..")
    
    itemId = args_parser.webmap_Name
   
    try:
        arcpy.AddMessage("Started configuring popup and visibility..")
        
        # Iterate through each ItemId and update the popup info for the specified feature layer
        webmapItem = gis.content.search(itemId, item_type="Web Map")  # create a Webmap object from the search result
        webmap = arcgis.mapping.WebMap(webmapItem[0])

        if 'popupInfo' in webmap['operationalLayers'][args_parser.layerIndex].keys():
            arcpy.arcpy.AddMessage("Service from ArcMap..")
            # Configure popup and set visibility on the GNSSMetadata fields.
            fieldInfos = webmap['operationalLayers'][args_parser.layerIndex]['popupInfo']['fieldInfos'] if args_parser.layerIndex else \
                         webmap['operationalLayers'][0]['popupInfo']['fieldInfos']
        else:
            arcpy.arcpy.AddMessage("Service from Pro..")
            featureServiceItemId = webmap['operationalLayers'][args_parser.layerIndex]['itemId'] if args_parser.layerIndex else \
                                   webmap['operationalLayers'][0]['itemId']
            featureServiceItem = gis.content.search(featureServiceItemId, item_type="Feature Service")
            params = {
                "token": gis._con.token,
                "f": "json"
                }
        
            feature_service_data = get_data(featureServiceItemId,params)
            feature_service_details = get_details(featureServiceItemId,params)

            owner = feature_service_details['owner']
            folder_Id = feature_service_details['ownerFolder']
            
            fieldInfos = feature_service_data['layers'][args_parser.layerIndex]['popupInfo']['fieldInfos'] if args_parser.layerIndex else \
                         feature_service_data['layers'][0]['popupInfo']['fieldInfos']            
            

        for field_info in fieldInfos:
            # Configure popup and visibility for GNSSMetadata fields
            if field_info['fieldName'].upper() == 'ESRIGNSS_H_RMS':
                if 'format' in field_info.keys():
                    field_info['format']['places'] = 2
                else:
                    field_info['format'] = {'places' : 2}                    
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_V_RMS':
                if 'format' in field_info.keys():
                    field_info['format']['places'] = 2
                else:
                    field_info['format'] = {'places' : 2}                
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_LATITUDE':
                if 'format' in field_info.keys():
                    field_info['format']['places'] = 8
                else:
                    field_info['format'] = {'places' : 8}                
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_LONGITUDE':
                if 'format' in field_info.keys():
                    field_info['format']['places'] = 8
                else:
                    field_info['format'] = {'places' : 8}                 
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_ALTITUDE':
                if 'format' in field_info.keys():
                    field_info['format']['places'] = 2
                else:
                    field_info['format'] = {'places' : 2}                 
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_PDOP':
                if 'format' in field_info.keys():
                    field_info['format']['places'] = 2
                else:
                    field_info['format'] = {'places' : 2} 
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_HDOP':
                if 'format' in field_info.keys():
                    field_info['format']['places'] = 2
                else:
                    field_info['format'] = {'places' : 2} 
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_VDOP':
                if 'format' in field_info.keys():
                    field_info['format']['places'] = 2
                else:
                    field_info['format'] = {'places' : 2} 
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_CORRECTIONAGE':
                if 'format' in field_info.keys():
                    field_info['format']['places'] = 0
                else:
                    field_info['format'] = {'places' : 0} 
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_FIXDATETIME':
                if 'format' in field_info.keys():
                    field_info['format']['dateFormat'] = 'shortDateShortTime'
                else:
                    field_info['format'] = {'dateFormat' : 'shortDateShortTime'}                    
                field_info['format']['timezone'] = 'utc'
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_AVG_H_RMS':
                if 'format' in field_info.keys():
                    field_info['format']['places'] = 2
                else:
                    field_info['format'] = {'places' : 2} 
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_AVG_V_RMS':
                if 'format' in field_info.keys():
                    field_info['format']['places'] = 2
                else:
                    field_info['format'] = {'places' : 2} 
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_H_STDDEV':
                if 'format' in field_info.keys():
                    field_info['format']['places'] = 3
                else:
                    field_info['format'] = {'places' : 3} 
                field_info['visible'] = True
                field_info['isEditable'] = False

            if field_info['fieldName'].upper() == 'ESRIGNSS_RECEIVER' or field_info[
                'fieldName'].upper() == 'ESRIGNSS_STATIONID' or \
                            field_info['fieldName'].upper() == 'ESRIGNSS_FIXTYPE' or field_info[
                'fieldName'].upper() == 'ESRIGNSS_NUMSATS' or \
                            field_info['fieldName'].upper() == 'ESRIGNSS_AVG_POSITIONS':
                field_info['visible'] = True
                field_info['isEditable'] = False

        # Set Webmap fieldInfos property
        if args_parser.layerIndex:
            if 'popupInfo' in webmap['operationalLayers'][args_parser.layerIndex].keys():
                webmap['operationalLayers'][args_parser.layerIndex]['popupInfo']['fieldInfos'] = fieldInfos
            else:
                webmap['operationalLayers'][args_parser.layerIndex]['popupInfo'] = {'fieldInfos' : fieldInfos}
                #feature_service_data['layers'][args_parser.layerIndex]['popupInfo']['fieldInfos'] = fieldInfos
                #update_feature_service(featureServiceItemId, owner, folder_Id, gis,feature_service_data)                
                
        else:
            if 'popupInfo' in webmap['operationalLayers'][0].keys():
                webmap['operationalLayers'][0]['popupInfo']['fieldInfos'] = fieldInfos
            else:
                webmap['operationalLayers'][0]['popupInfo'] = {'fieldInfos' : fieldInfos}
                #feature_service_data['layers'][0]['popupInfo']['fieldInfos'] = fieldInfos
                #update_feature_service(featureServiceItemId, owner, folder_Id,gis, feature_service_data)

        # Update Webmap
        webmap.update()
        arcpy.AddMessage("Successfully configured popup and visibility on the Webmap..")
    
    
    except Exception as e:
        arcpy.AddError(e)       


if __name__ == '__main__':
    args_parser = parseArguments()
    searchItems_UpdateGNSSMetadataFieldsPopup(args_parser)
