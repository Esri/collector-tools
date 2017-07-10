# Reset Required Fields
Sets the "required" fields to be null rather than white-space or 0 in the service definition template information.

Fields are said to be "required" in Collector if the field is not nullable. In the template information in the layer definition file, some of these fields are set to blank white-space (" ","") or to 0. These template values then auto-populate the fields in the Collector app meaning the end-user doesn't have to enter anything, when in reality, they should be forced to enter a value. The scripts automate the process of:

1. From My Content in ArcGIS Online, click View Item Details for desired Feature Layer
2. Go To Layers section of item details
3. Click on Chevron (down arrow) next to layer you want to update
4. Select Service URL from the menu. This should open the URL in the web browser
5. Change URL to include highlighted text: http\://services.arcgis.com/\<orgid\>/ArcGIS/rest/admin/services/\<Servicename\>/FeatureServer/\<sublayer\>/updateDefinition
6. In Update Layer Definition, Scroll down to “templates” section
    1. For each field in the template that is not nullable
    2. Change “ “ to null
    3. Change 0 to null
7. In Update Layer Definition, remove editing info
    1. Find section named editingInfo
    2. Remove property lastEditDate, should remove similar to the following: "lastEditDate" : 1455664570690
8. Tap Update Layer Definition.If successful, should see ‘Updated Feature Service Layer:

### Using as a Script Tool within ArcMap

**You must be signed into a Portal or AGOL Organization**

**Supports 'built-in' and 'SAML' authentication**

1. Connect to the folder containing the "CollectorUtils" toolbox
2. Double click on the "CollectorUtils" toolbox that should be shown in the catalog/project area
3. Double click the "Reset Required Fields" script tool (in the "OnlineUtils" toolset)
4. Choose your inputs
    1. Service ID - The id of the service to update (e.g. (f1bad03e6fd74f45a4708d034bd847a4)
5. Click Run

![Alt text](/images/ResetRequiredFields_interface.JPG "Interface")

### Using as a standalone script
Two scripts are provided. The [reset_required_fields_arcrest.py](reset_required_fields_arcrest.py) script relies on the [ArcREST](https://github.com/Esri/ArcREST) library to send requests to Portal and AGOL. This allows organizations that use PKI, IWA/NTLM, and LDAP to authenticate properly. The [reset_required_fields.py](reset_required.py) script only support the 'built-in' authentication but it is faster.

Run the [configure_gnss_popup.py](reset_required_fields.py) script in either Python 2.7+ or Python 3.4+ as:
```python
python reset_required_fields.py -u <username> -p <password> -url <org url> <id1> <id2> ... <idn>
```

In addition the script allows multiple services to be configured at the same time; just supply all ids at the end.

Example:
```python
python reset_required_fields.py -u mycoolusername -p myevencoolerpassword -url "https://myorg.maps.arcgis.com" "y933se6f51af4a89bac06808da5e7ed0"
```

----

Run the [reset_required_fields_arcrest.py](reset_required_fields_arcrest.py) script in either Python 2.7+ or Python 3.4+ as:
```python
python reset_required_fields_arcrest.py -u <username> -p <password> -url <org url> -ids <id1> <id2> ...<idn>
```

This shows how to authenticate with 'built-in' security. Additional parameters may be required if other authentication methods are desired (see source code or ArcREST documentation). In addition the script allows multiple services to be configured at the same time; just supply all ids after the "-ids" flag.

Example:
```python
python reset_required_fields_arcrest.py -u mycoolusername -p myevencoolerpassword -url "https://myorg.maps.arcgis.com" -v -e -ids "t933fe6f51af4a89bac06808da5e7ed3"
```

### What it does
1. Authenticates with Portal/AGOL and gets a token
2. Gets the specified item data and service url
3. Gets the service definition of each layer in the service
4. Updates the non-nullable fields in the template info section of the json
5. Submits edits to Portal/AGOL using the updateDefinition endpoint
