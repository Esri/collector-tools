# Configure GNSS Metadata fields visibility and Popup
Supported in ArcGIS Pro 2.0+ - requires Python API version 1.4.2+  - https://developers.arcgis.com/python/guide/install-and-set-up/

| Field name | Alias | Format |
|---|---|---|
| ESRIGNSS_DIRECTION | Direction of travel (°) | 2 decimal places |
| ESRIGNSS_SPEED | Speed (km/h) | 2 decimal places |
| ESRISNSR_AZIMUTH | Compass reading (°) | 2 decimal places |
| ESRIGNSS_POSITIONSOURCETYPE | Position source type | NA |
| ESRIGNSS_RECEIVER | Receiver Name | NA |
| ESRIGNSS_H_RMS | Horizontal Accuracy (m) | 2 decimal places |
| ESRIGNSS_V_RMS | Vertical Accuracy (m) | 2 decimal places |
| ESRIGNSS_LATITUDE | Latitude | 8 decimal places |
| ESRIGNSS_LONGITUDE | Longitude | 8 decimal places |
| ESRIGNSS_ALTITUDE | Altitude | 2 decimal places |
| ESRIGNSS_PDOP | PDOP | 2 decimal places |
| ESRIGNSS_HDOP | HDOP | 2 decimal places |
| ESRIGNSS_VDOP | VDOP | 2 decimal places |
| ESRIGNSS_FIXTYPE | Fix Type | NA |
| ESRIGNSS_CORRECTIONAGE | Correction Age (seconds) | 0 decimal places |
| ESRIGNSS_STATIONID | Station ID | NA |
| ESRIGNSS_NUMSATS | Number of Satellites | NA |
| ESRIGNSS_FIXDATETIME | Fix Time | ShortDateTime, 12hr |
| ESRIGNSS_AVG_H_RMS | Average Horizontal Accuracy (m) | 2 decimal places |
| ESRIGNSS_AVG_V_RMS | Average Vertical Accuracy (m) | 2 decimal places |
| ESRIGNSS_AVG_POSITIONS | Averaged Positions | NA |
| ESRIGNSS_H_STDDEV| Standard Deviation (m) | 3 decimal places |

**Note** Prior to running the tool, for hosted feature services published using ArcGIS Pro, once added into a new web map in ArcGIS Online/ArcGIS Enterprise, click `Save Layer`.

# Intructions to run from Pro.
![image](https://user-images.githubusercontent.com/26557666/28002780-05812fbe-64ed-11e7-975e-1b7e63bc2c83.png)

* See tool metadata in Pro for detailed instructions about parameters.

# Intructions to run the script.
1. Install ArcGIS API for Python using Conda (https://developers.arcgis.com/python/guide/install-and-set-up/).
2. Once installed start command prompt (with adminstrator rights). 
3. Navigate to the directory where Anaconda was installed and check if Python was installed successfully.

![image](https://cloud.githubusercontent.com/assets/26557666/24469021/ee2dbbee-146e-11e7-8984-00cbf690b5ca.png)

4. Exit out of Python's interactive shell.



5. Script usage help. Information on required and optional parameters can be obatined via -h flag

![image](https://user-images.githubusercontent.com/26557666/27195233-d493747e-51ba-11e7-98e2-005a8955cccf.png)



6. Run the script with the required arguments 


![image](https://user-images.githubusercontent.com/26557666/27195354-43b21f0e-51bb-11e7-8db1-c609c97f8781.png)


7. Running the script from within ArcGIS Pro python environment

![image](https://user-images.githubusercontent.com/26557666/27195298-0c17f320-51bb-11e7-8e88-0ce9e1c5cabb.png)




