# Add GNSS Metadata Fields
A Python script and corresponding toolbox to automatically add and update GNSS attributes to feature classes and domains to geodatabases.

Supported in at least ArcMap 10.4+ and ArcGIS Pro 2.0+

This script/tool attempts to add the following fields to a Point Feature Class:

| Attribute            | Field Alias             | Field Name           | Field Type  | Domain               | Notes                                                                                    |
|----------------------|-------------------------|----------------------|-------------|----------------------|------------------------------------------------------------------------------------------|
| Position source type        | Position source type           | ESRIGNSS_POSITIONSOURCETYPE    | Short |        ESRI_POSITIONSOURCETYPE_DOMAIN               |    0 - Unknown <br/>1 - User defined <br/>2 - Integrated (System) Location Provider <br/>3 - External GNSS Receiver <br/>4 - Network Location Provider                                                                                      |
| Receiver name        | Receiver Name           | ESRIGNSS_RECEIVER    | String(50) |                      |                                                                                          |
| Latitude             | Latitude                | ESRIGNSS_LATITUDE    | double      |                      |                                                                                          |
| Longitude            | Longitude               | ESRIGNSS_LONGITUDE   | double      |                      |                                                                                          |
| Altitude             | Altitude                | ESRIGNSS_ALTITUDE    | double      |                      |                                                                                          |
| Horizontal accuracy  | Horizontal Accuracy (m) | ESRIGNSS_H_RMS       | double      |                      |                                                                                          |
| Vertical accuracy    | Vertical Accuracy (m)   | ESRIGNSS_V_RMS       | double      |                      |                                                                                          |
| Fix time             | Fix Time                | ESRIGNSS_FIXDATETIME | Date        |                      | UTC                                                                                      |
| Fix type             | Fix Type                | ESRIGNSS_FIXTYPE     | Short       | ESRI_FIX_TYPE_DOMAIN |  0 - Fix not valid <br/>1 - GPS <br/>2 - Differential GPS <br/>4 - RTK Fixed <br/>5 - RTK Float |
| Correction age       | Correction Age          | ESRIGNSS_CORRECTIONAGE| double      |                      |                                                                                          |
| Station ID           | Station ID              | ESRIGNSS_STATIONID   | Short      | ESRI_STATION_ID_DOMAIN| Range 0-1023                                                                                      |                                             
| Number of satellites | Number of Satellites    | ESRIGNSS_NUMSATS     | Short       | ESRI_NUM_SATS_DOMAIN | Range 0-99                                                                               |
| PDOP                 | PDOP                    | ESRIGNSS_PDOP        | double      |                      |                                                                                          |
| HDOP                 | HDOP                    | ESRIGNSS_HDOP        | double      |                      |                                                                                          |
| VDOP                 | VDOP                    | ESRIGNSS_VDOP        | double      |                      |                                                                                          |
| Direction of travel        | Direction of travel (°)           | ESRIGNSS_DIRECTION    | double |                      |                                                                                          |
| Speed        | Speed (km/h)           | ESRIGNSS_SPEED    | double |                      |                      |                                                                                          |
| Compass reading        | Compass reading (°)           | ESRISNSR_AZIMUTH    | double |                      |                                                                                          |
| Average horizontal accuracy             | Average Horizontal Accuracy (m)                | ESRIGNSS_AVG_H_RMS | double       |                                                                                                          |
| Average vertical accuracy             | Average Vertical Accuracy (m)              | ESRIGNSS_AVG_V_RMS | double       |                                                                                                      |
| Number of positions averageed            | Averaged Positions                | ESRIGNSS_AVG_POSITIONS | Long       |                                                                                                         |
| Standard deviation           | Standard Deviation (m)                | ESRIGNSS_H_STDDEV | double        |                                                                                                         |

###Using as a Python Toolbox within ArcMap or ArcGIS Pro:

1. Connect to the folder containing the "CollectorUtils" toolbox
2. Double click on the "CollectorUtils" toolbox that should be shown in the catalog/project area
3. Double click the "Add GNSS Metadata Fields" script tool (in the "OfflineUtils" toolset)
4. Select a Feature class (can also use feature service in ArcGIS Pro)
5. Click Run


![Alt text](images/AddGNSSMetaData_interface.JPG "Interface")

![image](https://user-images.githubusercontent.com/26557666/28002480-726d501a-64ea-11e7-83bc-3c6cabffa38b.png)

### Re-building the toolbox (for ArcMap versions lower than 10.4)
1. Create a new toolbox (if you don't already have one)
2. Add the add_gnss_fields.py as a script
3. Set the parameters as follows:

    | Display Name        | Data Type     | Type     | Direction | Filter                |
    |---------------------|---------------|----------|-----------|-----------------------|
    | Input Feature Class | Feature Class | Required | Input     | Feature Class (Point) |


###Using as a standalone script
Run the [add_update_gnss_fields.py](add_update_gnss_fields.py) script in either Python 2.7+ or Python 3.4+ as:
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


