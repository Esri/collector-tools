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

    # The geometry fields that will be updated
    geometry_field_names = ["SHAPE@X", "SHAPE@Y", "SHAPE@Z"]
    # If the FC has m, then also include that
    if arcpy.Describe(input_fc).hasM:
        has_m = "ENABLED"
        geometry_field_names.append("SHAPE@M")
    else:
        has_m = "DISABLED"

    # Get the index of the attributes that represent geometries
    x_field_index = in_field_names.index(x_field)
    y_field_index = in_field_names.index(y_field)
    z_field_index = in_field_names.index(z_field)
    # Create the temporary FC, would like to use "in_memory" but it causes exceptions sometimes
    arcpy.AddMessage("Creating new FC...")
    temp_fc = arcpy.CreateFeatureclass_management(output_path,
                                                  output_name,
                                                  geometry_type="POINT",
                                                  template=input_fc,
                                                  has_m=has_m,
                                                  has_z="ENABLED",
                                                  spatial_reference=in_spatial_ref,
                                                  config_keyword="",
                                                  spatial_grid_1="0",
                                                  spatial_grid_2="0",
                                                  spatial_grid_3="0")
    arcpy.AddMessage("Adding data to new FC...")
    # If the FC has m, then we need to make sure we carry that over
    if has_m == "ENABLED":
        # Iterate over all of the ordinal rows of data and get the attributes
        with arcpy.da.SearchCursor(input_fc, in_field_names + ["SHAPE@M"]) as sc:
            # Use an insert cursor to insert the old features into the new FC
            with arcpy.da.InsertCursor(temp_fc, geometry_field_names + in_field_names) as uc:
                for row in sc:
                    # Get the normal attributes (non-geometry)
                    params = [row[i] for i in range(0, len(in_field_names))]
                    # Create a new row to insert [X-field, Y-field, Z-Field, M-Field] + [params...]
                    if row[x_field_index] and row[y_field_index] and row[z_field_index]:
                        row_to_insert = [row[x_field_index], row[y_field_index], row[z_field_index], row[-1]] + params
                        uc.insertRow(row_to_insert)

    else:
        # Iterate over all of the ordinal rows of data and get the attributes
        with arcpy.da.SearchCursor(input_fc, in_field_names) as sc:
            # Use an insert cursor to insert the old features into the new FC
            with arcpy.da.InsertCursor(temp_fc, geometry_field_names + in_field_names) as uc:
                for row in sc:
                    # Get the normal attributes (non-geometry)
                    params = [row[i] for i in range(0, len(in_field_names))]
                    # Create a new row to insert [X-field, Y-field, Z-Field] + [params...]
                    if row[x_field_index] and row[y_field_index] and row[z_field_index]:
                        row_to_insert = [row[x_field_index], row[y_field_index], row[z_field_index]] + params
                        uc.insertRow(row_to_insert)
    arcpy.AddMessage("Created geometry and updated attributes.")
   

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
