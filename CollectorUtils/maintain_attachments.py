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
    # Enable Attachments
    arcpy.AddMessage("Enabling Attachments")
    arcpy.EnableAttachments_management(output_fc)
    arcpy.AddMessage("Enabled Attachments")

    # Copy Attachments from Input feature class to Temp feature class.
    arcpy.AddMessage("Copying Attachments..")

    inputRow = input_fc + '__ATTACH'
    outputTable = output_fc + '__ATTACH'

    try:
        arcpy.Append_management(inputRow, outputTable)
        arcpy.AddMessage("Copied Attachments..")
    except Exception as e:
        arcpy.Error(e)

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
