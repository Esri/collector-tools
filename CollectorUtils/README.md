# CollectorUtils
A collection of scripts and tools to perform collector specific tasks

----

Four tools and corresponding scripts have been created to assist users with common Collector related tasks:

 - [Add GNSS Metadata Fields](add_gnss_fields.py) ([documentation](add_gnss_metadata_fields.md))
 - [Recreate Geometry](recreate_geometry.py) ([documentation](recreate_geometry.md))
 - ProjectZ (Model Builder) ([documentation](project_z.md))
 - [Configure GNSS Popup](configure_gnss_popup.py) ([documentation](configure_gnss_popup.md))
 
The tools have been combined into a single toolbox (10.4 version) as shown below:

![Alt text](images/toolbox_view.JPG "CollectorUtils Toolbox")

----

Some additional tools are available as standalone scripts:
- [Reset Required Fields (Pure Python)](reset_required_fields.py), [Reset Required Fields (ArcREST)](reset_required_fields_arcrest.py) ([documentation](ResetRequiredFields.md))
- [Update GNSS Metadata (ArcGIS API for Python)](UpdateGNSSSMetadata.py) ([documentation](UpdateGNSSMetadata.md))

## Dependencies
 - arcpy 10.4+ (Python 2.7.x) can use (3.4+ with arcpy in ArcGIS Pro for some of the tools, not all supported)
 - [ArcREST 3.5.3+](https://github.com/Esri/ArcREST) (for alternative ArcRest scripts, not required for the toolbox)
 - [ArcGIS API for Python](https://developers.arcgis.com/python/) (for Update GNSS Metadata script, not required for the toolbox)

## Instructions

1. Install [ArcREST](https://github.com/Esri/ArcREST) from source if you plan to use the scripts that rely on ArcREST (optional)
2. Clone this repo or download as zip and extract
3. In ArcMap connect to the folder containing the scripts. You should see a toolbox
4. Run the tools in the toolbox (requires ArcGIS 10.4+) or run the scripts from commandline

If you wish to use the toolbox in a version lower than 10.4, you can rebuild the toolbox in ArcGIS Desktop 10.x by creating a new toolbox, adding a script tool to it, and specifying the required parameters. Details can be seen in the documentation for each tool. Details on building script tools can be found [here.](http://desktop.arcgis.com/en/arcmap/latest/analyze/creating-tools/a-quick-tour-of-creating-tools-in-python.htm)

## Resources

 * [Collector for ArcGIS](http://www.esri.com/products/collector-for-arcgis)
 * [Arcpy](http://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy/what-is-arcpy-.htm)
 * [ArcGIS REST API](http://resources.arcgis.com/en/help/arcgis-rest-api/)

## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an issue.

## Contributing

Esri welcomes contributions from anyone and everyone.
Please see our [guidelines for contributing](https://github.com/esri/contributing).

## Licensing

Copyright 2016 Esri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the license is available in the repository's
[LICENSE](LICENSE) file.
