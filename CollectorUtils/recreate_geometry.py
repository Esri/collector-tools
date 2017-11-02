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


def main():
    # Get all of the input parameters as text
    parameters = arcpy.GetParameterInfo()
    input_fc = parameters[0].valueAsText
    output_path = arcpy.Describe(parameters[5].value).path
    output_name = arcpy.Describe(parameters[5].value).name
    in_spatial_ref = parameters[1].valueAsText
    x_field = parameters[2].valueAsText
    y_field = parameters[3].valueAsText
    z_field = parameters[4].valueAsText
    update_geom(input_fc, output_path, output_name, in_spatial_ref, x_field, y_field, z_field)


def update_geom(input_fc, output_path, output_name, in_spatial_ref, x_field, y_field, z_field):
    """
    Creates a new feature class with the specified spatial reference and populates the features using
    the geometrical attributes (Lat, Long, Z) rather than the original geometries geometry.

    :param input_fc: (string) The feature to create a new version of
    :param output_path: (string) Where to store the new feature
    :param output_name: (string) The name of the new feature
    :param in_spatial_ref: (string) The string representation of the spatial reference
    :param x_field: (string) The name of the field that contains the x values
    :param y_field: (string) The name of the field that contains the y values
    :param z_field: (string) The name of the field that contains the z values
    :return:
    """
    # Get all of the non-geometry attribute names
    in_field_names = [field.name for field in arcpy.Describe(input_fc).fields if
                      field.type not in ("OID", "Geometry")]
    field_len = len(in_field_names)

    # Check that all of the necessary fields exist
    if x_field not in in_field_names:
        arcpy.AddError("'{}' field not found.".format(x_field))
        return -1
    if y_field not in in_field_names:
        arcpy.AddError("'{}' field not found.".format(x_field))
        return -1
    if z_field not in in_field_names:
        arcpy.AddError("'{}' field not found.".format(x_field))
        return -1

    # Get the index of the attributes that represent geometries
    x_field_index = in_field_names.index(x_field)
    y_field_index = in_field_names.index(y_field)
    z_field_index = in_field_names.index(z_field)
    
    # Create the temporary FC, would like to use "in_memory" but it causes exceptions sometimes
    arcpy.AddMessage("Creating new FC...")
    arcpy.env.preserveGlobalIds = True
    temp_fc = arcpy.FeatureClassToFeatureClass_conversion(input_fc,output_path,output_name)
    arcpy.AddMessage("Copied data to new FC...")

    #Start edit session
    edit = arcpy.da.Editor(output_path)
    edit.startEditing(False, True)
    edit.startOperation()

    with arcpy.da.UpdateCursor(temp_fc, in_field_names+["SHAPE@X"]+["SHAPE@Y"]+["SHAPE@Z"]) as updateCursor:
        for row in updateCursor:
            row[field_len] = row[x_field_index]
            row[field_len + 1] = row[y_field_index]
            row[field_len + 2] = row[z_field_index]
            updateCursor.updateRow(row)

    # End edit session
    edit.stopOperation()
    edit.stopEditing(True)                            
                             
    arcpy.AddMessage("All Rows Updated..")   
   

if __name__ == "__main__":
    """
        Commandline use to recreate geometry based on attributes

        Inputs: input_fc - The full path to feature class to use
                in_spatial_ref - The spatial reference to use
                x_field - The name of the field containing the x information
                y_field - The name of the field containing the y information
                z_field - The name of the field containing the z information
                output_fc - The full path of the output feature class

        Example: python recreate_geometry.py "C:/Temp/Temp.gdb/Test" "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],VERTCS['WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PARAMETER['Vertical_Shift',0.0],PARAMETER['Direction',1.0],UNIT['Meter',1.0]]" "ESRIGNSS_LONGITUDE" "ESRIGNSS_LATITUDE" "ESRIGNSS_ALTITUDE" "C:/Temp/Output.gdb/Output3"
    """
    parser = argparse.ArgumentParser("Add GNSS Metadata fields to feature class")
    parser.add_argument("input_fc", help="The input feature class to use")
    parser.add_argument("in_spatial_ref", help="The spatial reference of the geometrical attributes")
    parser.add_argument("x_field", help="The field containing the x-values")
    parser.add_argument("y_field", help="The field containing the y-values")
    parser.add_argument("z_field", help="The field containing the z-values")
    parser.add_argument("output_fc", help="The output feature class")
    args = parser.parse_args()
    path = os.path.split(args.output_fc)[0]
    name = os.path.split(args.output_fc)[1]
    update_geom(args.input_fc, path, name, args.in_spatial_ref, args.x_field, args.y_field, args.z_field)
