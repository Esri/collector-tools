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
    This sample enables and copies over the attachments
"""
import arcpy
import argparse
import os


def main():
    # Get all of the input parameters as text
    parameters = arcpy.GetParameterInfo()
    input_fc = parameters[0].valueAsText
    output_fc = parameters[1].valueAsText
    enable_copy_attachments(input_fc, output_fc)


def enable_copy_attachments(input_fc, output_fc):
    # Check if the input feature class has attachments table
    input_attachment_table = input_fc + '__ATTACH'
    if not arcpy.Exists(input_attachment_table):
        desc = arcpy.Describe(input_fc)
        input_attachment_table = desc.Path.split('.')[0] + '.gdb\\' + desc.Name + '__ATTACH'
                            
        if not arcpy.Exists(input_attachment_table):
            arcpy.AddError("Unable to locate the attachment table for the input feature class.")
            return

    # Enable Attachments
    arcpy.AddMessage("Enabling Attachments")
    arcpy.EnableAttachments_management(output_fc)
    arcpy.AddMessage("Enabled Attachments")

    # Copy Attachments from Input feature class to Temp feature class.
    arcpy.AddMessage("Copying Attachments..")

    outputTable = output_fc + '__ATTACH'

    try:
        # Check if the input feature class was related to the attachment tables via the ObjectID field.
        input_table_desc = arcpy.Describe(input_attachment_table)
        field_rel_objectID = [field for field in input_table_desc.fields if field.name.lower() == 'rel_objectid']

        # If the input attachment table has REL_OBJECTID field then remap GUID fields between input and output attachment table.
        if field_rel_objectID:
            field_rel_globalID = [field for field in input_table_desc.fields if field.type.lower() == 'guid']
            if field_rel_globalID:
                output_field = field_rel_globalID[0]
            else:
                arcpy.AddError("Can't copy attachments...")

            output_table_field_mappings = arcpy.FieldMappings()
            output_table_field_mappings.addTable(outputTable)

            input_table_field_mappings = arcpy.FieldMappings()
            input_table_field_mappings.addTable(input_attachment_table)

            output_table_globalID = [field for field in output_table_field_mappings.fields if field.type.lower() == 'guid'][0]
            field_index = output_table_field_mappings.findFieldMapIndex(output_table_globalID.name)
            fmap = output_table_field_mappings.fieldMappings[field_index]
            output_table_field_mappings.removeFieldMap(field_index)
            fmap.addInputField(input_attachment_table,output_field.name)
            output_table_field_mappings.addFieldMap(fmap)

            for input_field_map in input_table_field_mappings.fieldMappings:
                output_table_field_mappings.addFieldMap(input_field_map)

            arcpy.Append_management(input_attachment_table, outputTable, 'NO_TEST', output_table_field_mappings)
        else:
            arcpy.Append_management(input_attachment_table, outputTable)
        arcpy.AddMessage("Copied Attachments..")
    except Exception as e:
        arcpy.AddError(e)

if __name__ == "__main__":
    """
        Commandline use to recreate geometry based on attributes

        Inputs: input_fc - The full path to feature class to use
                output_fc - The full path of the output feature class
        
    """
    parser = argparse.ArgumentParser("Add GNSS Metadata fields to feature class")
    parser.add_argument("input_fc", help="The input feature class to use")
    parser.add_argument("output_fc", help="The output feature class")
    args = parser.parse_args()
    enable_copy_attachments(args.input_fc, args.output_fc)
