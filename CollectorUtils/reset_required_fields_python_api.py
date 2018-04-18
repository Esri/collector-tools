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
   limitations under the License.
   This sample uses the ArcGIS api for Python to update the service definition of a
   feature service by resetting the required fields to None (null) in-place of 0 and whitespaces.​    
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
    if '*' in args_parser.password:
        args_parser.password = password = arcpy.GetParameterAsText(2)
    
    arcpy.AddMessage("Done parsing arguments..")
    return args_parser

def update_template(featureLayerCollection, layer_table,index,is_table):

    fields_to_reset = {field['name']: field['type'] for field in layer_table.properties['fields'] \
                       if not field['domain'] and \
                       not field['nullable']}
    for type in layer_table.properties.types:
        for template in type.templates:
            for field_name, value in template.prototype['attributes'].items():
                if field_name not in fields_to_reset.keys():
                    continue
                else:
                    if fields_to_reset[field_name] == 'esriFieldTypeDate' and \
                       template.prototype['attributes'][field_name] and \
                       template.prototype['attributes'][field_name] < 0:
                        template.prototype['attributes'][field_name] = None
                        updated_types = True
                        continue
                    if isinstance(template.prototype['attributes'][field_name], str) and \
                            template.prototype['attributes'][field_name].isspace() or \
                            not template.prototype['attributes'][field_name]:
                        template.prototype['attributes'][field_name] = None
                        updated_types = True
                        continue

    templates = layer_table.properties.templates
    for template in templates:
        for field_name, value in template.prototype['attributes'].items():
            if field_name not in fields_to_reset.keys():
                continue
            else:
                if fields_to_reset[field_name] == 'esriFieldTypeDate' and \
                        template.prototype['attributes'][field_name] and \
                                template.prototype['attributes'][field_name] < 0:
                    template.prototype['attributes'][field_name] = None
                    updated_templates = True
                    continue

                if isinstance(template.prototype['attributes'][field_name], str) and \
                        template.prototype['attributes'][field_name].isspace() or \
                        not template.prototype['attributes'][field_name]:
                    template.prototype['attributes'][field_name] = None
                    updated_templates = True
                    continue

    if updated_templates or updated_types:
        if 'editingInfo' in layer_table.properties and 'lastEditDate' in layer_table.properties['editingInfo']:
            del layer_table.properties.editingInfo['lastEditDate']
        if "currentVersion" in layer_table.properties:
            if updated_templates:
                updated_templates_dict = {"templates":layer_table.properties['templates']}
                if is_table:
                    featureLayerCollection.manager.tables[index].update_definition(updated_templates_dict)
                else:
                    featureLayerCollection.manager.layers[index].update_definition(updated_templates_dict)
            if updated_types:
                updated_types_dict = {"types":layer_table.properties['types']}
                if is_table:
                    featureLayerCollection.manager.tables[index].update_definition(updated_types_dict)
                else:
                    featureLayerCollection.manager.layers[index].update_definition(updated_types_dict)
        else:
            if is_table:
                featureLayerCollection.manager.tables[index].update_definition(layer_table.properties)
            else:
                featureLayerCollection.manager.layers[index].update_definition(layer_table.properties)
            

def update_service_definition(args_parser):
    try:
        gis = GIS(args_parser.url,args_parser.username, args_parser.password)
        featureLayerItem = gis.content.get(args_parser.itemId)

        featureLayerCollection = FeatureLayerCollection.fromitem(featureLayerItem)
        layers = featureLayerCollection.manager.layers
        tables = featureLayerCollection.manager.tables

        arcpy.AddMessage("Updating Service Definition..")        

        for layer in layers:
            layer_index = layers.index(layer)
            update_template(featureLayerCollection,layer,layer_index,False)

        for table in tables:
            table_index = tables.index(table)
            update_template(featureLayerCollection,table,table_index,True)

                
        arcpy.AddMessage("Updated Service Definition..")

    except Exception as e:
        arcpy.Fail(e)
    

if __name__ == '__main__':
    updated_types = False
    updated_templates = False
    args_parser = parseArguments()
    update_service_definition(args_parser)
