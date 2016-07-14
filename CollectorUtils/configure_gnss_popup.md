# Configure GNSS Popup 
Changes the visible properties of all ESRIGNSS related attributes in a web map

Supported in at least ArcGIS 10.3.x+

This tool changes the "visible" property of ESRIGNSS fields in the popup information in the specified web map. It also updates the number of decimals displayed.

### Using as a Script Tool within ArcMap

**You must be signed into a Portal or AGOL Organization**

**Supports 'built-in' and 'SAML' authentication**

1. Connect to the folder containing the "CollectorUtils" toolbox
2. Double click on the "CollectorUtils" toolbox that should be shown in the catalog/project area
3. Double click the "Configure GNSS Popup" script tool (in the "OnlineUtils" toolset)
    1. Visible - Should the GNSS fields be visible or not
    2. ID - The id of the webmap to update (e.g. (f1bad03e6fd74f45a4708d034bd847a4)
5. Click Run

![Alt text](images/ConfigureGNSSPopup_interface.JPG "Interface")

### Re-building the toolbox (for versions lower than 10.4)
1. Create a new toolbox (if you don't already have one)
2. Add the configure_gnss_popup.py as a script
3. Set the parameters as follows:

    | Display Name | Data Type | Type     | Direction | Filter |
    |--------------|-----------|----------|-----------|--------|
    | Map ID       | String    | Required | Input     | None   |
    | Visible      | Boolean   | Requried | Input     | None   |

4. Update the validation logic to make sure you are signed into ArcGIS online or a Portal

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
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        if not arcpy.GetSigninToken():
          self.params[0].setErrorMessage("You are currently not signed into a Portal or AGOL Organization.")
        else:
          self.params[0].clearMessage()
        return
```

### Using as a standalone script
Two scripts are provided. The [configure_gnss_popup_arcrest.py](configure_gnss_popup_arcrest.py) script relies on the [ArcREST](https://github.com/Esri/ArcREST) library to send requests to Portal and AGOL. This allows organizations that use PKI, IWA/NTLM, and LDAP to authenticate properly. The [configure_gnss_popup.py](configure_gnss_popup.py) script only support the 'built-in' authentication but it is faster.

Run the [configure_gnss_popup.py](configure_gnss_popup.py) script in either Python 2.7+ or Python 3.4+ as:
```python
python configure_gnss_popup.py -u <username> -p <password> -url <org url> <id1> <id2> ... <idn> <visible>
```

It is worth noting that the visible parameters are strings ("true" or "false"). This is so that the script can be using as a script tool in a toolbox as well as called from the commandline properly. In addition the script allows multiple maps to be configured at the same time; just supply all ids at the end.

Example:
```python
python configure_gnss_popup.py -u mycoolusername -p myevencoolerpassword -url "https://myorg.maps.arcgis.com" "t933fe6f51af4a89bac06808da5e7ed3" "true" 
```

----

Run the [configure_gnss_popup_arcrest.py](configure_gnss_popup_arcrest.py) script in either Python 2.7+ or Python 3.4+ as:
```python
python configure_gnss_popup.py -u <username> -p <password> -url <org url> -v -ids <id1> <id2> ...<idn>
```

This shows how to authenticate with 'built-in' security. Additional parameters may be required if other authentication methods are desired (see source code or ArcREST documentation). Adding "-v" sets the the GNSS fields to be visible, not including it will default to false (not visible). In addition the script allows multiple maps to be configured at the same time; just supply all ids after the "-ids" flag.

Example:
```python
python configure_gnss_popup.py -u mycoolusername -p myevencoolerpassword -url "https://myorg.maps.arcgis.com" -v -e -ids "t933fe6f51af4a89bac06808da5e7ed3"
```

### What it does
1. Authenticates with Portal/AGOL and gets a token
2. Gets the specified web map item
3. Gets the data of the web map (json)
4. Updates the "visible" parameter of the popup info json (ESRIGNSS fields only) and sets the displayed decimal places.
5. Submits edits to Portal/AGOL
