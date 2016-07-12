# ProjectZ
Assigns geometrical attributes to the geometry of a point (X, Y, Z), and creates a new feature class. Used when using GNSS GPS receivers with Collector to re-populate the Z-values in the correct coordinate system.

Supported in ArcGIS 10.4+

This tool is used convert attributes to geometries. The main use case for this is when using GNSS GPS receivers with the collector app, the meta data is stored (receiver name, lat, long, altitude, accuracy...) in the attribute table but the 3D z-values may not be projected properly when stored in the database. 

Suppose you have feature that has the following attributes where the geometry (X and Y) of the features has been projected to NAD83, but the Lat, Long, and Z attributes are still in WGS84. 

| ObjectID | Shape   | Lat       | Long        | Z         |
|----------|---------|-----------|-------------|-----------|
| 1        | Point | 34.057866 | -117.196879 | 369.05957 |

This tool will create a new feature class that uses the Lat, Long, and Z attributes to create the geometry (using the orginal projection: WGS84). It carries over any other attributes as well.

### Using as a Script Tool within ArcMap 10.4+:

1. Connect to the folder containing the "CollectorUtils" toolbox
2. Double click on the "CollectorUtils" toolbox that should be shown in the catalog/project area
3. Double click the "ProjectZ" model tool (in the "OfflineUtils" toolset)
4. Choose your inputs
    1. Input Features - This is the point feature class that you would like to update the geometry of and project
    2. Input Coordinate System - This is the Coordinate System of the X (long), Y (long), and Z (altitude) values. NOT necessarily the CS of the feature class
    3. X-Value Coordinates - The field that stores the X values or Longitude information (attempts to auto-populate)
    4. Y-Value Coordinates - The field that stores the Y values or Latitude information (attempts to auto-populate)
    5. Z-Value Coordinates - The field that stores the Z values or Elevation/Altitude information (attempts to auto-populate)
    6. Output Features - The location of the output feature class
    7. Output Coordinate System - The coordinate system the output feature class should be use
    8. Geographic Transformation - The transform to use when converting coordinates systems (updates when input feature class, input coordinate system, and output coordinate system are selected)
5. Click Run

![Alt text](images/ProjectZ_interface.JPG "Interface")

### What it does
1. Calls the [Recreate Geometry](recreate_geometry.md) tool to create a new feature class using the specified attributes as the geometry
2. Projects the new feature class to the desired projection

### Gotchas
1. There is no dedicated python script for this tool because the arcpy.ListTransformations() method does not work well with vertical coordinate systems
