A set of utilities to help configure web maps and feature layers for use with Collector for ArcGIS. Browse the sections below, or jump to a specific section.

**Note: Many of the scripts, notebooks, and toolboxes can also be applied to `ArcGIS Field Maps`.** 

[Notebooks](#notebooks)

[Scripts](#scripts)

[Toolboxes](#toolboxes)

## Notebooks

Jupyter notebooks are provided to demonstrate various methods to streamline and automate configuration, administration, and deployment of data collection projects.

| Functionality 
|-----------------|
| [Exclude web maps from Collector](https://github.com/Esri/collector-tools/blob/master/notebooks/UseInCollector.ipynb) 
| [Configure search for a web map](https://github.com/Esri/collector-tools/blob/master/notebooks/LayerSearchConfig.ipynb)
| [Generate app links for Collector](https://github.com/Esri/collector-tools/blob/master/notebooks/GenerateCollectorAppLinks.ipynb)

## Scripts

Supports ArcGIS API for Python v1.4.1 (https://developers.arcgis.com/python/) 

| Functionality   | Format |                                                                        
|-----------------|------------|
| [Reset Required Fields (ArcGIS API for Python)](CollectorUtils/pro/ResetRequiredFields.md)  | [Python script](https://github.com/Esri/collector-tools/blob/master/CollectorUtils/scripts/reset_required_fields_python_api.py) |
| [Add GNSS Metadata Fields (Pro) - FeatureClass](CollectorUtils/arcmap/add_update_gnss_fields.md) | [Python Script](CollectorUtils/scripts/add_update_gnss_fields.py) |
| [Add GNSS Metadata Fields (Pro) - Hosted Feature Service (ArcGIS API for Python)](CollectorUtils/pro/add_update_gnss_fields_python_api.md)|  [Python Script](CollectorUtils/scripts/add_update_gnss_fields_python_api.py) |
| [Configure GNSS Popup (ArcGIS API for Python)](CollectorUtils/pro/configure_gnss_popup_python_api.md) | [Python Script](CollectorUtils/scripts/configure_gnss_popup_python_api.py) | 
| [Project Z](CollectorUtils/pro/project_z.md) | [Model Builder](CollectorUtils/pro/project_z.md) | 

## Toolboxes

The scripts and ModelBuilder are also available as a [GeoProcessing Toolbox](https://github.com/Esri/collector-tools/blob/master/CollectorUtils/pro/CollectorUtils_Pro.tbx) for use in ArcGIS Pro.


![capture](https://user-images.githubusercontent.com/24723464/38952752-840ea9e0-4301-11e8-94d7-5bd824f708cb.PNG)

 If you are still using ArcMap, we offer a [GeoProcessing Toolbox](https://github.com/Esri/collector-tools/blob/master/CollectorUtils/arcmap/CollectorUtils_ArcMap.tbx) and associated python scripts that works with ArcMap 10.4 or higher.

## Dependencies
 - arcpy 3.4+
 - [ArcGIS API for Python](https://developers.arcgis.com/python)

## Instructions

<details>
<summary>
Script instructions
</summary>

1. Install ArcGIS API for Python package as described [here](https://developers.arcgis.com/python/guide/install-and-set-up/).
1. Clone or download this repository.
1. Run the scripts from command line.
</details>

<details>
<summary>
Toolbox instructions
</summary>

1. Clone or download this repository.
1. If you prefer to use in ArcGIS Pro, right-click on Toolboxes, and select **Add Toolbox**. Navigate and select **CollectorUtils_Pro** toolbox. 
1. Run the tools in the toolbox (Pro requires 2.0+) or run the scripts from command line.
</details>

## Resources

 * [Collector for ArcGIS](http://www.esri.com/products/collector-for-arcgis)
 * [ArcGIS API for Python](https://developers.arcgis.com/python/)
 * [ArcGIS Arcade Expressions](https://github.com/Esri/arcade-expressions)

## Issues

Although we do our best to ensure these scripts, notebooks, and toolboxes work as expected, they are provided as is and there is no official support.

If you find a bug, please let us know by [submitting an issue](https://github.com/Esri/collector-tools/issues/new).

## Contributing

Esri welcomes contributions from anyone and everyone.
Please see our [guidelines for contributing](https://github.com/esri/contributing).

## Licensing

Copyright 2020 Esri

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
