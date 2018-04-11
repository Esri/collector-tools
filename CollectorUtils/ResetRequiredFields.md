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

### Using as a Script Tool within ArcGIS Pro

![image](https://user-images.githubusercontent.com/26557666/38632020-4d8b5f12-3d70-11e8-8b6a-2ad4c18fd7f9.png)


**Script takes the following parameters as input**
1. Organization Url
2. Username 
3. Password
4. Feature Service ItemId

**Instructions to run the script**
1. Connect to the folder containing the "CollectorUtils_Pro" toolbox
2. Double click on the "CollectorUtils_Pro" toolbox that should be shown in the catalog/project area
3. Under GeneralUtils toolbox double click the "Reset Required Fields (Python api)" script tool
4. Key-in all the required inputs    
5. Click Run

![Alt text](/images/ResetRequiredFields_interface.JPG "Interface")

### Using as a standalone script
Run the [reset_required_fields_python_api.py](reset_required_fields_python_api.py) script in Python 3.4+ as:

![image](https://user-images.githubusercontent.com/26557666/38633594-115d5a9a-3d75-11e8-80cd-8b8729d48bd1.png)


