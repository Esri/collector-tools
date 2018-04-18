# CollectorUtils
A collection of scripts and tools, for both ArcMap and ArcGIS Pro, to perform collector specific tasks

----
# CollectorUtils_Pro


Seven tools and corresponding scripts have been created to assist users with common Collector related tasks:

 - [Add GNSS Metadata Fields (Pro) - FeatureClass](add_update_gnss_fields.py) ([documentation](add_update_gnss_fields.md))
 - [Add GNSS Metadata Fields (Pro) - Hosted Feature Service](add_update_gnss_fields_python_api.py) ([documentation](add_update_gnss_fields_python_api.md))
 - [Configure GNSS Popup (ArcGIS API for Python)](configure_gnss_popup_python_api.py) ([documentation](configure_gnss_popup_python_api.md))
 - [Recreate Geometry](recreate_geometry.py) ([documentation](recreate_geometry.md))
 - ProjectZ (Model Builder) ([documentation](project_z.md))
 - [Maintain Attachments](maintain_attachments.py)
 - [Reset Required Fields (Python api)](reset_required_fields_python_api.py)
 
The tools have been combined into a single toolbox in ArcGIS Pro:

![capture](https://user-images.githubusercontent.com/24723464/38952752-840ea9e0-4301-11e8-94d7-5bd824f708cb.PNG)

----
# CollectorUtils_ArcMap


One tool and corresponding script have been created to assist users with common Collector related tasks:

 - [Add GNSS Metadata Fields](add_update_gnss_fields.py) ([documentation](add_update_gnss_fields.md))

![capture](https://user-images.githubusercontent.com/24723464/38953012-451570b0-4302-11e8-8069-3b2ba26b67f0.PNG)

----
## Dependencies
 - arcpy 10.4+ (Python 2.7.x) can use (3.4+ with arcpy in ArcGIS Pro for some of the tools, not all supported)
 - [ArcGIS API for Python](ArcGIS Pro)

## Instructions

1. Clone this repo or download as zip and extract
2. In ArcGIS Pro (or ArcMap) connect to the folder containing the scripts. You should see the toolboxes; CollectorUtils_ArcMap, CollectorUtils_Pro. (Note: Ensure the correct toolbox is used for either ArcMap or Pro, as many of the scripts supported in Pro aren't supported to run in ArcMap.)
3. Run the tools in the toolbox (ArcMap requires ArcGIS 10.4+, Pro requires 2.0+) or run the scripts from commandline

(For ArcMap) If you wish to use the toolbox in a version lower than 10.4, you can rebuild the toolbox in ArcGIS Desktop 10.x by creating a new toolbox, adding a script tool to it, and specifying the required parameters. Details can be seen in the documentation for each tool. Details on building script tools can be found [here.](http://desktop.arcgis.com/en/arcmap/latest/analyze/creating-tools/a-quick-tour-of-creating-tools-in-python.htm)

## Resources

 * [Collector for ArcGIS](http://www.esri.com/products/collector-for-arcgis)
 * [Arcpy](http://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy/what-is-arcpy-.htm)
 * [ArcGIS API for Python](https://developers.arcgis.com/python/)
 

## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an issue.

## Contributing

Esri welcomes contributions from anyone and everyone.
Please see our [guidelines for contributing](https://github.com/esri/contributing).

## Licensing

Copyright 2017 Esri

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
