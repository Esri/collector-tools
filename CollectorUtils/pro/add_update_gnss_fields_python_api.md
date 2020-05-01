# Add GNSS Metadata Fields
A Python script and corresponding toolbox to automatically add and update GNSS attributes to feature services.

Supported in ArcGIS Pro 2.0+

This script/tool attempts to add the following fields to a Point Feature Class:

| Attribute            | Field Alias             | Field Name           | Field Type  | Domain               | Notes                                                                                    |
|----------------------|-------------------------|----------------------|-------------|----------------------|------------------------------------------------------------------------------------------|
| Position source type        | Position source type           | ESRIGNSS_POSITIONSOURCETYPE    | Short |        0 - Unknown <br/>1 - User defined <br/>2 - Integrated (System) Location Provider <br/>3 - External GNSS Receiver <br/>4 - Network Location Provider               |                                                                                          |
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


# Intructions to run from Pro. 
![image](https://user-images.githubusercontent.com/26557666/28002606-9442b8aa-64eb-11e7-8974-b44fa513a7a9.png)
* See tool metadata in Pro for detailed instructions about parameters.


# Intructions to run the script.
1. Install ArcGIS API for Python using Conda (https://developers.arcgis.com/python/guide/install-and-set-up/).
2. Once installed start command prompt (with adminstrator rights). 
3. Navigate to the directory where Anaconda was installed and check if Python was installed successfully.

![image](https://cloud.githubusercontent.com/assets/26557666/24469021/ee2dbbee-146e-11e7-8984-00cbf690b5ca.png)

4. Exit out of Python's interactive shell.



5. Script usage help. Information on required and optional parameters can be obatined via -h flag

![image](https://user-images.githubusercontent.com/26557666/27194938-6ad4b2ec-51b9-11e7-9edd-06efea81a3c7.png)



6. Run the script with the required arguments 


![image](https://user-images.githubusercontent.com/26557666/27195140-6a2fb9da-51ba-11e7-84ee-677938c18ac4.png)


7. Running the script from within ArcGIS Pro python environment

![image](https://user-images.githubusercontent.com/26557666/27195041-ed0ad44e-51b9-11e7-82a3-94b07379cd1d.png)





