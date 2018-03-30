"""
   Copyright 2018 Esri
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

from arcgis.gis import GIS
import arcpy
from arcgis.features import FeatureLayerCollection
import argparse

# Parse Command-line arguments
def parseArguments():
    parser = argparse.ArgumentParser(
        usage='Reset required fields to None in the feature templates')

    arcpy.AddMessage("Parsing Arguments..")

    parser.add_argument('url', help='Organization url')
    parser.add_argument('username', help='Organization username')
    parser.add_argument('password', help='Organization password')
    parser.add_argument('itemId', type=str, help='Feature service Item Id')

    args_parser = parser.parse_args()
    arcpy.AddMessage("Done parsing arguments..")
    return args_parser

def update_service_definition(args_parser):
    updated_types = False
    updated_templates = False

    try:
        gis = GIS(args_parser.url,args_parser.username, args_parser.password)
        featureLayerItem = gis.content.get(args_parser.itemId)

        featureLayerCollection = FeatureLayerCollection.fromitem(featureLayerItem)
        layers = featureLayerCollection.manager.layers

        arcpy.AddMessage("Updating Service Definition..")

        for layer in layers:
            layer_index = layers.index(layer)
            fields_to_reset = [field['name'] for field in layer.properties['fields'] \
                               if not field['domain'] and \
                               not field['nullable'] and \
                               not field['defaultValue']]
            for type in layer.properties.types:
                for template in type.templates:
                    for field_name,value in template.prototype['attributes'].items():
                        if field_name not in fields_to_reset:
                            continue
                        else:
                            if not template.prototype['attributes'][field_name]:
                                template.prototype['attributes'][field_name] = None
                                updated_templates = True

            templates = layer.properties.templates
            for template in templates:
                for field_name, value in template.prototype['attributes'].items():
                    if field_name not in fields_to_reset:
                        continue
                    else:
                        if not template.prototype['attributes'][field_name]:
                            template.prototype['attributes'][field_name] = None
                            updated_templates = True

            if updated_templates or updated_types:
                if 'editingInfo' in layer.properties and 'lastEditDate' in layer.properties['editingInfo']:
                    del layer.properties.editingInfo['lastEditDate']
                featureLayerCollection.manager.layers[layer_index].update_definition(layer.properties)
                
        arcpy.AddMessage("Updated Service Definition..")

    except Exception as e:
        arcpy.AddMessage(e)
    

if __name__ == '__main__':
    args_parser = parseArguments()
    update_service_definition(args_parser)
