# ProjectZ
Supported in ArcGIS Pro 2.0+

This tool is used to convert attributes to geometries. The main use-case for this is when using GNSS receivers with the Collector for ArcGIS app, the GNSS metadata is stored (receiver name, lat, long, altitude, accuracy...) in the attribute table but the 3D z-values may not be projected properly when stored in the database. 

The ProjectZ tool is a custom tool built on top of the normal Project tool found in ArcGIS Pro (https://pro.arcgis.com/en/pro-app/tool-reference/data-management/project.htm), which exposes this vertical datum transformation capability.

**Note:** These vertical datum transformations require the separate installation of the ArcGIS Coordinate Systems Data for ArcGIS Pro. It contains the data files required for the GEOCON transformation methods and vertical transformation files for the United States (VERTCON and GEOID12B) and the world (EGM2008).

The idea behind the use of the ProjectZ tool to obtain high precision elevations, begins with the capturing of point features in the field to initially store values in the Altitude metadata field as Height Above Ellipsoid (HAE), and then to "post-process" those altitude values with the ProjectZ tool using the latest vertical datum transformations in ArcGIS Pro. 

### Maintaining Attachments

The output feature class from the ProjectZ tool also maintains any existing attachments that were related to the input feature class. 

**Note** For existing attachments on the input feature class, the attachment relationship class `__ATTACHREL` needs to have been generated using GLOBAL ID's and not OBJECT ID's. When viewing the properties of the `__ATTACHREL` relationship class, it should appear similar to the following where the Primary Key is `GLOBALID` and the Foreign Key is `REL_GLOBALID`:
<img src="https://user-images.githubusercontent.com/24723464/63988726-806a5900-ca92-11e9-8b90-e1e891b5f66e.png" alt="Tool2" width="500" height="400">

If using OBJECT ID's for the attachments relationship, you will see the following error message when adding your input feature class into the ProjectZ tool:

<img src="https://user-images.githubusercontent.com/24723464/63988931-4188d300-ca93-11e9-8e75-bc4a8941a268.png" alt="Tool2" width="550" height="150">

In this case, you need to run the [Migrate Relationship Class tool](https://pro.arcgis.com/en/pro-app/tool-reference/data-management/migrate-relationship-class-tool.htm) using the `__ATTACHREL` relationship class as input to convert the relationship from OBJECTID-based to GLOBALID-based.

### Run the tool within ArcGIS Pro:
Here is a demonstration of this workflow. First let’s assume you have collected point features with GNSS metadata fields using Collector (check https://doc.arcgis.com/en/collector/ipad/help/high-accuracy-prep.htm#ESRI_SECTION1_C992B4FE465A4AFAB98A4972E336E808 for additional help) and you collect using a correction service based on the NAD83 2011 coordinate system. As a result, the values for Latitude/Longitude/Altitude in the GNSS metadata are based on NAD83 2011.

<img src="https://user-images.githubusercontent.com/24723464/55260526-e2920a00-5225-11e9-814d-504f86dcd822.png" alt="Tool1" width="250" height="350">

Select your collected feature class as the “Input Features”, and “Input Coordinate System” is the correction service coordinate system. We're using a NAD83 2011 basestation, thus the “Input Coordinate System” is NAD 1983 2011 for both XY and Z. For Z value, NAD 1983 2011 is ellipsoidal-based vertical datum. 

<img src="https://user-images.githubusercontent.com/24723464/55260856-b4f99080-5226-11e9-80d9-e1d3febb00dd.png" alt="Tool2" width="250" height="350">

X-value/Y-value/Z-value are auto-populated from GNSS metadata fields.

Then you select the location of the output feature class you would like to save as “Output Features” and select its “Output Coordinate System”. If you are interested in elevation, the coordinate is not based on Ellipsoidal. It is Gravity-based vertical datum. NAVD 1988 is selected. 

<img src="https://user-images.githubusercontent.com/24723464/55260979-fb4eef80-5226-11e9-919e-d10471597676.png" alt="Tool3" width="250" height="350">

Geographic Transformation is auto-populated with geoid12b model. Here is the final configuration of ProjectZ tool. 

<img src="https://user-images.githubusercontent.com/24723464/55260987-0013a380-5227-11e9-9ed9-5a219b727edd.png" alt="Tool4" width="250" height="350">

Run the tool, the output feature class is Z enabled with vertical datum NAVD 1988. The elevation is shown as Z value. (Use the Add XY tool to add a POINT_Z field to the attribute table. **Note** the original values in the Altitude field remain untouched.)

<img src="https://user-images.githubusercontent.com/24723464/55261242-a52e7c00-5227-11e9-9d81-84d748a98b49.png" alt="Tool5" width="300" height="400">

With this ProjectZ geoprocessing tool, you can postprocess your feature class with accurate elevation as Z value. This will streamline your workflow to collect elevation with Collector. You can not only use this tool to capture elevation or Z value but also as a workaround for other datum transformation limitation existing in Collector like grid based datum transformation. 


### What it does
1. Calls the [Recreate Geometry](scripts/recreate_geometry.md) tool to create a new feature class using the specified attributes as the geometry
2. Projects the new feature class to the desired projection
3. Calls the [Maintain Attachments](scripts/maintain_attachments.py) tool to enable attachments on the output feature class and append any existing attachments into it from the input feature class. 

### Additional Notes:
 - The tool will not maintain user-defined related tables on the output feature class. In this case, those relationship classes would need to be recreated manually in the ouput geodatabase. You can follow the same relationship class properties from the original feature class. 
 - The tool preserves the same Global ID's between the input and output feature classes.

### Gotchas
1. There is no dedicated python script for this tool because the arcpy.ListTransformations() method does not work well with vertical coordinate systems
