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
import os

def get_geodatabase_path(input_layer):
    """
    Gets the parent geodatabase of the layer
    :param input_layer: (string) The feature layer to get the parent database of
    :return: (string) The path to the geodatabase
    """
    workspace = os.path.dirname(arcpy.Describe(input_layer).catalogPath)
    if [any(ext) for ext in ('.gdb', '.mdb', '.sde') if ext in os.path.splitext(workspace)]:
        return workspace
    else:
        return os.path.dirname(workspace)

def check_and_create_domains(geodatabase):
    """
    Checks if the domains already exist, if they do
    then it checks the values and ranges

    If the domains do not exist, they are created

    :param geodatabase: (string) the path to the geodatabase to check
    :return:
    """
    domains = arcpy.da.ListDomains(geodatabase)
    domain_names = [domain.name for domain in domains]
    if 'ESRI_FIX_TYPE_DOMAIN' in domain_names:
        for domain in domains:
            if domain.name == 'ESRI_FIX_TYPE_DOMAIN':
                # check if cvs 0,1,2,4,5 are in teh codedValues
                values = [cv for cv in domain.codedValues]
                if not set(set([0, 1, 2, 4, 5])).issubset(values):
                    arcpy.AddError("ESRI_FIX_TYPE_DOMAIN is missing a coded value pair.")
                    return
    else:
        # Add the domain and values
        arcpy.AddMessage('Adding ESRI_FIX_TYPE_DOMAIN domain to parent geodatabase...')
        arcpy.CreateDomain_management(in_workspace=geodatabase,
                                      domain_name="ESRI_FIX_TYPE_DOMAIN",
                                      domain_description="Fix Type",
                                      field_type="SHORT",
                                      domain_type="CODED",
                                      split_policy="DEFAULT",
                                      merge_policy="DEFAULT")

        arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                               domain_name="ESRI_FIX_TYPE_DOMAIN",
                                               code="0",
                                               code_description="Fix not valid")
        arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                               domain_name="ESRI_FIX_TYPE_DOMAIN",
                                               code="1",
                                               code_description="GPS")
        arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                               domain_name="ESRI_FIX_TYPE_DOMAIN",
                                               code="2",
                                               code_description="Differential GPS")
        arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                               domain_name="ESRI_FIX_TYPE_DOMAIN",
                                               code="4",
                                               code_description="RTK Fixed")
        arcpy.AddCodedValueToDomain_management(in_workspace=geodatabase,
                                               domain_name="ESRI_FIX_TYPE_DOMAIN",
                                               code="5",
                                               code_description="RTK Float")
    # Check if 'NumSats" is a domain, if so check the range
    if 'ESRI_NUM_SATS_DOMAIN' in domain_names:
        if domain.name == "ESRI_NUM_SATS_DOMAIN":
            if domain.range[0] != 0 or domain.range[1] != 99:
                arcpy.AddError("ESRI_NUM_SATS_DOMAIN domain has invalid range")
                return
    else:
        # Add the domain and set the range
        arcpy.AddMessage("Adding ESRI_NUM_SATS_DOMAIN to parent database...")
        arcpy.CreateDomain_management(in_workspace=geodatabase,
                                      domain_name="ESRI_NUM_SATS_DOMAIN",
                                      domain_description="Number of Satellites",
                                      field_type="SHORT",
                                      domain_type="RANGE",
                                      split_policy="DEFAULT",
                                      merge_policy="DEFAULT")
        arcpy.SetValueForRangeDomain_management(geodatabase, "ESRI_NUM_SATS_DOMAIN", 0, 99)
    # Check if 'StationID" is a domain, if so check the range
    if 'ESRI_STATION_ID_DOMAIN' in domain_names:
        if domain.name == "ESRI_STATION_ID_DOMAIN":
            if domain.range[0] != 0 or domain.range[1] != 1023:
                arcpy.AddError("ESRI_STATION_ID_DOMAIN domain has invalid range")
                return
    else:
        # Add the domain and set the range
        arcpy.AddMessage("Adding ESRI_STATION_ID_DOMAIN to parent database...")
        arcpy.CreateDomain_management(in_workspace=geodatabase,
                                      domain_name="ESRI_STATION_ID_DOMAIN",
                                      domain_description="Station ID",
                                      field_type="SHORT",
                                      domain_type="RANGE",
                                      split_policy="DEFAULT",
                                      merge_policy="DEFAULT")
        arcpy.SetValueForRangeDomain_management(geodatabase, "ESRI_STATION_ID_DOMAIN", 0, 1023)


