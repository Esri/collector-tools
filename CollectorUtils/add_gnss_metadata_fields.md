# Add GNSS Metadata Fields
A Python script and corresponding toolbox to automatically add GNSS attributes to feature classes and domains to geodatabases.

Supported in at least ArcGIS 10.3.x+ and ArcGIS Pro 1.2+

This script/tool attempts to add the following fields to a Point Feature Class:

| Attribute            | Field Alias             | Field Name           | Field Type  | Domain               | Notes                                                                                    |
|----------------------|-------------------------|----------------------|-------------|----------------------|------------------------------------------------------------------------------------------|
| Receiver Name        | Receiver Name           | ESRIGNSS_RECEIVER    | string (50) |                      |                                                                                          |
| Horizontal Accuracy  | Horizontal Accuracy (m) | ESRIGNSS_H_RMS       | double      |                      |                                                                                          |
| Vertical Accuracy    | Vertical Accuracy (m)   | ESRIGNSS_V_RMS       | double      |                      |                                                                                          |
| Latitude             | Latitude                | ESRIGNSS_LATITUDE    | double      |                      |                                                                                          |
| Longitude            | Longitude               | ESRIGNSS_LONGITUDE   | double      |                      |                                                                                          |
| Altitude             | Altitude                | ESRIGNSS_ALTITUDE    | double      |                      |                                                                                          |
| PDOP                 | PDOP                    | ESRIGNSS_PDOP        | double      |                      |                                                                                          |
| HDOP                 | HDOP                    | ESRIGNSS_HDOP        | double      |                      |                                                                                          |
| VDOP                 | VDOP                    | ESRIGNSS_VDOP        | double      |                      |                                                                                          |
| Fix Type             | Fix Type                | ESRIGNSS_FIXTYPE     | short       | ESRI_FIX_TYPE_DOMAIN |  0 - Fix not valid; 1 - GPS; 2 - Differential GPS; 4 - RTK Fixed; 5 - RTK Float |
| Number of Satellites | Number of Satellites    | ESRIGNSS_NUMSATS     | short       | ESRI_NUM_SATS_DOMAIN | Range 0-99                                                                               |
| Fix Time             | Fix Time                | ESRIGNSS_FIXDATETIME | date        |                      | UTC                                                                                      |

###Using as a Python Toolbox within ArcMap or ArcGIS Pro:

1. Connect to the folder containing the "CollectorUtils" toolbox
2. Double click on the "CollectorUtils" toolbox that should be shown in the catalog/project area
3. Double click the "Add GNSS Metadata Fields" script tool (in the "OfflineUtils" toolset)
4. Select a Feature class (can also use feature service in ArcGIS Pro)
5. Click Run

![Alt text](images/AddGNSSMetaData_interface.JPG "Interface")

### Re-building the toolbox (for versions lower than 10.4)
1. Create a new toolbox (if you don't already have one)
2. Add the add_gnss_fields.py as a script
3. Set the parameters as follows:

    | Display Name        | Data Type     | Type     | Direction | Filter                |
    |---------------------|---------------|----------|-----------|-----------------------|
    | Input Feature Class | Feature Class | Required | Input     | Feature Class (Point) |

4. Update the validation logic to check that the fields don't exist (shown below)

```python
    import arcpy
    class ToolValidator(object):
      """Class for validating a tool's parameter values and controlling
      the behavior of the tool's dialog."""
    
      def __init__(self):
        """Setup arcpy and the list of tool parameters."""
        self.params = arcpy.GetParameterInfo()
    
      def initializeParameters(self):
        """Refine the properties of a tool's parameters.  This method is
        called when the tool is opened."""
        return
    
      def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return
    
      def updateMessages(self):
        if self.params[0].value is not None:
          fields_to_add = ['ESRIGNSS_RECEIVER',
                               'ESRIGNSS_H_RMS',
                               'ESRIGNSS_V_RMS',
                               'ESRIGNSS_LATITUDE',
                               'ESRIGNSS_LONGITUDE',
                               'ESRIGNSS_ALTITUDE',
                               'ESRIGNSS_PDOP',
                               'ESRIGNSS_HDOP',
                               'ESRIGNSS_VDOP',
                               'ESRIGNSS_FIXTYPE',
                               'ESRIGNSS_NUMSATS',
                               'ESRIGNSS_FIXDATETIME']
          existing_fields = arcpy.ListFields(self.params[0].valueAsText)
          fields = []
          for field in existing_fields:
              if field.name in fields_to_add:
                  fields.append(field.name)
          if fields != []:
            self.params[0].setErrorMessage("{} fields already exists!".format(",".join(["'{}'".format(field) for field in fields])))
          else:
            self.params[0].clearMessage()
        return
```


###Using as a standalone script
Run the [add_gnss_fields.py](add_gnss_fields.py) script in either Python 2.7+ or Python 3.4+ as:
```
python add_gnss_fields.py <FQP to first feature class> <FQP to second feature class> ... <FQP to Nth feature class>
```
The script can add the fields to as many feature classes as you specify (requires fully qualified path (FQP)). The standalone script will attempt to process all provided feature classes (if one fails, the others after it will still be processed)

Example:
```python
python add_gnss_fields.py "C:/temp/test.gdb/points1" "C:/temp/test.gdb/points2"
```

###What is does
1. If any of the fields already exist, the tool will stop and display an error message
2. If any of the domains don't exist in the parent geodatabase, they will be created
3. If any of the domains exist but the values or ranges are incorrect, the tool will stop and display an error message
4. All of the above fields will be added

###Gotchas
1. Shapefiles are not supported as they do not have domains and only allow field names of 10 characters or fewer
2. The input feature class must contain points (not polygons or polyline)
3. If running the standalone script, you must make sure you don't have the feature class open in ArcGIS as this will cause a schema lock


