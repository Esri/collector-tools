A set of Python scripts using the [ArcGIS API for Python v1.4.1+](https://developers.arcgis.com/python/) and ArcGIS Pro to perform collector specific tasks

## Features

| Script   | Functionality     |                                                                        
|-----------------|------------|
| [Reset Required Fields (Python api)](CollectorUtils/scripts/reset_required_fields_python_api.py) | [Documentation](CollectorUtils/pro/ResetRequiredFields.md) |
| [Add GNSS Metadata Fields (Pro) - FeatureClass](https://github.com/Esri/collector-tools/blob/NB/UpdateScriptLocation/CollectorUtils/scripts/add_update_gnss_fields.py) | [Documentation](https://github.com/Esri/collector-tools/blob/NB/UpdateScriptLocation/CollectorUtils/arcmap/add_update_gnss_fields.md) |
| [Add GNSS Metadata Fields (Pro) - Hosted Feature Service](https://github.com/Esri/collector-tools/blob/NB/UpdateScriptLocation/CollectorUtils/scripts/add_update_gnss_fields_python_api.py) | [Documentation](https://github.com/Esri/collector-tools/blob/NB/UpdateScriptLocation/CollectorUtils/pro/add_update_gnss_fields_python_api.md) |
| [Configure GNSS Popup (ArcGIS API for Python)](https://github.com/Esri/collector-tools/blob/NB/UpdateScriptLocation/CollectorUtils/scripts/configure_gnss_popup_python_api.py) | [Documentation](https://github.com/Esri/collector-tools/blob/NB/UpdateScriptLocation/CollectorUtils/pro/configure_gnss_popup_python_api.md) |
| [ProjectZ (Model Builder)] includes [Recreate Geometry](https://github.com/Esri/collector-tools/blob/NB/UpdateScriptLocation/CollectorUtils/scripts/recreate_geometry.py) and [Maintain Attachments](https://github.com/Esri/collector-tools/blob/NB/UpdateScriptLocation/CollectorUtils/scripts/maintain_attachments.py) | [Documentation](https://github.com/Esri/collector-tools/blob/NB/UpdateScriptLocation/CollectorUtils/pro/project_z.md) | 
 
The tools have been combined into a single toolbox in ArcGIS Pro:

![capture](https://user-images.githubusercontent.com/24723464/38952752-840ea9e0-4301-11e8-94d7-5bd824f708cb.PNG)

## Dependencies
 - arcpy 3.4+
 - [ArcGIS API for Python](https://developers.arcgis.com/python)

## Instructions

1. Clone or download this repository
2. If you are interested in running the scripts outside of ArcGIS Pro, install ArcGIS API for Python package as described [here](https://developers.arcgis.com/python/guide/install-and-set-up/).
3. If you prefer to use in ArcGIS Pro, right-click on Toolboxes, and select **Add Toolbox**. Navigate and select **CollectorUtils_Pro** toolbox. 
4. Run the tools in the toolbox (Pro requires 2.0+) or run the scripts from command line

## Resources

 * [Collector for ArcGIS](http://www.esri.com/products/collector-for-arcgis)
 * [ArcGIS API for Python](https://developers.arcgis.com/python/)

 ## For ArcMap

 If you are still using ArcMap, we offer a toolbox and associated python scripts that works with ArcMap 10.4 or higher [here](arcmap/collectorutils_arcmap.md).

## Issues

Find a bug or want to request a new feature?  Please let us know by submitting an issue.

## Contributing

Esri welcomes contributions from anyone and everyone.
Please see our [guidelines for contributing](https://github.com/esri/contributing).

## Licensing

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

A copy of the license is available in the repository's
[LICENSE](LICENSE) file.