def add_gnss_fields(feature_layer):
    """
    This adds specific fields required for GPS units to
        auto-populate in collector application

        This will report errors if:
            1) Any of the fields already exist
            2) The input layer is not a point layer
            3) The layer is not found
            4) The layer is a shapefile

    Example: add_gps_fields(r"C:/temp/test.shp")

    :param feature_layer: (string) The feature layer (shapefile, feature class, etc) to add the fields to
    :return:
    """

    try:
        if not arcpy.Exists(feature_layer):
            arcpy.AddError("Feature layer: {} not found!".format(feature_layer))
            return
        if arcpy.Describe(feature_layer).shapeType != "Point":
            arcpy.AddError("Feature layer: {} is not a point layer".format(feature_layer))
            return
        if arcpy.Describe(feature_layer).dataType == "Feature Layer":
            if arcpy.Describe(feature_layer).dataElement.dataType == "ShapeFile":
                arcpy.AddError("ShapeFiles are not supported.")
                return
        elif arcpy.Describe(feature_layer).dataType == "ShapeFile":
            arcpy.AddError("ShapeFiles are not supported.")
            return
        # List of field names that will be added (used to check if field exists)
        fields_to_add = ['ESRIGNSS_RECEIVER',
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
                         'ESRIGNSS_FIXDATETIME']
        existing_fields = arcpy.ListFields(feature_layer)
        for field in existing_fields:
            if field.name in fields_to_add:
                arcpy.AddError("'{}' field already exists!".format(field.name))
                return
        # check if it's a service or feature class in db
        # Check the domains to see if they exist and are valid
        # will update if necessary
        
        if r'/rest/services' not in arcpy.Describe(feature_layer).catalogPath:
            arcpy.AddMessage('Checking domains...')
            geodatabase = get_geodatabase_path(feature_layer)
            check_and_create_domains(geodatabase)

        # Add the fields
        arcpy.AddMessage('Adding Required Fields...')
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_RECEIVER',
                                  field_type="STRING",
                                  field_length=50,
                                  field_alias='Receiver Name',
                                  field_is_nullable="NULLABLE"
                                  )
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_H_RMS',
                                  field_type="DOUBLE",
                                  field_alias='Horizontal Accuracy (m)',
                                  field_is_nullable="NULLABLE"
                                  )
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_V_RMS',
                                  field_type="DOUBLE",
                                  field_alias='Vertical Accuracy (m)',
                                  field_is_nullable="NULLABLE"
                                  )
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_LATITUDE',
                                  field_type="DOUBLE",
                                  field_alias='Latitude',
                                  field_is_nullable="NULLABLE"
                                  )
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_LONGITUDE',
                                  field_type="DOUBLE",
                                  field_alias='Longitude',
                                  field_is_nullable="NULLABLE"
                                  )
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_ALTITUDE',
                                  field_type="DOUBLE",
                                  field_alias='Altitude',
                                  field_is_nullable="NULLABLE"
                                  )
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_PDOP',
                                  field_type="DOUBLE",
                                  field_alias='PDOP',
                                  field_is_nullable="NULLABLE"
                                  )
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_HDOP',
                                  field_type="DOUBLE",
                                  field_alias='HDOP',
                                  field_is_nullable="NULLABLE"
                                  )
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_VDOP',
                                  field_type="DOUBLE",
                                  field_alias='VDOP',
                                  field_is_nullable="NULLABLE"
                                  )
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_FIXTYPE',
                                  field_type="SHORT",
                                  field_alias='Fix Type',
                                  field_is_nullable="NULLABLE",
                                  field_domain = "ESRI_FIX_TYPE_DOMAIN"
                                  )
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_CORRECTIONAGE',
                                  field_type="DOUBLE",
                                  field_alias='Correction Age',
                                  field_is_nullable="NULLABLE"
                                  )
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_STATIONID',
                                  field_type="SHORT",
                                  field_alias='Station ID',
                                  field_is_nullable="NULLABLE",
                                  field_domain = "ESRI_STATION_ID_DOMAIN"
                                  )
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_NUMSATS',
                                  field_type="SHORT",
                                  field_alias='Number of Satellites',
                                  field_is_nullable="NULLABLE",
                                  field_domain="ESRI_NUM_SATS_DOMAIN"
                                  )
        arcpy.AddField_management(feature_layer,
                                  'ESRIGNSS_FIXDATETIME',
                                  field_type="Date",
                                  field_alias='Fix Time',
                                  field_is_nullable="NULLABLE",
                                  )
        arcpy.AddMessage("Successfully added GPS Metadata fields.\n")
    except Exception as e:
        arcpy.AddError("{}\n".format(e))
        return

if __name__ == "__main__":
    """
        Commandline use to add fields to a layer

        Input: layer names (fully qualified paths)

        Example: python add_gps_fields "C:/temp/test.gdb/test" "C:/temp/test.gdb/test2"
    """
    parser = argparse.ArgumentParser("Add GPS Fields to Feature Layers")
    parser.add_argument("layers", nargs='+', help="The layers to add fields to")
    args = parser.parse_args()
    for layer in args.layers:
        add_gnss_fields(layer)
